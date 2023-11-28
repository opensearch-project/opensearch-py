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


from collections import defaultdict
from typing import Any, Collection, Mapping, Optional, Union

import pytest

from opensearchpy import AsyncOpenSearch
from opensearchpy._async.transport import AsyncTransport

pytestmark = pytest.mark.asyncio


class DummyTransport(AsyncTransport):
    def __init__(self, hosts: Any, responses: Any = None, **kwargs: Any) -> None:
        self.hosts = hosts
        self.responses = responses
        self.call_count = 0
        self.calls: Any = defaultdict(list)

    async def perform_request(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        body: Optional[bytes] = None,
        timeout: Optional[Union[int, float]] = None,
        ignore: Collection[int] = (),
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        resp: Any = (200, {})
        if self.responses:
            resp = self.responses[self.call_count]
        self.call_count += 1
        self.calls[(method, url)].append((params, headers, body))
        return resp


class OpenSearchTestCaseWithDummyTransport:
    def assert_call_count_equals(self, count: int) -> None:
        assert isinstance(self.client.transport, DummyTransport)
        assert count == self.client.transport.call_count

    def assert_url_called(self, method: str, url: str, count: int = 1) -> Any:
        assert isinstance(self.client.transport, DummyTransport)
        assert (method, url) in self.client.transport.calls
        calls = self.client.transport.calls[(method, url)]
        assert count == len(calls)
        return calls

    def setup_method(self, method: Any) -> None:
        self.client = AsyncOpenSearch(transport_class=DummyTransport)


class TestClient(OpenSearchTestCaseWithDummyTransport):
    async def test_our_transport_used(self) -> None:
        assert isinstance(self.client.transport, DummyTransport)

    async def test_start_with_0_call(self) -> None:
        self.assert_call_count_equals(0)

    async def test_each_call_is_recorded(self) -> None:
        await self.client.transport.perform_request("GET", "/")
        await self.client.transport.perform_request(
            "DELETE", "/42", params={}, body="body"
        )
        self.assert_call_count_equals(2)
        assert [({}, None, "body")] == self.assert_url_called("DELETE", "/42", 1)
