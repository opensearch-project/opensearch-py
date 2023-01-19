# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from ..client.utils import (
    NamespacedClient as NamespacedClient,
    query_params as query_params,
)
from typing import Any, Union

class AlertingClient(NamespacedClient):
    def search_monitor(
        self, body, params: Any | None = ..., headers: Any | None = ...
    ) -> Union[bool, Any]: ...
    def get_monitor(
        self, monitor_id, params: Any | None = ..., headers: Any | None = ...
    ) -> Union[bool, Any]: ...
    def run_monitor(
        self, monitor_id, params: Any | None = ..., headers: Any | None = ...
    ) -> Union[bool, Any]: ...
    def create_monitor(
        self,
        body: Any | None = ...,
        params: Any | None = ...,
        headers: Any | None = ...,
    ) -> Union[bool, Any]: ...
    def update_monitor(
        self,
        monitor_id,
        body: Any | None = ...,
        params: Any | None = ...,
        headers: Any | None = ...,
    ) -> Union[bool, Any]: ...
    def delete_monitor(
        self, monitor_id, params: Any | None = ..., headers: Any | None = ...
    ) -> Union[bool, Any]: ...
    def get_destination(
        self,
        destination_id: Any | None = ...,
        params: Any | None = ...,
        headers: Any | None = ...,
    ) -> Union[bool, Any]: ...
    def create_destination(
        self,
        body: Any | None = ...,
        params: Any | None = ...,
        headers: Any | None = ...,
    ) -> Union[bool, Any]: ...
    def update_destination(
        self,
        destination_id,
        body: Any | None = ...,
        params: Any | None = ...,
        headers: Any | None = ...,
    ) -> Union[bool, Any]: ...
    def delete_destination(
        self, destination_id, params: Any | None = ..., headers: Any | None = ...
    ) -> Union[bool, Any]: ...
    def get_alerts(
        self, params: Any | None = ..., headers: Any | None = ...
    ) -> Union[bool, Any]: ...
    def acknowledge_alert(
        self,
        monitor_id,
        body: Any | None = ...,
        params: Any | None = ...,
        headers: Any | None = ...,
    ) -> Union[bool, Any]: ...
