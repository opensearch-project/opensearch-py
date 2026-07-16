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
test_grpc_secure.py — gRPC TLS + Basic Auth Integration Tests

End-to-end tests verifying that the gRPC transport works correctly with
TLS encryption and basic authentication enabled. Requires OpenSearch 3.x
running with secure-transport-grpc and security plugin (FGAC).

Uses the same pattern as other test_server_secured tests: derives
connection info from OPENSEARCH_URL and skips per-test if gRPC is
not available.
"""

import os
from typing import Any
from unittest import TestCase
from urllib.parse import urlparse

from opensearchpy.client.grpc_client import OpenSearchGrpc
from opensearchpy.exceptions import AuthenticationException
from opensearchpy.helpers.test import OPENSEARCH_URL

# Derive gRPC host from OPENSEARCH_URL (same host as REST)
_parsed = urlparse(OPENSEARCH_URL)
GRPC_PORT = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
GRPC_HOST = os.environ.get("OPENSEARCH_GRPC_HOST", _parsed.hostname or "localhost")
OPENSEARCH_PASSWORD = os.environ.get(
    "OPENSEARCH_INITIAL_ADMIN_PASSWORD", "myStrongPassword123!"
)


def _grpc_available() -> bool:
    """Check if gRPC port is reachable via TCP."""
    import socket

    try:
        sock = socket.create_connection((GRPC_HOST, GRPC_PORT), timeout=3)
        sock.close()
        return True
    except (OSError, socket.timeout):
        return False


class TestSecureGrpc(TestCase):
    """Test gRPC client with TLS + basic auth."""

    def setUp(self) -> None:
        if not _grpc_available():
            self.skipTest(f"gRPC not available on {GRPC_HOST}:{GRPC_PORT}")

    def _get_client(self, **kwargs: Any) -> OpenSearchGrpc:
        """Create a TLS + auth enabled gRPC client.

        Always uses ca_certs when available since gRPC Python cannot
        disable certificate verification (unlike REST with verify_certs=False).
        Uses ssl_assert_hostname="localhost" because the demo installer's cert
        is issued for localhost, but the Docker network uses hostname "instance".
        """
        ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        if not ca_certs:
            self.skipTest("OPENSEARCH_CA_CERTS not set — gRPC requires CA cert for TLS")
        defaults: dict = {
            "hosts": [OPENSEARCH_URL],
            "grpc_hosts": [{"host": GRPC_HOST, "port": GRPC_PORT}],
            "http_auth": ("admin", OPENSEARCH_PASSWORD),
            "use_ssl": True,
            "verify_certs": False,
            "ca_certs": ca_certs,
            "ssl_assert_hostname": "localhost",
        }
        defaults.update(kwargs)
        return OpenSearchGrpc(**defaults)

    # ─── Bulk over TLS + Auth ─────────────────────────────────────────────

    def test_bulk_over_secure_channel(self) -> None:
        """Bulk request succeeds over TLS with valid credentials."""
        client = self._get_client()
        try:
            resp = client.bulk(
                body=[
                    {"index": {"_index": "test-secure-grpc", "_id": "1"}},
                    {"title": "Secure doc"},
                ],
                refresh=True,
            )
            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 1)
            self.assertEqual(resp["items"][0]["index"]["result"], "created")
        finally:
            client.indices.delete(index="test-secure-grpc", ignore=[404])
            client.close()

    def test_bulk_multiple_docs(self) -> None:
        """Multiple documents indexed over authenticated TLS channel."""
        client = self._get_client()
        try:
            body = []
            for i in range(5):
                body.append({"index": {"_index": "test-secure-multi", "_id": str(i)}})
                body.append({"title": f"Secure doc {i}", "value": i})

            resp = client.bulk(body=body, refresh=True)
            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 5)
        finally:
            client.indices.delete(index="test-secure-multi", ignore=[404])
            client.close()

    def test_multiple_requests_maintain_auth(self) -> None:
        """Multiple sequential bulk requests all carry credentials."""
        client = self._get_client()
        try:
            for i in range(3):
                resp = client.bulk(
                    body=[
                        {"index": {"_index": "test-secure-seq", "_id": str(i)}},
                        {"title": f"Doc {i}"},
                    ],
                    refresh=True,
                )
                self.assertFalse(resp["errors"])
        finally:
            client.indices.delete(index="test-secure-seq", ignore=[404])
            client.close()

    # ─── REST Fallback with TLS + Auth ────────────────────────────────────

    def test_rest_fallback_search(self) -> None:
        """Search (REST fallback) works with same TLS + auth credentials."""
        client = self._get_client()
        try:
            client.bulk(
                body=[
                    {"index": {"_index": "test-secure-search", "_id": "1"}},
                    {"title": "Searchable", "category": "secure"},
                ],
                refresh=True,
            )
            resp = client.search(
                index="test-secure-search",
                body={"query": {"match": {"category": "secure"}}},
            )
            self.assertEqual(resp["hits"]["total"]["value"], 1)
        finally:
            client.indices.delete(index="test-secure-search", ignore=[404])
            client.close()

    def test_rest_fallback_get(self) -> None:
        """GET (REST fallback) works with same TLS + auth credentials."""
        client = self._get_client()
        try:
            client.bulk(
                body=[
                    {"index": {"_index": "test-secure-get", "_id": "1"}},
                    {"title": "Get me securely"},
                ],
                refresh=True,
            )
            doc = client.get(index="test-secure-get", id="1")
            self.assertEqual(doc["_source"]["title"], "Get me securely")
        finally:
            client.indices.delete(index="test-secure-get", ignore=[404])
            client.close()

    # ─── Auth Failure ─────────────────────────────────────────────────────

    def test_invalid_password_raises_authentication_exception(self) -> None:
        """Wrong password raises AuthenticationException."""
        client = self._get_client(http_auth=("admin", "wrongpassword"))
        try:
            with self.assertRaises(AuthenticationException):
                client.bulk(
                    body=[
                        {"index": {"_index": "test-secure-badauth", "_id": "1"}},
                        {"title": "Should fail"},
                    ],
                )
        finally:
            client.close()

    def test_no_credentials_raises_authentication_exception(self) -> None:
        """No credentials on a secured node raises AuthenticationException."""
        ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        if not ca_certs:
            self.skipTest("OPENSEARCH_CA_CERTS not set — gRPC requires CA cert for TLS")
        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            use_ssl=True,
            ca_certs=ca_certs,
            ssl_assert_hostname="localhost",
        )
        try:
            with self.assertRaises(AuthenticationException):
                client.bulk(
                    body=[
                        {"index": {"_index": "test-secure-noauth", "_id": "1"}},
                        {"title": "Should fail"},
                    ],
                )
        finally:
            client.close()


class TestTlsSettings(TestCase):
    """Test various TLS configuration options."""

    def setUp(self) -> None:
        if not _grpc_available():
            self.skipTest(f"gRPC not available on {GRPC_HOST}:{GRPC_PORT}")
        self.ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        if not self.ca_certs:
            self.skipTest("OPENSEARCH_CA_CERTS not set — gRPC requires CA cert for TLS")

    def _bulk_succeeds(self, client: OpenSearchGrpc) -> bool:
        """Helper: attempt a bulk request and return True if it succeeds."""
        try:
            resp = client.bulk(
                body=[
                    {"index": {"_index": "test-tls-settings", "_id": "1"}},
                    {"title": "TLS settings test"},
                ],
                refresh=True,
            )
            return not resp["errors"]
        finally:
            client.indices.delete(index="test-tls-settings", ignore=[404])

    def test_use_ssl_true_with_verify_certs_false(self) -> None:
        """TLS channel with verify_certs=False still needs CA for gRPC.

        Note: gRPC Python does not support disabling certificate verification.
        When verify_certs=False is passed, the REST fallback skips verification,
        but the gRPC channel still requires a valid root CA. This test verifies
        that the channel works when the CA cert is available.
        """
        ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        if not ca_certs:
            self.skipTest("OPENSEARCH_CA_CERTS not set — gRPC requires CA cert")

        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=True,
            verify_certs=False,
            ca_certs=ca_certs,
            ssl_assert_hostname="localhost",
        )
        try:
            self.assertTrue(self._bulk_succeeds(client))
        finally:
            client.close()

    def test_use_ssl_true_with_ca_certs(self) -> None:
        """TLS channel with explicit CA cert for server verification."""
        ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        if not ca_certs:
            self.skipTest("OPENSEARCH_CA_CERTS not set — cannot test ca_certs param")

        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=True,
            ca_certs=ca_certs,
            ssl_assert_hostname="localhost",
        )
        try:
            self.assertTrue(self._bulk_succeeds(client))
        finally:
            client.close()

    def test_use_ssl_true_with_ssl_context(self) -> None:
        """TLS channel using ssl_context to provide CA certs for gRPC."""
        import ssl

        ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        if not ca_certs:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        else:
            ctx = ssl.create_default_context(cafile=ca_certs)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_REQUIRED

        # Test that ssl_context works for the gRPC channel.
        # Use ssl_assert_hostname="localhost" for the gRPC hostname override.
        # Use ca_certs + verify_certs=False for the REST fallback (cleanup).
        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=True,
            ssl_context=ctx,
            ssl_assert_hostname="localhost",
            ca_certs=ca_certs,
        )
        try:
            # Bulk goes over gRPC — uses ssl_context for CA verification
            resp = client.bulk(
                body=[
                    {"index": {"_index": "test-tls-ctx", "_id": "1"}},
                    {"title": "ssl_context test"},
                ],
                refresh=True,
            )
            self.assertFalse(resp["errors"])
        finally:
            # Cleanup via a separate client that doesn't use ssl_context
            cleanup = OpenSearchGrpc(
                hosts=[OPENSEARCH_URL],
                grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
                http_auth=("admin", OPENSEARCH_PASSWORD),
                use_ssl=True,
                verify_certs=False,
                ca_certs=self.ca_certs,
                ssl_assert_hostname="localhost",
            )
            cleanup.indices.delete(index="test-tls-ctx", ignore=[404])
            cleanup.close()
            client.close()

    def test_ssl_assert_hostname_override(self) -> None:
        """TLS channel with ssl_assert_hostname overriding expected server name."""
        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=True,
            ca_certs=self.ca_certs,
            ssl_assert_hostname="localhost",
        )
        try:
            self.assertTrue(self._bulk_succeeds(client))
        finally:
            client.close()

    def test_ssl_version_accepted_silently(self) -> None:
        """ssl_version is accepted without error (gRPC auto-negotiates)."""
        import ssl

        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=True,
            ca_certs=self.ca_certs,
            ssl_assert_hostname="localhost",
            ssl_version=ssl.PROTOCOL_TLS_CLIENT,
        )
        try:
            self.assertTrue(self._bulk_succeeds(client))
        finally:
            client.close()

    def test_use_ssl_false_against_tls_server_fails(self) -> None:
        """Insecure channel against a TLS-enabled server should fail."""
        from opensearchpy.exceptions import ConnectionError

        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=False,
        )
        try:
            with self.assertRaises((ConnectionError, Exception)):
                client.bulk(
                    body=[
                        {"index": {"_index": "test-tls-insecure", "_id": "1"}},
                        {"title": "Should fail"},
                    ],
                )
        finally:
            client.close()


class TestMutualTls(TestCase):
    """Test mutual TLS (mTLS) with client certificates."""

    def setUp(self) -> None:
        if not _grpc_available():
            self.skipTest(f"gRPC not available on {GRPC_HOST}:{GRPC_PORT}")
        self.ca_certs = os.environ.get("OPENSEARCH_CA_CERTS", None)
        self.client_cert = os.environ.get("OPENSEARCH_CLIENT_CERT", None)
        self.client_key = os.environ.get("OPENSEARCH_CLIENT_KEY", None)
        if not self.ca_certs:
            self.skipTest("OPENSEARCH_CA_CERTS not set")
        if not self.client_cert or not self.client_key:
            self.skipTest("OPENSEARCH_CLIENT_CERT/KEY not set — cannot test mTLS")

    def test_mtls_bulk_succeeds(self) -> None:
        """Bulk request succeeds with mutual TLS (client cert + key)."""
        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=True,
            ca_certs=self.ca_certs,
            client_cert=self.client_cert,
            client_key=self.client_key,
            ssl_assert_hostname="localhost",
        )
        try:
            resp = client.bulk(
                body=[
                    {"index": {"_index": "test-mtls", "_id": "1"}},
                    {"title": "mTLS doc"},
                ],
                refresh=True,
            )
            self.assertFalse(resp["errors"])
            self.assertEqual(len(resp["items"]), 1)
        finally:
            # Cleanup with standard client
            cleanup = OpenSearchGrpc(
                hosts=[OPENSEARCH_URL],
                grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
                http_auth=("admin", OPENSEARCH_PASSWORD),
                use_ssl=True,
                verify_certs=False,
                ca_certs=self.ca_certs,
                ssl_assert_hostname="localhost",
            )
            cleanup.indices.delete(index="test-mtls", ignore=[404])
            cleanup.close()
            client.close()

    def test_mtls_with_rest_fallback(self) -> None:
        """REST fallback also uses client certs for mTLS."""
        client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            http_auth=("admin", OPENSEARCH_PASSWORD),
            use_ssl=True,
            ca_certs=self.ca_certs,
            client_cert=self.client_cert,
            client_key=self.client_key,
            ssl_assert_hostname="localhost",
        )
        try:
            # Bulk via gRPC with mTLS
            client.bulk(
                body=[
                    {"index": {"_index": "test-mtls-rest", "_id": "1"}},
                    {"title": "mTLS REST doc"},
                ],
                refresh=True,
            )
            # Search via REST — also uses mTLS
            resp = client.search(
                index="test-mtls-rest",
                body={"query": {"match_all": {}}},
            )
            self.assertEqual(resp["hits"]["total"]["value"], 1)
        finally:
            cleanup = OpenSearchGrpc(
                hosts=[OPENSEARCH_URL],
                grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
                http_auth=("admin", OPENSEARCH_PASSWORD),
                use_ssl=True,
                verify_certs=False,
                ca_certs=self.ca_certs,
                ssl_assert_hostname="localhost",
            )
            cleanup.indices.delete(index="test-mtls-rest", ignore=[404])
            cleanup.close()
            client.close()
