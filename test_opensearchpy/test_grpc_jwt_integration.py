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
test_grpc_jwt_integration.py — Mock-based Integration Tests for gRPC JWT Auth

Tests the full end-to-end flow: GrpcTransport → BearerTokenInterceptor →
mock gRPC server. Verifies that Bearer tokens arrive correctly at the
server side as gRPC metadata.

Uses a real gRPC server running in-process on a random port.
No external services required.
"""

from concurrent import futures
from unittest import TestCase

import grpc
from opensearch.protobufs.schemas import common_pb2
from opensearch.protobufs.services import document_service_pb2_grpc

from opensearch_grpc.grpc_transport import GrpcTransport


class MockDocumentServicer(document_service_pb2_grpc.DocumentServiceServicer):
    """Mock gRPC server that captures request metadata."""

    def __init__(self):
        self.received_metadata = {}
        self.call_count = 0

    def Bulk(self, request, context):  # pylint: disable=invalid-name
        """Handle Bulk — capture metadata and return a valid response."""
        self.call_count += 1
        metadata = dict(context.invocation_metadata())
        self.received_metadata = metadata

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


class TestJwtEndToEnd(TestCase):
    """End-to-end test: client → BearerTokenInterceptor → mock server."""

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

    def _make_body(self):
        return [
            {"index": {"_index": "test-index", "_id": "1"}},
            {"title": "JWT test doc"},
        ]

    def test_bearer_token_reaches_server(self) -> None:
        """Bearer token is received by the gRPC server as metadata."""
        jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGVzIjoiYWxsX2FjY2VzcyJ9.signature"

        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=f"Bearer {jwt_token}",
        )

        try:
            resp = transport.perform_request(
                "POST", "/_bulk", params={}, body=self._make_body()
            )

            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 1)

            metadata = self.servicer.received_metadata
            self.assertIn("authorization", metadata)
            self.assertEqual(metadata["authorization"], f"Bearer {jwt_token}")
        finally:
            transport.close()

    def test_bearer_token_lowercase_prefix(self) -> None:
        """'bearer ' (lowercase) prefix also works."""
        jwt_token = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyMSJ9.sig"

        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=f"bearer {jwt_token}",
        )

        try:
            transport.perform_request(
                "POST", "/_bulk", params={}, body=self._make_body()
            )

            metadata = self.servicer.received_metadata
            self.assertIn("authorization", metadata)
            # BearerTokenInterceptor normalizes to "Bearer " prefix
            self.assertTrue(
                metadata["authorization"].startswith("bearer ")
                or metadata["authorization"].startswith("Bearer ")
            )
        finally:
            transport.close()

    def test_token_persists_across_requests(self) -> None:
        """Multiple requests all carry the same Bearer token."""
        jwt_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.sig"

        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=f"Bearer {jwt_token}",
        )

        try:
            for _ in range(3):
                transport.perform_request(
                    "POST", "/_bulk", params={}, body=self._make_body()
                )

            self.assertEqual(self.servicer.call_count, 3)
            self.assertEqual(
                self.servicer.received_metadata["authorization"],
                f"Bearer {jwt_token}",
            )
        finally:
            transport.close()

    def test_basic_auth_not_confused_with_bearer(self) -> None:
        """Basic auth tuple does NOT produce a Bearer header."""
        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=("admin", "password"),
        )

        try:
            transport.perform_request(
                "POST", "/_bulk", params={}, body=self._make_body()
            )

            metadata = self.servicer.received_metadata
            self.assertIn("authorization", metadata)
            self.assertTrue(metadata["authorization"].startswith("Basic "))
            self.assertFalse(metadata["authorization"].startswith("Bearer "))
        finally:
            transport.close()

    def test_non_bulk_falls_back_to_rest(self) -> None:
        """Non-bulk requests don't go through gRPC (no metadata captured)."""
        jwt_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.sig"

        transport = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": self.port}],
            http_auth=f"Bearer {jwt_token}",
        )

        try:
            # Search goes through REST, not gRPC — server call_count stays 0
            # (This will fail because REST host isn't running, but we verify
            # the gRPC server was NOT called)
            try:
                transport.perform_request("GET", "/_search", params={}, body=None)
            except Exception:
                pass  # Expected — REST host not running

            self.assertEqual(self.servicer.call_count, 0)
        finally:
            transport.close()
