# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
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
