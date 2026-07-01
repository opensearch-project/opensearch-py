# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

# mypy: ignore-errors
"""
test_bulk_large_upload.py — Bulk Upload Integration Test

Tests bulk upload, update, delete, and mixed operations over gRPC.
"""

from . import OpenSearchGrpcTestCase


class TestBulkUpload(OpenSearchGrpcTestCase):
    def test_upload_documents(self) -> None:
        """Upload 10 documents via gRPC bulk and verify response format."""
        body = []
        for i in range(10):
            body.append({"index": {"_index": "test-bulk-upload", "_id": str(i)}})
            body.append(
                {
                    "title": f"Document {i}",
                    "category": f"category-{i % 10}",
                    "value": i,
                    "tags": ["bulk", "grpc"],
                }
            )

        resp = self.client.bulk(body=body, refresh=True)

        self.assertIn("took", resp)
        self.assertIn("errors", resp)
        self.assertIn("items", resp)
        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 10)

        # Verify item format
        item = resp["items"][0]["index"]
        self.assertEqual(item["_index"], "test-bulk-upload")
        self.assertEqual(item["_id"], "0")
        self.assertEqual(item["result"], "created")
        self.assertEqual(item["status"], 201)
        self.assertIn("_version", item)
        self.assertIn("_shards", item)
        self.assertGreaterEqual(item["_shards"]["successful"], 1)

    def test_verify_document_count(self) -> None:
        """Verify uploaded documents are searchable via REST."""
        body = []
        for i in range(10):
            body.append({"index": {"_index": "test-bulk-count", "_id": str(i)}})
            body.append({"title": f"Document {i}"})

        self.client.bulk(body=body, refresh=True)
        self.client.indices.refresh(index="test-bulk-count")

        count = self.client.count(index="test-bulk-count")["count"]
        self.assertEqual(count, 10)

    def test_search_uploaded_documents(self) -> None:
        """Search documents uploaded via gRPC."""
        body = []
        for i in range(10):
            body.append({"index": {"_index": "test-bulk-search", "_id": str(i)}})
            body.append({"title": f"Document {i}", "category": f"category-{i % 5}"})

        self.client.bulk(body=body, refresh=True)
        self.client.indices.refresh(index="test-bulk-search")

        resp = self.client.search(
            index="test-bulk-search",
            body={"query": {"term": {"category.keyword": "category-0"}}},
        )
        self.assertEqual(resp["hits"]["total"]["value"], 2)

    def test_bulk_update_batch(self) -> None:
        """Update documents via gRPC bulk."""
        # Create docs
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-bulk-update", "_id": str(i)}})
            body.append({"title": f"Original {i}", "value": i})
        self.client.bulk(body=body, refresh=True)

        # Update them
        update_body = []
        for i in range(5):
            update_body.append(
                {"update": {"_index": "test-bulk-update", "_id": str(i)}}
            )
            update_body.append({"doc": {"value": i * 100, "updated": True}})

        resp = self.client.bulk(body=update_body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 5)
        self.assertEqual(resp["items"][0]["update"]["result"], "updated")
        self.assertEqual(resp["items"][0]["update"]["status"], 200)

        # Verify via GET
        doc = self.client.get(index="test-bulk-update", id="0")
        self.assertEqual(doc["_source"]["value"], 0)
        self.assertTrue(doc["_source"]["updated"])

    def test_bulk_delete_batch(self) -> None:
        """Delete documents via gRPC bulk."""
        # Create docs
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-bulk-del", "_id": str(i)}})
            body.append({"title": f"Delete me {i}"})
        self.client.bulk(body=body, refresh=True)

        # Delete 2
        delete_body = [
            {"delete": {"_index": "test-bulk-del", "_id": "3"}},
            {"delete": {"_index": "test-bulk-del", "_id": "4"}},
        ]
        resp = self.client.bulk(body=delete_body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 2)
        self.assertEqual(resp["items"][0]["delete"]["result"], "deleted")
        self.assertEqual(resp["items"][0]["delete"]["status"], 200)

        self.client.indices.refresh(index="test-bulk-del")
        count = self.client.count(index="test-bulk-del")["count"]
        self.assertEqual(count, 3)

    def test_bulk_mixed_operations(self) -> None:
        """Index + update + delete in one bulk call."""
        # Seed data
        seed = [
            {"index": {"_index": "test-bulk-mixed", "_id": "existing"}},
            {"title": "Existing", "value": 1},
            {"index": {"_index": "test-bulk-mixed", "_id": "to-delete"}},
            {"title": "Will delete"},
        ]
        self.client.bulk(body=seed, refresh=True)

        # Mixed batch
        body = [
            {"index": {"_index": "test-bulk-mixed", "_id": "new"}},
            {"title": "New doc"},
            {"update": {"_index": "test-bulk-mixed", "_id": "existing"}},
            {"doc": {"value": 99}},
            {"delete": {"_index": "test-bulk-mixed", "_id": "to-delete"}},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 3)

        index_items = [i for i in resp["items"] if "index" in i]
        update_items = [i for i in resp["items"] if "update" in i]
        delete_items = [i for i in resp["items"] if "delete" in i]

        self.assertEqual(len(index_items), 1)
        self.assertEqual(len(update_items), 1)
        self.assertEqual(len(delete_items), 1)

        self.assertEqual(index_items[0]["index"]["result"], "created")
        self.assertEqual(update_items[0]["update"]["result"], "updated")
        self.assertEqual(delete_items[0]["delete"]["result"], "deleted")
