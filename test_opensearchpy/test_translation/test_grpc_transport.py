"""
test_grpc_transport.py — Integration Test: Standard opensearch-py Client with GrpcTransport

Tests the GrpcTransport as a drop-in replacement. Uses the normal OpenSearch
client API — bulk goes over gRPC, everything else over REST.

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_grpc_transport.py -v -s
"""

import os
import pytest

from opensearchpy import OpenSearch
from opensearch_grpc.grpc_transport import GrpcTransport


@pytest.fixture(scope="session")
def client():
    """Create a standard opensearch-py client with GrpcTransport."""
    opensearch_url = os.environ.get("OPENSEARCH_URL", "http://localhost:9200")
    grpc_port = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    port = int(opensearch_url.split(":")[-1])

    c = OpenSearch(
        hosts=[{"host": host, "port": port}],
        transport_class=GrpcTransport,
        grpc_port=grpc_port,
        use_ssl=False,
    )
    yield c
    c.close()


@pytest.fixture(scope="session")
def index_name():
    return "test-grpc-transport"


@pytest.fixture(autouse=True, scope="session")
def cleanup(client, index_name):
    client.indices.delete(index=index_name, ignore=[404])
    yield
    client.indices.delete(index=index_name, ignore=[404])


class TestBulkViaGrpc:
    """Test that client.bulk() routes over gRPC."""

    def test_bulk_index_documents(self, client, index_name):
        """Bulk index multiple documents via gRPC."""
        print("\n[TEST] client.bulk() — indexing 3 docs via gRPC")
        body = [
            {"index": {"_index": index_name, "_id": "1"}},
            {"title": "First", "value": 1},
            {"index": {"_index": index_name, "_id": "2"}},
            {"title": "Second", "value": 2},
            {"index": {"_index": index_name, "_id": "3"}},
            {"title": "Third", "value": 3},
        ]
        resp = client.bulk(body=body, refresh=True)
        print(f"[TEST] Response: errors={resp['errors']}, items={len(resp['items'])}")

        assert resp["errors"] is False
        assert len(resp["items"]) == 3
        for item in resp["items"]:
            assert item["index"]["result"] == "created"
        print("[TEST] ✅ 3 documents indexed via gRPC")

    def test_bulk_mixed_operations(self, client, index_name):
        """Bulk with index + update + delete via gRPC."""
        print("\n[TEST] client.bulk() — mixed ops via gRPC")
        body = [
            {"index": {"_index": index_name, "_id": "4"}},
            {"title": "New doc", "value": 4},
            {"update": {"_index": index_name, "_id": "1"}},
            {"doc": {"value": 100}},
            {"delete": {"_index": index_name, "_id": "3"}},
        ]
        resp = client.bulk(body=body, refresh=True)
        print(f"[TEST] Response: errors={resp['errors']}, items={len(resp['items'])}")

        assert resp["errors"] is False
        assert len(resp["items"]) == 3
        assert resp["items"][0]["index"]["result"] == "created"
        assert resp["items"][1]["update"]["result"] == "updated"
        assert resp["items"][2]["delete"]["result"] == "deleted"
        print("[TEST] ✅ Mixed bulk (index+update+delete) via gRPC")

    def test_bulk_with_index_param(self, client, index_name):
        """Bulk with default index parameter."""
        print("\n[TEST] client.bulk() — with index param")
        body = [
            {"index": {"_id": "5"}},
            {"title": "Default index doc"},
        ]
        resp = client.bulk(body=body, index=index_name, refresh=True)
        print(f"[TEST] Response: {resp['items'][0]}")

        assert resp["errors"] is False
        assert resp["items"][0]["index"]["_index"] == index_name
        print("[TEST] ✅ Bulk with default index param works")


class TestRestFallback:
    """Test that non-bulk operations fall back to REST."""

    def test_search(self, client, index_name):
        """Search uses REST transport."""
        print("\n[TEST] client.search() — via REST")
        # Force refresh first to ensure docs are searchable
        client.indices.refresh(index=index_name)
        resp = client.search(index=index_name, body={"query": {"match_all": {}}})
        hits = resp["hits"]["total"]["value"]
        print(f"[TEST] Found {hits} documents")

        assert hits >= 1
        print("[TEST] ✅ Search works via REST fallback")

    def test_get_document(self, client, index_name):
        """Get single document uses REST."""
        print("\n[TEST] client.get() — via REST")
        resp = client.get(index=index_name, id="1")
        print(f"[TEST] Got doc: {resp['_source']}")

        assert resp["found"] is True
        assert resp["_source"]["value"] == 100  # Updated in bulk test
        print("[TEST] ✅ Get document works via REST")

    def test_index_single_document(self, client, index_name):
        """Single index uses REST."""
        print("\n[TEST] client.index() — via REST")
        resp = client.index(index=index_name, body={"title": "REST doc"}, id="rest-1", refresh=True)
        print(f"[TEST] Result: {resp['result']}")

        assert resp["result"] == "created"
        print("[TEST] ✅ Single index works via REST")

    def test_delete_document(self, client, index_name):
        """Delete uses REST."""
        print("\n[TEST] client.delete() — via REST")
        resp = client.delete(index=index_name, id="rest-1", refresh=True)
        print(f"[TEST] Result: {resp['result']}")

        assert resp["result"] == "deleted"
        print("[TEST] ✅ Delete works via REST")

    def test_count(self, client, index_name):
        """Count uses REST."""
        print("\n[TEST] client.count() — via REST")
        resp = client.count(index=index_name)
        print(f"[TEST] Count: {resp['count']}")

        assert resp["count"] >= 3
        print("[TEST] ✅ Count works via REST")


class TestClientCompatibility:
    """Test that the client behaves identically to standard opensearch-py."""

    def test_create_index(self, client):
        """Create index via REST."""
        print("\n[TEST] client.indices.create() — via REST")
        idx = "test-grpc-compat"
        resp = client.indices.create(index=idx, body={"settings": {"number_of_shards": 1}})
        print(f"[TEST] Acknowledged: {resp['acknowledged']}")

        assert resp["acknowledged"] is True
        client.indices.delete(index=idx)
        print("[TEST] ✅ Index create/delete works via REST")

    def test_bulk_then_search(self, client, index_name):
        """Full workflow: bulk index via gRPC, then search via REST."""
        print("\n[TEST] Full workflow: bulk (gRPC) → search (REST)")

        # Bulk via gRPC
        body = [
            {"index": {"_index": index_name, "_id": "wf-1"}},
            {"title": "Workflow doc", "category": "test"},
        ]
        bulk_resp = client.bulk(body=body, refresh=True)
        assert bulk_resp["errors"] is False
        print("[TEST]   Bulk indexed via gRPC ✓")

        # Refresh to ensure searchable
        client.indices.refresh(index=index_name)

        # Search via REST
        search_resp = client.search(
            index=index_name,
            body={"query": {"match": {"category": "test"}}}
        )
        hits = search_resp["hits"]["hits"]
        assert len(hits) >= 1
        assert hits[0]["_source"]["title"] == "Workflow doc"
        print(f"[TEST]   Search found doc via REST ✓")
        print("[TEST] ✅ Full gRPC→REST workflow works")
