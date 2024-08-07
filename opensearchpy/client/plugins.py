# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import warnings
from typing import Any

from ..plugins.alerting import AlertingClient
from ..plugins.index_management import IndexManagementClient
from ..plugins.knn import KnnClient
from ..plugins.ml import MlClient
from ..plugins.notifications import NotificationsClient
from ..plugins.rollups import RollupsClient
from ..plugins.transforms import TransformsClient
from .client import Client
from .utils import NamespacedClient


class PluginsClient(NamespacedClient):
    alerting: Any
    index_management: Any

    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.ml = MlClient(client)
        self.transforms = TransformsClient(client)
        self.rollups = RollupsClient(client)
        self.notifications = NotificationsClient(client)
        self.knn = KnnClient(client)
        # self.query_workbench = QueryWorkbenchClient(client)
        # self.reporting = ReportingClient(client)
        # self.notebooks = NotebooksClient(client)
        self.alerting = AlertingClient(client)
        # self.anomaly_detection = AnomalyDetectionClient(client)
        # self.trace_analytics = TraceAnalyticsClient(client)
        self.index_management = IndexManagementClient(client)

        self._dynamic_lookup(client)

    def _dynamic_lookup(self, client: Any) -> None:
        # Issue : https://github.com/opensearch-project/opensearch-py/issues/90#issuecomment-1003396742

        plugins = [
            # "query_workbench",
            # "reporting",
            # "notebooks",
            "alerting",
            # "anomaly_detection",
            # "trace_analytics",
            "index_management",
        ]
        for plugin in plugins:
            if not hasattr(client, plugin):
                setattr(client, plugin, getattr(self, plugin))
            else:
                warnings.warn(
                    f"Cannot load `{plugin}` directly to {self.client.__class__.__name__} as it already exists. Use `{self.client.__class__.__name__}.plugin.{plugin}` instead.",
                    category=RuntimeWarning,
                    stacklevel=2,
                )
