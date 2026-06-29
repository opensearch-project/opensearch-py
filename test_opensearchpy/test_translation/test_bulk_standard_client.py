# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
test_bulk_standard_client.py — Bulk Upload via OpenSearchGrpc Client

Verifies that the OpenSearchGrpc client correctly routes bulk operations
over gRPC while maintaining the standard response format.
"""

from . import OpenSearchGrpcTestCase


class TestBulkViaGrpcClient(OpenSearchGrpcTestCase):
    def test_upload_documents(self) -> None:
        """Upload documents using OpenSearchGrpc and verify response."""
        body = []
        for i in range(10):
            body.append({"index": {"_index": "test-std-client", "_id": str(i)}})
            body.append({"title": f"Document {i}", "value": i})

        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 10)
        self.assertEqual(resp["items"][0]["index"]["result"], "created")
        self.assertEqual(resp["items"][0]["index"]["status"], 201)

    def test_bulk_then_search(self) -> None:
        """Bulk via gRPC, search via REST fallback."""
        body = [
            {"index": {"_index": "test-std-search", "_id": "1"}},
            {"title": "Searchable", "category": "test"},
        ]
        self.client.bulk(body=body, refresh=True)

        resp = self.client.search(
            index="test-std-search",
            body={"query": {"match": {"category": "test"}}},
        )
        self.assertEqual(resp["hits"]["total"]["value"], 1)
        self.assertEqual(resp["hits"]["hits"][0]["_source"]["title"], "Searchable")

    def test_bulk_then_get(self) -> None:
        """Bulk via gRPC, get via REST fallback."""
        body = [
            {"index": {"_index": "test-std-get", "_id": "1"}},
            {"title": "Get me"},
        ]
        self.client.bulk(body=body, refresh=True)

        doc = self.client.get(index="test-std-get", id="1")
        self.assertEqual(doc["_source"]["title"], "Get me")

    def test_bulk_then_count(self) -> None:
        """Bulk via gRPC, count via REST fallback."""
        body = []
        for i in range(5):
            body.append({"index": {"_index": "test-std-count", "_id": str(i)}})
            body.append({"x": i})

        self.client.bulk(body=body, refresh=True)

        count = self.client.count(index="test-std-count")["count"]
        self.assertEqual(count, 5)
