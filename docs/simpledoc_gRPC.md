# simpledoc_gRPC.py — Code Documentation

## Overview

`simpledoc_gRPC.py` is the translation layer that enables the opensearch-py low-level client to send single document operations over gRPC instead of REST. It handles the **full round-trip**:

```
Python Dict → Protobuf → gRPC → OpenSearch → gRPC → Protobuf → Python Dict
```

The user interacts with normal Python dicts — the gRPC transport is invisible to them.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User Code (Python dicts)                                    │
│  client.index(index="my-index", body={"title": "Hello"})    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  simpledoc_gRPC.py                                           │
│                                                              │
│  1. index_document() — receives Python dict                  │
│  2. _build_single_request() — converts to protobuf           │
│  3. _send_grpc_request() — sends over gRPC                   │
│  4. _response_to_dict() — converts response back to dict     │
└──────────────────────────┬──────────────────────────────────┘
                           │ gRPC (port 9400)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  OpenSearch Server (DocumentService.Bulk RPC)                │
└─────────────────────────────────────────────────────────────┘
```

## Public Functions

### `index_document(index, body, id=None, ...)`

Indexes a document (creates or overwrites).

```python
result = index_document(
    index="my-index",
    body={"title": "Hello", "value": 42},
    id="doc-1",
    refresh="true",
)
# Returns: {"_index": "my-index", "_id": "doc-1", "result": "created", ...}
```

### `create_document(index, body, id=None, ...)`

Creates a document — fails if it already exists.

```python
result = create_document(
    index="my-index",
    body={"title": "New doc"},
    id="doc-2",
)
# Returns: {"_index": "my-index", "_id": "doc-2", "result": "created", ...}
```

### `update_document(index, id, body, ...)`

Updates an existing document with partial data.

```python
result = update_document(
    index="my-index",
    id="doc-1",
    body={"doc": {"value": 99}},
)
# Returns: {"_index": "my-index", "_id": "doc-1", "result": "updated", ...}
```

### `delete_document(index, id, ...)`

Deletes a document by ID.

```python
result = delete_document(
    index="my-index",
    id="doc-1",
)
# Returns: {"_index": "my-index", "_id": "doc-1", "result": "deleted", ...}
```

## Internal Flow (Step by Step)

### Step 1: Build Metadata Dict

Each public function collects the operation parameters into a metadata dict:

```python
meta = {"_index": "my-index", "_id": "doc-1"}
```

### Step 2: Convert to Protobuf (`_build_single_request`)

The metadata and document body are converted into a protobuf `BulkRequest`:

- The document body is serialized as JSON bytes into the `object` field
- The operation type (index/create/update/delete) is set in `OperationContainer`
- Request-level params (refresh, timeout) are set on the `BulkRequest`

### Step 3: Send over gRPC (`_send_grpc_request`)

Opens a gRPC channel to `localhost:9400` and calls `DocumentService.Bulk()`:

- The protobuf bytes are sent over the wire
- OpenSearch processes the operation
- A `BulkResponse` protobuf is returned

### Step 4: Convert Response to Dict (`_response_to_dict`)

The protobuf `BulkResponse` is converted back to the Python dict format that opensearch-py normally returns:

```python
{
    "_index": "my-index",
    "_id": "doc-1",
    "result": "created",
    "_version": 1,
    "_seq_no": 0,
    "_primary_term": 1,
    "_shards": {"total": 2, "successful": 1, "failed": 0}
}
```

## Key Design Decisions

| Decision | Reason |
|----------|--------|
| Single doc wrapped in BulkRequest | The gRPC proto only exposes `DocumentService.Bulk()` — no separate index/delete RPCs |
| Response converted to opensearch-py format | Users should get the same dict whether using REST or gRPC |
| Document body as JSON bytes | Proto defines `object` as `bytes` — avoids complex ObjectMap conversion |
| Update body uses `UpdateAction` | Updates have special structure (doc, upsert, script) separate from the document |
| Channel opened per request | Simple for now; will be pooled when we build the client class |

## File Location

```
opensearch-py/
└── opensearch_grpc/
    ├── __init__.py
    ├── simpledoc_gRPC.py      ← This file
    ├── translation.py          ← Lower-level helpers (will be merged later)
    └── proto/
        ├── common_pb2.py       ← Generated protobuf stubs
        └── document_service_pb2_grpc.py
```
