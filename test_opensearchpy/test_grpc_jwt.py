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
test_grpc_jwt.py — Unit Tests for gRPC JWT/Bearer Token Auth

Tests that BearerTokenInterceptor correctly attaches Bearer tokens
as gRPC metadata. No running server needed.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from opensearch_grpc.grpc_transport import (
    BearerTokenInterceptor,
    GrpcTransport,
)


class TestBearerTokenInterceptor(TestCase):
    """Test BearerTokenInterceptor attaches tokens correctly."""

    def test_attaches_bearer_token_with_prefix(self) -> None:
        """Token with 'Bearer ' prefix is used as-is."""
        token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.sig"
        interceptor = BearerTokenInterceptor(token)
        self.assertEqual(interceptor._auth_header, token)

    def test_attaches_bearer_token_without_prefix(self) -> None:
        """Token without 'Bearer ' prefix gets it added."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.sig"
        interceptor = BearerTokenInterceptor(token)
        self.assertEqual(interceptor._auth_header, f"Bearer {token}")

    def test_adds_authorization_metadata(self) -> None:
        """Interceptor adds 'authorization' to call metadata."""
        interceptor = BearerTokenInterceptor("Bearer mytoken")

        call_details = MagicMock()
        call_details.metadata = []
        call_details._replace = MagicMock(return_value=call_details)

        continuation = MagicMock()
        request = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        call_details._replace.assert_called_once()
        metadata = call_details._replace.call_args[1]["metadata"]
        auth_headers = [m for m in metadata if m[0] == "authorization"]
        self.assertEqual(len(auth_headers), 1)
        self.assertEqual(auth_headers[0][1], "Bearer mytoken")

    def test_preserves_existing_metadata(self) -> None:
        """Interceptor preserves any existing metadata."""
        interceptor = BearerTokenInterceptor("Bearer mytoken")

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
        interceptor = BearerTokenInterceptor("Bearer mytoken")

        call_details = MagicMock()
        call_details.metadata = None
        call_details._replace = MagicMock(return_value=call_details)

        continuation = MagicMock()
        request = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        self.assertEqual(len(metadata), 1)
        self.assertEqual(metadata[0], ("authorization", "Bearer mytoken"))

    def test_full_jwt_token(self) -> None:
        """A realistic JWT token is handled correctly."""
        jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcyMjAwMDAwMCwiZXhwIjoxNzIyMDAzNjAwLCJyb2xlcyI6ImFsbF9hY2Nlc3MifQ.signature"
        interceptor = BearerTokenInterceptor(f"Bearer {jwt}")
        self.assertEqual(interceptor._auth_header, f"Bearer {jwt}")


class TestGrpcTransportBearerDetection(TestCase):
    """Test GrpcTransport detects Bearer tokens and creates correct interceptor."""

    def test_bearer_string_creates_bearer_interceptor(self) -> None:
        """http_auth starting with 'Bearer ' creates BearerTokenInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth="Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.sig",
        )
        self.assertIsNotNone(t._channel)
        t.close()

    def test_bearer_lowercase_creates_bearer_interceptor(self) -> None:
        """http_auth starting with 'bearer ' (lowercase) creates BearerTokenInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth="bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.sig",
        )
        self.assertIsNotNone(t._channel)
        t.close()

    def test_tuple_auth_still_creates_basic_interceptor(self) -> None:
        """Tuple http_auth still creates BasicAuthInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth=("admin", "password"),
        )
        self.assertIsNotNone(t._channel)
        t.close()

    def test_userpass_string_still_creates_basic_interceptor(self) -> None:
        """String 'user:pass' still creates BasicAuthInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth="admin:password",
        )
        self.assertIsNotNone(t._channel)
        t.close()

    def test_no_auth_no_interceptor(self) -> None:
        """No http_auth means no auth interceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
        )
        self.assertIsNone(t._http_auth)
        t.close()
