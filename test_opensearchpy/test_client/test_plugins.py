# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from test_opensearchpy.test_cases import OpenSearchTestCase


class TestAlerting(OpenSearchTestCase):
    def test_create_monitor(self):
        # Test Post Method
        self.client.plugins.alerting.create_monitor({})
        self.assert_url_called("POST", "/_plugins/_alerting/monitors")

    def test_run_monitor(self):
        self.client.plugins.alerting.run_monitor("...")
        self.assert_url_called("POST", "/_plugins/_alerting/monitors/.../_execute")

    def test_get_monitor(self):
        # Test Get Method
        self.client.plugins.alerting.get_monitor("...")
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/...")

    def test_search_monitor(self):
        # Test Search Method
        self.client.plugins.alerting.search_monitor({})
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/_search")

    def test_update_monitor(self):
        # Test Update Method
        self.client.plugins.alerting.update_monitor("...")
        self.assert_url_called("PUT", "/_plugins/_alerting/monitors/...")

    def test_delete_monitor(self):
        # Test Delete Method
        self.client.plugins.alerting.delete_monitor("...")
        self.assert_url_called("DELETE", "/_plugins/_alerting/monitors/...")

    def test_create_destination(self):
        # Test Post Method
        self.client.plugins.alerting.create_destination({})
        self.assert_url_called("POST", "/_plugins/_alerting/destinations")

    def test_get_destination(self):
        # Test Get Method

        # Get a specific destination
        self.client.plugins.alerting.get_destination("...")
        self.assert_url_called("GET", "/_plugins/_alerting/destinations/...")

        # Get all destinations
        self.client.plugins.alerting.get_destination()
        self.assert_url_called("GET", "/_plugins/_alerting/destinations")

    def test_update_destination(self):
        # Test Update Method
        self.client.plugins.alerting.update_destination("...")
        self.assert_url_called("PUT", "/_plugins/_alerting/destinations/...")

    def test_delete_destination(self):
        # Test Delete Method
        self.client.plugins.alerting.delete_destination("...")
        self.assert_url_called("DELETE", "/_plugins/_alerting/destinations/...")

    def test_get_alerts(self):
        self.client.plugins.alerting.get_alerts()
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/alerts")

    def test_acknowledge_alerts(self):
        self.client.plugins.alerting.acknowledge_alert("...")
        self.assert_url_called(
            "POST", "/_plugins/_alerting/monitors/.../_acknowledge/alerts"
        )
