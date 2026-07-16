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
test_grpc_tls_unit.py — Unit Tests for gRPC TLS Channel Creation

Tests that GrpcTransport creates the correct channel type (secure vs insecure)
based on the TLS parameters. No running server needed.
"""

import os
import tempfile
from unittest import TestCase

from opensearch_grpc.grpc_transport import GrpcTransport
from opensearchpy.client import OpenSearchGrpc
from opensearchpy.exceptions import ImproperlyConfigured


class TestGrpcChannelCreation(TestCase):
    """Test that GrpcTransport creates correct channel type."""

    def test_insecure_channel_by_default(self) -> None:
        """No use_ssl creates an insecure channel."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
        )
        self.assertFalse(t._use_ssl)
        self.assertIsNotNone(t._channel)
        t.close()

    def test_secure_channel_with_use_ssl(self) -> None:
        """use_ssl=True creates a secure channel."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=True,
        )
        self.assertTrue(t._use_ssl)
        self.assertIsNotNone(t._channel)
        t.close()

    def test_secure_channel_with_ca_certs(self) -> None:
        """use_ssl=True with ca_certs loads the CA file."""
        # Create a temp CA file
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pem", delete=False) as f:
            # Write a dummy cert (won't validate but tests file loading)
            f.write(
                b"-----BEGIN CERTIFICATE-----\nMIIBkTCB+wIJALx0v\n-----END CERTIFICATE-----\n"
            )
            ca_path = f.name

        try:
            t = GrpcTransport(
                [{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                use_ssl=True,
                ca_certs=ca_path,
            )
            self.assertTrue(t._use_ssl)
            self.assertEqual(t._ca_certs, ca_path)
            t.close()
        finally:
            os.unlink(ca_path)

    def test_secure_channel_with_client_certs(self) -> None:
        """use_ssl=True with client_cert and client_key loads mTLS files."""
        # Create temp cert/key files
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pem", delete=False) as f:
            f.write(
                b"-----BEGIN CERTIFICATE-----\nMIIBkTCB+wIJALx0v\n-----END CERTIFICATE-----\n"
            )
            cert_path = f.name

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pem", delete=False) as f:
            f.write(
                b"-----BEGIN PRIVATE KEY-----\nMIIBkTCB+wIJALx0v\n-----END PRIVATE KEY-----\n"
            )
            key_path = f.name

        try:
            t = GrpcTransport(
                [{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                use_ssl=True,
                client_cert=cert_path,
                client_key=key_path,
            )
            self.assertTrue(t._use_ssl)
            self.assertEqual(t._client_cert, cert_path)
            self.assertEqual(t._client_key, key_path)
            t.close()
        finally:
            os.unlink(cert_path)
            os.unlink(key_path)

    def test_use_ssl_false_creates_insecure(self) -> None:
        """Explicitly setting use_ssl=False creates insecure channel."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=False,
        )
        self.assertFalse(t._use_ssl)
        t.close()

    def test_secure_channel_with_ssl_context(self) -> None:
        """use_ssl=True with ssl_context extracts CA certs from context."""
        import ssl

        ctx = ssl.create_default_context()
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=True,
            ssl_context=ctx,
        )
        self.assertTrue(t._use_ssl)
        self.assertIs(t._ssl_context, ctx)
        self.assertIsNotNone(t._channel)
        t.close()

    def test_ssl_context_overrides_ca_certs(self) -> None:
        """ssl_context takes precedence over ca_certs when both provided."""
        import ssl

        ctx = ssl.create_default_context()
        # Provide both ssl_context and ca_certs — ssl_context wins
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pem", delete=False) as f:
            f.write(
                b"-----BEGIN CERTIFICATE-----\nMIIBkTCB+wIJALx0v\n-----END CERTIFICATE-----\n"
            )
            ca_path = f.name

        try:
            t = GrpcTransport(
                [{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                use_ssl=True,
                ssl_context=ctx,
                ca_certs=ca_path,
            )
            self.assertIs(t._ssl_context, ctx)
            t.close()
        finally:
            os.unlink(ca_path)

    def test_extract_ca_certs_from_context(self) -> None:
        """_extract_ca_certs_from_context returns PEM-encoded CA certs."""
        import ssl

        ctx = ssl.create_default_context()
        result = GrpcTransport._extract_ca_certs_from_context(ctx)
        # System CAs should be present
        self.assertIsNotNone(result)
        self.assertIn(b"-----BEGIN CERTIFICATE-----", result)
        self.assertIn(b"-----END CERTIFICATE-----", result)

    def test_ssl_assert_hostname_sets_channel_option(self) -> None:
        """ssl_assert_hostname maps to grpc.ssl_target_name_override."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=True,
            ssl_assert_hostname="my-server.example.com",
        )
        self.assertEqual(t._ssl_assert_hostname, "my-server.example.com")
        self.assertIsNotNone(t._channel)
        t.close()

    def test_extract_ca_certs_from_empty_context(self) -> None:
        """_extract_ca_certs_from_context returns None for empty context."""
        import ssl

        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        result = GrpcTransport._extract_ca_certs_from_context(ctx)
        self.assertIsNone(result)


class TestOpenSearchGrpcTlsParams(TestCase):
    """Test that OpenSearchGrpc handles TLS params correctly."""

    def test_accepts_use_ssl_true(self) -> None:
        """OpenSearchGrpc accepts use_ssl=True without error."""
        client = OpenSearchGrpc(
            hosts=[{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=True,
        )
        client.close()

    def test_accepts_ca_certs(self) -> None:
        """OpenSearchGrpc accepts ca_certs without error."""
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pem", delete=False) as f:
            f.write(
                b"-----BEGIN CERTIFICATE-----\nMIIBkTCB\n-----END CERTIFICATE-----\n"
            )
            ca_path = f.name

        try:
            client = OpenSearchGrpc(
                hosts=[{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                use_ssl=True,
                ca_certs=ca_path,
            )
            client.close()
        finally:
            os.unlink(ca_path)

    def test_accepts_ssl_context(self) -> None:
        """OpenSearchGrpc accepts ssl_context without error."""
        import ssl

        ctx = ssl.create_default_context()
        client = OpenSearchGrpc(
            hosts=[{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=True,
            ssl_context=ctx,
        )
        client.close()

    def test_accepts_ssl_version(self) -> None:
        """OpenSearchGrpc accepts ssl_version without error."""
        import ssl

        client = OpenSearchGrpc(
            hosts=[{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=True,
            ssl_version=ssl.PROTOCOL_TLS_CLIENT,
        )
        client.close()

    def test_accepts_ssl_assert_hostname(self) -> None:
        """OpenSearchGrpc accepts ssl_assert_hostname without error."""
        client = OpenSearchGrpc(
            hosts=[{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            use_ssl=True,
            ssl_assert_hostname="my-server.example.com",
        )
        client.close()

    def test_rejects_ssl_assert_fingerprint(self) -> None:
        """OpenSearchGrpc rejects ssl_assert_fingerprint with NotImplementedError."""
        with self.assertRaises(NotImplementedError) as ctx:
            OpenSearchGrpc(
                hosts=[{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                ssl_assert_fingerprint="AA:BB:CC",
            )
        self.assertIn("ssl_assert_fingerprint", str(ctx.exception))

    def test_missing_grpc_deps_raises_improperly_configured(self) -> None:
        """Missing gRPC deps raises ImproperlyConfigured."""
        import sys
        import unittest.mock

        with unittest.mock.patch.dict(
            sys.modules,
            {"opensearch_grpc": None, "opensearch_grpc.grpc_transport": None},
        ):
            import importlib

            import opensearchpy.client

            importlib.reload(opensearchpy.client)
            from opensearchpy.client import OpenSearchGrpc as ReloadedGrpc

            with self.assertRaises(ImproperlyConfigured):
                ReloadedGrpc(
                    hosts=[{"host": "localhost", "port": 9200}],
                    grpc_hosts=[{"host": "localhost", "port": 9400}],
                )
