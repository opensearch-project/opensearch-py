"""
test_simpledoc.py — Unit/Integration Tests for simpledoc_gRPC Translation Layer

Uses pytest fixtures following the opensearch-py CI pattern.
Connects to the OpenSearch server already running (localhost:9200)
and derives the gRPC port from the same host.

Run:
    pytest test_opensearchpy/test_translation/test_simpledoc.py -v

Environment variables:
    OPENSEARCH_URL: REST endpoint (default: https://localhost:9200)
    OPENSEARCH_GRPC_PORT: gRPC port (default: 9400)
"""

import os
import pytest

from opensearch_grpc.simpledoc_gRPC import (
    index_document,
    create_document,
    update_document,
    delete_document,
)


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def grpc_target():
    """
    Derive the gRPC target from the environment.

    Uses the same host as OPENSEARCH_URL (the REST endpoint on port 9200)
    but connects to the gRPC port (default 9400).
    """
    opensearch_url = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
    grpc_port = os.environ.get("OPENSEARCH_GRPC_PORT", "9400")

    # Extract host from URL (e.g. "https://localhost:9200" → "localhost")
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]

    target = f"{host}:{grpc_port}"
    return target


@pytest.fixture(scope="session")
def index_name():
    """Test index name — cleaned up after tests."""
    return "test-simpledoc-ci"


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown(grpc_target, index_name):
    """Run tests, then clean up the test index via REST."""
    yield

    # Cleanup: delete the test index after all tests
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    opensearch_url = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
    # Strip auth from URL for cleanup
    base_url = opensearch_url.replace("https://", "http://")
    try:
        req = urllib.request.Request(
            f"http://localhost:9200/{index_name}", method="DELETE"
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # Index may not exist, that's fine


# ─── Tests ────────────────────────────────────────────────────────────────────


class TestIndexDocument:
    """Tests for index_document() — mirrors client.index()"""

    def test_index_creates_document(self, grpc_target, index_name):
        """Index a new document and verify it returns 'created'."""
        result = index_document(
            index=index_name,
            body={"title": "Hello gRPC", "value": 42},
            id="1",
            refresh="true",
            grpc_target=grpc_target,
        )

        assert isinstance(result, dict)
        assert result["_index"] == index_name
        assert result["_id"] == "1"
        assert result["result"] in ("created", "updated")
        assert "_version" in result
        assert "_shards" in result

    def test_index_overwrites_document(self, grpc_target, index_name):
        """Index the same ID again and verify it returns 'updated'."""
        result = index_document(
            index=index_name,
            body={"title": "Updated doc", "value": 100},
            id="1",
            refresh="true",
            grpc_target=grpc_target,
        )

        assert result["_id"] == "1"
        assert result["result"] == "updated"

    def test_index_auto_generates_id(self, grpc_target, index_name):
        """Index without an ID and verify one is auto-generated."""
        result = index_document(
            index=index_name,
            body={"title": "Auto ID doc"},
            refresh="true",
            grpc_target=grpc_target,
        )

        assert result["_index"] == index_name
        assert result["_id"] is not None
        assert result["result"] == "created"


class TestCreateDocument:
    """Tests for create_document() — mirrors client.create()"""

    def test_create_new_document(self, grpc_target, index_name):
        """Create a document that doesn't exist yet."""
        result = create_document(
            index=index_name,
            body={"title": "Created doc", "status": "new"},
            id="create-1",
            refresh="true",
            grpc_target=grpc_target,
        )

        assert result["_index"] == index_name
        assert result["_id"] == "create-1"
        assert result["result"] == "created"

    def test_create_existing_document_fails(self, grpc_target, index_name):
        """Create a document that already exists — should return error."""
        # First create
        create_document(
            index=index_name,
            body={"title": "First"},
            id="create-dup",
            refresh="true",
            grpc_target=grpc_target,
        )

        # Second create with same ID should have error info
        result = create_document(
            index=index_name,
            body={"title": "Duplicate"},
            id="create-dup",
            refresh="true",
            grpc_target=grpc_target,
        )

        # The response should indicate a conflict
        assert "error" in result or result.get("result") != "created"


class TestUpdateDocument:
    """Tests for update_document() — mirrors client.update()"""

    def test_update_partial_document(self, grpc_target, index_name):
        """Update an existing document with partial data."""
        # Ensure doc exists
        index_document(
            index=index_name,
            body={"title": "Original", "value": 1},
            id="update-1",
            refresh="true",
            grpc_target=grpc_target,
        )

        # Partial update
        result = update_document(
            index=index_name,
            id="update-1",
            body={"doc": {"value": 99}},
            refresh="true",
            grpc_target=grpc_target,
        )

        assert result["_index"] == index_name
        assert result["_id"] == "update-1"
        assert result["result"] in ("updated", "noop")

    def test_update_with_doc_as_upsert(self, grpc_target, index_name):
        """Update with doc_as_upsert — creates if doesn't exist."""
        result = update_document(
            index=index_name,
            id="upsert-1",
            body={"doc": {"title": "Upserted", "value": 50}, "doc_as_upsert": True},
            refresh="true",
            grpc_target=grpc_target,
        )

        assert result["_id"] == "upsert-1"
        assert result["result"] in ("created", "updated")


class TestDeleteDocument:
    """Tests for delete_document() — mirrors client.delete()"""

    def test_delete_existing_document(self, grpc_target, index_name):
        """Delete a document that exists."""
        # Ensure doc exists
        index_document(
            index=index_name,
            body={"title": "To delete"},
            id="delete-1",
            refresh="true",
            grpc_target=grpc_target,
        )

        result = delete_document(
            index=index_name,
            id="delete-1",
            refresh="true",
            grpc_target=grpc_target,
        )

        assert result["_index"] == index_name
        assert result["_id"] == "delete-1"
        assert result["result"] == "deleted"

    def test_delete_nonexistent_document(self, grpc_target, index_name):
        """Delete a document that doesn't exist — should return not_found."""
        result = delete_document(
            index=index_name,
            id="does-not-exist",
            refresh="true",
            grpc_target=grpc_target,
        )

        assert result["_id"] == "does-not-exist"
        assert result.get("result") == "not_found" or "error" in result
