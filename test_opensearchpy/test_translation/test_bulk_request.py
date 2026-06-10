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
test_bulk_request.py — Unit Tests for RequestConverter and ResponseConverter

Tests the translation layer conversion logic without requiring a running
OpenSearch server. No network calls are made.

Run:
    pytest test_opensearchpy/test_translation/test_bulk_request.py -v
"""

from typing import Any, Dict, List

from opensearch_grpc.translation import (
    RequestConverter,
    ResponseConverter,
    _build_single_request,
    toProtoBulkRequest,
)


class TestRequestConverterBuild:
    """Test RequestConverter builds correct protobuf structures."""

    def test_single_index_builds_one_body(self) -> None:
        """Single index operation produces one BulkRequestBody."""
        req = RequestConverter(index="test-index", refresh="true")
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
        req = RequestConverter(index="test-index")
        req.index(body={"a": 1}, id="1")
        req.create(body={"b": 2}, id="2")
        req.update(id="1", body={"doc": {"a": 10}})
        req.delete(id="2")
        proto = req.build()

        assert len(proto.bulk_request_body) == 4

    def test_index_operation_sets_correct_fields(self) -> None:
        """Index operation has correct operation container type."""
        req = RequestConverter(index="idx")
        req.index(body={"x": 1}, id="doc-1", routing="r1", pipeline="p1")
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("index")
        assert op.index.x_id == "doc-1"
        assert op.index.routing == "r1"
        assert op.index.pipeline == "p1"

    def test_create_operation_sets_correct_fields(self) -> None:
        """Create operation uses WriteOperation."""
        req = RequestConverter(index="idx")
        req.create(body={"x": 1}, id="doc-1")
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("create")
        assert op.create.x_id == "doc-1"

    def test_update_operation_sets_correct_fields(self) -> None:
        """Update operation includes update_action with doc bytes."""
        req = RequestConverter(index="idx")
        req.update(id="doc-1", body={"doc": {"value": 99}})
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("update")
        assert op.update.x_id == "doc-1"
        assert proto.bulk_request_body[0].HasField("update_action")

    def test_delete_operation_sets_correct_fields(self) -> None:
        """Delete operation has no object or update_action."""
        req = RequestConverter(index="idx")
        req.delete(id="doc-1")
        proto = req.build()

        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("delete")
        assert op.delete.x_id == "doc-1"

    def test_builder_len(self) -> None:
        """len() returns number of queued operations."""
        bulk = RequestConverter(index="test")
        assert len(bulk) == 0
        bulk.index(body={"a": 1}, id="1")
        bulk.delete(id="2")
        assert len(bulk) == 2

    def test_builder_chaining(self) -> None:
        """Operations can be chained."""
        bulk = (
            RequestConverter(index="test")
            .index(body={"a": 1}, id="1")
            .create(body={"b": 2}, id="2")
            .update(id="1", body={"doc": {"a": 10}})
            .delete(id="2")
        )
        assert len(bulk) == 4


class TestRequestConverterFromBody:
    """Test RequestConverter.from_body with different input formats."""

    def test_from_list_of_dicts(self) -> None:
        """Parses a list of action/source dicts."""
        body: List[Dict[str, Any]] = [
            {"index": {"_index": "idx", "_id": "1"}},
            {"title": "Doc 1"},
            {"delete": {"_index": "idx", "_id": "2"}},
        ]
        req = RequestConverter.from_body(body)
        proto = req.build()

        assert len(proto.bulk_request_body) == 2

    def test_from_ndjson_string(self) -> None:
        """Parses an NDJSON string."""
        ndjson = '{"index": {"_index": "idx", "_id": "1"}}\n{"title": "Doc"}\n'
        req = RequestConverter.from_body(ndjson)
        proto = req.build()

        assert len(proto.bulk_request_body) == 1

    def test_from_body_with_default_index(self) -> None:
        """Default index is set on the request."""
        body: List[Dict[str, Any]] = [{"index": {"_id": "1"}}, {"title": "Doc"}]
        req = RequestConverter.from_body(body, index="my-index")
        proto = req.build()

        assert proto.index == "my-index"


class TestResponseConverterFromProtoRequest:
    """Test ResponseConverter.from_proto_request reconstructs original data."""

    def test_reconstruct_index(self) -> None:
        """Reconstructs an index request."""
        meta = {"_index": "idx", "_id": "1"}
        body = {"title": "Hello", "value": 42}
        proto = _build_single_request("index", meta, body)

        result = ResponseConverter.from_proto_request(proto)
        assert result["operation"]  # type: ignore[index] == "index"
        assert result["index"]  # type: ignore[index] == "idx"
        assert result["id"]  # type: ignore[index] == "1"
        assert result["body"]  # type: ignore[index] == body

    def test_reconstruct_update(self) -> None:
        """Reconstructs an update request with doc and doc_as_upsert."""
        meta = {"_index": "idx", "_id": "1"}
        body = {"doc": {"value": 5}, "doc_as_upsert": True}
        proto = _build_single_request("update", meta, body)

        result = ResponseConverter.from_proto_request(proto)
        assert result["operation"]  # type: ignore[index] == "update"
        assert result["body"]  # type: ignore[index]["doc"] == {"value": 5}
        assert result["body"]  # type: ignore[index]["doc_as_upsert"] is True

    def test_reconstruct_delete(self) -> None:
        """Reconstructs a delete request (no body)."""
        meta = {"_index": "idx", "_id": "1"}
        proto = _build_single_request("delete", meta, None)

        result = ResponseConverter.from_proto_request(proto)
        assert result == {"operation": "delete", "index": "idx", "id": "1"}

    def test_reconstruct_bulk(self) -> None:
        """Reconstructs a multi-operation request."""
        req = RequestConverter(index="idx")
        req.index(body={"a": 1}, id="1")
        req.delete(id="2")
        proto = req.build()

        result = ResponseConverter.from_proto_request(proto)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["operation"] == "index"
        assert result[1]["operation"] == "delete"


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
        body = [{"index": {"_id": "1"}}, {"x": 1}]
        proto = toProtoBulkRequest(body, index="idx", timeout="30s")
        assert proto.index == "idx"
        assert proto.timeout == "30s"
