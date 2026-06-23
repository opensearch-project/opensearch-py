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
test_client_operations.py — Integration Tests: Client Document Operations

Simulates a real client sending documents to OpenSearch via gRPC using
the standard OpenSearch client with GrpcTransport.

Tests:
    - Adding documents (index, create, bulk)
    - Updating documents
    - Deleting documents
    - Document count verification (via REST)
    - Error handling (create existing doc, delete missing doc)
    - Mixed operations in one bulk call

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_client_operations.py -v -s
"""

import os

import pytest

from opensearch_grpc.grpc_transport import GrpcTransport
from opensearchpy import OpenSearch


@pytest.fixture(scope="session")
def index_name():
    return "test-client-ops"


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


class TestAddDocuments:
    """Test adding documents as a client."""

    def test_index_single_document(self, client, index_name):
        """Client sends one document, gets response with _id and result."""
        print("\n[TEST] Indexing single document: {title: 'First Document', value: 1}")
        resp = client.index(
            index=index_name,
            body={"title": "First Document", "value": 1},
            id="doc-1",
            refresh=True,
        )
        print(f"[TEST] Response: {resp}")

        assert resp["_index"] == index_name
        assert resp["_id"] == "doc-1"
        assert resp["result"] == "created"
        print("[TEST] ✅ Document doc-1 created successfully")

        # Verify via REST get
        doc = client.get(index=index_name, id="doc-1")
        assert doc["_source"]["title"] == "First Document"
        print(f"[TEST] ✅ Verified via get: {doc['_source']}")

    def test_index_multiple_documents(self, client, index_name):
        """Client sends multiple documents in one bulk call."""
        print("\n[TEST] Indexing 3 documents in one bulk")
        body = [
            {"index": {"_index": index_name, "_id": "doc-2"}},
            {"title": "Doc 2", "value": 2},
            {"index": {"_index": index_name, "_id": "doc-3"}},
            {"title": "Doc 3", "value": 3},
            {"index": {"_index": index_name, "_id": "doc-4"}},
            {"title": "Doc 4", "value": 4},
        ]
        resp = client.bulk(body=body, refresh=True)
        print(f"[TEST] Got {len(resp['items'])} responses")

        assert resp["errors"] is False
        assert len(resp["items"]) == 3
        for item in resp["items"]:
            assert item["index"]["result"] == "created"
        print("[TEST] ✅ All 3 documents created")

    def test_create_document(self, client, index_name):
        """Client creates a document (fails if already exists)."""
        print("\n[TEST] Creating document doc-5 (will fail if exists)")
        resp = client.create(
            index=index_name,
            body={"title": "Created Doc", "value": 5},
            id="doc-5",
            refresh=True,
        )
        print(f"[TEST] Response: {resp}")

        assert resp["_id"] == "doc-5"
        assert resp["result"] == "created"
        print("[TEST] ✅ Document doc-5 created")

    def test_index_without_id(self, client, index_name):
        """Client indexes without specifying an ID — server generates one."""
        print("\n[TEST] Indexing document without ID (server will auto-generate)")
        resp = client.index(
            index=index_name, body={"title": "Auto ID Doc", "value": 99}, refresh=True
        )
        print(f"[TEST] Auto-generated ID: {resp['_id']}")

        assert resp["_id"] is not None
        assert resp["result"] == "created"
        print("[TEST] ✅ Document created with auto-generated ID")


class TestUpdateDocuments:
    """Test updating documents as a client."""

    def test_update_partial_document(self, client, index_name):
        """Client updates one field of an existing document."""
        print("\n[TEST] Updating doc-1: setting value=100")
        resp = client.update(
            index=index_name, id="doc-1", body={"doc": {"value": 100}}, refresh=True
        )
        print(f"[TEST] Response: {resp}")

        assert resp["_id"] == "doc-1"
        assert resp["result"] == "updated"

        # Verify the update
        doc = client.get(index=index_name, id="doc-1")
        assert doc["_source"]["value"] == 100
        assert doc["_source"]["title"] == "First Document"
        print(
            f"[TEST] ✅ Updated doc-1: value={doc['_source']['value']}, title unchanged"
        )

    def test_update_with_upsert(self, client, index_name):
        """Client upserts — creates doc if it doesn't exist."""
        print("\n[TEST] Upserting doc-upsert (creates if missing)")
        resp = client.update(
            index=index_name,
            id="doc-upsert",
            body={"doc": {"title": "Upserted", "value": 50}, "doc_as_upsert": True},
            refresh=True,
        )
        print(f"[TEST] Response: {resp}")

        assert resp["result"] in ("created", "updated")

        doc = client.get(index=index_name, id="doc-upsert")
        assert doc["_source"]["title"] == "Upserted"
        print(f"[TEST] ✅ Upserted doc-upsert: result={resp['result']}")


class TestDeleteDocuments:
    """Test deleting documents as a client."""

    def test_delete_existing_document(self, client, index_name):
        """Client deletes a document that exists."""
        print("\n[TEST] Creating doc-del, then deleting it")
        client.index(
            index=index_name, body={"title": "To Delete"}, id="doc-del", refresh=True
        )

        resp = client.delete(index=index_name, id="doc-del", refresh=True)
        print(f"[TEST] Delete response: {resp}")

        assert resp["_id"] == "doc-del"
        assert resp["result"] == "deleted"
        print("[TEST] ✅ Document doc-del deleted")

    def test_delete_nonexistent_document(self, client, index_name):
        """Client tries to delete a doc that doesn't exist — gets NotFoundError."""
        print("\n[TEST] Deleting non-existent document 'does-not-exist'")
        from opensearchpy.exceptions import NotFoundError

        with pytest.raises(NotFoundError):
            client.delete(index=index_name, id="does-not-exist", refresh=True)
        print("[TEST] ✅ Got expected NotFoundError")


class TestDocumentCount:
    """Test that the server reflects the correct document count."""

    def test_count_after_operations(self, client, index_name):
        """Verify the document count matches what we indexed."""
        resp = client.count(index=index_name)
        count = resp["count"]
        print(f"\n[TEST] Document count in '{index_name}': {count}")
        assert count >= 7, f"Expected at least 7 docs, got {count}"
        print(f"[TEST] ✅ Count is {count} (expected >= 7)")


class TestErrorHandling:
    """Test that the client gets proper error responses."""

    def test_create_duplicate_document(self, client, index_name):
        """Creating a doc that already exists raises ConflictError."""
        print(
            "\n[TEST] Attempting to create doc-1 again (should fail — already exists)"
        )
        from opensearchpy.exceptions import ConflictError

        with pytest.raises(ConflictError):
            client.create(
                index=index_name,
                body={"title": "Duplicate"},
                id="doc-1",
                refresh=True,
            )
        print("[TEST] ✅ Got expected ConflictError for duplicate create")


class TestMixedBatch:
    """Test sending a mix of operations in one batch (like a real client)."""

    def test_mixed_operations_batch(self, client, index_name):
        """Client sends index + update + delete in one bulk call."""
        print("\n[TEST] Sending mixed batch: index + update + delete")
        body = [
            {"index": {"_index": index_name, "_id": "batch-1"}},
            {"title": "Batch New"},
            {"update": {"_index": index_name, "_id": "doc-1"}},
            {"doc": {"batch": True}},
            {"delete": {"_index": index_name, "_id": "doc-5"}},
        ]
        resp = client.bulk(body=body, refresh=True)
        print(f"[TEST] Got {len(resp['items'])} responses:")
        for r in resp["items"]:
            print(f"[TEST]   {r}")

        assert len(resp["items"]) == 3
        assert resp["items"][0]["index"]["result"] == "created"
        assert resp["items"][1]["update"]["result"] == "updated"
        assert resp["items"][2]["delete"]["result"] == "deleted"
        print("[TEST] ✅ Mixed batch: index=created, update=updated, delete=deleted")
