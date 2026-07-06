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
test_grpc_basic_auth.py — gRPC Basic Auth Integration Tests

Tests that the gRPC client can authenticate with OpenSearch using
Basic auth (http_auth parameter).

Requires OpenSearch running with security enabled and gRPC on port 9400.
Skips automatically if gRPC is not available.
"""

import os
from typing import Any
from unittest import SkipTest, TestCase

import grpc

from opensearchpy.client import OpenSearchGrpc
from opensearchpy.exceptions import AuthenticationException

GRPC_PORT = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
GRPC_HOST = os.environ.get("OPENSEARCH_GRPC_HOST", "localhost")
OPENSEARCH_URL = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
OPENSEARCH_PASSWORD = os.environ.get("OPENSEARCH_INITIAL_ADMIN_PASSWORD", "admin")


def _grpc_available() -> bool:
    """Check if gRPC is reachable."""
    try:
        channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
        grpc.channel_ready_future(channel).result(timeout=3)
        channel.close()
        return True
    except Exception:
        # Try secure channel
        try:
            credentials = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(f"{GRPC_HOST}:{GRPC_PORT}", credentials)
            grpc.channel_ready_future(channel).result(timeout=3)
            channel.close()
            return True
        except Exception:
            return False


if not _grpc_available():
    raise SkipTest(f"gRPC not available on {GRPC_HOST}:{GRPC_PORT}")


class TestGrpcBasicAuth(TestCase):
    """Test gRPC client authenticates with Basic auth."""

    def _get_client(self, **kwargs: Any) -> OpenSearchGrpc:
        """Create a gRPC client with auth."""
        defaults: dict = {
            "hosts": [OPENSEARCH_URL],
            "grpc_hosts": [{"host": GRPC_HOST, "port": GRPC_PORT}],
            "http_auth": ("admin", OPENSEARCH_PASSWORD),
            "use_ssl": True,
            "verify_certs": False,
        }
        defaults.update(kwargs)
        return OpenSearchGrpc(**defaults)

    def test_bulk_with_valid_auth(self) -> None:
        """Bulk request succeeds with valid credentials."""
        client = self._get_client()
        try:
            resp = client.bulk(
                body=[
                    {"index": {"_index": "test-grpc-auth", "_id": "1"}},
                    {"title": "Authenticated doc"},
                ],
                refresh=True,
            )
            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 1)
            self.assertEqual(resp["items"][0]["index"]["result"], "created")
        finally:
            client.indices.delete(index="test-grpc-auth", ignore=[404])
            client.close()

    def test_bulk_with_invalid_auth(self) -> None:
        """Bulk request with wrong password raises AuthenticationException."""
        client = self._get_client(http_auth=("admin", "wrongpassword"))
        try:
            with self.assertRaises(AuthenticationException):
                client.bulk(
                    body=[
                        {"index": {"_index": "test-grpc-badauth", "_id": "1"}},
                        {"title": "Should fail"},
                    ],
                    refresh=True,
                )
        finally:
            client.close()

    def test_multiple_bulk_requests_with_auth(self) -> None:
        """Multiple bulk requests all carry auth credentials."""
        client = self._get_client()
        try:
            for i in range(3):
                resp = client.bulk(
                    body=[
                        {"index": {"_index": "test-grpc-auth-multi", "_id": str(i)}},
                        {"title": f"Doc {i}"},
                    ],
                    refresh=True,
                )
                self.assertFalse(resp["errors"])
        finally:
            client.indices.delete(index="test-grpc-auth-multi", ignore=[404])
            client.close()

    def test_rest_fallback_uses_auth(self) -> None:
        """REST fallback operations also use the same auth."""
        client = self._get_client()
        try:
            # Bulk via gRPC
            client.bulk(
                body=[
                    {"index": {"_index": "test-grpc-auth-rest", "_id": "1"}},
                    {"title": "Auth doc"},
                ],
                refresh=True,
            )
            # Search via REST — should also be authenticated
            resp = client.search(
                index="test-grpc-auth-rest",
                body={"query": {"match_all": {}}},
            )
            self.assertEqual(resp["hits"]["total"]["value"], 1)
        finally:
            client.indices.delete(index="test-grpc-auth-rest", ignore=[404])
            client.close()
