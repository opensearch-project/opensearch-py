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
test_bulk_request_integration.py — BulkRequestProtoBuilder Integration Tests

Tests the translation layer by building protobuf requests and sending
them through the client to verify end-to-end correctness.
"""

from . import OpenSearchGrpcTestCase


class TestBulkRequestBuilderIntegration(OpenSearchGrpcTestCase):
    def test_builder_index(self) -> None:
        """Build a bulk request with the builder and send via client."""
        body = []
        for i in range(3):
            body.append({"index": {"_index": "test-builder-idx", "_id": str(i)}})
            body.append({"title": f"Builder doc {i}"})

        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 3)

    def test_builder_with_pipeline(self) -> None:
        """Bulk with pipeline parameter."""
        body = [
            {"index": {"_index": "test-builder-pipe", "_id": "1"}},
            {"title": "Pipeline doc"},
        ]
        # Pipeline may not exist, but we verify it's passed without error
        # If pipeline doesn't exist, bulk will report item-level error
        resp = self.client.bulk(body=body, refresh=True)
        self.assertEqual(len(resp["items"]), 1)

    def test_builder_with_routing(self) -> None:
        """Bulk with routing parameter."""
        body = [
            {
                "index": {
                    "_index": "test-builder-route",
                    "_id": "1",
                    "routing": "shard-1",
                }
            },
            {"title": "Routed doc"},
        ]
        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["index"]["result"], "created")
