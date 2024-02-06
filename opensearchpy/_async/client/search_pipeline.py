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
    async def get(
        self,
        id: Any = None,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Returns a search pipeline.


        :arg id: Comma-separated list of pipeline ids. Wildcards
            supported.
        """
        return self.transport.perform_request(
            "GET", _make_path("_search", "pipeline", id), params=params, headers=headers
        )

    async def put(
        self,
        id: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or updates a search pipeline.


        :arg id: Pipeline ID.
        :arg body: The search pipeline definition
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

    async def delete(
        self,
        id: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Deletes a search pipeline.


        :arg id: Pipeline ID.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_search", "pipeline", id),
            params=params,
            headers=headers,
        )