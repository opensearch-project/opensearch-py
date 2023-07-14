# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
# ----------------------------------------------------
# THIS CODE IS GENERATED. MANUAL EDITS WILL BE LOST.

# To contribute, please make necessary modifications to either [Python generator](https://github.com/opensearch-project/opensearch-py/blob/main/utils/generate-api.py) or [OpenAPI specs](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) as needed.
# -----------------------------------------------------

from .utils import SKIP_IN_PATH, NamespacedClient, query_params


class RemoteStoreClient(NamespacedClient):
    @query_params("cluster_manager_timeout", "wait_for_completion")
    async def restore(self, body, params=None, headers=None):
        """
        Restores from remote store.


        :arg body: Comma-separated list of index IDs
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST", "/_remotestore/_restore", params=params, headers=headers, body=body
        )
