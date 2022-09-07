# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from .utils import NamespacedClient, query_params


class RemoteClient(NamespacedClient):
    @query_params()
    def info(self, params=None, headers=None):
        return self.transport.perform_request(
            "GET", "/_remote/info", params=params, headers=headers
        )
