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
test_client_operations.py — Integration Tests: Client Document Operations

Tests adding, updating, deleting documents and error handling
via gRPC using the OpenSearchGrpcTestCase framework.
"""

from . import OpenSearchGrpcTestCase


class TestAddDocuments(OpenSearchGrpcTestCase):
    def test_index_single_document(self) -> None:
        """Index a single document via gRPC bulk."""
        body = [
            {"index": {"_index": "test-ops-add", "_id": "1"}},
            {"title": "Single doc", "value": 42},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["index"]["result"], "created")

        doc = self.client.get(index="test-ops-add", id="1")
        self.assertEqual(doc["_source"]["title"], "Single doc")
        self.assertEqual(doc["_source"]["value"], 42)

    def test_index_multiple_documents(self) -> None:
        """Index multiple documents in one bulk call."""
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-ops-multi", "_id": str(i)}})
            body.append({"title": f"Doc {i}"})

        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 5)

        count = self.client.count(index="test-ops-multi")["count"]
        self.assertEqual(count, 5)

    def test_create_document(self) -> None:
        """Create (op_type=create) a document via bulk."""
        body = [
            {"create": {"_index": "test-ops-create", "_id": "1"}},
            {"title": "Created doc"},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["create"]["result"], "created")

    def test_index_without_id(self) -> None:
        """Index a document without specifying _id."""
        body = [
            {"index": {"_index": "test-ops-noid"}},
            {"title": "Auto ID"},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        # Server assigns an ID
        self.assertIn("_id", resp["items"][0]["index"])
        self.assertTrue(len(resp["items"][0]["index"]["_id"]) > 0)


class TestUpdateDocuments(OpenSearchGrpcTestCase):
    def test_update_partial_document(self) -> None:
        """Update a document partially via bulk."""
        # Create
        self.client.bulk(
            body=[
                {"index": {"_index": "test-ops-upd", "_id": "1"}},
                {"title": "Original", "value": 1},
            ],
            refresh=True,
        )

        # Update
        resp = self.client.bulk(
            body=[
                {"update": {"_index": "test-ops-upd", "_id": "1"}},
                {"doc": {"value": 99}},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["update"]["result"], "updated")

        doc = self.client.get(index="test-ops-upd", id="1")
        self.assertEqual(doc["_source"]["value"], 99)
        self.assertEqual(doc["_source"]["title"], "Original")

    def test_update_with_upsert(self) -> None:
        """Update with upsert — creates if not exists."""
        resp = self.client.bulk(
            body=[
                {"update": {"_index": "test-ops-upsert", "_id": "1"}},
                {"doc": {"value": 42}, "doc_as_upsert": True},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])

        doc = self.client.get(index="test-ops-upsert", id="1")
        self.assertEqual(doc["_source"]["value"], 42)


class TestDeleteDocuments(OpenSearchGrpcTestCase):
    def test_delete_existing_document(self) -> None:
        """Delete an existing document via bulk."""
        self.client.bulk(
            body=[
                {"index": {"_index": "test-ops-del", "_id": "1"}},
                {"title": "Delete me"},
            ],
            refresh=True,
        )

        resp = self.client.bulk(
            body=[
                {"delete": {"_index": "test-ops-del", "_id": "1"}},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["delete"]["result"], "deleted")

    def test_delete_nonexistent_document(self) -> None:
        """Delete a nonexistent document — should report not_found or error."""
        resp = self.client.bulk(
            body=[
                {"delete": {"_index": "test-ops-del-missing", "_id": "nonexistent"}},
            ],
            refresh=True,
        )

        # Bulk doesn't raise on individual failures, reports in items
        delete_item = resp["items"][0]["delete"]
        # Server may return result="not_found" or an error with status 404
        if "result" in delete_item:
            self.assertEqual(delete_item["result"], "not_found")
        else:
            self.assertEqual(delete_item["status"], 404)


class TestDocumentCount(OpenSearchGrpcTestCase):
    def test_count_after_operations(self) -> None:
        """Verify count reflects bulk operations."""
        # Add 5
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-ops-cnt", "_id": str(i)}})
            body.append({"x": i})
        self.client.bulk(body=body, refresh=True)

        self.assertEqual(self.client.count(index="test-ops-cnt")["count"], 5)

        # Delete 2
        self.client.bulk(
            body=[
                {"delete": {"_index": "test-ops-cnt", "_id": "0"}},
                {"delete": {"_index": "test-ops-cnt", "_id": "1"}},
            ],
            refresh=True,
        )

        self.client.indices.refresh(index="test-ops-cnt")
        self.assertEqual(self.client.count(index="test-ops-cnt")["count"], 3)


class TestErrorHandling(OpenSearchGrpcTestCase):
    def test_create_duplicate_document(self) -> None:
        """Creating a duplicate doc should report error in bulk response."""
        self.client.bulk(
            body=[
                {"create": {"_index": "test-ops-dup", "_id": "1"}},
                {"title": "First"},
            ],
            refresh=True,
        )

        # Try to create again
        resp = self.client.bulk(
            body=[
                {"create": {"_index": "test-ops-dup", "_id": "1"}},
                {"title": "Duplicate"},
            ],
            refresh=True,
        )

        self.assertTrue(resp["errors"])
        self.assertEqual(resp["items"][0]["create"]["status"], 409)
