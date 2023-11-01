# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

# ----------------------------------------------------
# THIS CODE IS GENERATED AND MANUAL EDITS WILL BE LOST.
#
# To contribute, kindly make essential modifications through either the "opensearch-py client generator":
# https://github.com/opensearch-project/opensearch-py/blob/main/utils/generate-api.py
# or the "OpenSearch API specification" available at:
# https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json
# -----------------------------------------------------


from typing import Any

from .utils import SKIP_IN_PATH, NamespacedClient, query_params


class RemoteStoreClient(NamespacedClient):
    @query_params("cluster_manager_timeout", "wait_for_completion")
    def restore(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Restores from remote store.


        :arg body: Comma-separated list of index IDs
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning. Default is false.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST", "/_remotestore/_restore", params=params, headers=headers, body=body
        )
