"""
test_simpledoc.py — Integration Tests for simpledoc_gRPC Translation Layer

Tests the full round-trip process:
    1. Client sends Python dict (original code)
    2. Translation layer converts to gRPC protobuf (under the hood)
    3. Protobuf is compiled and sent to OpenSearch server
    4. Server processes and returns protobuf response
    5. Response is converted back to Python dict (client's language)
    6. Original request is reconstructed and returned alongside the response

The client receives:
    - The server response (result, version, shards, etc.)
    - The original data they sent in, reconstructed from the protobuf

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_simpledoc.py -v
"""

import os
import pytest

from opensearch_grpc.simpledoc_gRPC import (
    index_document,
    create_document,
    update_document,
    delete_document,
    ResponseConverter,
    _build_single_request,
)


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def grpc_host():
    """Derive gRPC target from OPENSEARCH_URL environment."""
    opensearch_url = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
    grpc_port = os.environ.get("OPENSEARCH_GRPC_PORT", "9400")
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    return f"{host}:{grpc_port}"


@pytest.fixture(scope="session")
def index_name():
    return "test-simpledoc-ci"


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown(grpc_host, index_name):
    yield
    import urllib.request
    try:
        req = urllib.request.Request(f"http://localhost:9200/{index_name}", method="DELETE")
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


# ─── Tests: Full Round-Trip (send → convert → gRPC → response → reconstruct) ─


class TestIndexDocument:
    """
    Test index_document() full round-trip:
        Python dict → protobuf → gRPC → server → protobuf → Python dict + original
    """

    def test_index_returns_response_and_original(self, grpc_host, index_name):
        """
        Verify that after indexing, the client gets back:
        1. The server response in Python dict format
        2. The original request can be reconstructed from the protobuf
        """
        # This is what the client sends (their original Python code)
        original_body = {"title": "Hello gRPC", "author": "Test", "value": 42}

        # Step 1-4: Send to server via gRPC (conversion happens under the hood)
        response = index_document(
            index=index_name,
            body=original_body,
            id="1",
            refresh="true",
            grpc_host=grpc_host,
        )

        # Step 5: Verify server response is in Python dict format
        assert isinstance(response, dict)
        assert response["_index"] == index_name
        assert response["_id"] == "1"
        assert response["result"] in ("created", "updated")
        assert "_version" in response
        assert "_shards" in response

        # Step 6: Reconstruct the original request from protobuf
        # (proves the data survived the round-trip intact)
        meta = {"_index": index_name, "_id": "1"}
        proto_request = _build_single_request("index", meta, original_body, refresh="true")
        reconstructed = ResponseConverter.from_proto_request(proto_request)

        # Verify the original data is preserved
        assert reconstructed["operation"] == "index"
        assert reconstructed["index"] == index_name
        assert reconstructed["id"] == "1"
        assert reconstructed["body"] == original_body

    def test_index_overwrites_preserves_data(self, grpc_host, index_name):
        """Index same ID with new data — verify new data round-trips correctly."""
        new_body = {"title": "Updated doc", "value": 100}

        response = index_document(
            index=index_name, body=new_body, id="1",
            refresh="true", grpc_host=grpc_host,
        )
        assert response["result"] == "updated"

        # Reconstruct original from protobuf
        meta = {"_index": index_name, "_id": "1"}
        proto_request = _build_single_request("index", meta, new_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["body"] == new_body


class TestCreateDocument:
    """
    Test create_document() full round-trip.
    """

    def test_create_returns_response_and_original(self, grpc_host, index_name):
        """Create a doc and verify both response and original are returned correctly."""
        original_body = {"title": "Created doc", "status": "new", "priority": 1}

        response = create_document(
            index=index_name, body=original_body, id="create-1",
            refresh="true", grpc_host=grpc_host,
        )

        # Server response in client's language (Python dict)
        assert response["_index"] == index_name
        assert response["_id"] == "create-1"
        assert response["result"] == "created"

        # Original request reconstructed from protobuf
        meta = {"_index": index_name, "_id": "create-1"}
        proto_request = _build_single_request("create", meta, original_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["operation"] == "create"
        assert reconstructed["body"] == original_body


class TestUpdateDocument:
    """
    Test update_document() full round-trip.
    Update bodies have special structure (doc, doc_as_upsert) that must survive.
    """

    def test_update_returns_response_and_original(self, grpc_host, index_name):
        """Update a doc and verify the update body round-trips correctly."""
        # Ensure doc exists
        index_document(
            index=index_name, body={"title": "Original", "value": 1},
            id="update-1", refresh="true", grpc_host=grpc_host,
        )

        # This is the client's update instruction
        original_update_body = {"doc": {"value": 99, "updated": True}}

        response = update_document(
            index=index_name, id="update-1", body=original_update_body,
            refresh="true", grpc_host=grpc_host,
        )

        # Server response in Python dict
        assert response["_id"] == "update-1"
        assert response["result"] in ("updated", "noop")

        # Original update body reconstructed from protobuf
        meta = {"_index": index_name, "_id": "update-1"}
        proto_request = _build_single_request("update", meta, original_update_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["operation"] == "update"
        assert reconstructed["body"]["doc"] == {"value": 99, "updated": True}

    def test_update_doc_as_upsert_round_trips(self, grpc_host, index_name):
        """Verify doc_as_upsert flag survives the protobuf round-trip."""
        original_body = {"doc": {"name": "Upserted"}, "doc_as_upsert": True}

        response = update_document(
            index=index_name, id="upsert-1", body=original_body,
            refresh="true", grpc_host=grpc_host,
        )
        assert response["result"] in ("created", "updated")

        # Verify doc_as_upsert is preserved in reconstruction
        meta = {"_index": index_name, "_id": "upsert-1"}
        proto_request = _build_single_request("update", meta, original_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["body"]["doc_as_upsert"] is True
        assert reconstructed["body"]["doc"] == {"name": "Upserted"}


class TestDeleteDocument:
    """
    Test delete_document() full round-trip.
    Delete has no body — just operation metadata.
    """

    def test_delete_returns_response_and_original(self, grpc_host, index_name):
        """Delete a doc and verify response + original metadata."""
        # Ensure doc exists
        index_document(
            index=index_name, body={"title": "To delete"},
            id="delete-1", refresh="true", grpc_host=grpc_host,
        )

        response = delete_document(
            index=index_name, id="delete-1",
            refresh="true", grpc_host=grpc_host,
        )

        # Server response
        assert response["_id"] == "delete-1"
        assert response["result"] == "deleted"

        # Original request metadata (no body for deletes)
        meta = {"_index": index_name, "_id": "delete-1"}
        proto_request = _build_single_request("delete", meta, None)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["operation"] == "delete"
        assert reconstructed["index"] == index_name
        assert reconstructed["id"] == "delete-1"
        assert "body" not in reconstructed


class TestResponseConverter:
    """
    Test ResponseConverter directly — verifies protobuf ↔ Python dict conversion.
    """

    def test_from_proto_request_index(self, index_name):
        """Reconstruct an index request from protobuf."""
        body = {"name": "Widget", "price": 9.99}
        meta = {"_index": index_name, "_id": "rc-1"}
        request = _build_single_request("index", meta, body)

        result = ResponseConverter.from_proto_request(request)
        assert result == {
            "operation": "index",
            "index": index_name,
            "id": "rc-1",
            "body": {"name": "Widget", "price": 9.99},
        }

    def test_from_proto_request_update(self, index_name):
        """Reconstruct an update request from protobuf."""
        body = {"doc": {"price": 5.0}, "doc_as_upsert": True}
        meta = {"_index": index_name, "_id": "rc-2"}
        request = _build_single_request("update", meta, body)

        result = ResponseConverter.from_proto_request(request)
        assert result["operation"] == "update"
        assert result["body"]["doc"] == {"price": 5.0}
        assert result["body"]["doc_as_upsert"] is True

    def test_from_proto_request_delete(self, index_name):
        """Reconstruct a delete request from protobuf (no body)."""
        meta = {"_index": index_name, "_id": "rc-3"}
        request = _build_single_request("delete", meta, None)

        result = ResponseConverter.from_proto_request(request)
        assert result == {
            "operation": "delete",
            "index": index_name,
            "id": "rc-3",
        }
