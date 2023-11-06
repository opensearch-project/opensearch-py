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


import mock
import pytest
from _pytest.mark.structures import MarkDecorator
from multidict import CIMultiDict

from opensearchpy._async._extra_imports import aiohttp
from opensearchpy._async.compat import get_running_loop
from opensearchpy.connection.http_async import AsyncHttpConnection

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestAsyncHttpConnection:
    def test_auth_as_tuple(self) -> None:
        c = AsyncHttpConnection(http_auth=("username", "password"))
        assert isinstance(c._http_auth, aiohttp.BasicAuth)
        assert c._http_auth.login, "username"
        assert c._http_auth.password, "password"

    def test_auth_as_string(self) -> None:
        c = AsyncHttpConnection(http_auth="username:password")
        assert isinstance(c._http_auth, aiohttp.BasicAuth)
        assert c._http_auth.login, "username"
        assert c._http_auth.password, "password"

    def test_auth_as_callable(self) -> None:
        def auth_fn():
            pass

        c = AsyncHttpConnection(http_auth=auth_fn)
        assert callable(c._http_auth)

    @mock.patch("aiohttp.ClientSession.request", new_callable=mock.Mock)
    async def test_basicauth_in_request_session(self, mock_request) -> None:
        async def do_request(*args, **kwargs):
            response_mock = mock.AsyncMock()
            response_mock.headers = CIMultiDict()
            response_mock.status = 200
            return response_mock

        mock_request.return_value = aiohttp.client._RequestContextManager(do_request())

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

    @mock.patch("aiohttp.ClientSession.request", new_callable=mock.Mock)
    async def test_callable_in_request_session(self, mock_request) -> None:
        def auth_fn(*args, **kwargs):
            return {
                "Test": "PASSED",
            }

        async def do_request(*args, **kwargs):
            response_mock = mock.AsyncMock()
            response_mock.headers = CIMultiDict()
            response_mock.status = 200
            return response_mock

        mock_request.return_value = aiohttp.client._RequestContextManager(do_request())

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
