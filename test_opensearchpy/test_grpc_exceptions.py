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
test_grpc_exceptions.py — Unit Tests for gRPC Exception Mapping

Tests that GrpcTransport correctly maps gRPC status codes to opensearch-py
exceptions and that the retry loop behaves correctly.

No running server needed.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

import grpc

from opensearch_grpc.grpc_transport import GrpcTransport
from opensearchpy.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConflictError,
    ConnectionError,
    ConnectionTimeout,
    NotFoundError,
    RequestError,
    TransportError,
)


class TestGrpcExceptionMapping(TestCase):
    """Test _raise_grpc_error maps gRPC codes to opensearch-py exceptions."""

    def _make_rpc_error(self, code, details="test error"):
        """Create a mock grpc.RpcError with the given status code."""
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
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.UNAVAILABLE, "connection refused")
        with self.assertRaises(ConnectionError):
            t._raise_grpc_error(error)
        t.close()

    def test_deadline_exceeded_raises_connection_timeout(self) -> None:
        """DEADLINE_EXCEEDED → ConnectionTimeout."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.DEADLINE_EXCEEDED)
        with self.assertRaises(ConnectionTimeout):
            t._raise_grpc_error(error)
        t.close()

    def test_unauthenticated_raises_authentication_exception(self) -> None:
        """UNAUTHENTICATED → AuthenticationException with status 401."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.UNAUTHENTICATED)
        with self.assertRaises(AuthenticationException) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 401)
        t.close()

    def test_permission_denied_raises_authorization_exception(self) -> None:
        """PERMISSION_DENIED → AuthorizationException with status 403."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.PERMISSION_DENIED)
        with self.assertRaises(AuthorizationException) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 403)
        t.close()

    def test_not_found_raises_not_found_error(self) -> None:
        """NOT_FOUND → NotFoundError with status 404."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.NOT_FOUND)
        with self.assertRaises(NotFoundError) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 404)
        t.close()

    def test_already_exists_raises_conflict_error(self) -> None:
        """ALREADY_EXISTS → ConflictError with status 409."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.ALREADY_EXISTS)
        with self.assertRaises(ConflictError) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 409)
        t.close()

    def test_invalid_argument_raises_request_error(self) -> None:
        """INVALID_ARGUMENT → RequestError with status 400."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.INVALID_ARGUMENT)
        with self.assertRaises(RequestError) as ctx:
            t._raise_grpc_error(error)
        self.assertEqual(ctx.exception.status_code, 400)
        t.close()

    def test_internal_raises_transport_error(self) -> None:
        """INTERNAL → TransportError."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.INTERNAL, "internal error")
        with self.assertRaises(TransportError) as ctx:
            t._raise_grpc_error(error)
        self.assertIn("INTERNAL", str(ctx.exception))
        t.close()

    def test_cancelled_raises_transport_error(self) -> None:
        """CANCELLED → TransportError."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.CANCELLED)
        with self.assertRaises(TransportError):
            t._raise_grpc_error(error)
        t.close()

    def test_unimplemented_raises_transport_error(self) -> None:
        """UNIMPLEMENTED → TransportError."""
        t = self._get_transport()
        error = self._make_rpc_error(grpc.StatusCode.UNIMPLEMENTED)
        with self.assertRaises(TransportError):
            t._raise_grpc_error(error)
        t.close()

    def test_error_details_in_exception_message(self) -> None:
        """Error details are preserved in the exception message."""
        t = self._get_transport()
        error = self._make_rpc_error(
            grpc.StatusCode.UNAVAILABLE, "failed to connect to all addresses"
        )
        with self.assertRaises(ConnectionError) as ctx:
            t._raise_grpc_error(error)
        self.assertIn("failed to connect", str(ctx.exception))
        t.close()


class TestGrpcRetryBehavior(TestCase):
    """Test that the gRPC retry loop works correctly."""

    def test_connection_error_retries(self) -> None:
        """ConnectionError retries gRPC then falls back to REST."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 19400}],  # unreachable
            max_retries=2,
        )
        # gRPC fails after retries, falls back to REST which also fails
        # (no REST server running) — but the error comes from REST, not gRPC
        with self.assertRaises((ConnectionError, TransportError)):
            t.perform_request(
                "POST",
                "/_bulk",
                body=[{"index": {"_index": "test", "_id": "1"}}, {"x": 1}],
            )
        t.close()

    def test_no_retry_on_request_error(self) -> None:
        """RequestError is NOT retried — raises immediately."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            max_retries=3,
        )

        # Mock _handle_bulk to raise RequestError
        def mock_handler(method, url, params, body):
            raise RequestError(400, "bad request", {"error": "bad"})

        with patch.object(t, "_handle_bulk", side_effect=mock_handler):
            with self.assertRaises(RequestError):
                t.perform_request(
                    "POST",
                    "/_bulk",
                    body=[{"index": {"_index": "test", "_id": "1"}}, {"x": 1}],
                )
        t.close()

    def test_no_retry_on_auth_error(self) -> None:
        """AuthenticationException is NOT retried — raises immediately."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            max_retries=3,
        )

        def mock_handler(method, url, params, body):
            raise AuthenticationException(401, "unauthorized", {"error": "auth"})

        with patch.object(t, "_handle_bulk", side_effect=mock_handler):
            with self.assertRaises(AuthenticationException):
                t.perform_request(
                    "POST",
                    "/_bulk",
                    body=[{"index": {"_index": "test", "_id": "1"}}, {"x": 1}],
                )
        t.close()

    def test_non_bulk_goes_to_rest(self) -> None:
        """Non-bulk requests bypass gRPC and go to REST transport."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
        )
        # _get_grpc_handler should return None for non-bulk
        handler = t._get_grpc_handler("GET", "/test-index/_search")
        self.assertIsNone(handler)

        handler = t._get_grpc_handler("GET", "/test-index/_count")
        self.assertIsNone(handler)

        handler = t._get_grpc_handler("PUT", "/test-index")
        self.assertIsNone(handler)
        t.close()

    def test_bulk_routes_to_grpc(self) -> None:
        """Bulk requests route to gRPC handler."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
        )
        handler = t._get_grpc_handler("POST", "/_bulk")
        self.assertIsNotNone(handler)

        handler = t._get_grpc_handler("POST", "/my-index/_bulk")
        self.assertIsNotNone(handler)

        # PUT also supported for bulk
        handler = t._get_grpc_handler("PUT", "/_bulk")
        self.assertIsNotNone(handler)
        t.close()
