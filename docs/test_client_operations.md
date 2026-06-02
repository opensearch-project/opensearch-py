# test_client_operations.py — Integration Test Documentation

## Overview

`test_client_operations.py` simulates a real client sending documents to OpenSearch via gRPC
and verifying the responses come back correctly. It uses the `StreamClient` to send operations
and REST API calls to verify the data was actually stored.

## How to Run

```bash
cd opensearch-py
source ../.venv/bin/activate
OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_client_operations.py -v -s
```

The `-s` flag shows all print statements so you can see what each test is doing.

## Prerequisites

- OpenSearch running on localhost:9200 (REST) and localhost:9400 (gRPC)
- Start with: `cd OpenSearch && nohup ./gradlew run -Dsecurity.enabled=false > /tmp/opensearch-run.log 2>&1 & disown`
- Virtual environment activated with grpcio installed

## Test Classes

### TestAddDocuments (4 tests)

| Test | What it does | Verifies |
|------|-------------|----------|
| `test_index_single_document` | Index one doc with ID | Response has `result: created`, REST confirms data stored |
| `test_index_multiple_documents` | Index 3 docs in one batch | All 3 return `result: created` |
| `test_create_document` | Create doc (fails if exists) | Returns `result: created` |
| `test_index_without_id` | Index without specifying ID | Server auto-generates an ID |

### TestUpdateDocuments (2 tests)

| Test | What it does | Verifies |
|------|-------------|----------|
| `test_update_partial_document` | Update one field of doc-1 | `result: updated`, REST confirms field changed, other fields unchanged |
| `test_update_with_upsert` | Upsert (create if missing) | `result: created` or `updated`, REST confirms data |

### TestDeleteDocuments (2 tests)

| Test | What it does | Verifies |
|------|-------------|----------|
| `test_delete_existing_document` | Delete a doc that exists | `result: deleted`, REST confirms doc is gone |
| `test_delete_nonexistent_document` | Delete a doc that doesn't exist | `result: not_found` |

### TestDocumentCount (1 test)

| Test | What it does | Verifies |
|------|-------------|----------|
| `test_count_after_operations` | Check doc count via REST | At least 7 docs exist after all adds |

### TestErrorHandling (1 test)

| Test | What it does | Verifies |
|------|-------------|----------|
| `test_create_duplicate_document` | Create doc-1 again (already exists) | Returns error with `version_conflict_engine_exception` |

### TestMixedBatch (1 test)

| Test | What it does | Verifies |
|------|-------------|----------|
| `test_mixed_operations_batch` | Send index + update + delete in one flush | Each op returns correct result |

## How the Tests Work

```
Client (pytest)                    OpenSearch Server
      │                                    │
      │── StreamClient.index() ──────────→ │  (queued locally)
      │── StreamClient.update() ─────────→ │  (queued locally)
      │── StreamClient.delete() ─────────→ │  (queued locally)
      │                                    │
      │── StreamClient.flush() ──────────→ │  (all ops sent as one BulkRequest via gRPC:9400)
      │                                    │
      │←── responses[] ──────────────────── │  (BulkResponse converted to Python dicts)
      │                                    │
      │── REST GET /_doc/id ─────────────→ │  (verify via REST:9200)
      │←── document source ──────────────── │
```

## File Location

```
opensearch-py/
└── test_opensearchpy/
    └── test_translation/
        ├── test_client_operations.py  ← This test file
        ├── test_simpledoc.py          ← Original unit test
        ├── test_simpledoc_ci.py       ← Pytest CI tests
        ├── test_bulk_request.py       ← Bulk request tests
        └── test_bulk_stream.py        ← Raw bulk stream test
```
