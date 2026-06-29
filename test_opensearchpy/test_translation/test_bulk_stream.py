# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
test_bulk_stream.py — Bulk Streaming Integration Tests

Tests sending bulk data using the toProtoBulkRequest helper function
through the OpenSearchGrpc client.
"""

from . import OpenSearchGrpcTestCase


class TestBulkStream(OpenSearchGrpcTestCase):
    def test_stream_index_documents(self) -> None:
        """Stream multiple documents via bulk."""
        body = []
        for i in range(10):
            body.append({"index": {"_index": "test-stream", "_id": str(i)}})
            body.append({"title": f"Streamed {i}", "batch": 0})

        resp = self.client.bulk(body=body, refresh=True)

        self.assertFalse(resp["errors"])
        self.assertEqual(len(resp["items"]), 10)

        count = self.client.count(index="test-stream")["count"]
        self.assertEqual(count, 10)

    def test_stream_multiple_batches(self) -> None:
        """Send multiple bulk batches sequentially."""
        for batch in range(3):
            body = []
            for i in range(5):
                doc_id = f"{batch}-{i}"
                body.append({"index": {"_index": "test-stream-batch", "_id": doc_id}})
                body.append({"batch": batch, "seq": i})

            resp = self.client.bulk(body=body, refresh=True)
            self.assertFalse(resp["errors"])

        self.client.indices.refresh(index="test-stream-batch")
        count = self.client.count(index="test-stream-batch")["count"]
        self.assertEqual(count, 15)
