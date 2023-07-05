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


from unittest import IsolatedAsyncioTestCase

import pytest
from asynctest import patch

from opensearchpy import AsyncHttpConnection
from opensearchpy._async._extra_imports import aiohttp
from opensearchpy._async.compat import get_running_loop
from test_opensearchpy.utils import AsyncContextManagerMock


@pytest.mark.asyncio
class TestAsyncHttpConnection(IsolatedAsyncioTestCase):
    def test_auth_as_tuple(self):
        c = AsyncHttpConnection(http_auth=("username", "password"))
        self.assertIsInstance(c._http_auth, aiohttp.BasicAuth)
        self.assertEqual(c._http_auth.login, "username")
        self.assertEqual(c._http_auth.password, "username")

    def test_auth_as_string(self):
        c = AsyncHttpConnection(http_auth="username:password")
        self.assertIsInstance(c._http_auth, aiohttp.BasicAuth)
        self.assertEqual(c._http_auth.login, "username")
        self.assertEqual(c._http_auth.password, "password")

    def test_auth_as_callable(self):
        def auth_fn():
            pass

        c = AsyncHttpConnection(http_auth=auth_fn)
        self.assertTrue(callable(c._http_auth))

    @patch("aiohttp.ClientSession.request", new_callable=AsyncContextManagerMock)
    async def test_basicauth_in_request_session(self, mock_request):
        c = AsyncHttpConnection(
            http_auth=("username", "password"),
            loop=get_running_loop(),
        )
        c.headers = {}
        await c.perform_request("post", "/test")
        mock_request.assert_called_with(
            "post",
            "http://localhost:9200/test",
            data=None,
            auth=c._http_auth,
            headers={},
            timeout=aiohttp.ClientTimeout(
                total=10,
                connect=None,
                sock_read=None,
                sock_connect=None,
            ),
            fingerprint=None,
        )

    @patch("aiohttp.ClientSession.request", new_callable=AsyncContextManagerMock)
    async def test_callable_in_request_session(self, mock_request):
        def auth_fn(*args, **kwargs):
            return {
                "Test": "PASSED",
            }

        c = AsyncHttpConnection(http_auth=auth_fn, loop=get_running_loop())
        c.headers = {}
        await c.perform_request("post", "/test")

        mock_request.assert_called_with(
            "post",
            "http://localhost:9200/test",
            data=None,
            auth=None,
            headers={
                "Test": "PASSED",
            },
            timeout=aiohttp.ClientTimeout(
                total=10,
                connect=None,
                sock_read=None,
                sock_connect=None,
            ),
            fingerprint=None,
        )
