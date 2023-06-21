# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from test_opensearchpy.test_cases import OpenSearchTestCase


class TestAlerting(OpenSearchTestCase):
    def test_create_monitor(self):
        # Test Post Method
        self.client.alerting.create_monitor({})
        self.assert_url_called("POST", "/_plugins/_alerting/monitors")

    def test_run_monitor(self):
        self.client.alerting.run_monitor("...")
        self.assert_url_called("POST", "/_plugins/_alerting/monitors/.../_execute")

    def test_get_monitor(self):
        # Test Get Method
        self.client.alerting.get_monitor("...")
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/...")

    def test_search_monitor(self):
        # Test Search Method
        self.client.alerting.search_monitor({})
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/_search")

    def test_update_monitor(self):
        # Test Update Method
        self.client.alerting.update_monitor("...")
        self.assert_url_called("PUT", "/_plugins/_alerting/monitors/...")

    def test_delete_monitor(self):
        # Test Delete Method
        self.client.alerting.delete_monitor("...")
        self.assert_url_called("DELETE", "/_plugins/_alerting/monitors/...")

    def test_create_destination(self):
        # Test Post Method
        self.client.alerting.create_destination({})
        self.assert_url_called("POST", "/_plugins/_alerting/destinations")

    def test_get_destination(self):
        # Test Get Method

        # Get a specific destination
        self.client.alerting.get_destination("...")
        self.assert_url_called("GET", "/_plugins/_alerting/destinations/...")

        # Get all destinations
        self.client.alerting.get_destination()
        self.assert_url_called("GET", "/_plugins/_alerting/destinations")

    def test_update_destination(self):
        # Test Update Method
        self.client.alerting.update_destination("...")
        self.assert_url_called("PUT", "/_plugins/_alerting/destinations/...")

    def test_delete_destination(self):
        # Test Delete Method
        self.client.alerting.delete_destination("...")
        self.assert_url_called("DELETE", "/_plugins/_alerting/destinations/...")

    def test_get_alerts(self):
        self.client.alerting.get_alerts()
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/alerts")

    def test_acknowledge_alerts(self):
        self.client.alerting.acknowledge_alert("...")
        self.assert_url_called(
            "POST", "/_plugins/_alerting/monitors/.../_acknowledge/alerts"
        )


class TestIndexManagement(OpenSearchTestCase):
    def test_create_policy(self):
        self.client.index_management.put_policy("...")
        self.assert_url_called("PUT", "/_plugins/_ism/policies/...")

    def test_update_policy(self):
        self.client.index_management.put_policy(
            "...", params={"if_seq_no": 7, "if_primary_term": 1}
        )
        self.assertEqual(
            [({"if_seq_no": 7, "if_primary_term": 1}, {}, None)],
            self.assert_url_called("PUT", "/_plugins/_ism/policies/..."),
        )

    def test_add_policy(self):
        self.client.index_management.add_policy("...")
        self.assert_url_called("POST", "/_plugins/_ism/add/...")

    def test_get_policy(self):
        self.client.index_management.get_policy("...")
        self.assert_url_called("GET", "/_plugins/_ism/policies/...")

    def test_remove_policy_from_index(self):
        self.client.index_management.remove_policy_from_index("...")
        self.assert_url_called("POST", "/_plugins/_ism/remove/...")

    def test_change_policy(self):
        self.client.index_management.change_policy("...")
        self.assert_url_called("POST", "/_plugins/_ism/change_policy/...")

    def test_retry(self):
        self.client.index_management.retry("...")
        self.assert_url_called("POST", "/_plugins/_ism/retry/...")

    def test_explain_index(self):
        self.client.index_management.explain_index("...", show_policy=True)
        self.assertEqual(
            [({"show_policy": b"true"}, {}, None)],
            self.assert_url_called("GET", "/_plugins/_ism/explain/..."),
        )

    def test_delete_policy(self):
        self.client.index_management.delete_policy("...")
        self.assert_url_called("DELETE", "/_plugins/_ism/policies/...")
