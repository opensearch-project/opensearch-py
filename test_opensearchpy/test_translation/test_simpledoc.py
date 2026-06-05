#!/usr/bin/env python3
"""
test_simpledoc.py — Manual Integration Test for Translation Layer

Run: python -m test_opensearchpy.test_translation.test_simpledoc
"""

from opensearch_grpc.stream_client import StreamClient

INDEX = "test-simpledoc"
GRPC_HOST = "localhost:9400"


def test_index_document():
    print("\n" + "=" * 60)
    print("TEST: Index Document")
    print("=" * 60)
    with StreamClient(GRPC_HOST, refresh="true") as client:
        client.index(INDEX, body={"title": "Hello gRPC", "value": 42}, id="1")
        responses = client.flush()
    resp = responses[0]["index"]
    assert resp["_id"] == "1"
    assert resp["result"] in ("created", "updated")
    print(f"[TEST] ✅ PASSED — result={resp['result']}")


def test_create_document():
    print("\n" + "=" * 60)
    print("TEST: Create Document")
    print("=" * 60)
    with StreamClient(GRPC_HOST, refresh="true") as client:
        client.create(INDEX, body={"title": "Created via gRPC"}, id="2")
        responses = client.flush()
    resp = responses[0]["create"]
    assert resp["_id"] == "2"
    assert resp["result"] == "created"
    print(f"[TEST] ✅ PASSED — result={resp['result']}")


def test_update_document():
    print("\n" + "=" * 60)
    print("TEST: Update Document")
    print("=" * 60)
    with StreamClient(GRPC_HOST, refresh="true") as client:
        client.update(INDEX, id="1", body={"doc": {"value": 99}})
        responses = client.flush()
    resp = responses[0]["update"]
    assert resp["_id"] == "1"
    assert resp["result"] in ("updated", "noop")
    print(f"[TEST] ✅ PASSED — result={resp['result']}")


def test_delete_document():
    print("\n" + "=" * 60)
    print("TEST: Delete Document")
    print("=" * 60)
    with StreamClient(GRPC_HOST, refresh="true") as client:
        client.delete(INDEX, id="2")
        responses = client.flush()
    resp = responses[0]["delete"]
    assert resp["_id"] == "2"
    assert resp["result"] == "deleted"
    print(f"[TEST] ✅ PASSED — result={resp['result']}")


def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  Translation Layer Integration Tests                        ║")
    print("║  Testing: Python Dict → gRPC → OpenSearch → gRPC → Dict    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    test_index_document()
    test_create_document()
    test_update_document()
    test_delete_document()
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)


if __name__ == "__main__":
    main()
