# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#

from test_opensearchpy.test_cases import OpenSearchTestCase


class TestHttp(OpenSearchTestCase):
    def test_http_get(self) -> None:
        self.client.http.get("/")
        self.assert_call_count_equals(1)
        self.assertEqual([(None, None, None)], self.assert_url_called("GET", "/", 1))

    def test_http_head(self) -> None:
        self.client.http.head("/")
        self.assert_call_count_equals(1)
        self.assertEqual([(None, None, None)], self.assert_url_called("HEAD", "/", 1))

    def test_http_put(self) -> None:
        self.client.http.put("/xyz", headers={"X": "Y"}, body="body")
        self.assert_call_count_equals(1)
        self.assertEqual(
            [(None, {"X": "Y"}, "body")], self.assert_url_called("PUT", "/xyz", 1)
        )

    def test_http_post(self) -> None:
        self.client.http.post("/xyz", headers={"X": "Y"}, body="body")
        self.assert_call_count_equals(1)
        self.assertEqual(
            [(None, {"X": "Y"}, "body")], self.assert_url_called("POST", "/xyz", 1)
        )

    def test_http_post_with_params(self) -> None:
        self.client.http.post(
            "/xyz", headers={"X": "Y"}, params={"A": "B"}, body="body"
        )
        self.assert_call_count_equals(1)
        self.assertEqual(
            [({"A": "B"}, {"X": "Y"}, "body")],
            self.assert_url_called("POST", "/xyz", 1),
        )

    def test_http_delete(self) -> None:
        self.client.http.delete("/xyz", headers={"X": "Y"}, body="body")
        self.assert_call_count_equals(1)
        self.assertEqual(
            [(None, {"X": "Y"}, "body")], self.assert_url_called("DELETE", "/xyz", 1)
        )
