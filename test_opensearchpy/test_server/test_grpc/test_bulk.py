# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
test_bulk.py — gRPC Bulk Integration Tests

Tests bulk operations routed over gRPC using the standard OpenSearch client
with grpc=True. Validates response format, mixed operations, and error handling.
"""

from . import OpenSearchGrpcTestCase


class TestBulkIndex(OpenSearchGrpcTestCase):
    def test_bulk_index_documents(self) -> None:
        """Bulk index multiple documents over gRPC."""
        body = []
        for i in range(10):
            body.append({"index": {"_index": "test-grpc-bulk", "_id": str(i)}})
            body.append({"title": f"Document {i}", "value": i})

        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 10)
        self.assertIn("took", resp)

        # Verify response item format
        item = resp["items"][0]["index"]
        self.assertEqual(item["_index"], "test-grpc-bulk")
        self.assertEqual(item["_id"], "0")
        self.assertEqual(item["result"], "created")
        self.assertEqual(item["status"], 201)
        self.assertIn("_version", item)
        self.assertIn("_shards", item)
        self.assertGreaterEqual(item["_shards"]["successful"], 1)

    def test_bulk_with_refresh(self) -> None:
        """Verify refresh=True makes docs immediately searchable."""
        body = [
            {"index": {"_index": "test-grpc-refresh", "_id": "1"}},
            {"title": "Refreshed doc"},
        ]
        self.client.bulk(body=body, refresh=True)

        count = self.client.count(index="test-grpc-refresh")
        self.assertEqual(count["count"], 1)

    def test_bulk_index_param(self) -> None:
        """Bulk with index specified at request level, not per-action."""
        body = [
            {"index": {"_id": "1"}},
            {"title": "Doc 1"},
            {"index": {"_id": "2"}},
            {"title": "Doc 2"},
        ]
        resp = self.client.bulk(body=body, index="test-grpc-idx-param", refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 2)
        self.assertEqual(resp["items"][0]["index"]["_index"], "test-grpc-idx-param")


class TestBulkUpdate(OpenSearchGrpcTestCase):
    def test_bulk_update_documents(self) -> None:
        """Bulk update existing documents over gRPC."""
        # Create docs first
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-grpc-update", "_id": str(i)}})
            body.append({"title": f"Original {i}", "value": i})
        self.client.bulk(body=body, refresh=True)

        # Update them
        update_body = []
        for i in range(5):
            update_body.append({"update": {"_index": "test-grpc-update", "_id": str(i)}})
            update_body.append({"doc": {"value": i * 100, "updated": True}})

        resp = self.client.bulk(body=update_body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 5)
        self.assertEqual(resp["items"][0]["update"]["result"], "updated")
        self.assertEqual(resp["items"][0]["update"]["status"], 200)

        # Verify via GET
        doc = self.client.get(index="test-grpc-update", id="0")
        self.assertEqual(doc["_source"]["value"], 0)
        self.assertTrue(doc["_source"]["updated"])


class TestBulkDelete(OpenSearchGrpcTestCase):
    def test_bulk_delete_documents(self) -> None:
        """Bulk delete documents over gRPC."""
        # Create docs
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-grpc-delete", "_id": str(i)}})
            body.append({"title": f"Delete me {i}"})
        self.client.bulk(body=body, refresh=True)

        # Delete them
        delete_body = []
        for i in range(5):
            delete_body.append({"delete": {"_index": "test-grpc-delete", "_id": str(i)}})

        resp = self.client.bulk(body=delete_body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 5)
        self.assertEqual(resp["items"][0]["delete"]["result"], "deleted")
        self.assertEqual(resp["items"][0]["delete"]["status"], 200)

        # Verify count is 0
        count = self.client.count(index="test-grpc-delete")
        self.assertEqual(count["count"], 0)


class TestBulkMixed(OpenSearchGrpcTestCase):
    def test_mixed_operations(self) -> None:
        """Index + update + delete in one bulk call."""
        # Seed data
        seed = [
            {"index": {"_index": "test-grpc-mixed", "_id": "existing"}},
            {"title": "Existing doc", "value": 1},
            {"index": {"_index": "test-grpc-mixed", "_id": "to-delete"}},
            {"title": "Will be deleted"},
        ]
        self.client.bulk(body=seed, refresh=True)

        # Mixed batch
        body = [
            # Index new doc
            {"index": {"_index": "test-grpc-mixed", "_id": "new"}},
            {"title": "New doc"},
            # Update existing
            {"update": {"_index": "test-grpc-mixed", "_id": "existing"}},
            {"doc": {"value": 99}},
            # Delete
            {"delete": {"_index": "test-grpc-mixed", "_id": "to-delete"}},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 3)

        # Verify each operation type
        index_items = [i for i in resp["items"] if "index" in i]
        update_items = [i for i in resp["items"] if "update" in i]
        delete_items = [i for i in resp["items"] if "delete" in i]

        self.assertEqual(len(index_items), 1)
        self.assertEqual(len(update_items), 1)
        self.assertEqual(len(delete_items), 1)

        self.assertEqual(index_items[0]["index"]["result"], "created")
        self.assertEqual(update_items[0]["update"]["result"], "updated")
        self.assertEqual(delete_items[0]["delete"]["result"], "deleted")

        # Final state: 2 docs (existing + new), to-delete gone
        count = self.client.count(index="test-grpc-mixed")
        self.assertEqual(count["count"], 2)
