"""
test_simpledoc_ci.py — Integration Tests for Translation Layer Round-Trip

Tests the full round-trip process:
    1. Client sends Python dict
    2. Translation layer converts to gRPC protobuf
    3. Protobuf is sent to OpenSearch server
    4. Server responds with protobuf
    5. Response is converted back to Python dict
    6. Original request is reconstructable from protobuf

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_simpledoc_ci.py -v
"""

import os

import pytest

from opensearch_grpc.stream_client import StreamClient
from opensearch_grpc.translation import (
    RequestConverter,
    ResponseConverter,
    _build_single_request,
)


@pytest.fixture(scope="session")
def grpc_host():
    opensearch_url = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
    grpc_port = os.environ.get("OPENSEARCH_GRPC_PORT", "9400")
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    return f"{host}:{grpc_port}"


@pytest.fixture(scope="session")
def index_name():
    return "test-simpledoc-ci"


@pytest.fixture(scope="session")
def client(grpc_host):
    c = StreamClient(grpc_host, refresh="true")
    c.connect()
    yield c
    c.close()


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown(index_name):
    yield
    import urllib.request
    try:
        req = urllib.request.Request(f"http://localhost:9200/{index_name}", method="DELETE")
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


class TestIndexDocument:
    """Test index full round-trip: Python dict → gRPC → response → reconstruct."""

    def test_index_returns_response_and_original(self, client, index_name):
        original_body = {"title": "Hello gRPC", "author": "Test", "value": 42}

        client.index(index_name, body=original_body, id="1")
        responses = client.flush()

        resp = responses[0]["index"]
        assert resp["_index"] == index_name
        assert resp["_id"] == "1"
        assert resp["result"] in ("created", "updated")

        # Reconstruct original from protobuf
        meta = {"_index": index_name, "_id": "1"}
        proto_request = _build_single_request("index", meta, original_body, refresh="true")
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["operation"] == "index"
        assert reconstructed["index"] == index_name
        assert reconstructed["id"] == "1"
        assert reconstructed["body"] == original_body

    def test_index_overwrites_preserves_data(self, client, index_name):
        new_body = {"title": "Updated doc", "value": 100}

        client.index(index_name, body=new_body, id="1")
        responses = client.flush()
        assert responses[0]["index"]["result"] == "updated"

        meta = {"_index": index_name, "_id": "1"}
        proto_request = _build_single_request("index", meta, new_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["body"] == new_body


class TestCreateDocument:
    """Test create full round-trip."""

    def test_create_returns_response_and_original(self, client, index_name):
        original_body = {"title": "Created doc", "status": "new", "priority": 1}

        client.create(index_name, body=original_body, id="create-1")
        responses = client.flush()

        resp = responses[0]["create"]
        assert resp["_index"] == index_name
        assert resp["_id"] == "create-1"
        assert resp["result"] == "created"

        meta = {"_index": index_name, "_id": "create-1"}
        proto_request = _build_single_request("create", meta, original_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["operation"] == "create"
        assert reconstructed["body"] == original_body


class TestUpdateDocument:
    """Test update full round-trip."""

    def test_update_returns_response_and_original(self, client, index_name):
        # Ensure doc exists
        client.index(index_name, body={"title": "Original", "value": 1}, id="update-1")
        client.flush()

        original_update_body = {"doc": {"value": 99, "updated": True}}
        client.update(index_name, id="update-1", body=original_update_body)
        responses = client.flush()

        resp = responses[0]["update"]
        assert resp["_id"] == "update-1"
        assert resp["result"] in ("updated", "noop")

        meta = {"_index": index_name, "_id": "update-1"}
        proto_request = _build_single_request("update", meta, original_update_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["operation"] == "update"
        assert reconstructed["body"]["doc"] == {"value": 99, "updated": True}

    def test_update_doc_as_upsert_round_trips(self, client, index_name):
        original_body = {"doc": {"name": "Upserted"}, "doc_as_upsert": True}

        client.update(index_name, id="upsert-1", body=original_body)
        responses = client.flush()
        assert responses[0]["update"]["result"] in ("created", "updated")

        meta = {"_index": index_name, "_id": "upsert-1"}
        proto_request = _build_single_request("update", meta, original_body)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["body"]["doc_as_upsert"] is True
        assert reconstructed["body"]["doc"] == {"name": "Upserted"}


class TestDeleteDocument:
    """Test delete full round-trip."""

    def test_delete_returns_response_and_original(self, client, index_name):
        client.index(index_name, body={"title": "To delete"}, id="delete-1")
        client.flush()

        client.delete(index_name, id="delete-1")
        responses = client.flush()

        resp = responses[0]["delete"]
        assert resp["_id"] == "delete-1"
        assert resp["result"] == "deleted"

        meta = {"_index": index_name, "_id": "delete-1"}
        proto_request = _build_single_request("delete", meta, None)
        reconstructed = ResponseConverter.from_proto_request(proto_request)
        assert reconstructed["operation"] == "delete"
        assert reconstructed["index"] == index_name
        assert reconstructed["id"] == "delete-1"
        assert "body" not in reconstructed


class TestResponseConverter:
    """Test ResponseConverter directly."""

    def test_from_proto_request_index(self, index_name):
        body = {"name": "Widget", "price": 9.99}
        meta = {"_index": index_name, "_id": "rc-1"}
        request = _build_single_request("index", meta, body)
        result = ResponseConverter.from_proto_request(request)
        assert result == {
            "operation": "index", "index": index_name,
            "id": "rc-1", "body": {"name": "Widget", "price": 9.99},
        }

    def test_from_proto_request_update(self, index_name):
        body = {"doc": {"price": 5.0}, "doc_as_upsert": True}
        meta = {"_index": index_name, "_id": "rc-2"}
        request = _build_single_request("update", meta, body)
        result = ResponseConverter.from_proto_request(request)
        assert result["operation"] == "update"
        assert result["body"]["doc"] == {"price": 5.0}
        assert result["body"]["doc_as_upsert"] is True

    def test_from_proto_request_delete(self, index_name):
        meta = {"_index": index_name, "_id": "rc-3"}
        request = _build_single_request("delete", meta, None)
        result = ResponseConverter.from_proto_request(request)
        assert result == {"operation": "delete", "index": index_name, "id": "rc-3"}
