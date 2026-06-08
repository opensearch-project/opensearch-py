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
test_simpledoc_ci.py — General gRPC Integration Tests

Tests all gRPC functionality: conversion, transport, and round-trip.
Can be used to verify any part of the gRPC pipeline works correctly.

Covers:
    - RequestConverter: Python dict → protobuf conversion
    - ResponseConverter: protobuf → Python dict conversion
    - GrpcTransport: drop-in transport with standard OpenSearch client
    - Round-trip data integrity

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_simpledoc_ci.py -v
"""

import os

import pytest

from opensearch_grpc.grpc_transport import GrpcTransport
from opensearch_grpc.translation import (
    RequestConverter,
    ResponseConverter,
    _build_single_request,
)
from opensearchpy import OpenSearch

# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def index_name():
    return "test-grpc-integration"


@pytest.fixture(scope="session")
def client():
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


@pytest.fixture(autouse=True, scope="session")
def cleanup(client, index_name):
    client.indices.delete(index=index_name, ignore=[404])
    yield
    client.indices.delete(index=index_name, ignore=[404])


# ─── Test: RequestConverter (Python dict → Protobuf) ──────────────────────────


class TestRequestConversion:
    """Test that Python dicts are correctly converted to protobuf."""

    def test_single_index_conversion(self, index_name):
        req = RequestConverter(index=index_name, refresh="true")
        req.index(body={"title": "Test"}, id="1")
        proto = req.build()

        assert len(proto.bulk_request_body) == 1
        assert proto.index == index_name
        op = proto.bulk_request_body[0].operation_container
        assert op.HasField("index")
        assert op.index.x_id == "1"

    def test_bulk_conversion(self, index_name):
        req = RequestConverter(index=index_name)
        req.index(body={"a": 1}, id="1")
        req.create(body={"b": 2}, id="2")
        req.update(id="1", body={"doc": {"a": 10}})
        req.delete(id="2")
        proto = req.build()

        assert len(proto.bulk_request_body) == 4

    def test_from_body_list(self, index_name):
        body = [
            {"index": {"_index": index_name, "_id": "1"}},
            {"title": "Doc"},
        ]
        req = RequestConverter.from_body(body)
        proto = req.build()

        assert len(proto.bulk_request_body) == 1

    def test_from_body_ndjson(self, index_name):
        ndjson = (
            f'{{"index": {{"_index": "{index_name}", "_id": "1"}}}}\n'
            f'{{"title": "Doc"}}\n'
        )
        req = RequestConverter.from_body(ndjson)
        proto = req.build()

        assert len(proto.bulk_request_body) == 1


# ─── Test: ResponseConverter (Protobuf → Python dict) ─────────────────────────


class TestResponseConversion:
    """Test that protobuf responses/requests are correctly converted back."""

    def test_reconstruct_index_request(self, index_name):
        meta = {"_index": index_name, "_id": "1"}
        body = {"title": "Hello", "price": 9.99}
        proto = _build_single_request("index", meta, body)

        result = ResponseConverter.from_proto_request(proto)
        assert result["operation"] == "index"
        assert result["index"] == index_name
        assert result["id"] == "1"
        assert result["body"] == body

    def test_reconstruct_update_request(self, index_name):
        meta = {"_index": index_name, "_id": "1"}
        body = {"doc": {"price": 5.0}, "doc_as_upsert": True}
        proto = _build_single_request("update", meta, body)

        result = ResponseConverter.from_proto_request(proto)
        assert result["operation"] == "update"
        assert result["body"]["doc"] == {"price": 5.0}
        assert result["body"]["doc_as_upsert"] is True

    def test_reconstruct_delete_request(self, index_name):
        meta = {"_index": index_name, "_id": "1"}
        proto = _build_single_request("delete", meta, None)

        result = ResponseConverter.from_proto_request(proto)
        assert result == {"operation": "delete", "index": index_name, "id": "1"}

    def test_reconstruct_bulk_request(self, index_name):
        req = RequestConverter(index=index_name)
        req.index(body={"a": 1}, id="1")
        req.delete(id="2")
        proto = req.build()

        result = ResponseConverter.from_proto_request(proto)
        assert len(result) == 2
        assert result[0]["operation"] == "index"
        assert result[1]["operation"] == "delete"


# ─── Test: GrpcTransport (Drop-in with Standard Client) ──────────────────────


class TestGrpcTransport:
    """Test GrpcTransport as drop-in replacement for standard client."""

    def test_bulk_via_grpc(self, client, index_name):
        body = [
            {"index": {"_index": index_name, "_id": "t1"}},
            {"title": "Transport doc"},
        ]
        resp = client.bulk(body=body, refresh=True)

        assert resp["errors"] is False
        assert len(resp["items"]) == 1

    def test_index_via_grpc(self, client, index_name):
        resp = client.index(
            index=index_name, body={"title": "Single"}, id="t2", refresh=True
        )

        assert resp["result"] in ("created", "updated")

    def test_create_via_grpc(self, client, index_name):
        resp = client.create(
            index=index_name, body={"title": "Created"}, id="t3", refresh=True
        )

        assert resp["result"] == "created"

    def test_update_via_grpc(self, client, index_name):
        resp = client.update(
            index=index_name, id="t2", body={"doc": {"value": 99}}, refresh=True
        )

        assert resp["result"] == "updated"

    def test_delete_via_grpc(self, client, index_name):
        resp = client.delete(index=index_name, id="t3", refresh=True)

        assert resp["result"] == "deleted"

    def test_search_via_rest(self, client, index_name):
        client.indices.refresh(index=index_name)
        resp = client.search(index=index_name, body={"query": {"match_all": {}}})

        assert resp["hits"]["total"]["value"] >= 1

    def test_count_via_rest(self, client, index_name):
        resp = client.count(index=index_name)

        assert resp["count"] >= 1
