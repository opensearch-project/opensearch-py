# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

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
