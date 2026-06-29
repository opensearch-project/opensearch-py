# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
test_grpc_transport.py — GrpcTransport Integration Tests

Verifies bulk via gRPC, single-doc via REST fallback,
and end-to-end workflows.
"""

from . import OpenSearchGrpcTestCase


class TestBulkViaGrpc(OpenSearchGrpcTestCase):
    def test_bulk_index_documents(self) -> None:
        """Bulk index via gRPC."""
        body = [
            {"index": {"_index": "test-transport-bulk", "_id": "1"}},
            {"title": "Bulk 1"},
            {"index": {"_index": "test-transport-bulk", "_id": "2"}},
            {"title": "Bulk 2"},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 2)

    def test_bulk_mixed_operations(self) -> None:
        """Bulk with index + update + delete."""
        # Seed
        self.client.bulk(body=[
            {"index": {"_index": "test-transport-mixed", "_id": "1"}},
            {"title": "Seed", "value": 1},
        ], refresh=True)

        # Mixed
        resp = self.client.bulk(body=[
            {"index": {"_index": "test-transport-mixed", "_id": "2"}},
            {"title": "New"},
            {"update": {"_index": "test-transport-mixed", "_id": "1"}},
            {"doc": {"value": 100}},
            {"delete": {"_index": "test-transport-mixed", "_id": "2"}},
        ], refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 3)

    def test_bulk_with_index_param(self) -> None:
        """Bulk with index at request level."""
        resp = self.client.bulk(
            body=[
                {"index": {"_id": "1"}},
                {"title": "Request-level index"},
            ],
            index="test-transport-idx",
            refresh=True,
        )
        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["index"]["_index"], "test-transport-idx")

    def test_bulk_large_batch(self) -> None:
        """Bulk with 10 docs to verify batching."""
        body = []
        for i in range(10):
            body.append({"index": {"_index": "test-transport-batch", "_id": str(i)}})
            body.append({"value": i})

        resp = self.client.bulk(body=body, refresh=True)
        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 10)


class TestSingleDocViaRest(OpenSearchGrpcTestCase):
    """Single-doc operations go through REST fallback."""

    def test_index_single_document(self) -> None:
        """client.index() goes through REST."""
        resp = self.client.index(
            index="test-transport-single", id="1", body={"title": "REST index"}
        )
        self.assertIn(resp["result"], ("created", "updated"))

    def test_get_document(self) -> None:
        """client.get() goes through REST."""
        self.client.index(
            index="test-transport-get", id="1", body={"title": "Get me"}, refresh=True
        )
        doc = self.client.get(index="test-transport-get", id="1")
        self.assertEqual(doc["_source"]["title"], "Get me")

    def test_delete_document(self) -> None:
        """client.delete() goes through REST."""
        self.client.index(
            index="test-transport-delete", id="1", body={"title": "Delete me"}, refresh=True
        )
        resp = self.client.delete(index="test-transport-delete", id="1")
        self.assertEqual(resp["result"], "deleted")


class TestRestFallback(OpenSearchGrpcTestCase):
    """Non-bulk operations correctly fall back to REST."""

    def test_search(self) -> None:
        self.client.bulk(body=[
            {"index": {"_index": "test-transport-search", "_id": "1"}},
            {"title": "Findme"},
        ], refresh=True)

        resp = self.client.search(
            index="test-transport-search",
            body={"query": {"match": {"title": "Findme"}}},
        )
        self.assertEqual(resp["hits"]["total"]["value"], 1)

    def test_count(self) -> None:
        self.client.bulk(body=[
            {"index": {"_index": "test-transport-count", "_id": "1"}},
            {"x": 1},
            {"index": {"_index": "test-transport-count", "_id": "2"}},
            {"x": 2},
        ], refresh=True)

        count = self.client.count(index="test-transport-count")["count"]
        self.assertEqual(count, 2)

    def test_create_and_delete_index(self) -> None:
        self.client.indices.create(index="test-transport-idx-mgmt")
        self.assertTrue(self.client.indices.exists(index="test-transport-idx-mgmt"))
        self.client.indices.delete(index="test-transport-idx-mgmt")
        self.assertFalse(self.client.indices.exists(index="test-transport-idx-mgmt"))


class TestEndToEndWorkflow(OpenSearchGrpcTestCase):
    """Full workflows combining gRPC bulk and REST operations."""

    def test_bulk_then_search(self) -> None:
        self.client.bulk(body=[
            {"index": {"_index": "test-e2e-search", "_id": "1"}},
            {"title": "End to end", "status": "active"},
        ], refresh=True)

        resp = self.client.search(
            index="test-e2e-search",
            body={"query": {"term": {"status.keyword": "active"}}},
        )
        self.assertEqual(resp["hits"]["total"]["value"], 1)

    def test_bulk_update_then_get(self) -> None:
        self.client.bulk(body=[
            {"index": {"_index": "test-e2e-update", "_id": "1"}},
            {"title": "Original", "value": 1},
        ], refresh=True)

        self.client.bulk(body=[
            {"update": {"_index": "test-e2e-update", "_id": "1"}},
            {"doc": {"value": 999}},
        ], refresh=True)

        doc = self.client.get(index="test-e2e-update", id="1")
        self.assertEqual(doc["_source"]["value"], 999)
        self.assertEqual(doc["_source"]["title"], "Original")

    def test_bulk_delete_then_verify(self) -> None:
        self.client.bulk(body=[
            {"index": {"_index": "test-e2e-del", "_id": "1"}},
            {"title": "Will be deleted"},
        ], refresh=True)

        self.client.bulk(body=[
            {"delete": {"_index": "test-e2e-del", "_id": "1"}},
        ], refresh=True)

        self.assertFalse(self.client.exists(index="test-e2e-del", id="1"))
