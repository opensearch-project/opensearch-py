# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from test_opensearchpy.test_cases import OpenSearchTestCase


class TestPointInTime(OpenSearchTestCase):
    def test_create_one_point_in_time(self):
        index_name = "test-index"
        self.client.create_point_in_time(index=index_name)
        self.assert_url_called("POST", "/test-index/_search/point_in_time")

    def test_delete_one_point_in_time(self):
        self.client.delete_point_in_time(body={"pit_id": ["Sample-PIT-ID"]})
        self.assert_url_called("DELETE", "/_search/point_in_time")

    def test_delete_all_point_in_time(self):
        self.client.delete_point_in_time(all=True)
        self.assert_url_called("DELETE", "/_search/point_in_time/_all")

    def test_list_all_point_in_time(self):
        self.client.list_all_point_in_time()
        self.assert_url_called("GET", "/_search/point_in_time/_all")
