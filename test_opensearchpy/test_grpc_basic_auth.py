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
test_grpc_basic_auth.py — Unit Tests for gRPC Basic Auth

Tests that BasicAuthInterceptor correctly encodes credentials and
attaches them to gRPC metadata. No running server needed.
"""

import base64
from unittest import TestCase
from unittest.mock import MagicMock

import grpc

from opensearch_grpc.grpc_transport import BasicAuthInterceptor, GrpcTransport
from opensearchpy.exceptions import AuthenticationException, AuthorizationException


class TestBasicAuthInterceptor(TestCase):
    """Test BasicAuthInterceptor encodes credentials correctly."""

    def test_encodes_credentials_as_base64(self) -> None:
        """Credentials are base64-encoded in Basic format."""
        interceptor = BasicAuthInterceptor("admin", "password")
        expected = base64.b64encode(b"admin:password").decode("utf-8")
        self.assertEqual(interceptor._auth_header, f"Basic {expected}")

    def test_encodes_special_characters(self) -> None:
        """Special characters in password are encoded correctly."""
        interceptor = BasicAuthInterceptor("admin", "myStr0ng!P@ss:w0rd")
        expected = base64.b64encode(b"admin:myStr0ng!P@ss:w0rd").decode("utf-8")
        self.assertEqual(interceptor._auth_header, f"Basic {expected}")

    def test_adds_authorization_metadata(self) -> None:
        """Interceptor adds 'authorization' to call metadata."""
        interceptor = BasicAuthInterceptor("admin", "password")

        # Mock call details
        call_details = MagicMock()
        call_details.metadata = []
        call_details._replace = MagicMock(return_value=call_details)

        continuation = MagicMock()
        request = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        # Verify _replace was called with metadata containing authorization
        call_details._replace.assert_called_once()
        metadata = call_details._replace.call_args[1]["metadata"]
        auth_headers = [m for m in metadata if m[0] == "authorization"]
        self.assertEqual(len(auth_headers), 1)
        self.assertTrue(auth_headers[0][1].startswith("Basic "))

    def test_preserves_existing_metadata(self) -> None:
        """Interceptor preserves any existing metadata."""
        interceptor = BasicAuthInterceptor("admin", "password")

        call_details = MagicMock()
        call_details.metadata = [("x-custom-header", "value")]
        call_details._replace = MagicMock(return_value=call_details)

        continuation = MagicMock()
        request = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        self.assertEqual(len(metadata), 2)
        self.assertEqual(metadata[0], ("x-custom-header", "value"))
        self.assertEqual(metadata[1][0], "authorization")

    def test_handles_none_metadata(self) -> None:
        """Interceptor handles None metadata gracefully."""
        interceptor = BasicAuthInterceptor("admin", "password")

        call_details = MagicMock()
        call_details.metadata = None
        call_details._replace = MagicMock(return_value=call_details)

        continuation = MagicMock()
        request = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        self.assertEqual(len(metadata), 1)
        self.assertEqual(metadata[0][0], "authorization")


class TestGrpcTransportBasicAuth(TestCase):
    """Test GrpcTransport creates interceptor from http_auth."""

    def test_tuple_auth_creates_interceptor(self) -> None:
        """http_auth as tuple creates BasicAuthInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth=("admin", "password"),
        )
        self.assertIsNotNone(t._http_auth)
        t.close()

    def test_string_auth_creates_interceptor(self) -> None:
        """http_auth as string creates BasicAuthInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth="admin:password",
        )
        self.assertIsNotNone(t._http_auth)
        t.close()

    def test_no_auth_no_interceptor(self) -> None:
        """No http_auth means no auth interceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
        )
        self.assertIsNone(t._http_auth)
        t.close()

    def test_opensearch_grpc_accepts_http_auth(self) -> None:
        """OpenSearchGrpc accepts http_auth without error."""
        from opensearchpy.client import OpenSearchGrpc

        client = OpenSearchGrpc(
            hosts=[{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth=("admin", "password"),
        )
        client.close()


class TestGrpcAuthExceptions(TestCase):
    """Test that auth-related gRPC errors raise correct exceptions."""

    def _make_rpc_error(self, code, details="test error"):
        error = MagicMock()
        error.code.return_value = code
        error.details.return_value = details
        return error

    def _get_transport(self, **kwargs):
        return GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            **kwargs,
        )

    def test_unauthenticated_raises_authentication_exception(self) -> None:
        """UNAUTHENTICATED → AuthenticationException (401)."""
        t = self._get_transport(http_auth=("admin", "wrongpassword"))
        error = self._make_rpc_error(
            grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials"
        )
        with self.assertRaises(AuthenticationException) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Invalid credentials", str(ctx.exception))
        t.close()

    def test_permission_denied_raises_authorization_exception(self) -> None:
        """PERMISSION_DENIED → AuthorizationException (403)."""
        t = self._get_transport(http_auth=("readonly_user", "password"))
        error = self._make_rpc_error(
            grpc.StatusCode.PERMISSION_DENIED, "Insufficient permissions"
        )
        with self.assertRaises(AuthorizationException) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("Insufficient permissions", str(ctx.exception))
        t.close()

    def test_no_auth_unauthenticated_raises_exception(self) -> None:
        """Server requiring auth without credentials → AuthenticationException."""
        t = self._get_transport()
        error = self._make_rpc_error(
            grpc.StatusCode.UNAUTHENTICATED, "Authentication required"
        )
        with self.assertRaises(AuthenticationException):
            t._raise_grpc_error(error)
        t.close()
