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

import warnings

from ..plugins.alerting import AlertingClient
from .utils import NamespacedClient


class PluginsClient(NamespacedClient):
    def __init__(self, client):
        super(PluginsClient, self).__init__(client)
        # self.query_workbench = QueryWorkbenchClient(client)
        # self.reporting = ReportingClient(client)
        # self.notebooks = NotebooksClient(client)
        self.alerting = AlertingClient(client)
        # self.anomaly_detection = AnomalyDetectionClient(client)
        # self.trace_analytics = TraceAnalyticsClient(client)
        # self.index_management = IndexManagementClient(client)
        # self.security = SecurityClient(client)

        self._dynamic_lookup(client)

    def _dynamic_lookup(self, client):
        # Issue : https://github.com/opensearch-project/opensearch-py/issues/90#issuecomment-1003396742

        plugins = [
            # "query_workbench",
            # "reporting",
            # "notebooks",
            "alerting",
            # "anomaly_detection",
            # "trace_analytics",
            # "index_management",
            # "security"
        ]
        for plugin in plugins:
            if not hasattr(client, plugin):
                setattr(client, plugin, getattr(self, plugin))
            else:
                warnings.warn(
                    "Cannot load `{plugin}` directly to OpenSearch. `{plugin}` already exists in OpenSearch. Please use `OpenSearch.plugin.{plugin}` instead.".format(
                        plugin=plugin
                    ),
                    category=RuntimeWarning,
                    stacklevel=2,
                )
