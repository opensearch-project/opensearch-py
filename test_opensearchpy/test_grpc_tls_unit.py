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

import grpc

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

    def test_rejects_ssl_context(self) -> None:
        """OpenSearchGrpc rejects ssl_context with NotImplementedError."""
        with self.assertRaises(NotImplementedError) as ctx:
            OpenSearchGrpc(
                hosts=[{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                ssl_context="something",
            )
        self.assertIn("ssl_context", str(ctx.exception))

    def test_rejects_ssl_version(self) -> None:
        """OpenSearchGrpc rejects ssl_version with NotImplementedError."""
        with self.assertRaises(NotImplementedError) as ctx:
            OpenSearchGrpc(
                hosts=[{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                ssl_version="TLSv1_2",
            )
        self.assertIn("ssl_version", str(ctx.exception))

    def test_rejects_ssl_assert_hostname(self) -> None:
        """OpenSearchGrpc rejects ssl_assert_hostname with NotImplementedError."""
        with self.assertRaises(NotImplementedError) as ctx:
            OpenSearchGrpc(
                hosts=[{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                ssl_assert_hostname=True,
            )
        self.assertIn("ssl_assert_hostname", str(ctx.exception))

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


class TestGrpcExceptionMapping(TestCase):
    """Test that _raise_grpc_error maps gRPC codes to opensearch-py exceptions."""

    def _make_rpc_error(self, code, details="test error"):
        """Create a mock grpc.RpcError with the given status code."""
        from unittest.mock import MagicMock

        error = MagicMock()
        error.code.return_value = code
        error.details.return_value = details
        return error

    def _get_transport(self):
        """Create a GrpcTransport instance for testing."""
        return GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
        )

    def test_unavailable_raises_connection_error(self) -> None:
        """UNAVAILABLE → ConnectionError."""
        from opensearchpy.exceptions import ConnectionError

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.UNAVAILABLE, "connection refused")
        with self.assertRaises(ConnectionError):
            t._raise_grpc_error(error)
        t.close()

    def test_unavailable_with_ssl_raises_ssl_error(self) -> None:
        """UNAVAILABLE with SSL details → SSLError."""
        from opensearchpy.exceptions import SSLError

        t = self._get_transport()
        error = self._make_rpc_error(
            grpc.StatusCode.UNAVAILABLE, "SSL handshake failed"
        )
        with self.assertRaises(SSLError):
            t._raise_grpc_error(error)
        t.close()

    def test_unavailable_with_tls_raises_ssl_error(self) -> None:
        """UNAVAILABLE with TLS details → SSLError."""
        from opensearchpy.exceptions import SSLError

        t = self._get_transport()
        error = self._make_rpc_error(
            grpc.StatusCode.UNAVAILABLE, "TLS certificate verification failed"
        )
        with self.assertRaises(SSLError):
            t._raise_grpc_error(error)
        t.close()

    def test_deadline_exceeded_raises_connection_timeout(self) -> None:
        """DEADLINE_EXCEEDED → ConnectionTimeout."""
        from opensearchpy.exceptions import ConnectionTimeout

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.DEADLINE_EXCEEDED)
        with self.assertRaises(ConnectionTimeout):
            t._raise_grpc_error(error)
        t.close()

    def test_unauthenticated_raises_authentication_exception(self) -> None:
        """UNAUTHENTICATED → AuthenticationException."""
        from opensearchpy.exceptions import AuthenticationException

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.UNAUTHENTICATED)
        with self.assertRaises(AuthenticationException) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 401)
        t.close()

    def test_permission_denied_raises_authorization_exception(self) -> None:
        """PERMISSION_DENIED → AuthorizationException."""
        from opensearchpy.exceptions import AuthorizationException

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.PERMISSION_DENIED)
        with self.assertRaises(AuthorizationException) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 403)
        t.close()

    def test_not_found_raises_not_found_error(self) -> None:
        """NOT_FOUND → NotFoundError."""
        from opensearchpy.exceptions import NotFoundError

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.NOT_FOUND)
        with self.assertRaises(NotFoundError) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 404)
        t.close()

    def test_already_exists_raises_conflict_error(self) -> None:
        """ALREADY_EXISTS → ConflictError."""
        from opensearchpy.exceptions import ConflictError

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.ALREADY_EXISTS)
        with self.assertRaises(ConflictError) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 409)
        t.close()

    def test_invalid_argument_raises_request_error(self) -> None:
        """INVALID_ARGUMENT → RequestError."""
        from opensearchpy.exceptions import RequestError

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.INVALID_ARGUMENT)
        with self.assertRaises(RequestError) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 400)
        t.close()

    def test_unknown_code_raises_transport_error(self) -> None:
        """Unknown gRPC code → TransportError."""
        from opensearchpy.exceptions import TransportError

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.INTERNAL, "internal error")
        with self.assertRaises(TransportError) as ctx:
            t._raise_grpc_error(error)
        self.assertIn("INTERNAL", str(ctx.exception))
        t.close()

    def test_cancelled_raises_transport_error(self) -> None:
        """CANCELLED → TransportError."""
        from opensearchpy.exceptions import TransportError

        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.CANCELLED)
        with self.assertRaises(TransportError):
            t._raise_grpc_error(error)
        t.close()

    def test_error_details_in_exception_message(self) -> None:
        """Error details are included in the exception message."""
        from opensearchpy.exceptions import ConnectionError

        t = self._get_transport()
        error = self._make_rpc_error(
            grpc.StatusCode.UNAVAILABLE, "failed to connect to all addresses"
        )
        with self.assertRaises(ConnectionError) as ctx:
            t._raise_grpc_error(error)
        self.assertIn("failed to connect", str(ctx.exception))
        t.close()
