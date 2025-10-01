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


from typing import Any, Dict, Optional
from unittest import mock

import pytest
import yarl
from multidict import CIMultiDict

from opensearchpy._async._extra_imports import aiohttp  # type: ignore
from opensearchpy._async.compat import get_running_loop
from opensearchpy.connection.http_async import AsyncHttpConnection


class TestAsyncHttpConnection:
    class MockResponse:

        def __init__(
            self,
            text: Any = None,
            status: int = 200,
            headers: Any = CIMultiDict(),
        ) -> None:
            self._text = text
            self.status = status
            self.headers = headers

        async def text(self) -> Any:
            return self._text

        async def __aexit__(self, *args: Any) -> None:
            pass

        async def __aenter__(self) -> Any:
            return self

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
        def auth_fn(
            _method: str, _url: str, _body: Optional[bytes], _headers: Dict[str, str]
        ) -> Dict[str, str]:
            return {}

        c = AsyncHttpConnection(http_auth=auth_fn)
        assert callable(c._http_auth)

    @pytest.mark.asyncio  # type: ignore
    @mock.patch("aiohttp.ClientSession.request")
    async def test_basicauth_in_request_session(self, mock_request: Any) -> None:

        mock_request.return_value = TestAsyncHttpConnection.MockResponse()

        c = AsyncHttpConnection(
            http_auth=("username", "password"),
            loop=get_running_loop(),
        )
        c.headers = {}
        await c.perform_request("post", "/test")
        mock_request.assert_called_with(
            "post",
            yarl.URL("http://localhost:9200/test", encoded=True),
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

    @pytest.mark.asyncio  # type: ignore
    @mock.patch("aiohttp.ClientSession.request")
    async def test_callable_in_request_session(self, mock_request: Any) -> None:
        calls = []

        def auth_fn(*args: Any, **kwargs: Any) -> Any:
            calls.append((args, kwargs))
            return {"Test": "PASSED"}

        mock_request.return_value = TestAsyncHttpConnection.MockResponse()

        c = AsyncHttpConnection(http_auth=auth_fn, loop=get_running_loop())
        c.headers = {"a-header": "a-value"}
        await c.perform_request("post", "/test")

        assert calls == [
            (
                tuple(),
                {
                    "body": None,
                    "headers": {"a-header": "a-value"},
                    "method": "post",
                    "url": "http://localhost:9200/test",
                },
            )
        ]
        mock_request.assert_called_with(
            "post",
            yarl.URL("http://localhost:9200/test", encoded=True),
            data=None,
            auth=None,
            headers={
                "Test": "PASSED",
                "a-header": "a-value",
            },
            timeout=aiohttp.ClientTimeout(
                total=10,
                connect=None,
                sock_read=None,
                sock_connect=None,
            ),
            fingerprint=None,
        )
