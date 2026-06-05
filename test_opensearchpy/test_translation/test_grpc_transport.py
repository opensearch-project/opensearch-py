"""
test_grpc_transport.py — Automated Integration Tests: OpenSearch Client with GrpcTransport

Fully automated tests that verify the GrpcTransport works as a drop-in
replacement for the standard opensearch-py transport. Uses grpc_hosts parameter.

Requires:
    - OpenSearch running on localhost:9200 (REST) with gRPC on localhost:9400
    - No manual setup needed — tests create/cleanup their own indexes

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_grpc_transport.py -v
"""

import os

import pytest

from opensearch_grpc.grpc_transport import GrpcTransport
from opensearchpy import OpenSearch


@pytest.fixture(scope="session")
def client():
    """Create a standard opensearch-py client with GrpcTransport using grpc_hosts."""
    opensearch_url = os.environ.get("OPENSEARCH_URL", "http://localhost:9200")
    grpc_port = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    port = int(opensearch_url.split(":")[-1])

    c = OpenSearch(
        hosts=[{"host": host, "port": port}],
        grpc_hosts=[{"host": host, "port": grpc_port}],
        transport_class=GrpcTransport,
        use_ssl=False,
    )
    yield c
    c.close()


@pytest.fixture(scope="session")
def index_name():
    return "test-grpc-transport"


@pytest.fixture(autouse=True, scope="session")
def cleanup(client, index_name):
    """Ensure clean state before and after all tests."""
    client.indices.delete(index=index_name, ignore=[404])
    yield
    client.indices.delete(index=index_name, ignore=[404])


class TestBulkViaGrpc:
    """Verify client.bulk() is routed over gRPC."""

    def test_bulk_index_documents(self, client, index_name):
        """Bulk index 3 documents — all should be created."""
        body = [
            {"index": {"_index": index_name, "_id": "1"}},
            {"title": "First", "value": 1},
            {"index": {"_index": index_name, "_id": "2"}},
            {"title": "Second", "value": 2},
            {"index": {"_index": index_name, "_id": "3"}},
            {"title": "Third", "value": 3},
        ]
        resp = client.bulk(body=body, refresh=True)

        assert resp["errors"] is False
        assert len(resp["items"]) == 3
        for item in resp["items"]:
            assert item["index"]["result"] == "created"

    def test_bulk_mixed_operations(self, client, index_name):
        """Bulk with index + update + delete in one call."""
        body = [
            {"index": {"_index": index_name, "_id": "4"}},
            {"title": "New doc", "value": 4},
            {"update": {"_index": index_name, "_id": "1"}},
            {"doc": {"value": 100}},
            {"delete": {"_index": index_name, "_id": "3"}},
        ]
        resp = client.bulk(body=body, refresh=True)

        assert resp["errors"] is False
        assert len(resp["items"]) == 3
        assert resp["items"][0]["index"]["result"] == "created"
        assert resp["items"][1]["update"]["result"] == "updated"
        assert resp["items"][2]["delete"]["result"] == "deleted"

    def test_bulk_with_index_param(self, client, index_name):
        """Bulk with default index parameter (not in each action)."""
        body = [
            {"index": {"_id": "5"}},
            {"title": "Default index doc"},
        ]
        resp = client.bulk(body=body, index=index_name, refresh=True)

        assert resp["errors"] is False
        assert resp["items"][0]["index"]["_index"] == index_name

    def test_bulk_large_batch(self, client, index_name):
        """Bulk index 50 documents in one call."""
        body = []
        for i in range(100, 150):
            body.append({"index": {"_index": index_name, "_id": str(i)}})
            body.append({"title": f"Batch doc {i}", "value": i})

        resp = client.bulk(body=body, refresh=True)

        assert resp["errors"] is False
        assert len(resp["items"]) == 50


class TestSingleDocViaGrpc:
    """Verify single-doc operations route over gRPC (via Bulk wrapper)."""

    def test_index_single_document(self, client, index_name):
        """client.index() creates a document via gRPC."""
        resp = client.index(index=index_name, body={"title": "Single"}, id="single-1", refresh=True)

        assert resp["result"] == "created"
        assert resp["_id"] == "single-1"

    def test_create_document(self, client, index_name):
        """client.create() creates a document, fails if exists."""
        resp = client.create(index=index_name, body={"title": "Created"}, id="create-1", refresh=True)

        assert resp["result"] == "created"
        assert resp["_id"] == "create-1"

    def test_update_document(self, client, index_name):
        """client.update() partially updates a document via gRPC."""
        resp = client.update(index=index_name, id="single-1", body={"doc": {"value": 999}}, refresh=True)

        assert resp["result"] == "updated"
        assert resp["_id"] == "single-1"

    def test_delete_document(self, client, index_name):
        """client.delete() removes a document via gRPC."""
        resp = client.delete(index=index_name, id="create-1", refresh=True)

        assert resp["result"] == "deleted"
        assert resp["_id"] == "create-1"


class TestRestFallback:
    """Verify non-gRPC operations fall back to REST transparently."""

    def test_search(self, client, index_name):
        """client.search() uses REST."""
        client.indices.refresh(index=index_name)
        resp = client.search(index=index_name, body={"query": {"match_all": {}}})

        assert resp["hits"]["total"]["value"] >= 1

    def test_get_document(self, client, index_name):
        """client.get() uses REST."""
        resp = client.get(index=index_name, id="1")

        assert resp["found"] is True
        assert resp["_source"]["value"] == 100

    def test_count(self, client, index_name):
        """client.count() uses REST."""
        resp = client.count(index=index_name)

        assert resp["count"] >= 3

    def test_create_and_delete_index(self, client):
        """client.indices.create/delete() uses REST."""
        idx = "test-grpc-auto-compat"
        resp = client.indices.create(index=idx, body={"settings": {"number_of_shards": 1}})
        assert resp["acknowledged"] is True

        resp = client.indices.delete(index=idx)
        assert resp["acknowledged"] is True


class TestEndToEndWorkflow:
    """Verify full workflows: gRPC writes → REST reads."""

    def test_bulk_then_search(self, client, index_name):
        """Bulk index via gRPC, then search via REST finds the documents."""
        body = [
            {"index": {"_index": index_name, "_id": "wf-1"}},
            {"title": "Workflow doc", "category": "automated"},
        ]
        bulk_resp = client.bulk(body=body, refresh=True)
        assert bulk_resp["errors"] is False

        client.indices.refresh(index=index_name)
        search_resp = client.search(
            index=index_name,
            body={"query": {"match": {"category": "automated"}}}
        )
        hits = search_resp["hits"]["hits"]
        assert len(hits) >= 1
        assert hits[0]["_source"]["title"] == "Workflow doc"

    def test_index_then_get(self, client, index_name):
        """Index via gRPC, then get via REST returns the document."""
        client.index(index=index_name, body={"title": "Get test", "x": 42}, id="get-1", refresh=True)

        resp = client.get(index=index_name, id="get-1")
        assert resp["found"] is True
        assert resp["_source"]["x"] == 42

    def test_update_then_get(self, client, index_name):
        """Update via gRPC, then get via REST shows updated values."""
        client.update(index=index_name, id="get-1", body={"doc": {"x": 99}}, refresh=True)

        resp = client.get(index=index_name, id="get-1")
        assert resp["_source"]["x"] == 99
        assert resp["_source"]["title"] == "Get test"  # unchanged field

    def test_delete_then_get_404(self, client, index_name):
        """Delete via gRPC, then get via REST returns not found."""
        client.delete(index=index_name, id="get-1", refresh=True)

        with pytest.raises(Exception):
            client.get(index=index_name, id="get-1")
