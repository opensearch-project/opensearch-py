"""
stream_client.py — Bidirectional Streaming gRPC Client for OpenSearch

Provides a persistent streaming interface where the client can continuously
send document operations and receive responses without reopening connections.

Architecture:
    Client (Python) ←→ Persistent gRPC Channel ←→ OpenSearch Server (port 9400)

The client streams operations to the server and gets responses back in real-time.
Since DocumentService.Bulk is currently unary (BulkRequest → BulkResponse),
we implement bidirectional behavior by:
    1. Maintaining a persistent gRPC channel (no reconnection overhead)
    2. Allowing the client to queue operations continuously
    3. Flushing batches to the server and yielding responses back
    4. Supporting auto-flush when batch size threshold is reached

When the proto evolves to support true bidirectional streaming, the internal
implementation changes but the client API stays the same.

Usage:
    from opensearch_grpc.stream_client import StreamClient

    with StreamClient("localhost:9400") as client:
        # Stream operations one at a time
        client.index("my-index", body={"title": "Doc 1"}, id="1")
        client.index("my-index", body={"title": "Doc 2"}, id="2")
        client.update("my-index", id="1", body={"doc": {"title": "Updated"}})
        client.delete("my-index", id="2")

        # Flush sends all queued operations and returns responses
        responses = client.flush()
        for resp in responses:
            print(resp)

    # Or use auto-flush with batch_size
    with StreamClient("localhost:9400", batch_size=100) as client:
        for i in range(1000):
            resp = client.index("my-index", body={"value": i}, id=str(i))
            if resp:  # auto-flushed, got responses back
                print(f"Batch complete: {len(resp)} docs")

References:
    - https://grpc.io/docs/languages/python/basics/
    - https://docs.opensearch.org/latest/api-reference/grpc-apis/bulk/
    - https://docs.opensearch.org/latest/clients/python-low-level/
"""

import grpc

from opensearch_grpc.proto_adapter import DocumentServiceStub
from opensearch_grpc.translation import RequestConverter, ResponseConverter


class StreamClient:
    """
    Bidirectional streaming client for OpenSearch gRPC.

    Maintains a persistent channel and allows continuous streaming of
    document operations with batched responses.
    """

    def __init__(self, target="localhost:9400", batch_size=0, refresh=None, timeout=None):
        """
        Args:
            target: gRPC server address (host:port).
            batch_size: Auto-flush after this many operations. 0 = manual flush only.
            refresh: Default refresh policy for all operations.
            timeout: Default timeout for all operations.
        """
        self._target = target
        self._batch_size = batch_size
        self._refresh = refresh
        self._timeout = timeout
        self._channel = None
        self._stub = None
        self._converter = RequestConverter(refresh=refresh, timeout=timeout)
        self._pending_count = 0

    def connect(self):
        """Open the persistent gRPC channel."""
        self._channel = grpc.insecure_channel(self._target)
        self._stub = DocumentServiceStub(self._channel)
        return self

    def close(self):
        """Flush remaining operations and close the channel."""
        results = []
        if self._pending_count > 0:
            results = self.flush()
        if self._channel:
            self._channel.close()
            self._channel = None
            self._stub = None
        return results

    def __enter__(self):
        return self.connect()

    def __exit__(self, *args):
        self.close()

    # ─── Streaming Operations ─────────────────────────────────────────────────

    def index(self, index, body, id=None, routing=None, pipeline=None,
              if_primary_term=None, if_seq_no=None, version=None, version_type=None):
        """
        Stream an index operation. Mirrors client.index().

        Returns None if buffered, or list of response dicts if auto-flushed.
        """
        self._converter.index(
            body=body, index=index, id=id, routing=routing, pipeline=pipeline,
            if_primary_term=if_primary_term, if_seq_no=if_seq_no,
            version=version, version_type=version_type,
        )
        self._pending_count += 1
        return self._maybe_auto_flush()

    def create(self, index, body, id=None, routing=None, pipeline=None):
        """
        Stream a create operation. Mirrors client.create().

        Returns None if buffered, or list of response dicts if auto-flushed.
        """
        self._converter.create(body=body, index=index, id=id, routing=routing, pipeline=pipeline)
        self._pending_count += 1
        return self._maybe_auto_flush()

    def update(self, index, id, body, routing=None, if_primary_term=None,
               if_seq_no=None, retry_on_conflict=None):
        """
        Stream an update operation. Mirrors client.update().

        Returns None if buffered, or list of response dicts if auto-flushed.
        """
        self._converter.update(
            id=id, body=body, index=index, routing=routing,
            if_primary_term=if_primary_term, if_seq_no=if_seq_no,
            retry_on_conflict=retry_on_conflict,
        )
        self._pending_count += 1
        return self._maybe_auto_flush()

    def delete(self, index, id, routing=None, if_primary_term=None,
               if_seq_no=None, version=None, version_type=None):
        """
        Stream a delete operation. Mirrors client.delete().

        Returns None if buffered, or list of response dicts if auto-flushed.
        """
        self._converter.delete(
            id=id, index=index, routing=routing,
            if_primary_term=if_primary_term, if_seq_no=if_seq_no,
            version=version, version_type=version_type,
        )
        self._pending_count += 1
        return self._maybe_auto_flush()

    # ─── Flush ────────────────────────────────────────────────────────────────

    def flush(self):
        """
        Send all queued operations to the server and return responses.

        Returns:
            List of dicts in bulk format: [{"index": {...}}, {"create": {...}}, ...]
        """
        if self._pending_count == 0:
            return []

        # Build the protobuf request from all queued operations
        request = self._converter.build()

        # Send over gRPC
        response = self._stub.Bulk(request)

        # Convert response — always use bulk format for consistency
        items = []
        for item in response.items:
            for op_type in ("index", "create", "update", "delete"):
                if item.HasField(op_type):
                    resp_item = getattr(item, op_type)
                    item_dict = {
                        "_index": resp_item.x_index,
                        "_id": resp_item.x_id if resp_item.x_id else None,
                        "result": resp_item.result if resp_item.result else None,
                        "_version": resp_item.x_version if resp_item.HasField("x_version") else None,
                        "_seq_no": resp_item.x_seq_no if resp_item.HasField("x_seq_no") else None,
                        "_primary_term": resp_item.x_primary_term if resp_item.HasField("x_primary_term") else None,
                        "status": resp_item.status,
                    }
                    if resp_item.HasField("x_shards"):
                        item_dict["_shards"] = {
                            "total": resp_item.x_shards.total,
                            "successful": resp_item.x_shards.successful,
                            "failed": resp_item.x_shards.failed,
                        }
                    if resp_item.HasField("error"):
                        item_dict["error"] = {
                            "type": resp_item.error.type,
                            "reason": resp_item.error.reason if resp_item.error.HasField("reason") else None,
                        }
                    item_dict = {k: v for k, v in item_dict.items() if v is not None}
                    items.append({op_type: item_dict})
                    break

        # Reset the converter for next batch
        self._converter = RequestConverter(refresh=self._refresh, timeout=self._timeout)
        self._pending_count = 0

        return items

    @property
    def pending(self):
        """Number of operations waiting to be flushed."""
        return self._pending_count

    # ─── Internal ─────────────────────────────────────────────────────────────

    def _maybe_auto_flush(self):
        """Auto-flush if batch_size threshold is reached."""
        if self._batch_size > 0 and self._pending_count >= self._batch_size:
            return self.flush()
        return None
