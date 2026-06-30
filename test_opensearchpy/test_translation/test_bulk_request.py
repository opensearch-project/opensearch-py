# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
"""
test_bulk_request.py — Unit Tests for BulkRequestProtoBuilder

Tests the translation layer conversion logic without requiring a running
OpenSearch server. No network calls are made.

Run:
    pytest test_opensearchpy/test_translation/test_bulk_request.py -v
"""

from typing import Any, Dict, List

from opensearch_grpc.translation import (
    BulkRequestProtoBuilder,
    toProtoBulkRequest,
)


class TestBulkRequestProtoBuilderBuild:
    """Test BulkRequestProtoBuilder builds correct protobuf structures."""

    def test_single_index_builds_one_body(self) -> None:
        """Single index operation produces one BulkRequestBody."""
        req = BulkRequestProtoBuilder(index="test-index", refresh="true")
        req.index(body={"title": "Doc 1"}, id="1")
        proto = req.build()

        assert len(proto.bulk_request_body) == 1
        assert proto.index == "test-index"
        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("index")
        assert op.index.x_id == "1"
        assert op.index.x_index == "test-index"

    def test_bulk_builds_multiple_bodies(self) -> None:
        """Multiple operations produce correct number of BulkRequestBody."""
        req = BulkRequestProtoBuilder(index="test-index")
        req.index(body={"a": 1}, id="1")
        req.create(body={"b": 2}, id="2")
        req.update(id="1", body={"doc": {"a": 10}})
        req.delete(id="2")
        proto = req.build()

        assert len(proto.bulk_request_body) == 4

    def test_index_operation_sets_correct_fields(self) -> None:
        """Index operation has correct operation container type."""
        req = BulkRequestProtoBuilder(index="idx")
        req.index(body={"x": 1}, id="doc-1", routing="r1", pipeline="p1")
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("index")
        assert op.index.x_id == "doc-1"
        assert op.index.routing == "r1"
        assert op.index.pipeline == "p1"

    def test_create_operation_sets_correct_fields(self) -> None:
        """Create operation uses WriteOperation."""
        req = BulkRequestProtoBuilder(index="idx")
        req.create(body={"x": 1}, id="doc-1")
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("create")
        assert op.create.x_id == "doc-1"

    def test_update_operation_sets_correct_fields(self) -> None:
        """Update operation includes update_action with doc bytes."""
        req = BulkRequestProtoBuilder(index="idx")
        req.update(id="doc-1", body={"doc": {"value": 99}})
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("update")
        assert op.update.x_id == "doc-1"
        assert proto.bulk_request_body[0].HasField("update_action")

    def test_delete_operation_sets_correct_fields(self) -> None:
        """Delete operation has no object or update_action."""
        req = BulkRequestProtoBuilder(index="idx")
        req.delete(id="doc-1")
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("delete")
        assert op.delete.x_id == "doc-1"

    def test_builder_len(self) -> None:
        """len() returns number of queued operations."""
        bulk = BulkRequestProtoBuilder(index="test")
        assert len(bulk) == 0
        bulk.index(body={"a": 1}, id="1")
        bulk.delete(id="2")
        assert len(bulk) == 2

    def test_builder_chaining(self) -> None:
        """Operations can be chained."""
        bulk = (
            BulkRequestProtoBuilder(index="test")
            .index(body={"a": 1}, id="1")
            .create(body={"b": 2}, id="2")
            .update(id="1", body={"doc": {"a": 10}})
            .delete(id="2")
        )
        assert len(bulk) == 4


class TestBulkRequestProtoBuilderFromBody:
    """Test BulkRequestProtoBuilder.from_body with different input formats."""

    def test_from_list_of_dicts(self) -> None:
        """Parses a list of action/source dicts."""
        body: List[Dict[str, Any]] = [
            {"index": {"_index": "idx", "_id": "1"}},
            {"title": "Doc 1"},
            {"delete": {"_index": "idx", "_id": "2"}},
        ]
        req = BulkRequestProtoBuilder.from_body(body)
        proto = req.build()

        assert len(proto.bulk_request_body) == 2

    def test_from_ndjson_string(self) -> None:
        """Parses an NDJSON string."""
        ndjson = '{"index": {"_index": "idx", "_id": "1"}}\n{"title": "Doc"}\n'
        req = BulkRequestProtoBuilder.from_body(ndjson)
        proto = req.build()

        assert len(proto.bulk_request_body) == 1

    def test_from_body_with_default_index(self) -> None:
        """Default index is set on the request."""
        body: List[Dict[str, Any]] = [{"index": {"_id": "1"}}, {"title": "Doc"}]
        req = BulkRequestProtoBuilder.from_body(body, index="my-index")
        proto = req.build()

        assert proto.index == "my-index"


class TestProtoFieldAssertions:
    """Test that built protobuf has correct fields set directly."""

    def test_index_proto_fields(self) -> None:
        """Assert index operation fields on the protobuf directly."""
        req = BulkRequestProtoBuilder(
            index="my-index", refresh="true", timeout="30s", pipeline="ingest-1"
        )
        req.index(
            body={"title": "Hello"},
            id="1",
            routing="shard-1",
            version=5,
            version_type="external",
        )
        proto = req.build()

        assert proto.index == "my-index"
        assert proto.timeout == "30s"
        assert proto.pipeline == "ingest-1"

        op = proto.bulk_request_body[0].operation_container.index
        assert op.x_id == "1"
        assert op.x_index == "my-index"
        assert op.routing == "shard-1"
        assert op.version == 5

    def test_update_proto_fields(self) -> None:
        """Assert update operation fields on the protobuf directly."""
        req = BulkRequestProtoBuilder(index="idx")
        req.update(id="1", body={"doc": {"value": 5}, "doc_as_upsert": True})
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container.update
        assert op.x_id == "1"
        assert op.x_index == "idx"

        action = proto.bulk_request_body[0].update_action
        assert action.doc_as_upsert is True
        assert action.HasField("doc")

    def test_delete_proto_fields(self) -> None:
        """Assert delete operation fields on the protobuf directly."""
        req = BulkRequestProtoBuilder(index="idx")
        req.delete(id="1", routing="r1")
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container.delete
        assert op.x_id == "1"
        assert op.x_index == "idx"
        assert op.routing == "r1"
        assert not proto.bulk_request_body[0].HasField("object")

    def test_bulk_proto_has_multiple_bodies(self) -> None:
        """Assert bulk request has correct number of operations."""
        req = BulkRequestProtoBuilder(index="idx")
        req.index(body={"a": 1}, id="1")
        req.create(body={"b": 2}, id="2")
        req.delete(id="3")
        proto = req.build()

        assert len(proto.bulk_request_body) == 3
        assert proto.bulk_request_body[0].operation_container.HasField("index")
        assert proto.bulk_request_body[1].operation_container.HasField("create")
        assert proto.bulk_request_body[2].operation_container.HasField("delete")


class TestToProtoBulkRequest:
    """Test the legacy toProtoBulkRequest function."""

    def test_builds_from_list(self) -> None:
        """Converts list of dicts to protobuf."""
        body: List[Dict[str, Any]] = [
            {"index": {"_index": "idx", "_id": "1"}},
            {"title": "Doc"},
        ]
        proto = toProtoBulkRequest(body)
        assert len(proto.bulk_request_body) == 1

    def test_builds_from_ndjson(self) -> None:
        """Converts NDJSON string to protobuf."""
        ndjson = '{"index": {"_index": "idx", "_id": "1"}}\n{"title": "Doc"}\n'
        proto = toProtoBulkRequest(ndjson)
        assert len(proto.bulk_request_body) == 1

    def test_sets_request_level_params(self) -> None:
        """Sets refresh, timeout, pipeline on the request."""
        body: List[Dict[str, Any]] = [{"index": {"_id": "1"}}, {"x": 1}]
        proto = toProtoBulkRequest(body, index="idx", timeout="30s")
        assert proto.index == "idx"
        assert proto.timeout == "30s"


class TestResponseConverter:
    """Unit tests for ResponseConverter — proto response back to Python dict."""

    def test_single_index_response(self) -> None:
        """Convert a single index item response from proto to Python dict."""
        from opensearch.protobufs.schemas.common_pb2 import BulkResponse
        from opensearch_grpc.translation import ResponseConverter

        response = BulkResponse()
        response.took = 5
        response.errors = False

        item = response.items.add()
        item.index.x_index = "test-index"
        item.index.x_id = "1"
        item.index.x_version = 1
        item.index.result = "created"
        item.index.status = 0  # gRPC OK
        item.index.x_seq_no = 0
        item.index.x_primary_term = 1
        item.index.x_shards.total = 2
        item.index.x_shards.successful = 1
        item.index.x_shards.failed = 0

        result = ResponseConverter.from_bulk_response(response)

        assert result["took"] == 5
        assert result["errors"] is False
        assert len(result["items"]) == 1

        index_item = result["items"][0]["index"]
        assert index_item["_index"] == "test-index"
        assert index_item["_id"] == "1"
        assert index_item["_version"] == 1
        assert index_item["result"] == "created"
        assert index_item["status"] == 201
        assert index_item["_seq_no"] == 0
        assert index_item["_primary_term"] == 1
        assert index_item["_shards"]["total"] == 2
        assert index_item["_shards"]["successful"] == 1
        assert index_item["_shards"]["failed"] == 0

    def test_update_response(self) -> None:
        """Convert an update item response from proto to Python dict."""
        from opensearch.protobufs.schemas.common_pb2 import BulkResponse
        from opensearch_grpc.translation import ResponseConverter

        response = BulkResponse()
        response.took = 3
        response.errors = False

        item = response.items.add()
        item.update.x_index = "test-index"
        item.update.x_id = "1"
        item.update.x_version = 2
        item.update.result = "updated"
        item.update.status = 0  # gRPC OK
        item.update.x_seq_no = 1
        item.update.x_primary_term = 1
        item.update.x_shards.total = 2
        item.update.x_shards.successful = 1
        item.update.x_shards.failed = 0

        result = ResponseConverter.from_bulk_response(response)

        assert result["errors"] is False
        update_item = result["items"][0]["update"]
        assert update_item["_index"] == "test-index"
        assert update_item["_id"] == "1"
        assert update_item["_version"] == 2
        assert update_item["result"] == "updated"
        assert update_item["status"] == 200

    def test_delete_response(self) -> None:
        """Convert a delete item response from proto to Python dict."""
        from opensearch.protobufs.schemas.common_pb2 import BulkResponse
        from opensearch_grpc.translation import ResponseConverter

        response = BulkResponse()
        response.took = 2
        response.errors = False

        item = response.items.add()
        item.delete.x_index = "test-index"
        item.delete.x_id = "1"
        item.delete.x_version = 3
        item.delete.result = "deleted"
        item.delete.status = 0  # gRPC OK
        item.delete.x_seq_no = 2
        item.delete.x_primary_term = 1
        item.delete.x_shards.total = 2
        item.delete.x_shards.successful = 1
        item.delete.x_shards.failed = 0

        result = ResponseConverter.from_bulk_response(response)

        assert result["errors"] is False
        delete_item = result["items"][0]["delete"]
        assert delete_item["_index"] == "test-index"
        assert delete_item["_id"] == "1"
        assert delete_item["result"] == "deleted"
        assert delete_item["status"] == 200

    def test_create_response(self) -> None:
        """Convert a create item response from proto to Python dict."""
        from opensearch.protobufs.schemas.common_pb2 import BulkResponse
        from opensearch_grpc.translation import ResponseConverter

        response = BulkResponse()
        response.took = 4
        response.errors = False

        item = response.items.add()
        item.create.x_index = "test-index"
        item.create.x_id = "2"
        item.create.x_version = 1
        item.create.result = "created"
        item.create.status = 0  # gRPC OK
        item.create.x_seq_no = 3
        item.create.x_primary_term = 1
        item.create.x_shards.total = 2
        item.create.x_shards.successful = 1
        item.create.x_shards.failed = 0

        result = ResponseConverter.from_bulk_response(response)

        assert result["errors"] is False
        create_item = result["items"][0]["create"]
        assert create_item["_index"] == "test-index"
        assert create_item["_id"] == "2"
        assert create_item["result"] == "created"
        assert create_item["status"] == 201

    def test_mixed_operations_response(self) -> None:
        """Convert a response with index + update + delete items."""
        from opensearch.protobufs.schemas.common_pb2 import BulkResponse
        from opensearch_grpc.translation import ResponseConverter

        response = BulkResponse()
        response.took = 10
        response.errors = False

        # Index item
        item1 = response.items.add()
        item1.index.x_index = "test-index"
        item1.index.x_id = "1"
        item1.index.x_version = 1
        item1.index.result = "created"
        item1.index.status = 0
        item1.index.x_shards.total = 2
        item1.index.x_shards.successful = 1
        item1.index.x_shards.failed = 0

        # Update item
        item2 = response.items.add()
        item2.update.x_index = "test-index"
        item2.update.x_id = "2"
        item2.update.x_version = 2
        item2.update.result = "updated"
        item2.update.status = 0
        item2.update.x_shards.total = 2
        item2.update.x_shards.successful = 1
        item2.update.x_shards.failed = 0

        # Delete item
        item3 = response.items.add()
        item3.delete.x_index = "test-index"
        item3.delete.x_id = "3"
        item3.delete.x_version = 3
        item3.delete.result = "deleted"
        item3.delete.status = 0
        item3.delete.x_shards.total = 2
        item3.delete.x_shards.successful = 1
        item3.delete.x_shards.failed = 0

        result = ResponseConverter.from_bulk_response(response)

        assert result["took"] == 10
        assert result["errors"] is False
        assert len(result["items"]) == 3
        assert "index" in result["items"][0]
        assert "update" in result["items"][1]
        assert "delete" in result["items"][2]

    def test_error_response(self) -> None:
        """Convert a response with errors (duplicate create)."""
        from opensearch.protobufs.schemas.common_pb2 import BulkResponse
        from opensearch_grpc.translation import ResponseConverter

        response = BulkResponse()
        response.took = 5
        response.errors = True

        item = response.items.add()
        item.create.x_index = "test-index"
        item.create.x_id = "1"
        item.create.status = 6  # gRPC ALREADY_EXISTS
        item.create.result = ""
        item.create.error.type = "version_conflict_engine_exception"
        item.create.error.reason = "[1]: version conflict, document already exists"

        result = ResponseConverter.from_bulk_response(response)

        assert result["errors"] is True
        create_item = result["items"][0]["create"]
        assert create_item["status"] == 409
        assert "error" in create_item
        assert create_item["error"]["type"] == "version_conflict_engine_exception"
        assert "already exists" in create_item["error"]["reason"]

    def test_not_found_delete_response(self) -> None:
        """Convert a delete response for a nonexistent document."""
        from opensearch.protobufs.schemas.common_pb2 import BulkResponse
        from opensearch_grpc.translation import ResponseConverter

        response = BulkResponse()
        response.took = 1
        response.errors = False

        item = response.items.add()
        item.delete.x_index = "test-index"
        item.delete.x_id = "missing"
        item.delete.x_version = 1
        item.delete.result = "not_found"
        item.delete.status = 5  # gRPC NOT_FOUND
        item.delete.x_shards.total = 2
        item.delete.x_shards.successful = 1
        item.delete.x_shards.failed = 0

        result = ResponseConverter.from_bulk_response(response)

        assert result["errors"] is False
        delete_item = result["items"][0]["delete"]
        assert delete_item["result"] == "not_found"
        assert delete_item["status"] == 404
