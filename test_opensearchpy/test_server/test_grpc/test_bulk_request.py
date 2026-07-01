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
test_bulk_request.py — Integration Tests for the Translation Layer

Tests the full round-trip: Python dict → protobuf → server → protobuf response → Python dict.
Verifies BulkRequestProtoBuilder builds correct requests and ResponseConverter
returns correct responses when sent through an actual OpenSearch server.

Requires OpenSearch running with gRPC on port 9400.
"""

from . import OpenSearchGrpcTestCase


class TestBulkRequestBuilderBuild(OpenSearchGrpcTestCase):
    """Test that BulkRequestProtoBuilder builds correct requests via the server."""

    def test_single_index_operation(self) -> None:
        """Single index operation produces correct server response."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-builder-single", "_id": "1"}},
                {"title": "Doc 1"},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 1)
        self.assertEqual(resp["items"][0]["index"]["_index"], "test-builder-single")
        self.assertEqual(resp["items"][0]["index"]["_id"], "1")
        self.assertEqual(resp["items"][0]["index"]["result"], "created")
        self.assertEqual(resp["items"][0]["index"]["status"], 201)

    def test_multiple_index_operations(self) -> None:
        """Multiple operations produce correct number of response items."""
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-builder-multi", "_id": str(i)}})
            body.append({"title": f"Doc {i}"})

        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 5)

    def test_create_operation(self) -> None:
        """Create operation produces correct response fields."""
        resp = self.client.bulk(
            body=[
                {"create": {"_index": "test-builder-create", "_id": "1"}},
                {"title": "Created doc"},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["create"]["result"], "created")
        self.assertEqual(resp["items"][0]["create"]["status"], 201)

    def test_update_operation(self) -> None:
        """Update operation produces correct response fields."""
        # Create first
        self.client.bulk(
            body=[
                {"index": {"_index": "test-builder-update", "_id": "1"}},
                {"title": "Original", "value": 1},
            ],
            refresh=True,
        )

        # Update
        resp = self.client.bulk(
            body=[
                {"update": {"_index": "test-builder-update", "_id": "1"}},
                {"doc": {"value": 99}},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["update"]["result"], "updated")
        self.assertEqual(resp["items"][0]["update"]["status"], 200)

        # Verify content via GET
        doc = self.client.get(index="test-builder-update", id="1")
        self.assertEqual(doc["_source"]["value"], 99)
        self.assertEqual(doc["_source"]["title"], "Original")

    def test_delete_operation(self) -> None:
        """Delete operation produces correct response fields."""
        # Create first
        self.client.bulk(
            body=[
                {"index": {"_index": "test-builder-delete", "_id": "1"}},
                {"title": "Delete me"},
            ],
            refresh=True,
        )

        # Delete
        resp = self.client.bulk(
            body=[
                {"delete": {"_index": "test-builder-delete", "_id": "1"}},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["delete"]["result"], "deleted")
        self.assertEqual(resp["items"][0]["delete"]["status"], 200)


class TestBulkRequestFromBody(OpenSearchGrpcTestCase):
    """Test from_body parsing with different input formats."""

    def test_from_list_of_dicts(self) -> None:
        """List of dicts produces correct server response."""
        body = [
            {"index": {"_index": "test-from-list", "_id": "1"}},
            {"title": "From list"},
            {"index": {"_index": "test-from-list", "_id": "2"}},
            {"title": "From list 2"},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 2)

    def test_from_ndjson_string(self) -> None:
        """NDJSON string produces correct server response."""
        ndjson = (
            '{"index": {"_index": "test-from-ndjson", "_id": "1"}}\n'
            '{"title": "From NDJSON"}\n'
        )
        resp = self.client.bulk(body=ndjson, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 1)
        self.assertEqual(resp["items"][0]["index"]["result"], "created")

    def test_with_default_index(self) -> None:
        """Index specified at request level applies to all operations."""
        body = [
            {"index": {"_id": "1"}},
            {"title": "Default index"},
        ]
        resp = self.client.bulk(body=body, index="test-default-idx", refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["index"]["_index"], "test-default-idx")


class TestResponseFormat(OpenSearchGrpcTestCase):
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


class TestStatusCodeMapping(OpenSearchGrpcTestCase):
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
        # Server may return result="not_found" or omit result on error
        if "result" in delete_item:
            self.assertEqual(delete_item["result"], "not_found")


class TestMixedOperations(OpenSearchGrpcTestCase):
    """Test mixed operations in a single bulk request."""

    def test_index_update_delete_in_one_request(self) -> None:
        """All operation types work correctly in one bulk call."""
        # Seed
        self.client.bulk(
            body=[
                {"index": {"_index": "test-mixed-ops", "_id": "existing"}},
                {"title": "Existing", "value": 1},
                {"index": {"_index": "test-mixed-ops", "_id": "to-delete"}},
                {"title": "Will delete"},
            ],
            refresh=True,
        )

        # Mixed batch
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-mixed-ops", "_id": "new"}},
                {"title": "New doc"},
                {"update": {"_index": "test-mixed-ops", "_id": "existing"}},
                {"doc": {"value": 99}},
                {"delete": {"_index": "test-mixed-ops", "_id": "to-delete"}},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 3)

        # Verify operation types in response
        self.assertIn("index", resp["items"][0])
        self.assertIn("update", resp["items"][1])
        self.assertIn("delete", resp["items"][2])

        # Verify results
        self.assertEqual(resp["items"][0]["index"]["result"], "created")
        self.assertEqual(resp["items"][1]["update"]["result"], "updated")
        self.assertEqual(resp["items"][2]["delete"]["result"], "deleted")

    def test_request_level_params(self) -> None:
        """Request-level parameters (index, refresh) are applied."""
        body = [
            {"index": {"_id": "1"}},
            {"title": "Param test"},
            {"index": {"_id": "2"}},
            {"title": "Param test 2"},
        ]
        resp = self.client.bulk(body=body, index="test-req-params", refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 2)
        self.assertEqual(resp["items"][0]["index"]["_index"], "test-req-params")
        self.assertEqual(resp["items"][1]["index"]["_index"], "test-req-params")

        # Verify docs are searchable (refresh worked)
        count = self.client.count(index="test-req-params")["count"]
        self.assertEqual(count, 2)
