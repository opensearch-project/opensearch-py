# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

# ------------------------------------------------------------------------------------------
# THIS CODE IS AUTOMATICALLY GENERATED AND MANUAL EDITS WILL BE LOST
#
# To contribute, kindly make modifications in the opensearch-py client generator
# or in the OpenSearch API specification, and run `nox -rs generate`. See DEVELOPER_GUIDE.md
# and https://github.com/opensearch-project/opensearch-api-specification for details.
# -----------------------------------------------------------------------------------------+


from typing import Any

from .utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class SearchPipelineClient(NamespacedClient):
    @query_params("cluster_manager_timeout")
    def get(
        self,
        id: Any = None,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves information about a specified search pipeline.


        :arg id: Comma-separated list of search pipeline ids. Wildcards
            supported.
        :arg cluster_manager_timeout: operation timeout for connection
            to cluster-manager node.
        """
        return self.transport.perform_request(
            "GET", _make_path("_search", "pipeline", id), params=params, headers=headers
        )

    @query_params("cluster_manager_timeout", "timeout")
    def delete(
        self,
        id: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Deletes the specified search pipeline.


        :arg id: Pipeline ID.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg timeout: Operation timeout.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_search", "pipeline", id),
            params=params,
            headers=headers,
        )

    @query_params("cluster_manager_timeout", "timeout")
    def put(
        self,
        id: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or replaces the specified search pipeline.


        :arg id: Pipeline ID.
        :arg cluster_manager_timeout: operation timeout for connection
            to cluster-manager node.
        :arg timeout: Operation timeout.
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_search", "pipeline", id),
            params=params,
            headers=headers,
            body=body,
        )
