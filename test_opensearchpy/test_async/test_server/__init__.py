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


from unittest import IsolatedAsyncioTestCase  # type: ignore

from opensearchpy._async.helpers.test import get_test_client
from opensearchpy.connection.async_connections import add_connection

from ...utils import wipe_cluster


class AsyncOpenSearchTestCase(IsolatedAsyncioTestCase):  # type: ignore
    async def asyncSetUp(
        self,
    ) -> None:
        # pylint: disable=invalid-name,missing-function-docstring
        self.client = await get_test_client(
            verify_certs=False, http_auth=("admin", "admin")
        )
        await add_connection("default", self.client)

    async def asyncTearDown(
        self,
    ) -> None:
        # pylint: disable=invalid-name,missing-function-docstring
        wipe_cluster(self.client)
        if self.client:
            await self.client.close()
