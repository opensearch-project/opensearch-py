# test_simpledoc.py — Test Documentation

## Overview

`test_simpledoc.py` is an integration test that verifies the full round-trip of single document operations through the gRPC translation layer. It confirms that:

1. Python dicts are correctly converted to protobuf
2. Protobuf messages are sent over gRPC to OpenSearch
3. OpenSearch processes the operations
4. Protobuf responses are converted back to Python dicts
5. The returned dicts match the opensearch-py format

## How to Run

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run the test
python -m test_opensearchpy.test_translation.test_simpledoc
```

**Prerequisites:**
- OpenSearch running with gRPC on port 9400
- Start with: `cd OpenSearch && nohup ./gradlew run -Dsecurity.enabled=false > /tmp/opensearch-run.log 2>&1 & disown`

## Test Sequence

The tests run in order because they depend on each other:

```
1. test_index_document()   → Creates doc-1 in "test-simpledoc" index
2. test_create_document()  → Creates doc-2 (would fail if it existed)
3. test_update_document()  → Updates doc-1 (must exist from step 1)
4. test_delete_document()  → Deletes doc-2 (must exist from step 2)
```

## What Each Test Verifies

### `test_index_document()`

| What | Expected |
|------|----------|
| Simulates | `client.index(index="test-simpledoc", body={"title": "Hello gRPC"}, id="1")` |
| Response type | Python dict (not protobuf) |
| `_index` | `"test-simpledoc"` |
| `_id` | `"1"` |
| `result` | `"created"` or `"updated"` |

### `test_create_document()`

| What | Expected |
|------|----------|
| Simulates | `client.create(index="test-simpledoc", body={"title": "Created"}, id="2")` |
| `result` | `"created"` (fails if doc already exists) |

### `test_update_document()`

| What | Expected |
|------|----------|
| Simulates | `client.update(index="test-simpledoc", id="1", body={"doc": {"value": 99}})` |
| `result` | `"updated"` or `"noop"` |
| Note | Uses `"doc"` key for partial update, not full document |

### `test_delete_document()`

| What | Expected |
|------|----------|
| Simulates | `client.delete(index="test-simpledoc", id="2")` |
| `result` | `"deleted"` |
| Note | No body — just index and ID |

## Reading the Output

The test output shows every step of the round-trip:

```
[simpledoc_gRPC] INDEX: index=test-simpledoc, id=1          ← Function called
[simpledoc_gRPC] Document body: {'title': 'Hello gRPC'}     ← Input dict
[simpledoc_gRPC] Built protobuf: op=index, ...              ← Dict → Protobuf
[simpledoc_gRPC] Sending protobuf over gRPC to ...          ← Network transport
[simpledoc_gRPC] Received protobuf BulkResponse             ← Server responded
[simpledoc_gRPC] Converting protobuf response → Python dict ← Protobuf → Dict
[simpledoc_gRPC] Response converted back to Python dict: {} ← Final result
[TEST] ✅ PASSED                                            ← Assertions passed
```

## File Location

```
opensearch-py/
└── test_opensearchpy/
    └── test_translation/
        ├── __init__.py
        └── test_simpledoc.py    ← This file
```

## Assertions

Each test asserts:
- Response is a `dict` (not a protobuf object)
- `_index` matches the target index
- `_id` matches the expected document ID
- `result` is the expected operation outcome
