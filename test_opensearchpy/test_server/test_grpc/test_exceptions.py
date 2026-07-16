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
test_exceptions.py — gRPC Exception Integration Tests

Tests that the gRPC client raises the correct opensearch-py exceptions
when interacting with a real OpenSearch server.

Requires OpenSearch running with gRPC on port 9400.
"""

from . import OpenSearchGrpcTestCase


class TestGrpcExceptionsIntegration(OpenSearchGrpcTestCase):
    """Test that gRPC operations raise correct exceptions via real server."""

    def test_conflict_on_duplicate_create(self) -> None:
        """Creating a document that already exists returns errors in bulk response."""
        # Create the document first
        self.client.bulk(
            body=[
                {"create": {"_index": "test-exc-conflict", "_id": "1"}},
                {"title": "Original"},
            ],
            refresh=True,
        )

        # Try to create again — should report error in items
        resp = self.client.bulk(
            body=[
                {"create": {"_index": "test-exc-conflict", "_id": "1"}},
                {"title": "Duplicate"},
            ],
            refresh=True,
        )

        self.assertTrue(resp["errors"])
        self.assertEqual(resp["items"][0]["create"]["status"], 409)

    def test_successful_bulk_no_errors(self) -> None:
        """Successful bulk returns errors=False."""
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-exc-success", "_id": "1"}},
                {"title": "Success"},
            ],
            refresh=True,
        )

        self.assertFalse(resp["errors"])
        self.assertEqual(resp["items"][0]["index"]["status"], 201)

    def test_update_nonexistent_reports_error(self) -> None:
        """Updating a nonexistent doc without upsert reports error in items."""
        resp = self.client.bulk(
            body=[
                {"update": {"_index": "test-exc-missing", "_id": "nonexistent"}},
                {"doc": {"title": "Update missing"}},
            ],
            refresh=True,
        )

        self.assertTrue(resp["errors"])
        # Should be 404 — document not found
        self.assertEqual(resp["items"][0]["update"]["status"], 404)

    def test_delete_nonexistent_reports_not_found(self) -> None:
        """Deleting a nonexistent doc reports not_found in items."""
        resp = self.client.bulk(
            body=[
                {"delete": {"_index": "test-exc-del-missing", "_id": "nonexistent"}},
            ],
            refresh=True,
        )

        delete_item = resp["items"][0]["delete"]
        self.assertEqual(delete_item["status"], 404)

    def test_mixed_success_and_error(self) -> None:
        """Bulk with mix of successful and failed operations."""
        # Create a doc
        self.client.bulk(
            body=[
                {"create": {"_index": "test-exc-mixed", "_id": "existing"}},
                {"title": "Existing"},
            ],
            refresh=True,
        )

        # Mixed: one success (index new), one failure (create duplicate)
        resp = self.client.bulk(
            body=[
                {"index": {"_index": "test-exc-mixed", "_id": "new"}},
                {"title": "New doc"},
                {"create": {"_index": "test-exc-mixed", "_id": "existing"}},
                {"title": "Duplicate"},
            ],
            refresh=True,
        )

        self.assertTrue(resp["errors"])
        self.assertEqual(len(resp["items"]), 2)
        # First succeeds
        self.assertEqual(resp["items"][0]["index"]["status"], 201)
        # Second fails with 409
        self.assertEqual(resp["items"][1]["create"]["status"], 409)

    def test_rest_fallback_not_found(self) -> None:
        """GET on nonexistent doc via REST fallback raises NotFoundError."""
        from opensearchpy.exceptions import NotFoundError

        with self.assertRaises(NotFoundError):
            self.client.get(index="test-exc-rest-404", id="nonexistent")

    def test_rest_fallback_request_error(self) -> None:
        """Invalid index name via REST fallback raises RequestError."""
        from opensearchpy.exceptions import RequestError

        with self.assertRaises(RequestError):
            self.client.indices.create(index="INVALID/NAME")
