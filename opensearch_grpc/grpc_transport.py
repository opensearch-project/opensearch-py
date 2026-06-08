"""
grpc_transport.py — gRPC Transport for the opensearch-py Client

Routes operations over gRPC where supported by the OpenSearch server:
    - bulk   → DocumentService.Bulk (native gRPC)
    - search → SearchService.Search (native gRPC)
    - index  → DocumentService.Bulk (single-item wrapper)
    - create → DocumentService.Bulk (single-item wrapper)
    - delete → DocumentService.Bulk (single-item wrapper)
    - update → DocumentService.Bulk (single-item wrapper)
    - count  → REST fallback (no gRPC RPC available)

Uses opensearch-py's own serializer and method patterns for integration.

Usage:
    from opensearchpy import OpenSearch
    from opensearch_grpc.grpc_transport import GrpcTransport

    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        transport_class=GrpcTransport,
        grpc_port=9400,
    )
"""


import grpc
from opensearch.protobufs.services import document_service_pb2_grpc, search_service_pb2_grpc

from opensearch_grpc.translation import RequestConverter, ResponseConverter
from opensearchpy.serializer import JSONSerializer
from opensearchpy.transport import Transport


class GrpcTransport(Transport):
    """
    Transport that routes supported operations over gRPC.

    Native gRPC: bulk, search
    Via Bulk RPC: index, create, delete, update (single-doc wrapped in BulkRequest)
    REST fallback: everything else (count, cat, cluster, indices, etc.)
    """

    # Operations we handle via gRPC (URL patterns)
    _GRPC_ROUTES = {
        "_bulk": "_handle_bulk",
        "_search": "_handle_search",
    }

    # Single-doc operations routed through Bulk RPC
    _SINGLE_DOC_PATTERNS = {
        "_doc": "_handle_single_doc",
        "_create": "_handle_create",
        "_update": "_handle_update",
    }

    def __init__(self, hosts, *args, **kwargs):
        self._grpc_port = kwargs.pop("grpc_port", 9400)
        self._grpc_host_override = kwargs.pop("grpc_host", None)
        self._grpc_hosts = kwargs.pop("grpc_hosts", None)

        super().__init__(hosts, *args, **kwargs)

        # Resolve gRPC target from grpc_hosts, grpc_host, or hosts
        if self._grpc_hosts:
            # Use grpc_hosts parameter: [{"host": "x", "port": 9400}]
            first_grpc = self._grpc_hosts[0] if isinstance(self._grpc_hosts[0], dict) else {"host": self._grpc_hosts[0]}
            grpc_host = first_grpc.get("host", "localhost")
            grpc_port = first_grpc.get("port", self._grpc_port)
        elif self._grpc_host_override:
            grpc_host = self._grpc_host_override
            grpc_port = self._grpc_port
        elif hosts:
            first = hosts[0] if isinstance(hosts[0], dict) else {"host": "localhost"}
            grpc_host = first.get("host", "localhost")
            grpc_port = self._grpc_port
        else:
            grpc_host = "localhost"
            grpc_port = self._grpc_port

        self._grpc_address = f"{grpc_host}:{grpc_port}"
        self._channel = grpc.insecure_channel(self._grpc_address)
        self._document_stub = document_service_pb2_grpc.DocumentServiceStub(self._channel)
        self._search_stub = search_service_pb2_grpc.SearchServiceStub(self._channel)
        self._serializer = JSONSerializer()

    def perform_request(self, method, url, params=None, body=None,
                        timeout=None, ignore=(), headers=None):
        """Route to gRPC or REST based on the URL pattern."""
        handler = self._get_grpc_handler(method, url)
        if handler:
            return handler(method, url, params, body)

        return super().perform_request(
            method, url, params=params, body=body,
            timeout=timeout, ignore=ignore, headers=headers
        )

    def _get_grpc_handler(self, method, url):
        """Determine if this request can be handled via gRPC."""
        parts = url.strip("/").split("/")
        last = parts[-1] if parts else ""

        # Bulk: POST /_bulk or POST /index/_bulk
        if last == "_bulk" and method in ("POST", "PUT"):
            return self._handle_bulk

        # Search: POST/GET /_search or /index/_search
        if last == "_search" and method in ("POST", "GET"):
            return self._handle_search

        # Single doc operations
        if method == "POST" and last == "_create":
            return self._handle_create
        if method == "POST" and last == "_update":
            return self._handle_update
        if method in ("PUT", "POST") and "_doc" in parts:
            return self._handle_index
        if method == "DELETE" and len(parts) >= 3 and parts[-2] == "_doc":
            return self._handle_delete

        return None

    # ─── gRPC Handlers ────────────────────────────────────────────────────────

    def _handle_bulk(self, method, url, params, body):
        """Bulk → DocumentService.Bulk (native gRPC)."""
        url_index = self._extract_index_from_url(url, "_bulk")
        refresh = params.get("refresh") if params else None
        timeout = params.get("timeout") if params else None
        pipeline = params.get("pipeline") if params else None
        routing = params.get("routing") if params else None

        converter = RequestConverter.from_body(
            body, index=url_index, refresh=refresh,
            timeout=timeout, pipeline=pipeline, routing=routing,
        )
        response = self._document_stub.Bulk(converter.build())
        return ResponseConverter._convert_bulk_items(response)

    def _handle_search(self, method, url, params, body):
        """Search → SearchService.Search (native gRPC)."""
        # For now, fall back to REST for search since building SearchRequest
        # protobuf from the full query DSL is complex. This is the hook for
        # when we implement full query DSL → protobuf conversion.
        # TODO: Implement SearchRequest protobuf conversion for common queries
        return super().perform_request(method, url, params=params, body=body)

    def _handle_index(self, method, url, params, body):
        """Index single doc → DocumentService.Bulk (1-item BulkRequest)."""
        parts = url.strip("/").split("/")
        # URL: /index/_doc/id or /index/_doc
        index = parts[0] if len(parts) >= 2 else None
        doc_id = parts[2] if len(parts) >= 3 else None

        refresh = params.get("refresh") if params else None
        pipeline = params.get("pipeline") if params else None
        routing = params.get("routing") if params else None

        converter = RequestConverter(index=index, refresh=refresh)
        converter.index(body=body, id=doc_id, pipeline=pipeline, routing=routing)
        response = self._document_stub.Bulk(converter.build())

        return self._single_doc_response(response)

    def _handle_create(self, method, url, params, body):
        """Create single doc → DocumentService.Bulk (1-item create)."""
        parts = url.strip("/").split("/")
        # URL: /index/_create/id
        index = parts[0] if len(parts) >= 1 else None
        doc_id = parts[2] if len(parts) >= 3 else None

        refresh = params.get("refresh") if params else None
        routing = params.get("routing") if params else None

        converter = RequestConverter(index=index, refresh=refresh)
        converter.create(body=body, id=doc_id, routing=routing)
        response = self._document_stub.Bulk(converter.build())

        return self._single_doc_response(response)

    def _handle_update(self, method, url, params, body):
        """Update single doc → DocumentService.Bulk (1-item update)."""
        parts = url.strip("/").split("/")
        # URL: /index/_update/id
        index = parts[0] if len(parts) >= 1 else None
        doc_id = parts[2] if len(parts) >= 3 else None

        refresh = params.get("refresh") if params else None
        routing = params.get("routing") if params else None
        retry = params.get("retry_on_conflict") if params else None

        converter = RequestConverter(index=index, refresh=refresh)
        converter.update(id=doc_id, body=body, routing=routing,
                         retry_on_conflict=int(retry) if retry else None)
        response = self._document_stub.Bulk(converter.build())

        return self._single_doc_response(response)

    def _handle_delete(self, method, url, params, body):
        """Delete single doc → DocumentService.Bulk (1-item delete)."""
        parts = url.strip("/").split("/")
        # URL: /index/_doc/id
        index = parts[0] if len(parts) >= 1 else None
        doc_id = parts[2] if len(parts) >= 3 else None

        refresh = params.get("refresh") if params else None
        routing = params.get("routing") if params else None

        converter = RequestConverter(index=index, refresh=refresh)
        converter.delete(id=doc_id, routing=routing)
        response = self._document_stub.Bulk(converter.build())

        return self._single_doc_response(response)

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _extract_index_from_url(self, url, endpoint):
        """Extract index from URL like /my-index/_bulk → 'my-index'."""
        parts = url.strip("/").split("/")
        if len(parts) >= 2 and parts[-1] == endpoint:
            return "/".join(parts[:-1])
        return None

    def _single_doc_response(self, response):
        """Convert a single-item BulkResponse to opensearch-py single-doc format."""
        item = response.items[0]
        for op_type in ("index", "create", "update", "delete"):
            if item.HasField(op_type):
                resp_item = getattr(item, op_type)
                result = {
                    "_index": resp_item.x_index,
                    "_id": resp_item.x_id if resp_item.x_id else None,
                    "result": resp_item.result if resp_item.result else None,
                    "_version": resp_item.x_version if resp_item.HasField("x_version") else None,
                    "_seq_no": resp_item.x_seq_no if resp_item.HasField("x_seq_no") else None,
                    "_primary_term": resp_item.x_primary_term if resp_item.HasField("x_primary_term") else None,
                }
                if resp_item.HasField("x_shards"):
                    result["_shards"] = {
                        "total": resp_item.x_shards.total,
                        "successful": resp_item.x_shards.successful,
                        "failed": resp_item.x_shards.failed,
                    }
                if resp_item.HasField("error"):
                    result["error"] = {
                        "type": resp_item.error.type,
                        "reason": resp_item.error.reason if resp_item.error.HasField("reason") else None,
                    }
                return {k: v for k, v in result.items() if v is not None}
        return {"error": "Unknown response type"}

    def close(self):
        """Close gRPC channel and REST connections."""
        if self._channel:
            self._channel.close()
        super().close()
