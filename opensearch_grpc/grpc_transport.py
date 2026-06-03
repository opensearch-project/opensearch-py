"""
grpc_transport.py — gRPC Transport for the opensearch-py Client

Plugs into the existing opensearch-py transport system. Routes supported
operations (bulk) over gRPC while falling back to REST for everything else.

Usage:
    from opensearchpy import OpenSearch
    from opensearch_grpc.grpc_transport import GrpcTransport

    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        transport_class=GrpcTransport,
        grpc_port=9400,
    )

    # Bulk operations go over gRPC automatically
    client.bulk(body=[
        {"index": {"_index": "my-index", "_id": "1"}},
        {"title": "Hello"},
    ])

    # Everything else uses REST as normal
    client.search(index="my-index", body={"query": {"match_all": {}}})
"""


import grpc

from opensearchpy.transport import Transport

from opensearch_grpc.proto_adapter import DocumentServiceStub
from opensearch_grpc.translation import RequestConverter, ResponseConverter


class GrpcTransport(Transport):
    """
    Transport that routes bulk operations over gRPC and falls back to REST
    for all other operations.

    Extends the standard opensearch-py Transport class so it works as a
    drop-in replacement.

    Additional args (passed via **kwargs to OpenSearch client):
        grpc_port: gRPC port (default 9400)
        grpc_host: Override gRPC host (defaults to first host in hosts list)
    """

    def __init__(self, hosts, *args, **kwargs):
        # Extract gRPC-specific kwargs before passing to parent
        self._grpc_port = kwargs.pop("grpc_port", 9400)
        self._grpc_host_override = kwargs.pop("grpc_host", None)

        # Initialize the REST transport
        super().__init__(hosts, *args, **kwargs)

        # Resolve gRPC host from the first host in the list
        if self._grpc_host_override:
            grpc_host = self._grpc_host_override
        elif hosts:
            first_host = hosts[0] if isinstance(hosts[0], dict) else {"host": "localhost"}
            grpc_host = first_host.get("host", "localhost")
        else:
            grpc_host = "localhost"

        self._grpc_address = f"{grpc_host}:{self._grpc_port}"

        # Create persistent gRPC channel
        self._grpc_channel = grpc.insecure_channel(self._grpc_address)
        self._document_stub = DocumentServiceStub(self._grpc_channel)

    def perform_request(self, method, url, params=None, body=None,
                        timeout=None, ignore=(), headers=None):
        """
        Route requests: bulk goes over gRPC, everything else over REST.

        The opensearch-py client calls this for every API operation.
        We intercept bulk requests and handle them via gRPC.
        """
        # Check if this is a bulk request we can handle via gRPC
        if self._is_bulk_request(method, url):
            return self._perform_grpc_bulk(url, body, params)

        # Fall back to REST for everything else
        return super().perform_request(
            method, url, params=params, body=body,
            timeout=timeout, ignore=ignore, headers=headers
        )

    def _is_bulk_request(self, method, url):
        """Check if this request is a bulk operation."""
        return method in ("POST", "PUT") and url.rstrip("/").endswith("_bulk")

    def _perform_grpc_bulk(self, url, body, params):
        """
        Handle a bulk request over gRPC.

        Converts the body to protobuf, sends via gRPC, converts response back.
        Returns the response dict directly (same as REST transport would).
        """
        # Extract index from URL if present (e.g. "/my-index/_bulk" → "my-index")
        url_index = None
        parts = url.strip("/").split("/")
        if len(parts) >= 2 and parts[-1] == "_bulk":
            url_index = "/".join(parts[:-1])

        # Parse params for request-level options
        refresh = params.get("refresh") if params else None
        timeout = params.get("timeout") if params else None
        pipeline = params.get("pipeline") if params else None
        routing = params.get("routing") if params else None

        # Convert body to protobuf BulkRequest
        converter = RequestConverter.from_body(
            body, index=url_index, refresh=refresh, timeout=timeout,
            pipeline=pipeline, routing=routing,
        )
        request = converter.build()

        # Send over gRPC
        response = self._document_stub.Bulk(request)

        # Convert response to opensearch-py bulk format (always bulk, never single-item)
        return ResponseConverter._convert_bulk_items(response)

    def close(self):
        """Close both gRPC channel and REST connections."""
        if self._grpc_channel:
            self._grpc_channel.close()
        super().close()
