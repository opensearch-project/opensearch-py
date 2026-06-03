# GrpcTransport — Code Documentation

## Overview

`GrpcTransport` is a drop-in replacement for the opensearch-py `Transport` class that routes document operations over gRPC for better performance, while falling back to REST for unsupported operations.

```python
from opensearchpy import OpenSearch
from opensearch_grpc.grpc_transport import GrpcTransport

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    transport_class=GrpcTransport,
    grpc_port=9400,
)
```

## Architecture

```
┌──────────────────────────────────────────────────────┐
│  opensearch-py Client                                 │
│  client.bulk() / client.index() / client.search()    │
└───────────────────────┬──────────────────────────────┘
                        │ perform_request(method, url, body)
                        ▼
┌──────────────────────────────────────────────────────┐
│  GrpcTransport                                        │
│                                                       │
│  _get_grpc_handler(method, url)                       │
│    ├── /_bulk        → _handle_bulk()     → gRPC     │
│    ├── /_doc (PUT)   → _handle_index()    → gRPC     │
│    ├── /_create      → _handle_create()   → gRPC     │
│    ├── /_update      → _handle_update()   → gRPC     │
│    ├── /_doc (DELETE) → _handle_delete()  → gRPC     │
│    ├── /_search      → _handle_search()   → REST *   │
│    └── everything else                    → REST      │
└────────┬─────────────────────────────┬───────────────┘
         │ gRPC (port 9400)            │ REST (port 9200)
         ▼                             ▼
┌─────────────────┐          ┌─────────────────────┐
│ DocumentService  │          │ OpenSearch REST API  │
│   .Bulk()        │          │                     │
└─────────────────┘          └─────────────────────┘

* Search has a SearchService.Search RPC stub ready but currently
  falls back to REST until query DSL → protobuf converter is built.
```

## Routing Table

| Client Method | URL Pattern | Handler | Transport |
|--------------|-------------|---------|-----------|
| `client.bulk()` | `POST /_bulk` | `_handle_bulk` | gRPC (native) |
| `client.index()` | `PUT /index/_doc/id` | `_handle_index` | gRPC (1-item bulk) |
| `client.create()` | `PUT /index/_create/id` | `_handle_create` | gRPC (1-item bulk) |
| `client.update()` | `POST /index/_update/id` | `_handle_update` | gRPC (1-item bulk) |
| `client.delete()` | `DELETE /index/_doc/id` | `_handle_delete` | gRPC (1-item bulk) |
| `client.search()` | `POST /index/_search` | `_handle_search` | REST (for now) |
| `client.count()` | `POST /index/_count` | — | REST |
| `client.get()` | `GET /index/_doc/id` | — | REST |
| `client.indices.*` | Various | — | REST |

## How Single-Doc Operations Work via gRPC

The OpenSearch server only exposes `DocumentService.Bulk` as the document gRPC RPC. There's no `DocumentService.Index` or `DocumentService.Delete`.

For single-doc operations, we wrap them in a `BulkRequest` with 1 item:

```
client.index(index="x", body={"title": "Hi"}, id="1")

    ↓ GrpcTransport._handle_index()

BulkRequest {
    index: "x"
    bulk_request_body: [
        BulkRequestBody {
            operation_container: { index: { x_id: "1", x_index: "x" } }
            object: b'{"title": "Hi"}'
        }
    ]
}

    ↓ DocumentService.Bulk()

BulkResponse { items: [{ index: { x_id: "1", result: "created" } }] }

    ↓ _single_doc_response()

{"_index": "x", "_id": "1", "result": "created", "_version": 1, ...}
```

The client receives the same response format as REST — they never know it went through Bulk.

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `grpc_port` | `9400` | gRPC server port |
| `grpc_host` | First host in hosts list | Override gRPC host |

All standard opensearch-py parameters (hosts, ssl, auth, etc.) still work for REST fallback.

## Performance: Bulk via gRPC vs REST

For massive bulk operations, gRPC provides:
- No NDJSON text parsing (binary protobuf instead)
- No HTTP headers/chunked encoding overhead
- Persistent channel (no TCP handshake per request)
- Faster protobuf serialization vs JSON text

## File Location

```
opensearch_grpc/
├── grpc_transport.py      ← This file
├── translation.py         ← RequestConverter + ResponseConverter
├── stream_client.py       ← StreamClient for manual streaming
├── simpledoc_gRPC.py      ← Standalone single-doc functions
├── proto_adapter.py       ← Import abstraction
└── proto/
    ├── common_pb2.py
    ├── document_service_pb2_grpc.py
    ├── search_service_pb2.py
    └── search_service_pb2_grpc.py
```
