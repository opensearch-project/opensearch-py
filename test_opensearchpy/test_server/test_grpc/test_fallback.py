# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
test_fallback.py — REST Fallback Verification

Verifies that non-bulk operations correctly fall back to REST
when using the gRPC-enabled client.
"""

from . import OpenSearchGrpcTestCase


class TestRestFallback(OpenSearchGrpcTestCase):
    def test_index_management(self) -> None:
        """Index create/exists/delete go through REST."""
        self.client.indices.create(index="test-grpc-fallback")
        self.assertTrue(self.client.indices.exists(index="test-grpc-fallback"))
        self.client.indices.delete(index="test-grpc-fallback")
        self.assertFalse(self.client.indices.exists(index="test-grpc-fallback"))

    def test_search(self) -> None:
        """Search goes through REST."""
        self.client.bulk(
            body=[
                {"index": {"_index": "test-grpc-search", "_id": "1"}},
                {"title": "Searchable", "category": "grpc"},
            ],
            refresh=True,
        )
        resp = self.client.search(
            index="test-grpc-search",
            body={"query": {"match": {"category": "grpc"}}},
        )
        self.assertEqual(resp["hits"]["total"]["value"], 1)
        self.assertEqual(resp["hits"]["hits"][0]["_source"]["title"], "Searchable")

    def test_get_document(self) -> None:
        """GET goes through REST."""
        self.client.bulk(
            body=[
                {"index": {"_index": "test-grpc-get", "_id": "1"}},
                {"title": "Get me"},
            ],
            refresh=True,
        )
        doc = self.client.get(index="test-grpc-get", id="1")
        self.assertEqual(doc["_source"]["title"], "Get me")
        self.assertEqual(doc["_id"], "1")

    def test_count(self) -> None:
        """Count goes through REST."""
        self.client.bulk(
            body=[
                {"index": {"_index": "test-grpc-count", "_id": "1"}},
                {"x": 1},
                {"index": {"_index": "test-grpc-count", "_id": "2"}},
                {"x": 2},
            ],
            refresh=True,
        )
        resp = self.client.count(index="test-grpc-count")
        self.assertEqual(resp["count"], 2)

    def test_cluster_health(self) -> None:
        """Cluster health goes through REST."""
        resp = self.client.cluster.health()
        self.assertIn("status", resp)
        self.assertIn(resp["status"], ("green", "yellow", "red"))

    def test_cat_indices(self) -> None:
        """Cat APIs go through REST."""
        self.client.bulk(
            body=[
                {"index": {"_index": "test-grpc-cat", "_id": "1"}},
                {"x": 1},
            ],
            refresh=True,
        )
        resp = self.client.cat.indices(index="test-grpc-cat", format="json")
        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]["index"], "test-grpc-cat")
