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
    def test_create_monitor(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Post Method
        self.client.alerting.create_monitor({})
        self.assert_url_called("POST", "/_plugins/_alerting/monitors")

    def test_run_monitor(self) -> None:
        # pylint: disable=missing-function-docstring
        self.client.alerting.run_monitor("...")
        self.assert_url_called("POST", "/_plugins/_alerting/monitors/.../_execute")

    def test_get_monitor(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Get Method
        self.client.alerting.get_monitor("...")
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/...")

    def test_search_monitor(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Search Method
        self.client.alerting.search_monitor({})
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/_search")

    def test_update_monitor(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Update Method
        self.client.alerting.update_monitor("...")
        self.assert_url_called("PUT", "/_plugins/_alerting/monitors/...")

    def test_delete_monitor(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Delete Method
        self.client.alerting.delete_monitor("...")
        self.assert_url_called("DELETE", "/_plugins/_alerting/monitors/...")

    def test_create_destination(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Post Method
        self.client.alerting.create_destination({})
        self.assert_url_called("POST", "/_plugins/_alerting/destinations")

    def test_get_destination(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Get Method

        # Get a specific destination
        self.client.alerting.get_destination("...")
        self.assert_url_called("GET", "/_plugins/_alerting/destinations/...")

        # Get all destinations
        self.client.alerting.get_destination()
        self.assert_url_called("GET", "/_plugins/_alerting/destinations")

    def test_update_destination(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Update Method
        self.client.alerting.update_destination("...")
        self.assert_url_called("PUT", "/_plugins/_alerting/destinations/...")

    def test_delete_destination(self) -> None:
        # pylint: disable=missing-function-docstring
        # Test Delete Method
        self.client.alerting.delete_destination("...")
        self.assert_url_called("DELETE", "/_plugins/_alerting/destinations/...")

    def test_get_alerts(self) -> None:
        # pylint: disable=missing-function-docstring
        self.client.alerting.get_alerts()
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/alerts")

    def test_acknowledge_alerts(self) -> None:
        # pylint: disable=missing-function-docstring
        self.client.alerting.acknowledge_alert("...")
        self.assert_url_called(
            "POST", "/_plugins/_alerting/monitors/.../_acknowledge/alerts"
        )
