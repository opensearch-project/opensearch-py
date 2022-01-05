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
    def test_create_alert(self):
        # Test Post Method
        self.client.plugins.alerting.create_monitor({})
        self.assert_url_called("POST", "/_plugins/_alerting/monitors")

    def test_get_alert(self):
        # Test Get Method
        self.client.plugins.alerting.get_monitor("...")
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/...")

    def test_search_alert(self):
        # Test Search Method
        self.client.plugins.alerting.search_monitor({})
        self.assert_url_called("GET", "/_plugins/_alerting/monitors/_search")

    def test_update_alert(self):
        # Test Update Method
        self.client.plugins.alerting.update_monitor("...")
        self.assert_url_called("PUT", "/_plugins/_alerting/monitors/...")

    def test_delete_alert(self):
        # Test Delete Method
        self.client.plugins.alerting.delete_monitor("...")
        self.assert_url_called("DELETE", "/_plugins/_alerting/monitors/...")
