"""
grpc_transport.py — gRPC Transport for the opensearch-py Client

Routes bulk operations over gRPC for improved performance.
All other operations (search, index, create, delete, update, count, etc.)
fall back to REST automatically.

    - bulk → DocumentService.Bulk (native gRPC)
    - everything else → REST fallback

Uses opensearch-py's own serializer and method patterns for integration.

Usage:
    from opensearchpy import OpenSearchGrpc

    client = OpenSearchGrpc(
        hosts=[{"host": "localhost", "port": 9200}],
        grpc_hosts=[{"host": "localhost", "port": 9400}],
    )
"""

import re
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
    TransportError,
)
from opensearchpy.transport import Transport


class GrpcTransport(Transport):
    """
    Transport that routes bulk operations over gRPC.

    Bulk requests are sent via DocumentService.Bulk for better performance.
    All other operations fall back to REST automatically.
    """

    def __init__(self, hosts: Any, *args: Any, **kwargs: Any) -> None:
        self._grpc_port = kwargs.pop("grpc_port", 9400)
        self._grpc_hosts = kwargs.pop("grpc_hosts", None)

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
        self._channel = grpc.insecure_channel(self._grpc_address)
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
        """Route to gRPC or REST based on the URL pattern.

        If a gRPC handler exists for this request, attempts gRPC first with
        retries. If gRPC is unavailable after all retries, falls back to REST
        silently so the operation still succeeds.
        """
        handler = self._get_grpc_handler(method, url)
        if handler:
            # Ensure channel is healthy before attempting gRPC
            self._ensure_channel_connected()

            # Retry loop for gRPC — mirrors Transport.perform_request behavior
            for attempt in range(self.max_retries + 1):
                try:
                    return handler(method, url, params, body)
                except ConnectionTimeout:
                    if self.retry_on_timeout and attempt < self.max_retries:
                        continue
                    # Fall back to REST on final failure
                    break
                except ConnectionError:
                    if attempt < self.max_retries:
                        # Attempt channel reconnect before next retry
                        self._reconnect_channel()
                        continue
                    # Fall back to REST on final failure
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

            # gRPC unavailable after retries — fall back to REST silently

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
        require_alias = params.get("require_alias") if params else None

        converter = BulkRequestProtoBuilder.from_body(
            body,
            index=url_index,
            refresh=refresh,
            timeout=timeout,
            pipeline=pipeline,
            routing=routing,
            require_alias=require_alias,
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

        Mapping follows the comprehensive gRPC-to-HTTP status code table
        from opensearch-project/OpenSearch#18926:
            OK (0)                → (no error)
            CANCELLED (1)        → TransportError
            UNKNOWN (2)          → TransportError
            INVALID_ARGUMENT (3) → RequestError (400)
            DEADLINE_EXCEEDED (4)→ ConnectionTimeout
            NOT_FOUND (5)        → NotFoundError (404)
            ALREADY_EXISTS (6)   → ConflictError (409)
            PERMISSION_DENIED (7)→ AuthorizationException (403)
            RESOURCE_EXHAUSTED(8)→ TransportError (429)
            FAILED_PRECONDITION(9)→ RequestError (400)
            ABORTED (10)         → ConflictError (409)
            OUT_OF_RANGE (11)    → RequestError (400)
            UNIMPLEMENTED (12)   → TransportError (501)
            INTERNAL (13)        → TransportError (500)
            UNAVAILABLE (14)     → ConnectionError / SSLError
            UNAUTHENTICATED (16) → AuthenticationException (401)
            DATA_LOSS (15)       → TransportError (500)
        """
        code = error.code()
        details = error.details() or "gRPC error"

        if code == grpc.StatusCode.OK:
            return  # No error
        elif code == grpc.StatusCode.UNAVAILABLE:
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
        elif code == grpc.StatusCode.ABORTED:
            raise ConflictError(409, details, {"error": details})
        elif code == grpc.StatusCode.INVALID_ARGUMENT:
            raise RequestError(400, details, {"error": details})
        elif code == grpc.StatusCode.FAILED_PRECONDITION:
            raise RequestError(400, details, {"error": details})
        elif code == grpc.StatusCode.OUT_OF_RANGE:
            raise RequestError(400, details, {"error": details})
        elif code == grpc.StatusCode.RESOURCE_EXHAUSTED:
            raise TransportError(429, f"gRPC RESOURCE_EXHAUSTED: {details}", error)
        elif code == grpc.StatusCode.UNIMPLEMENTED:
            raise TransportError(501, f"gRPC UNIMPLEMENTED: {details}", error)
        elif code == grpc.StatusCode.INTERNAL:
            raise TransportError(500, f"gRPC INTERNAL: {details}", error)
        elif code == grpc.StatusCode.DATA_LOSS:
            raise TransportError(500, f"gRPC DATA_LOSS: {details}", error)
        elif code == grpc.StatusCode.CANCELLED:
            raise TransportError("N/A", f"gRPC CANCELLED: {details}", error)
        else:
            # UNKNOWN or any future codes
            raise TransportError("N/A", f"gRPC {code.name}: {details}", error)

    def _extract_index_from_url(self, url: str, endpoint: str) -> Optional[str]:
        """Extract index from URL like /my-index/_bulk → 'my-index'."""
        parts = url.strip("/").split("/")
        if len(parts) >= 2 and parts[-1] == endpoint:
            return "/".join(parts[:-1])
        return None

    def _ensure_channel_connected(self) -> None:
        """Check channel state and reconnect if in SHUTDOWN state.

        gRPC channels handle TRANSIENT_FAILURE internally with backoff,
        but SHUTDOWN is terminal — the channel must be recreated.
        """
        try:
            state = self._channel.get_state(try_to_connect=False)  # type: ignore[attr-defined]
            if state == grpc.ChannelConnectivity.SHUTDOWN:
                self._reconnect_channel()
        except AttributeError:
            # get_state not available in all grpc versions — skip check
            pass

    def _reconnect_channel(self) -> None:
        """Recreate the gRPC channel and document stub.

        Called when the channel enters an unrecoverable state or after
        a connection failure during retry.
        """
        try:
            self._channel.close()
        except Exception:
            pass
        self._channel = grpc.insecure_channel(self._grpc_address)
        self._document_stub = document_service_pb2_grpc.DocumentServiceStub(
            self._channel
        )

    def close(self) -> None:
        """Close gRPC channel and REST connections."""
        if self._channel:
            self._channel.close()
        super().close()
