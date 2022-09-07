# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from .utils import NamespacedClient, query_params


class FeaturesClient(NamespacedClient):
    @query_params("master_timeout")
    async def get_features(self, params=None, headers=None):
        """
        Gets a list of features which can be included in snapshots using the
        feature_states field when creating a snapshot


        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        return await self.transport.perform_request(
            "GET", "/_features", params=params, headers=headers
        )

    @query_params()
    async def reset_features(self, params=None, headers=None):
        """
        Resets the internal state of features, usually by deleting system indices


        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version
        """
        return await self.transport.perform_request(
            "POST", "/_features/_reset", params=params, headers=headers
        )
