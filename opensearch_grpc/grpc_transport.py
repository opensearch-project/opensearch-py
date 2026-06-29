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

import grpc
from opensearch.protobufs.services import document_service_pb2_grpc

from opensearch_grpc.translation import BulkRequestProtoBuilder, ResponseConverter
from opensearchpy.serializer import JSONSerializer
from opensearchpy.transport import Transport


class GrpcTransport(Transport):
    """
    Transport that routes bulk operations over gRPC.

    Bulk requests are sent via DocumentService.Bulk for better performance.
    All other operations fall back to REST automatically.
    """

    # Operations we handle via gRPC (URL patterns)
    _GRPC_ROUTES = {
        "_bulk": "_handle_bulk",
    }

    def __init__(self, hosts, *args, **kwargs):
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
        self._serializer = JSONSerializer()

    def perform_request(
        self, method, url, params=None, body=None, timeout=None, ignore=(), headers=None
    ):
        """Route to gRPC or REST based on the URL pattern."""
        handler = self._get_grpc_handler(method, url)
        if handler:
            return handler(method, url, params, body)

        return super().perform_request(
            method,
            url,
            params=params,
            body=body,
            timeout=timeout,
            ignore=ignore,
            headers=headers,
        )

    def _get_grpc_handler(self, method, url):
        """Determine if this request can be handled via gRPC.

        Only bulk requests are routed over gRPC.
        All other operations fall through to REST.
        """
        parts = url.strip("/").split("/")
        last = parts[-1] if parts else ""

        # Bulk: POST /_bulk or POST /index/_bulk
        if last == "_bulk" and method in ("POST", "PUT"):
            return self._handle_bulk

        return None

    # ─── gRPC Handlers ────────────────────────────────────────────────────────

    def _handle_bulk(self, method, url, params, body):
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
        response = self._document_stub.Bulk(converter.build())
        return ResponseConverter._convert_bulk_items(response)

    def _extract_index_from_url(self, url, endpoint):
        """Extract index from URL like /my-index/_bulk → 'my-index'."""
        parts = url.strip("/").split("/")
        if len(parts) >= 2 and parts[-1] == endpoint:
            return "/".join(parts[:-1])
        return None

    def close(self):
        """Close gRPC channel and REST connections."""
        if self._channel:
            self._channel.close()
        super().close()
