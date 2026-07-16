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
test_bulk.py — gRPC Bulk Integration Tests

Tests bulk operations routed over gRPC. Validates correctness of index,
create, update, delete, mixed operations, response format, status codes,
input formats, and request-level parameters.
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

    def test_bulk_create_operation(self) -> None:
        """Create operation produces correct response fields."""
        resp = self.client.bulk(
            body=[
                {"create": {"_index": "test-grpc-create", "_id": "1"}},
                {"title": "Created doc"},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["create"]["result"], "created")
        self.assertEqual(resp["items"][0]["create"]["status"], 201)

    def test_bulk_from_ndjson_string(self) -> None:
        """NDJSON string input produces correct server response."""
        ndjson = (
            '{"index": {"_index": "test-grpc-ndjson", "_id": "1"}}\n'
            '{"title": "From NDJSON"}\n'
        )
        resp = self.client.bulk(body=ndjson, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 1)
        self.assertEqual(resp["items"][0]["index"]["result"], "created")

    def test_bulk_with_routing(self) -> None:
        """Bulk with routing parameter."""
        body = [
            {
                "index": {
                    "_index": "test-grpc-route",
                    "_id": "1",
                    "routing": "shard-1",
                }
            },
            {"title": "Routed doc"},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["index"]["result"], "created")


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
            update_body.append(
                {"update": {"_index": "test-grpc-update", "_id": str(i)}}
            )
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
            delete_body.append(
                {"delete": {"_index": "test-grpc-delete", "_id": str(i)}}
            )

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
            {"index": {"_index": "test-grpc-mixed", "_id": "new"}},
            {"title": "New doc"},
            {"update": {"_index": "test-grpc-mixed", "_id": "existing"}},
            {"doc": {"value": 99}},
            {"delete": {"_index": "test-grpc-mixed", "_id": "to-delete"}},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 3)

        # Verify each operation type
        self.assertIn("index", resp["items"][0])
        self.assertIn("update", resp["items"][1])
        self.assertIn("delete", resp["items"][2])

        self.assertEqual(resp["items"][0]["index"]["result"], "created")
        self.assertEqual(resp["items"][1]["update"]["result"], "updated")
        self.assertEqual(resp["items"][2]["delete"]["result"], "deleted")

        # Final state: 2 docs (existing + new), to-delete gone
        count = self.client.count(index="test-grpc-mixed")
        self.assertEqual(count["count"], 2)


class TestBulkResponseFormat(OpenSearchGrpcTestCase):
    """Test that responses match the expected Python client format."""

    def test_response_has_took(self) -> None:
        """Response contains 'took' field (milliseconds)."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-resp-took", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        self.assertIn("took", resp)
        self.assertIsInstance(resp["took"], int)
        self.assertGreaterEqual(resp["took"], 0)

    def test_response_has_errors_boolean(self) -> None:
        """Response contains 'errors' boolean."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-resp-errors", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        self.assertIn("errors", resp)
        self.assertIsInstance(resp["errors"], bool)

    def test_response_item_has_shards(self) -> None:
        """Response items contain _shards with total/successful/failed."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-resp-shards", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        item = resp["items"][0]["index"]
        self.assertIn("_shards", item)
        self.assertIn("total", item["_shards"])
        self.assertIn("successful", item["_shards"])
        self.assertIn("failed", item["_shards"])
        self.assertGreaterEqual(item["_shards"]["successful"], 1)

    def test_response_item_has_version(self) -> None:
        """Response items contain _version field."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-resp-version", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        item = resp["items"][0]["index"]
        self.assertIn("_version", item)
        self.assertEqual(item["_version"], 1)

    def test_response_item_has_seq_no(self) -> None:
        """Response items contain _seq_no and _primary_term."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-resp-seq", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        item = resp["items"][0]["index"]
        self.assertIn("_seq_no", item)
        self.assertIn("_primary_term", item)
        self.assertGreaterEqual(item["_seq_no"], 0)
        self.assertGreaterEqual(item["_primary_term"], 1)


class TestBulkStatusCodes(OpenSearchGrpcTestCase):
    """Test that gRPC status codes map correctly to REST status codes."""

    def test_created_returns_201(self) -> None:
        """Index/create new document returns status 201."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-status-create", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        self.assertEqual(resp["items"][0]["index"]["status"], 201)

    def test_updated_returns_200(self) -> None:
        """Update existing document returns status 200."""
        self.client.bulk(
            body=[
                {"index": {"_index": "test-status-update", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        resp = self.client.bulk(
            body=[
                {"update": {"_index": "test-status-update", "_id": "1"}},
                {"doc": {"x": 2}},
            ],
            refresh=True,
        )
        self.assertEqual(resp["items"][0]["update"]["status"], 200)

    def test_deleted_returns_200(self) -> None:
        """Delete existing document returns status 200."""
        self.client.bulk(
            body=[
                {"index": {"_index": "test-status-delete", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        resp = self.client.bulk(
            body=[
                {"delete": {"_index": "test-status-delete", "_id": "1"}},
            ],
            refresh=True,
        )
        self.assertEqual(resp["items"][0]["delete"]["status"], 200)

    def test_conflict_returns_409(self) -> None:
        """Create duplicate document returns status 409."""
        self.client.bulk(
            body=[
                {"create": {"_index": "test-status-conflict", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        resp = self.client.bulk(
            body=[
                {"create": {"_index": "test-status-conflict", "_id": "1"}},
                {"x": 2},
            ],
            refresh=True,
        )
        self.assertTrue(resp["errors"])
        self.assertEqual(resp["items"][0]["create"]["status"], 409)

    def test_not_found_returns_404(self) -> None:
        """Delete nonexistent document returns status 404."""
        resp = self.client.bulk(
            body=[
                {"delete": {"_index": "test-status-notfound", "_id": "nonexistent"}},
            ],
            refresh=True,
        )
        delete_item = resp["items"][0]["delete"]
        self.assertEqual(delete_item["status"], 404)
        if "result" in delete_item:
            self.assertEqual(delete_item["result"], "not_found")
