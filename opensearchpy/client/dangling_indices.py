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


# ----------------------------------------------------
# THIS CODE IS GENERATED AND MANUAL EDITS WILL BE LOST.
#
# To contribute, kindly make essential modifications through either the "opensearch-py client generator":
# https://github.com/opensearch-project/opensearch-py/blob/main/utils/generate-api.py
# or the "OpenSearch API specification" available at:
# https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json
# -----------------------------------------------------


from typing import Any

from .utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class DanglingIndicesClient(NamespacedClient):
    @query_params(
        "accept_data_loss", "cluster_manager_timeout", "master_timeout", "timeout"
    )
    def delete_dangling_index(
        self,
        index_uuid: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Deletes the specified dangling index.


        :arg index_uuid: The UUID of the dangling index.
        :arg accept_data_loss: Must be set to true in order to delete
            the dangling index.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout (Deprecated: To promote inclusive language,
            use 'cluster_manager_timeout' instead.): Operation timeout for
            connection to master node.
        :arg timeout: Operation timeout.
        """
        if index_uuid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index_uuid'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_dangling", index_uuid),
            params=params,
            headers=headers,
        )

    @query_params(
        "accept_data_loss", "cluster_manager_timeout", "master_timeout", "timeout"
    )
    def import_dangling_index(
        self,
        index_uuid: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Imports the specified dangling index.


        :arg index_uuid: The UUID of the dangling index.
        :arg accept_data_loss: Must be set to true in order to import
            the dangling index.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout (Deprecated: To promote inclusive language,
            use 'cluster_manager_timeout' instead.): Operation timeout for
            connection to master node.
        :arg timeout: Operation timeout.
        """
        if index_uuid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index_uuid'.")

        return self.transport.perform_request(
            "POST", _make_path("_dangling", index_uuid), params=params, headers=headers
        )

    @query_params()
    def list_dangling_indices(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Returns all dangling indices.

        """
        return self.transport.perform_request(
            "GET", "/_dangling", params=params, headers=headers
        )
