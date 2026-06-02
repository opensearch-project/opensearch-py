"""
test_client_operations.py — Integration Tests: Client Document Operations

Simulates a real client sending documents to OpenSearch via gRPC and
verifying the responses come back correctly.

Tests:
    - Adding documents (index, create)
    - Updating documents
    - Deleting documents
    - Bulk operations
    - Document count verification (via REST)
    - Error handling (create existing doc, delete missing doc)

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_client_operations.py -v
"""

import os
import json
import urllib.request
import pytest

from opensearch_grpc.stream_client import StreamClient


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def grpc_target():
    opensearch_url = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
    grpc_port = os.environ.get("OPENSEARCH_GRPC_PORT", "9400")
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    return f"{host}:{grpc_port}"


@pytest.fixture(scope="session")
def rest_url():
    return os.environ.get("OPENSEARCH_URL", "http://localhost:9200")


@pytest.fixture(scope="session")
def index_name():
    return "test-client-ops"


@pytest.fixture(scope="session")
def client(grpc_target):
    c = StreamClient(grpc_target, refresh="true")
    c.connect()
    yield c
    c.close()


@pytest.fixture(autouse=True, scope="session")
def cleanup(index_name, rest_url):
    # Delete index before tests
    _rest_request(rest_url, f"/{index_name}", method="DELETE")
    yield
    # Delete index after tests
    _rest_request(rest_url, f"/{index_name}", method="DELETE")


def _rest_request(base_url, path, method="GET"):
    """Helper to make REST requests to OpenSearch for verification."""
    try:
        req = urllib.request.Request(f"{base_url}{path}", method=method)
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except Exception:
        return None


def _get_doc(rest_url, index, doc_id):
    """Get a document via REST to verify gRPC operations."""
    return _rest_request(rest_url, f"/{index}/_doc/{doc_id}")


def _get_count(rest_url, index):
    """Get document count via REST."""
    result = _rest_request(rest_url, f"/{index}/_count")
    return result["count"] if result else 0


# ─── Test: Adding Documents ───────────────────────────────────────────────────


class TestAddDocuments:
    """Test adding documents as a client."""

    def test_index_single_document(self, client, index_name, rest_url):
        """Client sends one document, gets response with _id and result."""
        client.index(index_name, body={"title": "First Document", "value": 1}, id="doc-1")
        responses = client.flush()

        assert len(responses) == 1
        resp = responses[0]["index"]
        assert resp["_index"] == index_name
        assert resp["_id"] == "doc-1"
        assert resp["result"] == "created"

        # Verify via REST
        doc = _get_doc(rest_url, index_name, "doc-1")
        assert doc["_source"]["title"] == "First Document"

    def test_index_multiple_documents(self, client, index_name, rest_url):
        """Client sends multiple documents in one batch."""
        client.index(index_name, body={"title": "Doc 2", "value": 2}, id="doc-2")
        client.index(index_name, body={"title": "Doc 3", "value": 3}, id="doc-3")
        client.index(index_name, body={"title": "Doc 4", "value": 4}, id="doc-4")
        responses = client.flush()

        assert len(responses) == 3
        for resp in responses:
            assert resp["index"]["result"] == "created"

    def test_create_document(self, client, index_name):
        """Client creates a document (fails if already exists)."""
        client.create(index_name, body={"title": "Created Doc", "value": 5}, id="doc-5")
        responses = client.flush()

        assert len(responses) == 1
        assert responses[0]["create"]["_id"] == "doc-5"
        assert responses[0]["create"]["result"] == "created"

    def test_index_without_id(self, client, index_name):
        """Client indexes without specifying an ID — server generates one."""
        client.index(index_name, body={"title": "Auto ID Doc", "value": 99})
        responses = client.flush()

        assert len(responses) == 1
        assert responses[0]["index"]["_id"] is not None
        assert responses[0]["index"]["result"] == "created"


# ─── Test: Updating Documents ─────────────────────────────────────────────────


class TestUpdateDocuments:
    """Test updating documents as a client."""

    def test_update_partial_document(self, client, index_name, rest_url):
        """Client updates one field of an existing document."""
        client.update(index_name, id="doc-1", body={"doc": {"value": 100}})
        responses = client.flush()

        assert len(responses) == 1
        assert responses[0]["update"]["_id"] == "doc-1"
        assert responses[0]["update"]["result"] == "updated"

        # Verify the update via REST
        doc = _get_doc(rest_url, index_name, "doc-1")
        assert doc["_source"]["value"] == 100
        assert doc["_source"]["title"] == "First Document"  # unchanged

    def test_update_with_upsert(self, client, index_name, rest_url):
        """Client upserts — creates doc if it doesn't exist."""
        client.update(
            index_name, id="doc-upsert",
            body={"doc": {"title": "Upserted", "value": 50}, "doc_as_upsert": True}
        )
        responses = client.flush()

        assert len(responses) == 1
        result = responses[0]["update"]["result"]
        assert result in ("created", "updated")

        doc = _get_doc(rest_url, index_name, "doc-upsert")
        assert doc["_source"]["title"] == "Upserted"


# ─── Test: Deleting Documents ─────────────────────────────────────────────────


class TestDeleteDocuments:
    """Test deleting documents as a client."""

    def test_delete_existing_document(self, client, index_name, rest_url):
        """Client deletes a document that exists."""
        # Ensure doc exists
        client.index(index_name, body={"title": "To Delete"}, id="doc-del")
        client.flush()

        # Delete it
        client.delete(index_name, id="doc-del")
        responses = client.flush()

        assert len(responses) == 1
        assert responses[0]["delete"]["_id"] == "doc-del"
        assert responses[0]["delete"]["result"] == "deleted"

        # Verify it's gone
        doc = _get_doc(rest_url, index_name, "doc-del")
        assert doc is None or doc.get("found") is False

    def test_delete_nonexistent_document(self, client, index_name):
        """Client tries to delete a doc that doesn't exist — gets not_found."""
        client.delete(index_name, id="does-not-exist")
        responses = client.flush()

        assert len(responses) == 1
        assert responses[0]["delete"]["result"] == "not_found"


# ─── Test: Document Count ─────────────────────────────────────────────────────


class TestDocumentCount:
    """Test that the server reflects the correct document count."""

    def test_count_after_operations(self, client, index_name, rest_url):
        """Verify the document count matches what we indexed."""
        count = _get_count(rest_url, index_name)
        # We should have: doc-1, doc-2, doc-3, doc-4, doc-5, auto-id, doc-upsert = 7
        assert count >= 7, f"Expected at least 7 docs, got {count}"


# ─── Test: Error Handling ─────────────────────────────────────────────────────


class TestErrorHandling:
    """Test that the client gets proper error responses."""

    def test_create_duplicate_document(self, client, index_name):
        """Creating a doc that already exists returns an error."""
        # doc-1 already exists from earlier tests
        client.create(index_name, body={"title": "Duplicate"}, id="doc-1")
        responses = client.flush()

        assert len(responses) == 1
        resp = responses[0]["create"]
        # Should have error or non-created result
        assert "error" in resp or resp.get("result") != "created"


# ─── Test: Mixed Batch ────────────────────────────────────────────────────────


class TestMixedBatch:
    """Test sending a mix of operations in one batch (like a real client)."""

    def test_mixed_operations_batch(self, client, index_name):
        """Client sends index + update + delete in one flush."""
        client.index(index_name, body={"title": "Batch New"}, id="batch-1")
        client.update(index_name, id="doc-1", body={"doc": {"batch": True}})
        client.delete(index_name, id="doc-5")
        responses = client.flush()

        assert len(responses) == 3
        assert responses[0]["index"]["result"] == "created"
        assert responses[1]["update"]["result"] == "updated"
        assert responses[2]["delete"]["result"] == "deleted"
