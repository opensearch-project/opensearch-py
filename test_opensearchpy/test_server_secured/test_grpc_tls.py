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
test_tls.py — gRPC TLS Integration Tests

Tests that the gRPC client can connect to OpenSearch over a TLS-secured
gRPC channel. Requires OpenSearch running with secure-transport-grpc.

Skips automatically if gRPC TLS is not available.
"""

import os
from typing import Any
from unittest import SkipTest, TestCase

import grpc

from opensearchpy.client import OpenSearchGrpc

GRPC_PORT = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
GRPC_HOST = os.environ.get("OPENSEARCH_GRPC_HOST", "localhost")
OPENSEARCH_URL = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")


def _grpc_tls_available() -> bool:
    """Check if secure gRPC is reachable."""
    try:
        credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(f"{GRPC_HOST}:{GRPC_PORT}", credentials)
        grpc.channel_ready_future(channel).result(timeout=3)
        channel.close()
        return True
    except Exception:
        return False


if not _grpc_tls_available():
    raise SkipTest(f"Secure gRPC not available on {GRPC_HOST}:{GRPC_PORT}")


class TestGrpcTlsConnection(TestCase):
    """Test gRPC client connects over TLS."""

    def _get_client(self, **kwargs: Any) -> OpenSearchGrpc:
        """Create a TLS-enabled gRPC client."""
        ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        defaults: dict = {
            "hosts": [OPENSEARCH_URL],
            "grpc_hosts": [{"host": GRPC_HOST, "port": GRPC_PORT}],
            "use_ssl": True,
            "verify_certs": False,
        }
        if ca_certs:
            defaults["ca_certs"] = ca_certs
            defaults["verify_certs"] = True
        defaults.update(kwargs)
        return OpenSearchGrpc(**defaults)

    def test_bulk_over_tls(self) -> None:
        """Bulk request succeeds over TLS gRPC channel."""
        client = self._get_client()
        try:
            resp = client.bulk(
                body=[
                    {"index": {"_index": "test-grpc-tls", "_id": "1"}},
                    {"title": "TLS doc"},
                ],
                refresh=True,
            )
            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 1)
            self.assertEqual(resp["items"][0]["index"]["result"], "created")
        finally:
            client.indices.delete(index="test-grpc-tls", ignore=[404])
            client.close()

    def test_bulk_multiple_docs_over_tls(self) -> None:
        """Multiple documents indexed over TLS."""
        client = self._get_client()
        try:
            body = []
            for i in range(5):
                body.append({"index": {"_index": "test-grpc-tls-multi", "_id": str(i)}})
                body.append({"title": f"TLS doc {i}", "value": i})

            resp = client.bulk(body=body, refresh=True)
            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 5)
        finally:
            client.indices.delete(index="test-grpc-tls-multi", ignore=[404])
            client.close()

    def test_rest_fallback_over_tls(self) -> None:
        """Non-bulk operations fall back to REST (also over TLS)."""
        client = self._get_client()
        try:
            client.bulk(
                body=[
                    {"index": {"_index": "test-grpc-tls-rest", "_id": "1"}},
                    {"title": "Fallback doc"},
                ],
                refresh=True,
            )
            # Search goes through REST
            resp = client.search(
                index="test-grpc-tls-rest",
                body={"query": {"match_all": {}}},
            )
            self.assertEqual(resp["hits"]["total"]["value"], 1)
        finally:
            client.indices.delete(index="test-grpc-tls-rest", ignore=[404])
            client.close()
