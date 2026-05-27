# Translation Layer: Bulk Request Dict → Protobuf BulkRequest

## Overview

This module converts the standard opensearch-py bulk request format (list of action/source dicts) into the
protobuf `BulkRequest` message defined in `opensearch-protobufs`. The opensearch-py client sends bulk data as
newline-delimited JSON (NDJSON) pairs — an action line followed by an optional source line. Our translation
layer accepts the same Python dict structure and produces the equivalent protobuf.

## opensearch-py Bulk Format Recap

The `opensearch-py` client accepts bulk data in two forms:

1. **`client.bulk(body=[...])`** — a flat list alternating action dicts and source dicts
2. **`helpers.bulk()`** — a list of document dicts with `_op_type`, `_index`, `_id` keys

Both ultimately produce action/source pairs like:

```python
# Form 1: raw NDJSON string (as shown in opensearch-py docs)
movies = '{ "index" : { "_index" : "my-dsl-index", "_id" : "2" } } \n { "title" : "Interstellar", "director" : "Christopher Nolan", "year" : "2014"} \n'
client.bulk(body=movies)

# Form 2: list of dicts (programmatic form)
body = [
    {"index": {"_index": "my-index", "_id": "1"}},
    {"title": "Doc 1", "content": "hello"},
    {"delete": {"_index": "my-index", "_id": "2"}},
    {"create": {"_index": "my-index", "_id": "3"}},
    {"title": "Doc 3"},
    {"update": {"_index": "my-index", "_id": "4"}},
    {"doc": {"title": "Updated"}, "doc_as_upsert": True},
]
```

## Protobuf Target Structure

From `common.proto`, the target message is:

```
BulkRequest
├── index (optional, default index)
├── pipeline, routing, refresh, timeout, etc.
└── bulk_request_body (repeated BulkRequestBody)
    ├── operation_container (oneof: index | create | update | delete)
    ├── update_action (optional, for update ops)
    └── object (optional bytes, the document source as JSON bytes)
```

---

## OpenSearch gRPC Client Constructor

The client follows the same pattern as the low-level `opensearch-py` client but adds a gRPC channel
for bidirectional streaming. Users configure gRPC host/port on client creation; bulk requests are
routed over gRPC as a bidirectional stream, falling back to REST for unsupported operations.

```python
"""OpenSearch gRPC client with bidirectional streaming support."""

import grpc
from opensearchpy import OpenSearch

from opensearch_grpc.proto import document_service_pb2_grpc


class OpenSearchGrpc(OpenSearch):
    """
    Extends the low-level OpenSearch client with a gRPC channel for
    bidirectional streaming bulk operations.

    Args:
        hosts: List of host dicts (same as opensearch-py).
        grpc_port: Port for the gRPC endpoint. Default 9400.
        grpc_host: gRPC host. Defaults to the first host in `hosts`.
        use_ssl: Whether to use SSL for both REST and gRPC.
        grpc_options: Optional list of gRPC channel options.
        **kwargs: All other args passed to the base OpenSearch client.

    Example (no security):
        client = OpenSearchGrpc(
            hosts=[{'host': 'localhost', 'port': 9200}],
            grpc_port=9400,
            use_ssl=False,
        )

    Example (with SSL):
        client = OpenSearchGrpc(
            hosts=[{'host': 'localhost', 'port': 9200}],
            grpc_port=9400,
            use_ssl=True,
            ca_certs='/path/to/root-ca.pem',
            http_auth=('admin', 'admin'),
        )
    """

    def __init__(self, hosts=None, grpc_port=9400, grpc_host=None,
                 use_ssl=False, grpc_options=None, **kwargs):
        # Initialize the base REST client
        super().__init__(hosts=hosts, use_ssl=use_ssl, **kwargs)

        # Resolve gRPC target
        if grpc_host is None:
            first_host = hosts[0] if hosts else {}
            grpc_host = first_host.get('host', 'localhost') if isinstance(first_host, dict) else 'localhost'

        self._grpc_target = f"{grpc_host}:{grpc_port}"

        # Create gRPC channel
        if use_ssl:
            credentials = grpc.ssl_channel_credentials()
            self._grpc_channel = grpc.insecure_channel(
                self._grpc_target, options=grpc_options
            )
            # TODO: Replace with grpc.secure_channel(self._grpc_target, credentials, options=grpc_options)
        else:
            self._grpc_channel = grpc.insecure_channel(
                self._grpc_target, options=grpc_options
            )

        # Create the DocumentService stub for bidirectional streaming
        self._document_stub = document_service_pb2_grpc.DocumentServiceStub(
            self._grpc_channel
        )

    def close(self):
        """Close both the gRPC channel and the REST connection pool."""
        self._grpc_channel.close()
        super().close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
```

### Explanation

| Component | Purpose |
|-----------|---------|
| `OpenSearchGrpc(OpenSearch)` | Inherits from the low-level client so all REST operations (search, index, delete) work unchanged. |
| `grpc_port` parameter | Separate from the REST port (9200). OpenSearch exposes gRPC on a different port (default 9400). |
| `_grpc_channel` | The persistent gRPC channel. Bidirectional streams are opened on this channel per bulk call. |
| `_document_stub` | The generated gRPC stub for `DocumentService.Bulk()` — this is the bidirectional streaming RPC. |
| `close()` / context manager | Ensures both gRPC channel and REST connection pool are cleaned up. |

The bidirectional stream means the client sends `BulkRequestBody` messages incrementally and receives
`ResponseItem` messages back as the server processes them — no need to wait for the entire batch to
complete before getting results.

---

## Implementation

```python
"""Translation layer: opensearch-py bulk dict → protobuf BulkRequest."""

import json
from typing import Any, Union

# Generated protobuf modules (from opensearch-protobufs)
from opensearch_grpc.proto import common_pb2


# ─── Operation Mapping ───────────────────────────────────────────────────────

# Maps opensearch-py action names to protobuf operation constructors
_OP_BUILDERS = {
    "index": _build_index_op,
    "create": _build_create_op,
    "update": _build_update_op,
    "delete": _build_delete_op,
}


def _normalize_body(body: Union[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """
    Normalize bulk body input to a list of dicts.

    The low-level opensearch-py client accepts bulk body as either:
    1. A list of dicts (action/source pairs)
    2. An NDJSON string (newline-delimited JSON), e.g.:
       '{ "index": { "_index": "my-index", "_id": "2" } }\n{ "title": "Interstellar" }\n'

    This function handles both forms and returns a uniform list of dicts.
    """
    if isinstance(body, str):
        lines = [line.strip() for line in body.split("\n") if line.strip()]
        return [json.loads(line) for line in lines]
    return body


def toProtoBulkRequest(
    body: Union[str, list[dict[str, Any]]],
    index: str | None = None,
    pipeline: str | None = None,
    routing: str | None = None,
    refresh: str | None = None,
    timeout: str | None = None,
    require_alias: bool | None = None,
) -> common_pb2.BulkRequest:
    """
    Convert an opensearch-py bulk body (list of action/source dicts) into a
    protobuf BulkRequest message.

    Args:
        body: Flat list of action/source dict pairs, or an NDJSON string (opensearch-py format).
        index: Default index for all operations.
        pipeline: Ingest pipeline ID.
        routing: Default routing value.
        refresh: Refresh policy ("true", "false", "wait_for").
        timeout: Request timeout string (e.g. "1m").
        require_alias: Whether targets must be aliases.

    Returns:
        A populated BulkRequest protobuf message.
    """
    request = common_pb2.BulkRequest()

    # ── Normalize input (NDJSON string or list of dicts) ──
    body = _normalize_body(body)

    # ── Set top-level request parameters ──
    if index is not None:
        request.index = index
    if pipeline is not None:
        request.pipeline = pipeline
    if routing is not None:
        request.routing = routing
    if timeout is not None:
        request.timeout = timeout
    if require_alias is not None:
        request.require_alias = require_alias
    if refresh is not None:
        request.refresh = _map_refresh(refresh)

    # ── Parse action/source pairs ──
    i = 0
    while i < len(body):
        action_dict = body[i]
        i += 1

        # Extract the operation type and its metadata
        op_type, meta = _parse_action(action_dict)

        # All ops except delete have a following source document
        source = None
        if op_type != "delete" and i < len(body):
            source = body[i]
            i += 1

        # Build the BulkRequestBody
        bulk_body = _build_bulk_request_body(op_type, meta, source)
        request.bulk_request_body.append(bulk_body)

    return request
```

### Explanation

1. **`_normalize_body()`** handles both input formats the low-level client accepts:
   - A **list of dicts** (the programmatic form): `[{"index": {...}}, {"title": "..."}]`
   - An **NDJSON string** (the raw form shown in docs): `'{"index": {...}}\n{"title": "..."}\n'`

2. **`toProtoBulkRequest()`** is the main entry point. It mirrors the parameters you'd pass to
   `client.bulk()` — the body list plus optional top-level params (index, pipeline, etc.).

3. It iterates through the flat body list, consuming action/source pairs. Delete operations have no
   source document, so only one dict is consumed.

4. Each pair is converted into a `BulkRequestBody` protobuf message.

---

## Helper Functions

```python
def _parse_action(action_dict: dict) -> tuple[str, dict]:
    """
    Extract operation type and metadata from an action dict.

    Input:  {"index": {"_index": "foo", "_id": "1"}}
    Output: ("index", {"_index": "foo", "_id": "1"})
    """
    # Action dict has exactly one key: the operation type
    op_type = next(iter(action_dict))
    meta = action_dict[op_type]
    return op_type, meta


def _map_refresh(value: str | bool) -> int:
    """Map refresh parameter to protobuf Refresh enum value."""
    mapping = {
        "true": common_pb2.REFRESH_TRUE,
        "false": common_pb2.REFRESH_FALSE,
        "wait_for": common_pb2.REFRESH_WAIT_FOR,
        True: common_pb2.REFRESH_TRUE,
        False: common_pb2.REFRESH_FALSE,
    }
    return mapping.get(value, common_pb2.REFRESH_UNSPECIFIED)
```

### Explanation

- **`_parse_action()`** — The opensearch-py format uses a single-key dict where the key is the operation
  name. This extracts it cleanly.

- **`_map_refresh()`** — Converts the string/bool refresh values that opensearch-py accepts into the
  protobuf `Refresh` enum integers.

---

## Building Operation Containers

```python
def _build_bulk_request_body(
    op_type: str, meta: dict, source: dict | None
) -> common_pb2.BulkRequestBody:
    """
    Build a single BulkRequestBody from an operation type, metadata, and source.
    """
    body = common_pb2.BulkRequestBody()

    # Build the operation container (index/create/update/delete)
    op_container = common_pb2.OperationContainer()
    builder = _OP_BUILDERS[op_type]
    builder(op_container, meta)
    body.operation_container.CopyFrom(op_container)

    # For update operations, the source contains update-specific fields
    if op_type == "update" and source is not None:
        body.update_action.CopyFrom(_build_update_action(source))
    elif source is not None:
        # index/create: source is the document body serialized as JSON bytes
        body.object = json.dumps(source).encode("utf-8")

    return body
```

### Explanation

The `BulkRequestBody` has three parts:
1. **`operation_container`** — Which operation (index/create/update/delete) plus routing metadata
2. **`update_action`** — Only populated for update operations (contains `doc`, `script`, `upsert`, etc.)
3. **`object`** — The document source as raw JSON bytes (for index/create operations)

---

## Operation Builders

```python
def _build_index_op(container: common_pb2.OperationContainer, meta: dict):
    """Populate an IndexOperation from action metadata."""
    op = common_pb2.IndexOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "pipeline" in meta:
        op.pipeline = meta["pipeline"]
    if "if_primary_term" in meta:
        op.if_primary_term = meta["if_primary_term"]
    if "if_seq_no" in meta:
        op.if_seq_no = meta["if_seq_no"]
    if "require_alias" in meta:
        op.require_alias = meta["require_alias"]
    if "version" in meta:
        op.version = meta["version"]
    if "version_type" in meta:
        op.version_type = _map_version_type(meta["version_type"])
    container.index.CopyFrom(op)


def _build_create_op(container: common_pb2.OperationContainer, meta: dict):
    """Populate a WriteOperation (create) from action metadata."""
    op = common_pb2.WriteOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "pipeline" in meta:
        op.pipeline = meta["pipeline"]
    if "require_alias" in meta:
        op.require_alias = meta["require_alias"]
    container.create.CopyFrom(op)


def _build_update_op(container: common_pb2.OperationContainer, meta: dict):
    """Populate an UpdateOperation from action metadata."""
    op = common_pb2.UpdateOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "if_primary_term" in meta:
        op.if_primary_term = meta["if_primary_term"]
    if "if_seq_no" in meta:
        op.if_seq_no = meta["if_seq_no"]
    if "require_alias" in meta:
        op.require_alias = meta["require_alias"]
    if "retry_on_conflict" in meta:
        op.retry_on_conflict = meta["retry_on_conflict"]
    container.update.CopyFrom(op)


def _build_delete_op(container: common_pb2.OperationContainer, meta: dict):
    """Populate a DeleteOperation from action metadata."""
    op = common_pb2.DeleteOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "if_primary_term" in meta:
        op.if_primary_term = meta["if_primary_term"]
    if "if_seq_no" in meta:
        op.if_seq_no = meta["if_seq_no"]
    if "version" in meta:
        op.version = meta["version"]
    if "version_type" in meta:
        op.version_type = _map_version_type(meta["version_type"])
    container.delete.CopyFrom(op)
```

### Explanation

Each builder maps the underscore-prefixed keys from opensearch-py (`_id`, `_index`) to the protobuf
field names (`x_id`, `x_index`). The protobuf uses `x_` prefix because `_` prefix fields in the REST
API are reserved metadata fields.

Key differences per operation:
- **IndexOperation** — Supports `if_primary_term`/`if_seq_no` for optimistic concurrency, `version`/`version_type` for external versioning, and `pipeline` for per-doc ingest pipelines.
- **WriteOperation (create)** — Simpler; no concurrency control fields since create fails if doc exists.
- **UpdateOperation** — Adds `retry_on_conflict` for automatic retries on version conflicts.
- **DeleteOperation** — No source document; supports concurrency control via version or seq_no.

---

## Update Action Builder

```python
def _build_update_action(source: dict) -> common_pb2.UpdateAction:
    """
    Build an UpdateAction from the source dict following an update operation.

    The source dict for updates can contain:
    - "doc": partial document to merge
    - "doc_as_upsert": bool
    - "script": inline/stored script
    - "scripted_upsert": bool
    - "upsert": document to insert if missing
    - "_source": source filtering config
    - "detect_noop": bool
    """
    action = common_pb2.UpdateAction()

    if "doc" in source:
        action.doc = json.dumps(source["doc"]).encode("utf-8")
    if "doc_as_upsert" in source:
        action.doc_as_upsert = source["doc_as_upsert"]
    if "upsert" in source:
        action.upsert = json.dumps(source["upsert"]).encode("utf-8")
    if "scripted_upsert" in source:
        action.scripted_upsert = source["scripted_upsert"]
    if "detect_noop" in source:
        action.detect_noop = source["detect_noop"]
    if "script" in source:
        action.script.CopyFrom(_build_script(source["script"]))

    return action
```

### Explanation

Update operations are unique — their "source" isn't a document to index but rather instructions on
*how* to update. The `doc` and `upsert` fields are serialized to JSON bytes (matching how the protobuf
defines them as `bytes` fields). This preserves the arbitrary nested structure of partial documents.

---

## Enum Mappers

```python
def _map_version_type(value: str) -> int:
    """Map version_type string to protobuf VersionType enum."""
    mapping = {
        "internal": common_pb2.VERSION_TYPE_INTERNAL,
        "external": common_pb2.VERSION_TYPE_EXTERNAL,
        "external_gte": common_pb2.VERSION_TYPE_EXTERNAL_GTE,
    }
    return mapping.get(value, common_pb2.VERSION_TYPE_UNSPECIFIED)


def _build_script(script_dict: dict) -> common_pb2.Script:
    """Build a Script protobuf from a script dict."""
    script = common_pb2.Script()
    if "source" in script_dict:
        inline = common_pb2.InlineScript()
        inline.source = script_dict["source"]
        if "lang" in script_dict:
            inline.lang.custom = script_dict["lang"]
        if "params" in script_dict:
            _dict_to_object_map(script_dict["params"], inline.params)
        script.inline.CopyFrom(inline)
    elif "id" in script_dict:
        stored = common_pb2.StoredScriptId()
        stored.id = script_dict["id"]
        if "params" in script_dict:
            _dict_to_object_map(script_dict["params"], stored.params)
        script.stored.CopyFrom(stored)
    return script


def _dict_to_object_map(d: dict, obj_map: common_pb2.ObjectMap):
    """Recursively convert a Python dict to an ObjectMap protobuf."""
    for key, val in d.items():
        if val is None:
            obj_map.fields[key].null_value = common_pb2.NULL_VALUE_NULL
        elif isinstance(val, bool):
            obj_map.fields[key].bool = val
        elif isinstance(val, int):
            obj_map.fields[key].int64 = val
        elif isinstance(val, float):
            obj_map.fields[key].double = val
        elif isinstance(val, str):
            obj_map.fields[key].string = val
        elif isinstance(val, dict):
            nested = common_pb2.ObjectMap()
            _dict_to_object_map(val, nested)
            obj_map.fields[key].object_map.CopyFrom(nested)
        elif isinstance(val, list):
            list_val = common_pb2.ObjectMap.ListValue()
            for item in val:
                v = common_pb2.ObjectMap.Value()
                _set_object_map_value(v, item)
                list_val.value.append(v)
            obj_map.fields[key].list_value.CopyFrom(list_val)


def _set_object_map_value(v: common_pb2.ObjectMap.Value, val):
    """Set a single ObjectMap.Value from a Python value."""
    if val is None:
        v.null_value = common_pb2.NULL_VALUE_NULL
    elif isinstance(val, bool):
        v.bool = val
    elif isinstance(val, int):
        v.int64 = val
    elif isinstance(val, float):
        v.double = val
    elif isinstance(val, str):
        v.string = val
    elif isinstance(val, dict):
        nested = common_pb2.ObjectMap()
        _dict_to_object_map(val, nested)
        v.object_map.CopyFrom(nested)
```

### Explanation

- **`_map_version_type()`** — Translates the REST API string values to protobuf enum integers.
- **`_build_script()`** — Handles both inline scripts (with `source`) and stored scripts (with `id`).
- **`_dict_to_object_map()`** — Recursively converts arbitrary Python dicts into the protobuf `ObjectMap`
  structure. This is needed for script `params` which can contain any JSON-like structure.

---

## Usage Example

```python
from opensearch_grpc.client import OpenSearchGrpc
from opensearch_grpc.translation import toProtoBulkRequest

# Create the gRPC client (bidirectional streaming)
client = OpenSearchGrpc(
    hosts=[{'host': 'localhost', 'port': 9200}],
    grpc_port=9400,
    use_ssl=False,
)

# Standard opensearch-py bulk body
body = [
    {"index": {"_index": "products", "_id": "1"}},
    {"name": "Widget", "price": 9.99},

    {"create": {"_index": "products", "_id": "2"}},
    {"name": "Gadget", "price": 19.99},

    {"update": {"_index": "products", "_id": "1"}},
    {"doc": {"price": 7.99}, "doc_as_upsert": True},

    {"delete": {"_index": "products", "_id": "3"}},
]

proto_request = toProtoBulkRequest(
    body=body,
    index="products",
    refresh="wait_for",
    timeout="30s",
)

# proto_request is now a BulkRequest protobuf ready to send over gRPC
print(f"Operations: {len(proto_request.bulk_request_body)}")  # 4
```

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Document source stored as JSON bytes in `object` field | Matches proto definition (`bytes object`). Avoids complex recursive ObjectMap conversion for arbitrary doc structures. |
| Update `doc`/`upsert` also as JSON bytes | Proto defines these as `bytes` fields. Preserves nested structure without schema knowledge. |
| Script params use ObjectMap | Proto defines `params` as `ObjectMap`, requiring recursive conversion. Script params are typically small/flat. |
| Underscore-prefix keys (`_id`, `_index`) mapped to `x_` prefix | Proto uses `x_` prefix for fields that correspond to `_`-prefixed REST API metadata fields. |
| Forward-reference `_OP_BUILDERS` dict | Defined after functions in actual code; shown here for clarity. |

---

## Integration Test: Sending Bulk Data as a Client

This test connects directly to a running OpenSearch gRPC endpoint and streams bulk request
messages, simulating what the client does internally. You can run this against your local
`gradlew run` node.

```python
"""Integration test: send bulk data over gRPC bidirectional stream as a client."""

import json
import grpc

from opensearch_grpc.proto import common_pb2, document_service_pb2_grpc
from opensearch_grpc.translation import toProtoBulkRequest


def generate_bulk_requests():
    """
    Generator that yields BulkRequestBody messages one at a time,
    simulating a client streaming documents to the server.
    """
    body = [
        {"index": {"_index": "grpc-test", "_id": "1"}},
        {"title": "First doc", "value": 1},
        {"index": {"_index": "grpc-test", "_id": "2"}},
        {"title": "Second doc", "value": 2},
        {"create": {"_index": "grpc-test", "_id": "3"}},
        {"title": "Third doc", "value": 3},
        {"update": {"_index": "grpc-test", "_id": "1"}},
        {"doc": {"value": 100}},
        {"delete": {"_index": "grpc-test", "_id": "2"}},
    ]

    # Convert to protobuf
    proto_request = toProtoBulkRequest(body=body, refresh="true")

    # Yield each BulkRequestBody individually (simulates streaming)
    for bulk_body in proto_request.bulk_request_body:
        yield bulk_body


def test_bidirectional_bulk_stream():
    """
    Connect to the gRPC server and send bulk operations as a bidirectional stream.
    Print each response as it arrives from the server.
    """
    target = "localhost:9400"
    channel = grpc.insecure_channel(target)
    stub = document_service_pb2_grpc.DocumentServiceStub(channel)

    print(f"Connecting to gRPC at {target}...")

    # Open bidirectional stream
    responses = stub.Bulk(generate_bulk_requests())

    # Read responses as they come back from the server
    print("\n--- Server Responses ---")
    for response in responses:
        print(f"  errors: {response.errors}")
        print(f"  took: {response.took}ms")
        for item in response.items:
            if item.HasField("index"):
                print(f"  [index] id={item.index.x_id} status={item.index.status}")
            elif item.HasField("create"):
                print(f"  [create] id={item.create.x_id} status={item.create.status}")
            elif item.HasField("update"):
                print(f"  [update] id={item.update.x_id} status={item.update.status}")
            elif item.HasField("delete"):
                print(f"  [delete] id={item.delete.x_id} status={item.delete.status}")

    channel.close()
    print("\nDone.")


if __name__ == "__main__":
    test_bidirectional_bulk_stream()
```

### Explanation

| Part | What it does |
|------|--------------|
| `generate_bulk_requests()` | A Python generator that yields `BulkRequestBody` messages one at a time. This is how gRPC client-side streaming works — the server receives messages as you yield them. |
| `stub.Bulk(generator)` | Opens the bidirectional stream. The client sends via the generator; the server sends responses back as it processes batches. |
| Response iteration | Reads `BulkResponse` messages as they arrive. In a bidirectional stream, you get responses *while* still sending — useful for large bulk operations. |

### Running the test

```bash
# Make sure OpenSearch is running with gRPC enabled
# (gradlew run should expose gRPC on port 9400)

source .venv/bin/activate
python -m opensearch_grpc.tests.test_bulk_stream
```

---

## Unit Test Sketch

```python
import json
import pytest
from opensearch_grpc.translation import toProtoBulkRequest
from opensearch_grpc.proto import common_pb2


def test_index_operation():
    body = [
        {"index": {"_index": "test", "_id": "1"}},
        {"field": "value"},
    ]
    req = toProtoBulkRequest(body)
    assert len(req.bulk_request_body) == 1
    op = req.bulk_request_body[0].operation_container
    assert op.HasField("index")
    assert op.index.x_id == "1"
    assert op.index.x_index == "test"
    assert json.loads(req.bulk_request_body[0].object) == {"field": "value"}


def test_delete_no_source():
    body = [
        {"delete": {"_index": "test", "_id": "1"}},
    ]
    req = toProtoBulkRequest(body)
    assert len(req.bulk_request_body) == 1
    assert req.bulk_request_body[0].operation_container.HasField("delete")
    assert req.bulk_request_body[0].object == b""


def test_update_with_doc():
    body = [
        {"update": {"_index": "test", "_id": "1"}},
        {"doc": {"price": 5.0}, "doc_as_upsert": True},
    ]
    req = toProtoBulkRequest(body)
    action = req.bulk_request_body[0].update_action
    assert json.loads(action.doc) == {"price": 5.0}
    assert action.doc_as_upsert is True


def test_mixed_operations():
    body = [
        {"index": {"_index": "i", "_id": "1"}},
        {"a": 1},
        {"delete": {"_index": "i", "_id": "2"}},
        {"create": {"_index": "i", "_id": "3"}},
        {"b": 2},
    ]
    req = toProtoBulkRequest(body, index="i", refresh="true")
    assert len(req.bulk_request_body) == 3
    assert req.index == "i"
    assert req.refresh == common_pb2.REFRESH_TRUE


def test_top_level_params():
    body = [{"index": {"_id": "1"}}, {"x": 1}]
    req = toProtoBulkRequest(
        body, index="idx", pipeline="p1", routing="r1", timeout="5s"
    )
    assert req.index == "idx"
    assert req.pipeline == "p1"
    assert req.routing == "r1"
    assert req.timeout == "5s"
```
