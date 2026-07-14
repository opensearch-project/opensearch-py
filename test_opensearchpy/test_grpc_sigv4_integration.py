# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
# mypy: ignore-errors

"""
test_grpc_sigv4_integration.py — Mock-based Integration Tests for gRPC SigV4

Tests the full end-to-end flow: OpenSearchGrpc client → GrpcTransport →
AWSV4GrpcInterceptor → mock gRPC server. Verifies that SigV4 headers
arrive correctly at the server side.

Uses a real gRPC server running in-process on a random port.
No AWS credentials or external services required.
"""

import threading
from concurrent import futures
from unittest import TestCase
from unittest.mock import Mock

import grpc
from opensearch.protobufs.schemas import common_pb2
from opensearch.protobufs.services import (
    document_service_pb2_grpc,
)

from opensearch_grpc.grpc_transport import AWSV4GrpcInterceptor, GrpcTransport


class MockDocumentServicer(document_service_pb2_grpc.DocumentServiceServicer):
    """Mock gRPC server that captures request metadata."""

    def __init__(self):
        self.received_metadata = {}
        self.call_count = 0

    def Bulk(self, request, context):
        """Handle Bulk — capture metadata and return a valid response."""
        self.call_count += 1
        # Capture all metadata from the incoming call
        metadata = dict(context.invocation_metadata())
        self.received_metadata = metadata

        # Build a minimal valid BulkResponse
        response = common_pb2.BulkResponse()
        response.errors = False
        response.took = 5

        item = response.items.add()
        item.index.x_index = "test-index"
        item.index.x_id = "1"
        item.index.result = "created"
        item.index.status = 201
        item.index.x_version = 1
        item.index.x_seq_no = 0
        item.index.x_primary_term = 1

        return response


class TestSigV4EndToEnd(TestCase):
    """End-to-end test: client → interceptor → mock server."""

    @classmethod
    def setUpClass(cls):
        """Start a mock gRPC server on a random port."""
        cls.servicer = MockDocumentServicer()
        cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        document_service_pb2_grpc.add_DocumentServiceServicer_to_server(
            cls.servicer, cls.server
        )
        cls.port = cls.server.add_insecure_port("[::]:0")
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the mock server."""
        cls.server.stop(grace=0)

    def setUp(self):
        """Reset servicer state between tests."""
        self.servicer.received_metadata = {}
        self.servicer.call_count = 0

    def _mock_credentials(self):
        """Create mock AWS credentials."""
        import uuid

        creds = Mock()
        creds.access_key = "AKIAIOSFODNN7EXAMPLE"
        creds.secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        creds.token = "FwoGZXIvYXdzEBYaDHqa0AP"
        del creds.get_frozen_credentials
        return creds

    def _mock_signer_auth(self, creds):
        """Create a mock Urllib3AWSV4SignerAuth-like object."""
        auth = Mock()
        auth.signer = Mock()
        auth.signer.credentials = creds
        auth.signer.region = "us-east-1"
        auth.signer.service = "es"
        return auth

    def test_sigv4_headers_reach_server(self) -> None:
        """SigV4 signed headers are received by the gRPC server."""
        creds = self._mock_credentials()
        auth = self._mock_signer_auth(creds)

        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=auth,
        )

        try:
            body = [
                {"index": {"_index": "test-index", "_id": "1"}},
                {"title": "SigV4 test doc"},
            ]
            resp = transport.perform_request("POST", "/_bulk", params={}, body=body)

            # Verify the response came back correctly
            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 1)

            # Verify SigV4 headers were received by the server
            metadata = self.servicer.received_metadata
            self.assertIn("authorization", metadata)
            self.assertTrue(metadata["authorization"].startswith("AWS4-HMAC-SHA256"))
            self.assertIn("x-amz-date", metadata)
            self.assertIn("x-amz-content-sha256", metadata)
            self.assertIn("x-amz-security-token", metadata)
        finally:
            transport.close()

    def test_sigv4_signs_every_request(self) -> None:
        """Each request gets a fresh signature."""
        creds = self._mock_credentials()
        auth = self._mock_signer_auth(creds)

        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=auth,
        )

        try:
            body = [
                {"index": {"_index": "test-index", "_id": "1"}},
                {"title": "Request 1"},
            ]

            # First request
            transport.perform_request("POST", "/_bulk", params={}, body=body)
            first_auth = self.servicer.received_metadata.get("authorization")

            # Second request
            body[1] = {"title": "Request 2"}
            transport.perform_request("POST", "/_bulk", params={}, body=body)
            second_auth = self.servicer.received_metadata.get("authorization")

            # Both should be valid SigV4 signatures
            self.assertTrue(first_auth.startswith("AWS4-HMAC-SHA256"))
            self.assertTrue(second_auth.startswith("AWS4-HMAC-SHA256"))

            # Server was called twice
            self.assertEqual(self.servicer.call_count, 2)
        finally:
            transport.close()

    def test_sigv4_includes_security_token(self) -> None:
        """Temporary credentials include x-amz-security-token."""
        creds = self._mock_credentials()
        auth = self._mock_signer_auth(creds)

        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=auth,
        )

        try:
            body = [
                {"index": {"_index": "test-index", "_id": "1"}},
                {"title": "Token test"},
            ]
            transport.perform_request("POST", "/_bulk", params={}, body=body)

            metadata = self.servicer.received_metadata
            self.assertIn("x-amz-security-token", metadata)
            self.assertEqual(metadata["x-amz-security-token"], creds.token)
        finally:
            transport.close()

    def test_basic_auth_headers_reach_server(self) -> None:
        """Basic auth also works with the mock server (sanity check)."""
        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=("admin", "password"),
        )

        try:
            body = [
                {"index": {"_index": "test-index", "_id": "1"}},
                {"title": "Basic auth test"},
            ]
            resp = transport.perform_request("POST", "/_bulk", params={}, body=body)

            self.assertFalse(resp["errors"])
            metadata = self.servicer.received_metadata
            self.assertIn("authorization", metadata)
            self.assertTrue(metadata["authorization"].startswith("Basic "))
        finally:
            transport.close()
