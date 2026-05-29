#!/usr/bin/env python3
"""
test_simpledoc.py — Integration Test for simpledoc_gRPC Translation Layer

This test verifies the full round-trip for single document operations:
    Python Dict → Protobuf → gRPC → OpenSearch → gRPC → Protobuf → Python Dict

Each test function exercises one operation type (index, create, update, delete)
and verifies that:
    1. The Python dict is correctly converted to protobuf
    2. The protobuf is sent over gRPC to OpenSearch
    3. The server processes the operation
    4. The protobuf response is converted back to a Python dict
    5. The returned dict matches the expected opensearch-py format

Prerequisites:
    - OpenSearch running with gRPC enabled on localhost:9400
    - Start with: cd OpenSearch && nohup ./gradlew run -Dsecurity.enabled=false &
    - Activate venv: source .venv/bin/activate

Run:
    python -m test_opensearchpy.test_translation.test_simpledoc
"""

import sys
sys.path.insert(0, ".")  # Ensure we can import from the repo root

from opensearch_grpc.simpledoc_gRPC import (
    index_document,
    create_document,
    update_document,
    delete_document,
)

# ─── Test Configuration ───────────────────────────────────────────────────────

INDEX = "test-simpledoc"  # Index name used for all tests
GRPC_TARGET = "localhost:9400"  # gRPC endpoint


# ─── Test Functions ───────────────────────────────────────────────────────────


def test_index_document():
    """
    Test: Index a document (create or overwrite).

    This mirrors what happens when a user calls:
        client.index(index="test-simpledoc", body={"title": "Hello"}, id="1")

    Expected flow:
        1. The dict {"title": "Hello"} is serialized to JSON bytes
        2. An IndexOperation protobuf is created with _index and _id
        3. Sent over gRPC as a BulkRequest with 1 item
        4. Server indexes the document and returns status
        5. Response is converted back to a dict with _index, _id, result, etc.
    """
    print("\n" + "=" * 60)
    print("TEST: Index Document")
    print("=" * 60)
    print("Simulating: client.index(index='test-simpledoc', body={...}, id='1')")
    print("-" * 60)

    # This is what the user passes to the client
    document = {"title": "Hello gRPC", "author": "Test", "value": 42}

    # Call our translation layer — it handles the full round-trip
    result = index_document(
        index=INDEX,
        body=document,
        id="1",
        refresh="true",  # Make immediately searchable
        grpc_target=GRPC_TARGET,
    )

    # Verify the response is a proper Python dict (not protobuf)
    print(f"\n[TEST] Returned Python dict: {result}")
    assert isinstance(result, dict), "Response should be a Python dict"
    assert result.get("_index") == INDEX, f"Expected index={INDEX}"
    assert result.get("_id") == "1", "Expected id=1"
    assert result.get("result") in ("created", "updated"), "Expected created or updated"
    print("[TEST] ✅ PASSED — Document indexed successfully")


def test_create_document():
    """
    Test: Create a document (fails if already exists).

    This mirrors what happens when a user calls:
        client.create(index="test-simpledoc", body={"title": "New"}, id="2")

    The difference from index is that create will FAIL if the document
    already exists, while index will overwrite it.
    """
    print("\n" + "=" * 60)
    print("TEST: Create Document")
    print("=" * 60)
    print("Simulating: client.create(index='test-simpledoc', body={...}, id='2')")
    print("-" * 60)

    document = {"title": "Created via gRPC", "status": "new"}

    result = create_document(
        index=INDEX,
        body=document,
        id="2",
        refresh="true",
        grpc_target=GRPC_TARGET,
    )

    print(f"\n[TEST] Returned Python dict: {result}")
    assert isinstance(result, dict), "Response should be a Python dict"
    assert result.get("_index") == INDEX, f"Expected index={INDEX}"
    assert result.get("_id") == "2", "Expected id=2"
    assert result.get("result") == "created", "Expected result=created"
    print("[TEST] ✅ PASSED — Document created successfully")


def test_update_document():
    """
    Test: Update an existing document with partial data.

    This mirrors what happens when a user calls:
        client.update(index="test-simpledoc", id="1", body={"doc": {"value": 99}})

    The body for updates is different from index/create — it contains
    instructions like "doc" (partial update) rather than the full document.
    """
    print("\n" + "=" * 60)
    print("TEST: Update Document")
    print("=" * 60)
    print("Simulating: client.update(index='test-simpledoc', id='1', body={...})")
    print("-" * 60)

    # Update body uses "doc" key for partial updates
    update_body = {"doc": {"value": 99, "updated": True}}

    result = update_document(
        index=INDEX,
        id="1",
        body=update_body,
        refresh="true",
        grpc_target=GRPC_TARGET,
    )

    print(f"\n[TEST] Returned Python dict: {result}")
    assert isinstance(result, dict), "Response should be a Python dict"
    assert result.get("_index") == INDEX, f"Expected index={INDEX}"
    assert result.get("_id") == "1", "Expected id=1"
    assert result.get("result") in ("updated", "noop"), "Expected updated or noop"
    print("[TEST] ✅ PASSED — Document updated successfully")


def test_delete_document():
    """
    Test: Delete a document by ID.

    This mirrors what happens when a user calls:
        client.delete(index="test-simpledoc", id="2")

    Delete operations have no body — just the index and ID.
    """
    print("\n" + "=" * 60)
    print("TEST: Delete Document")
    print("=" * 60)
    print("Simulating: client.delete(index='test-simpledoc', id='2')")
    print("-" * 60)

    result = delete_document(
        index=INDEX,
        id="2",
        refresh="true",
        grpc_target=GRPC_TARGET,
    )

    print(f"\n[TEST] Returned Python dict: {result}")
    assert isinstance(result, dict), "Response should be a Python dict"
    assert result.get("_index") == INDEX, f"Expected index={INDEX}"
    assert result.get("_id") == "2", "Expected id=2"
    assert result.get("result") == "deleted", "Expected result=deleted"
    print("[TEST] ✅ PASSED — Document deleted successfully")


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    """Run all tests in sequence."""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  simpledoc_gRPC Integration Tests                           ║")
    print("║  Testing: Python Dict → gRPC → OpenSearch → gRPC → Dict    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"\nTarget: {GRPC_TARGET}")
    print(f"Index:  {INDEX}")

    # Run tests in order (create depends on index, delete depends on create)
    test_index_document()
    test_create_document()
    test_update_document()
    test_delete_document()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)
    print("\nFull round-trip verified:")
    print("  Python Dict → Protobuf → gRPC → OpenSearch → gRPC → Protobuf → Python Dict")


if __name__ == "__main__":
    main()
