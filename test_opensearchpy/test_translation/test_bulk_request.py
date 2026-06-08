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
test_bulk_request.py — Tests for BulkRequestBuilder and toProtoBulkRequest

Tests the bulk translation layer:
    - BulkRequestBuilder: compose individual operations into one bulk request
    - toProtoBulkRequest: convert raw action/source pairs into protobuf
    - ResponseConverter: verify bulk responses convert back to Python dicts

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_bulk_request.py -v
"""

import os

import grpc
import pytest

from opensearch.protobufs.services.document_service_pb2_grpc import DocumentServiceStub
from opensearch_grpc.translation import (
    BulkRequestBuilder,
    ResponseConverter,
    toProtoBulkRequest,
)


@pytest.fixture(scope="session")
def grpc_host():
    opensearch_url = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
    grpc_port = os.environ.get("OPENSEARCH_GRPC_PORT", "9400")
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    return f"{host}:{grpc_port}"


@pytest.fixture(scope="session")
def index_name():
    return "test-bulk-ci"


@pytest.fixture(scope="session")
def stub(grpc_host):
    channel = grpc.insecure_channel(grpc_host)
    stub = DocumentServiceStub(channel)
    yield stub
    channel.close()


@pytest.fixture(autouse=True, scope="session")
def cleanup(index_name):
    yield
    import urllib.request

    try:
        req = urllib.request.Request(
            f"http://localhost:9200/{index_name}", method="DELETE"
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


class TestBulkRequestBuilder:
    """Tests for BulkRequestBuilder — composing operations into bulk."""

    def test_build_mixed_operations(self, stub, index_name):
        """Build a bulk with index, create, update, delete and send it."""
        bulk = BulkRequestBuilder(index=index_name, refresh="true")
        bulk.index(body={"title": "Doc 1", "value": 1}, id="b1")
        bulk.index(body={"title": "Doc 2", "value": 2}, id="b2")
        bulk.create(body={"title": "Doc 3", "value": 3}, id="b3")

        request = bulk.build()
        response = stub.Bulk(request)

        assert not response.errors
        assert len(response.items) == 3

    def test_bulk_update_and_delete(self, stub, index_name):
        """Update and delete docs created in previous test."""
        bulk = BulkRequestBuilder(index=index_name, refresh="true")
        bulk.update(id="b1", body={"doc": {"value": 100}})
        bulk.delete(id="b2")

        request = bulk.build()
        response = stub.Bulk(request)

        assert not response.errors
        assert len(response.items) == 2

        # Verify update result
        item = response.items[0]
        assert item.HasField("update")
        assert item.update.x_id == "b1"
        assert item.update.result == "updated"

        # Verify delete result
        item = response.items[1]
        assert item.HasField("delete")
        assert item.delete.x_id == "b2"
        assert item.delete.result == "deleted"

    def test_bulk_with_per_operation_index(self, stub, index_name):
        """Override index on individual operations."""
        bulk = BulkRequestBuilder(refresh="true")
        bulk.index(body={"title": "In index A"}, id="x1", index=index_name)
        bulk.index(body={"title": "In index A too"}, id="x2", index=index_name)

        request = bulk.build()
        response = stub.Bulk(request)

        assert not response.errors
        assert len(response.items) == 2

    def test_bulk_builder_len(self):
        """len() returns number of queued operations."""
        bulk = BulkRequestBuilder(index="test")
        assert len(bulk) == 0
        bulk.index(body={"a": 1}, id="1")
        bulk.delete(id="2")
        assert len(bulk) == 2

    def test_bulk_builder_chaining(self):
        """Operations can be chained."""
        bulk = (
            BulkRequestBuilder(index="test")
            .index(body={"a": 1}, id="1")
            .create(body={"b": 2}, id="2")
            .update(id="1", body={"doc": {"a": 10}})
            .delete(id="2")
        )
        assert len(bulk) == 4


class TestToProtoBulkRequest:
    """Tests for toProtoBulkRequest — raw action/source pair conversion."""

    def test_list_of_dicts(self, stub, index_name):
        """Convert a list of action/source dicts and send."""
        body = [
            {"index": {"_index": index_name, "_id": "raw1"}},
            {"title": "Raw doc 1"},
            {"index": {"_index": index_name, "_id": "raw2"}},
            {"title": "Raw doc 2"},
            {"delete": {"_index": index_name, "_id": "raw1"}},
        ]

        request = toProtoBulkRequest(body, refresh="true")
        response = stub.Bulk(request)

        assert len(response.items) == 3

    def test_ndjson_string(self, stub, index_name):
        """Convert an NDJSON string and send."""
        ndjson = (
            f'{{"index": {{"_index": "{index_name}", "_id": "nj1"}}}}\n'
            f'{{"title": "NDJSON doc"}}\n'
        )

        request = toProtoBulkRequest(ndjson, refresh="true")
        response = stub.Bulk(request)

        assert len(response.items) == 1
        assert not response.errors

    def test_with_default_index(self, stub, index_name):
        """Use index parameter as default for all operations."""
        body = [
            {"index": {"_id": "di1"}},
            {"title": "Default index doc"},
        ]

        request = toProtoBulkRequest(body, index=index_name, refresh="true")
        response = stub.Bulk(request)

        assert not response.errors


class TestBulkResponseConverter:
    """Tests for ResponseConverter with bulk responses."""

    def test_convert_bulk_response_first_item(self, stub, index_name):
        """ResponseConverter.from_bulk_response returns first item as dict."""
        bulk = BulkRequestBuilder(index=index_name, refresh="true")
        bulk.index(body={"title": "Converter test"}, id="conv1")

        request = bulk.build()
        response = stub.Bulk(request)

        result = ResponseConverter.from_bulk_response(response)
        assert result["_index"] == index_name
        assert result["_id"] == "conv1"
        assert result["result"] in ("created", "updated")
        assert "_version" in result
        assert "_shards" in result
