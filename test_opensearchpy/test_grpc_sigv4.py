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
test_grpc_sigv4.py — Unit Tests for gRPC SigV4 Auth

Tests that AWSV4GrpcInterceptor correctly signs gRPC requests using
AWS SigV4 and attaches signed headers as gRPC metadata.
No running server or real AWS credentials needed.
"""

import uuid
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from opensearch_grpc.grpc_transport import AWSV4GrpcInterceptor, GrpcTransport


class TestAWSV4GrpcInterceptor(TestCase):
    """Test AWSV4GrpcInterceptor signs requests correctly."""

    def _mock_credentials(self):
        """Create mock AWS credentials."""
        creds = Mock()
        creds.access_key = uuid.uuid4().hex
        creds.secret_key = uuid.uuid4().hex
        creds.token = uuid.uuid4().hex
        del creds.get_frozen_credentials
        return creds

    def _mock_credentials_with_frozen(self):
        """Create mock credentials with get_frozen_credentials."""
        frozen = Mock()
        frozen.access_key = uuid.uuid4().hex
        frozen.secret_key = uuid.uuid4().hex
        frozen.token = uuid.uuid4().hex

        creds = Mock()
        creds.get_frozen_credentials = Mock(return_value=frozen)
        return creds, frozen

    def _make_call_details(self, method="/opensearch.DocumentService/Bulk"):
        """Create mock gRPC client_call_details."""
        details = MagicMock()
        details.method = method
        details.metadata = []
        details._replace = MagicMock(return_value=details)
        return details

    def _make_request(self, data=b"fake protobuf bytes"):
        """Create mock protobuf request."""
        request = MagicMock()
        request.SerializeToString = MagicMock(return_value=data)
        return request

    def test_interceptor_adds_authorization_metadata(self) -> None:
        """Verify SigV4 headers are added as gRPC metadata."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(
            creds, "us-east-1", "es", "my-domain.us-east-1.es.amazonaws.com"
        )

        call_details = self._make_call_details()
        request = self._make_request()
        continuation = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        # Verify _replace was called with metadata
        call_details._replace.assert_called_once()
        metadata = call_details._replace.call_args[1]["metadata"]

        # Should have signed headers as metadata
        meta_keys = [k for k, v in metadata]
        self.assertIn("authorization", meta_keys)
        self.assertIn("x-amz-date", meta_keys)
        self.assertIn("x-amz-content-sha256", meta_keys)

        # Authorization header should start with AWS4-HMAC-SHA256
        auth_value = next(v for k, v in metadata if k == "authorization")
        self.assertTrue(auth_value.startswith("AWS4-HMAC-SHA256"))

    def test_interceptor_includes_security_token(self) -> None:
        """Verify X-Amz-Security-Token is included when token is present."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(
            creds, "us-east-1", "es", "my-domain.us-east-1.es.amazonaws.com"
        )

        call_details = self._make_call_details()
        request = self._make_request()
        continuation = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        meta_keys = [k for k, v in metadata]
        self.assertIn("x-amz-security-token", meta_keys)

    def test_interceptor_signs_with_grpc_method_path(self) -> None:
        """Verify the signing URL uses the gRPC method path."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(
            creds, "us-west-2", "es", "my-domain.us-west-2.es.amazonaws.com"
        )

        call_details = self._make_call_details("/opensearch.DocumentService/Bulk")
        request = self._make_request()
        continuation = MagicMock()

        with patch.object(
            interceptor._signer, "sign", wraps=interceptor._signer.sign
        ) as mock_sign:
            interceptor.intercept_unary_unary(continuation, call_details, request)

            mock_sign.assert_called_once()
            call_args = mock_sign.call_args
            self.assertEqual(call_args[1]["method"], "POST")
            self.assertIn("/opensearch.DocumentService/Bulk", call_args[1]["url"])
            self.assertIn("my-domain.us-west-2.es.amazonaws.com", call_args[1]["url"])

    def test_interceptor_signs_serialized_body(self) -> None:
        """Verify serialized protobuf body is passed to signer."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", "localhost")

        call_details = self._make_call_details()
        body_bytes = b"\x0a\x05hello"
        request = self._make_request(data=body_bytes)
        continuation = MagicMock()

        with patch.object(
            interceptor._signer, "sign", wraps=interceptor._signer.sign
        ) as mock_sign:
            interceptor.intercept_unary_unary(continuation, call_details, request)

            call_args = mock_sign.call_args
            self.assertEqual(call_args[1]["body"], body_bytes)

    def test_interceptor_uses_frozen_credentials(self) -> None:
        """get_frozen_credentials is called if available."""
        creds, _frozen = self._mock_credentials_with_frozen()
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", "localhost")

        call_details = self._make_call_details()
        request = self._make_request()
        continuation = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        # get_frozen_credentials should be called by AWSV4Signer.sign()
        creds.get_frozen_credentials.assert_called()

    def test_interceptor_preserves_existing_metadata(self) -> None:
        """Existing gRPC metadata is not overwritten."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", "localhost")

        call_details = self._make_call_details()
        call_details.metadata = [("x-custom-header", "custom-value")]
        continuation = MagicMock()
        request = self._make_request()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        custom_headers = [v for k, v in metadata if k == "x-custom-header"]
        self.assertEqual(custom_headers, ["custom-value"])

    def test_interceptor_signs_per_request(self) -> None:
        """Each call generates a fresh signature."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", "localhost")

        continuation = MagicMock()
        request = self._make_request()

        # First call
        details1 = self._make_call_details()
        interceptor.intercept_unary_unary(continuation, details1, request)
        metadata1 = details1._replace.call_args[1]["metadata"]
        auth1 = next(v for k, v in metadata1 if k == "authorization")

        # Second call (same instant in tests, but signature should still be computed fresh)
        details2 = self._make_call_details()
        interceptor.intercept_unary_unary(continuation, details2, request)
        metadata2 = details2._replace.call_args[1]["metadata"]
        auth2 = next(v for k, v in metadata2 if k == "authorization")

        # Both should have authorization (proves sign() was called both times)
        self.assertTrue(auth1.startswith("AWS4-HMAC-SHA256"))
        self.assertTrue(auth2.startswith("AWS4-HMAC-SHA256"))

    def test_interceptor_region_validation(self) -> None:
        """Region cannot be empty."""
        creds = self._mock_credentials()
        with self.assertRaises(ValueError) as ctx:
            AWSV4GrpcInterceptor(creds, "", "es", "localhost")
        self.assertIn("Region", str(ctx.exception))

    def test_interceptor_credentials_validation(self) -> None:
        """Credentials cannot be empty."""
        with self.assertRaises(ValueError) as ctx:
            AWSV4GrpcInterceptor(None, "us-east-1", "es", "localhost")
        self.assertIn("Credentials", str(ctx.exception))

    def test_interceptor_service_name(self) -> None:
        """Service name is passed through (es vs aoss)."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "aoss", "localhost")
        self.assertEqual(interceptor._signer.service, "aoss")

    def test_credential_scope_in_authorization(self) -> None:
        """Authorization header contains credential scope (date/region/service/aws4_request)."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(
            creds, "us-west-2", "es", "my-domain.us-west-2.es.amazonaws.com"
        )

        call_details = self._make_call_details()
        request = self._make_request()
        continuation = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        auth_value = next(v for k, v in metadata if k == "authorization")

        # Credential scope format: YYYYMMDD/region/service/aws4_request
        self.assertIn("us-west-2", auth_value)
        self.assertIn("es", auth_value)
        self.assertIn("aws4_request", auth_value)
        self.assertIn("Credential=", auth_value)

    def test_signed_headers_includes_host(self) -> None:
        """SignedHeaders in Authorization includes 'host'."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", "localhost")

        call_details = self._make_call_details()
        request = self._make_request()
        continuation = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        auth_value = next(v for k, v in metadata if k == "authorization")

        # SignedHeaders should include 'host'
        self.assertIn("SignedHeaders=", auth_value)
        self.assertIn("host", auth_value)

    def test_no_security_token_without_session_token(self) -> None:
        """Without a session token, x-amz-security-token is NOT included."""
        creds = Mock()
        creds.access_key = "AKIAIOSFODNN7EXAMPLE"
        creds.secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        creds.token = None  # No session token
        del creds.get_frozen_credentials

        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", "localhost")

        call_details = self._make_call_details()
        request = self._make_request()
        continuation = MagicMock()

        interceptor.intercept_unary_unary(continuation, call_details, request)

        metadata = call_details._replace.call_args[1]["metadata"]
        meta_keys = [k for k, v in metadata]
        self.assertNotIn("x-amz-security-token", meta_keys)

    def test_different_body_produces_different_signature(self) -> None:
        """Different request bodies produce different signatures (payload hash changes)."""
        creds = self._mock_credentials()
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", "localhost")

        continuation = MagicMock()

        # First request with body A
        details1 = self._make_call_details()
        request1 = self._make_request(data=b"body-content-A")
        interceptor.intercept_unary_unary(continuation, details1, request1)
        metadata1 = details1._replace.call_args[1]["metadata"]
        auth1 = next(v for k, v in metadata1 if k == "authorization")

        # Second request with body B
        details2 = self._make_call_details()
        request2 = self._make_request(data=b"body-content-B")
        interceptor.intercept_unary_unary(continuation, details2, request2)
        metadata2 = details2._replace.call_args[1]["metadata"]
        auth2 = next(v for k, v in metadata2 if k == "authorization")

        # Different bodies → different signatures
        self.assertNotEqual(auth1, auth2)

    def test_signing_url_includes_host(self) -> None:
        """The signing URL includes the configured host."""
        creds = self._mock_credentials()
        host = "search-my-domain.us-east-1.es.amazonaws.com"
        interceptor = AWSV4GrpcInterceptor(creds, "us-east-1", "es", host)

        call_details = self._make_call_details("/opensearch.DocumentService/Bulk")
        request = self._make_request()
        continuation = MagicMock()

        with patch.object(
            interceptor._signer, "sign", wraps=interceptor._signer.sign
        ) as mock_sign:
            interceptor.intercept_unary_unary(continuation, call_details, request)

            call_args = mock_sign.call_args
            signed_url = call_args[1]["url"]
            self.assertIn(host, signed_url)
            self.assertTrue(signed_url.startswith("https://"))


class TestGrpcTransportSigV4Detection(TestCase):
    """Test GrpcTransport detects SigV4 callable and creates interceptor."""

    def _mock_signer_auth(self):
        """Create a mock Urllib3AWSV4SignerAuth-like object."""
        auth = MagicMock()
        auth.signer = MagicMock()
        auth.signer.credentials = MagicMock()
        auth.signer.credentials.access_key = "AKIAIOSFODNN7EXAMPLE"
        auth.signer.credentials.secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        auth.signer.credentials.token = None
        auth.signer.region = "us-east-1"
        auth.signer.service = "es"
        # Make it callable
        auth.__call__ = MagicMock()
        return auth

    def test_callable_with_signer_creates_sigv4_interceptor(self) -> None:
        """Callable http_auth with .signer creates AWSV4GrpcInterceptor."""
        auth = self._mock_signer_auth()
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "my-domain.us-east-1.es.amazonaws.com", "port": 9400}],
            http_auth=auth,
            use_ssl=True,
        )
        # Channel should be intercepted (no direct way to inspect, but no error)
        self.assertIsNotNone(t._channel)
        t.close()

    def test_callable_without_signer_raises(self) -> None:
        """Callable http_auth without .signer raises NotImplementedError."""
        auth = MagicMock()
        # Remove signer attribute
        del auth.signer

        with self.assertRaises(NotImplementedError) as ctx:
            GrpcTransport(
                [{"host": "localhost", "port": 9200}],
                grpc_hosts=[{"host": "localhost", "port": 9400}],
                http_auth=auth,
            )
        self.assertIn("Custom callable auth", str(ctx.exception))

    def test_tuple_auth_still_works(self) -> None:
        """Tuple http_auth still creates BasicAuthInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth=("admin", "password"),
        )
        self.assertIsNotNone(t._channel)
        t.close()

    def test_string_auth_still_works(self) -> None:
        """String http_auth still creates BasicAuthInterceptor."""
        t = GrpcTransport(
            [{"host": "localhost", "port": 9200}],
            grpc_hosts=[{"host": "localhost", "port": 9400}],
            http_auth="admin:password",
        )
        self.assertIsNotNone(t._channel)
        t.close()
