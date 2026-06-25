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
test_bulk_large_upload.py — Large Bulk Upload Integration Test

Simulates a real Python client uploading 10+ documents over gRPC
and verifying the response matches what the client expects.

Requires OpenSearch running with gRPC on port 9400.
Skips automatically if server is not available.

Run:
    pytest test_opensearchpy/test_translation/test_bulk_large_upload.py -v -s
"""

import os
import time

import grpc
import pytest

from opensearchpy import OpenSearchGrpc

# Skip if gRPC server not available
_grpc_port = os.environ.get("OPENSEARCH_GRPC_PORT", "9400")
try:
    _channel = grpc.insecure_channel(f"localhost:{_grpc_port}")
    grpc.channel_ready_future(_channel).result(timeout=2)
    _channel.close()
except Exception:
    pytest.skip("gRPC server not available", allow_module_level=True)


@pytest.fixture(scope="module")
def client():
    opensearch_url = os.environ.get("OPENSEARCH_URL", "http://localhost:9200")
    grpc_port = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    port = int(opensearch_url.split(":")[-1])

    c = OpenSearchGrpc(
        hosts=[{"host": host, "port": port}],
        grpc_hosts=[{"host": host, "port": grpc_port}],
        use_ssl=False,
    )
    yield c
    c.close()


@pytest.fixture(scope="module")
def index_name():
    return "test-bulk-large-upload"


@pytest.fixture(autouse=True, scope="module")
def cleanup(client, index_name):
    client.indices.delete(index=index_name, ignore=[404])
    yield
    client.indices.delete(index=index_name, ignore=[404])


class TestLargeBulkUpload:
    """Simulate a real client uploading 10K+ documents over gRPC."""

    def test_upload_documents(self, client, index_name):
        """
        Client uploads 10 documents in one bulk request.
        Verifies all documents are indexed and response format is correct.
        """
        print("\n[TEST] Uploading 10 documents via gRPC bulk...")

        # Build bulk body exactly like a Python client would
        body = []
        for i in range(10):
            body.append({"index": {"_index": index_name, "_id": str(i)}})
            body.append({
                "title": f"Document {i}",
                "category": f"category-{i % 10}",
                "value": i,
                "timestamp": "2024-01-01T00:00:00Z",
                "tags": ["bulk", "grpc", f"batch-{i // 1000}"],
            })

        start = time.time()
        resp = client.bulk(body=body, refresh=True)
        elapsed = time.time() - start

        print(f"[TEST] Upload complete: {elapsed:.2f}s ({10 / elapsed:.0f} docs/sec)")

        # Verify response format matches what Python client expects
        assert "took" in resp, "Response missing 'took'"
        assert "errors" in resp, "Response missing 'errors'"
        assert "items" in resp, "Response missing 'items'"
        assert resp["errors"] is False, f"Bulk had errors: {resp['errors']}"
        assert len(resp["items"]) == 10, f"Expected 10 items, got {len(resp['items'])}"

        print(f"[TEST] Response: took={resp['took']}ms, errors={resp['errors']}, items={len(resp['items'])}")

        # Verify individual item response format
        first_item = resp["items"][0]
        assert "index" in first_item, "Item missing operation type"
        item = first_item["index"]
        assert "_index" in item, "Item missing _index"
        assert "_id" in item, "Item missing _id"
        assert "result" in item, "Item missing result"
        assert "status" in item, "Item missing status"
        assert "_version" in item, "Item missing _version"
        assert "_shards" in item, "Item missing _shards"

        assert item["_index"] == index_name
        assert item["result"] == "created"
        assert item["status"] == 201
        assert item["_shards"]["successful"] >= 1

        print(f"[TEST] Sample item: {first_item}")
        # Explicit refresh to ensure docs are visible via REST
        client.indices.refresh(index=index_name)
        print(f"[TEST] ✅ 10 documents uploaded successfully via gRPC")

    def test_verify_document_count(self, client, index_name):
        """Verify all 10 documents are searchable."""
        print("\n[TEST] Verifying document count...")
        client.indices.refresh(index=index_name)
        resp = client.count(index=index_name)
        count = resp["count"]
        print(f"[TEST] Document count: {count}")
        assert count == 10, f"Expected 10, got {count}"
        print("[TEST] ✅ All 10 documents confirmed in index")

    def test_search_uploaded_documents(self, client, index_name):
        """Search the uploaded documents to verify content is correct."""
        print("\n[TEST] Searching uploaded documents...")
        client.indices.refresh(index=index_name)
        resp = client.search(
            index=index_name,
            body={
                "query": {"term": {"category.keyword": "category-5"}},
                "size": 5,
            },
        )
        hits = resp["hits"]["total"]["value"]
        print(f"[TEST] Search for category-5: {hits} hits")
        assert hits == 1, f"Expected 1 doc in category-5, got {hits}"

        # Verify document content
        doc = resp["hits"]["hits"][0]["_source"]
        assert "title" in doc
        assert "category" in doc
        assert doc["category"] == "category-5"
        print(f"[TEST] Sample doc: {doc}")
        print("[TEST] ✅ Documents searchable with correct content")

    def test_bulk_update_batch(self, client, index_name):
        """Client updates a batch of existing documents."""
        print("\n[TEST] Updating 5 documents via gRPC bulk...")

        body = []
        for i in range(5):
            body.append({"update": {"_index": index_name, "_id": str(i)}})
            body.append({"doc": {"value": i * 100, "updated": True}})

        start = time.time()
        resp = client.bulk(body=body, refresh=True)
        elapsed = time.time() - start

        print(f"[TEST] Update complete: {elapsed:.2f}s")
        assert resp["errors"] is False
        assert len(resp["items"]) == 5

        # Verify update response format
        first_item = resp["items"][0]
        assert "update" in first_item
        assert first_item["update"]["result"] == "updated"
        assert first_item["update"]["status"] == 200

        # Verify via GET
        doc = client.get(index=index_name, id="0")
        assert doc["_source"]["value"] == 0  # 0 * 100
        assert doc["_source"]["updated"] is True
        print("[TEST] ✅ 5 documents updated successfully")

    def test_bulk_delete_batch(self, client, index_name):
        """Client deletes a batch of documents."""
        print("\n[TEST] Deleting 2 documents via gRPC bulk...")

        body = []
        for i in range(8, 10):
            body.append({"delete": {"_index": index_name, "_id": str(i)}})

        start = time.time()
        resp = client.bulk(body=body, refresh=True)
        elapsed = time.time() - start

        print(f"[TEST] Delete complete: {elapsed:.2f}s")
        assert resp["errors"] is False
        assert len(resp["items"]) == 2

        # Verify delete response format
        first_item = resp["items"][0]
        assert "delete" in first_item
        assert first_item["delete"]["result"] == "deleted"
        assert first_item["delete"]["status"] == 200

        # Verify count decreased
        client.indices.refresh(index=index_name)
        count = client.count(index=index_name)["count"]
        assert count == 8, f"Expected 8 after delete, got {count}"
        print(f"[TEST] ✅ 2 documents deleted, {count} remaining")

    def test_bulk_mixed_operations(self, client, index_name):
        """Client sends mixed operations (index + update + delete) in one bulk."""
        print("\n[TEST] Mixed bulk: 2 index + 2 update + 2 delete...")

        body = []
        # 100 new docs
        for i in range(20, 22):
            body.append({"index": {"_index": index_name, "_id": str(i)}})
            body.append({"title": f"New doc {i}", "value": i})
        # 100 updates
        for i in range(1, 3):
            body.append({"update": {"_index": index_name, "_id": str(i)}})
            body.append({"doc": {"mixed_batch": True}})
        # 100 deletes
        for i in range(6, 8):
            body.append({"delete": {"_index": index_name, "_id": str(i)}})

        start = time.time()
        resp = client.bulk(body=body, refresh=True)
        elapsed = time.time() - start

        print(f"[TEST] Mixed bulk complete: {elapsed:.2f}s, {len(resp['items'])} items")
        assert resp["errors"] is False
        assert len(resp["items"]) == 6

        # Verify each operation type in response
        index_items = [i for i in resp["items"] if "index" in i]
        update_items = [i for i in resp["items"] if "update" in i]
        delete_items = [i for i in resp["items"] if "delete" in i]

        assert len(index_items) == 2
        assert len(update_items) == 2
        assert len(delete_items) == 2

        assert all(i["index"]["result"] == "created" for i in index_items)
        assert all(i["update"]["result"] == "updated" for i in update_items)
        assert all(i["delete"]["result"] == "deleted" for i in delete_items)

        print("[TEST] ✅ Mixed batch: 2 created, 2 updated, 2 deleted")
