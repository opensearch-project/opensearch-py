"""
grpc_transport.py — gRPC Transport for the opensearch-py Client

Routes bulk operations over gRPC for improved performance.
All other operations (search, index, create, delete, update, count, etc.)
fall back to REST automatically.

    - bulk → DocumentService.Bulk (native gRPC)
    - everything else → REST fallback

TLS/SSL Support:
    The gRPC channel supports TLS and mutual TLS (mTLS) using the same
    parameters as the REST client:

    - use_ssl=True: Creates a secure gRPC channel (grpc.secure_channel)
    - ssl_context: A Python ssl.SSLContext — CA certs are extracted from it
      and used for server verification. When provided, ca_certs is ignored.
    - ca_certs: Path to CA bundle for server certificate verification
    - client_cert: Path to client certificate for mTLS
    - client_key: Path to client private key for mTLS

    When use_ssl=True without ca_certs or ssl_context, system default
    trusted CAs are used.
    When use_ssl=False (default), an insecure channel is created.

    Not supported (no gRPC equivalent):
    - ssl_assert_fingerprint: Not available in gRPC Python
    - ssl_show_warn: No equivalent in gRPC

Usage:
    from opensearchpy.client import OpenSearchGrpc

    # Insecure (no TLS)
    client = OpenSearchGrpc(
        hosts=[{"host": "localhost", "port": 9200}],
        grpc_hosts=[{"host": "localhost", "port": 9400}],
    )

    # TLS with server verification
    client = OpenSearchGrpc(
        hosts=[{"host": "localhost", "port": 9200}],
        grpc_hosts=[{"host": "localhost", "port": 9400}],
        use_ssl=True,
        ca_certs="/path/to/root-ca.pem",
    )

    # TLS with ssl_context
    import ssl
    ctx = ssl.create_default_context(cafile="/path/to/root-ca.pem")
    client = OpenSearchGrpc(
        hosts=[{"host": "localhost", "port": 9200}],
        grpc_hosts=[{"host": "localhost", "port": 9400}],
        use_ssl=True,
        ssl_context=ctx,
    )

    # Mutual TLS (mTLS)
    client = OpenSearchGrpc(
        hosts=[{"host": "localhost", "port": 9200}],
        grpc_hosts=[{"host": "localhost", "port": 9400}],
        use_ssl=True,
        ca_certs="/path/to/root-ca.pem",
        client_cert="/path/to/client-cert.pem",
        client_key="/path/to/client-key.pem",
    )
"""

import base64
import re
import ssl
from typing import Any, Callable, Collection, Mapping, Optional, Tuple, Union

import grpc
from opensearch.protobufs.services import document_service_pb2_grpc

from opensearch_grpc.translation import BulkRequestProtoBuilder, ResponseConverter
from opensearchpy.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConflictError,
    ConnectionError,
    ConnectionTimeout,
    NotFoundError,
    RequestError,
    SSLError,
    TransportError,
)
from opensearchpy.transport import Transport


class BasicAuthInterceptor(grpc.UnaryUnaryClientInterceptor):  # type: ignore[misc]
    """gRPC interceptor that adds Basic auth to every unary call.

    Attaches an 'authorization' metadata header with base64-encoded
    credentials, matching how the REST client sends Basic auth.
    """

    def __init__(self, username: str, password: str) -> None:
        credentials = f"{username}:{password}".encode("utf-8")
        self._auth_header = f"Basic {base64.b64encode(credentials).decode('utf-8')}"

    def intercept_unary_unary(
        self, continuation: Any, client_call_details: Any, request: Any
    ) -> Any:
        metadata = list(client_call_details.metadata or [])
        metadata.append(("authorization", self._auth_header))
        new_details = client_call_details._replace(metadata=metadata)
        return continuation(new_details, request)


class GrpcTransport(Transport):
    """
    Transport that routes bulk operations over gRPC.

    Bulk requests are sent via DocumentService.Bulk for better performance.
    All other operations fall back to REST automatically.

    Channel Security:
        - use_ssl=False (default): grpc.insecure_channel
        - use_ssl=True: grpc.secure_channel with ssl_channel_credentials
        - ca_certs: Root CA for server verification (or system defaults)
        - client_cert + client_key: Mutual TLS (mTLS)

    Error Handling:
        gRPC errors are mapped to opensearch-py exceptions:
        - UNAVAILABLE → ConnectionError (retried)
        - DEADLINE_EXCEEDED → ConnectionTimeout (retried if retry_on_timeout)
        - UNAUTHENTICATED → AuthenticationException
        - PERMISSION_DENIED → AuthorizationException
        - NOT_FOUND → NotFoundError
        - ALREADY_EXISTS → ConflictError
        - INVALID_ARGUMENT → RequestError
        - Other → TransportError

    Retry Behavior:
        ConnectionError and ConnectionTimeout are retried up to max_retries
        times, matching the REST transport behavior.
    """

    def __init__(self, hosts: Any, *args: Any, **kwargs: Any) -> None:
        self._grpc_port = kwargs.pop("grpc_port", 9400)
        self._grpc_hosts = kwargs.pop("grpc_hosts", None)

        # Read auth params (don't pop — REST fallback needs them too)
        self._http_auth = kwargs.get("http_auth", None)

        # Read TLS params (don't pop — REST fallback needs them too)
        self._use_ssl = kwargs.get("use_ssl", False)
        self._verify_certs = kwargs.get("verify_certs", True)
        self._ssl_context = kwargs.get("ssl_context", None)
        self._ca_certs = kwargs.get("ca_certs", None)
        self._client_cert = kwargs.get("client_cert", None)
        self._client_key = kwargs.get("client_key", None)
        self._ssl_assert_hostname = kwargs.get("ssl_assert_hostname", None)

        # Validate single gRPC host — multiple targets not yet supported
        if self._grpc_hosts and len(self._grpc_hosts) > 1:
            raise ValueError("Multiple gRPC host targets not yet supported")

        super().__init__(hosts, *args, **kwargs)

        # Resolve gRPC target — grpc_hosts is required
        if not self._grpc_hosts:
            raise ValueError("grpc_hosts parameter is required for GrpcTransport")

        first_grpc = (
            self._grpc_hosts[0]
            if isinstance(self._grpc_hosts[0], dict)
            else {"host": self._grpc_hosts[0]}
        )
        grpc_host = first_grpc.get("host", "localhost")
        grpc_port = first_grpc.get("port", self._grpc_port)

        self._grpc_address = f"{grpc_host}:{grpc_port}"

        # Create channel — secure (TLS/mTLS) or insecure
        # TLS behavior:
        #   - use_ssl=True + ssl_context: Extract CA certs from context
        #   - use_ssl=True + ca_certs: Verify server using provided CA
        #   - use_ssl=True + no ca_certs/ssl_context: Verify using system CAs
        #   - use_ssl=True + client_cert + client_key: Mutual TLS (mTLS)
        #   - use_ssl=False: No encryption (insecure channel)
        if self._use_ssl:
            # gRPC Python does not support disabling certificate verification.
            # When verify_certs=False without ca_certs, gRPC will use system CAs
            # and fail against self-signed certificates. Users MUST provide
            # ca_certs (or ssl_context with CA loaded) for self-signed certs.
            if not self._verify_certs and not self._ca_certs and not self._ssl_context:
                import warnings

                warnings.warn(
                    "gRPC does not support verify_certs=False. The gRPC channel "
                    "will still verify the server certificate using system CAs. "
                    "For self-signed certificates, provide ca_certs or ssl_context. "
                    "The REST fallback will respect verify_certs=False.",
                    stacklevel=2,
                )

            # Determine root CA certificates
            root_certs = None
            if self._ssl_context:
                # Extract CA certs from ssl.SSLContext (DER → PEM)
                root_certs = self._extract_ca_certs_from_context(self._ssl_context)
            elif self._ca_certs:
                with open(self._ca_certs, "rb") as f:
                    root_certs = f.read()

            # Load client certificate and key for mutual TLS (mTLS)
            private_key = None
            cert_chain = None
            if self._client_cert:
                with open(self._client_cert, "rb") as f:
                    cert_chain = f.read()
            if self._client_key:
                with open(self._client_key, "rb") as f:
                    private_key = f.read()

            credentials = grpc.ssl_channel_credentials(
                root_certificates=root_certs,
                private_key=private_key,
                certificate_chain=cert_chain,
            )
            # Build channel options
            options = []
            if self._ssl_assert_hostname:
                options.append(
                    ("grpc.ssl_target_name_override", self._ssl_assert_hostname)
                )

            self._channel = grpc.secure_channel(
                self._grpc_address, credentials, options=options or None
            )
        else:
            self._channel = grpc.insecure_channel(self._grpc_address)

        # Wrap channel with auth interceptor if credentials provided
        if self._http_auth is not None:
            if isinstance(self._http_auth, (tuple, list)):
                username, password = self._http_auth[0], self._http_auth[1]
            else:
                # String format "user:pass"
                username, password = str(self._http_auth).split(":", 1)
            interceptor = BasicAuthInterceptor(username, password)
            self._channel = grpc.intercept_channel(self._channel, interceptor)

        self._document_stub = document_service_pb2_grpc.DocumentServiceStub(
            self._channel
        )

    def perform_request(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        body: Any = None,
        timeout: Optional[Union[int, float]] = None,
        ignore: Collection[int] = (),
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """Route to gRPC or REST based on the URL pattern."""
        handler = self._get_grpc_handler(method, url)
        if handler:
            # Retry loop for gRPC — mirrors Transport.perform_request behavior
            for attempt in range(self.max_retries + 1):
                try:
                    return handler(method, url, params, body)
                except ConnectionTimeout:
                    if self.retry_on_timeout and attempt < self.max_retries:
                        continue
                    # Fallback to REST after retries exhausted
                    break
                except ConnectionError:
                    if attempt < self.max_retries:
                        continue
                    # Fallback to REST after retries exhausted
                    break
                except TransportError as e:
                    if (
                        hasattr(e, "status_code")
                        and e.status_code in self.retry_on_status
                        and attempt < self.max_retries
                    ):
                        continue
                    # Non-retryable errors (auth, request errors) should NOT
                    # fall back to REST — raise immediately
                    raise

        return super().perform_request(
            method,
            url,
            params=params,
            body=body,
            timeout=timeout,
            ignore=ignore,
            headers=headers,
        )

    # Matches: /_bulk or /<index>/_bulk
    _BULK_PATTERN = re.compile(r"^/([^/]+/)?_bulk$")

    def _get_grpc_handler(self, method: str, url: str) -> Optional[Callable[..., Any]]:
        """Determine if this request can be handled via gRPC.

        Only bulk requests are routed over gRPC.
        All other operations fall through to REST.

        Matches endpoints:
            POST /_bulk
            POST /<index>/_bulk
        """
        if method in ("POST", "PUT") and self._BULK_PATTERN.match(url):
            return self._handle_bulk

        return None

    # ─── gRPC Handlers ────────────────────────────────────────────────────────

    def _handle_bulk(
        self, method: str, url: str, params: Optional[Mapping[str, Any]], body: Any
    ) -> Any:
        """Bulk → DocumentService.Bulk (native gRPC)."""
        url_index = self._extract_index_from_url(url, "_bulk")
        refresh = params.get("refresh") if params else None
        timeout = params.get("timeout") if params else None
        pipeline = params.get("pipeline") if params else None
        routing = params.get("routing") if params else None

        converter = BulkRequestProtoBuilder.from_body(
            body,
            index=url_index,
            refresh=refresh,
            timeout=timeout,
            pipeline=pipeline,
            routing=routing,
        )

        try:
            response = self._document_stub.Bulk(converter.build())
        except grpc.RpcError as e:
            self._raise_grpc_error(e)

        return ResponseConverter._convert_bulk_items(response)

    def _raise_grpc_error(self, error: grpc.RpcError) -> None:
        """Convert grpc.RpcError to opensearch-py exceptions.

        Maps gRPC status codes to the same exception types that the REST
        client raises, so users' existing except blocks work unchanged.
        """
        code = error.code()
        details = error.details() or "gRPC error"

        if code == grpc.StatusCode.UNAVAILABLE:
            # Detect SSL/TLS-specific failures
            if "SSL" in details or "TLS" in details or "handshake" in details:
                raise SSLError("N/A", details, error)
            raise ConnectionError("N/A", details, error)
        elif code == grpc.StatusCode.DEADLINE_EXCEEDED:
            raise ConnectionTimeout("TIMEOUT", details, error)
        elif code == grpc.StatusCode.UNAUTHENTICATED:
            raise AuthenticationException(401, details, {"error": details})
        elif code == grpc.StatusCode.PERMISSION_DENIED:
            raise AuthorizationException(403, details, {"error": details})
        elif code == grpc.StatusCode.NOT_FOUND:
            raise NotFoundError(404, details, {"error": details})
        elif code == grpc.StatusCode.ALREADY_EXISTS:
            raise ConflictError(409, details, {"error": details})
        elif code == grpc.StatusCode.INVALID_ARGUMENT:
            raise RequestError(400, details, {"error": details})
        else:
            raise TransportError("N/A", f"gRPC {code.name}: {details}", error)

    def _extract_index_from_url(self, url: str, endpoint: str) -> Optional[str]:
        """Extract index from URL like /my-index/_bulk → 'my-index'."""
        parts = url.strip("/").split("/")
        if len(parts) >= 2 and parts[-1] == endpoint:
            return "/".join(parts[:-1])
        return None

    @staticmethod
    def _extract_ca_certs_from_context(ctx: ssl.SSLContext) -> Optional[bytes]:
        """Extract CA certificates from an ssl.SSLContext as PEM bytes.

        Retrieves all loaded CA certs in DER format and converts them to
        PEM for use with grpc.ssl_channel_credentials(root_certificates=...).

        Returns None if no CA certs are loaded in the context.
        """
        der_certs = ctx.get_ca_certs(binary_form=True)
        if not der_certs:
            return None

        import base64

        pem_certs = []
        for der_cert in der_certs:
            b64 = base64.b64encode(der_cert).decode("ascii")
            # Wrap at 64 characters per line (PEM standard)
            lines = [b64[i : i + 64] for i in range(0, len(b64), 64)]
            pem = "-----BEGIN CERTIFICATE-----\n"
            pem += "\n".join(lines)
            pem += "\n-----END CERTIFICATE-----\n"
            pem_certs.append(pem)

        return "".join(pem_certs).encode("ascii")

    def close(self) -> None:
        """Close gRPC channel and REST connections."""
        if self._channel:
            self._channel.close()
        super().close()
