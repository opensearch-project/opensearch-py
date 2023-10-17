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


from collections import defaultdict

import pytest

from opensearchpy import AsyncOpenSearch

pytestmark = pytest.mark.asyncio


class DummyTransport(object):
    def __init__(self, hosts, responses=None, **kwargs):
        self.hosts = hosts
        self.responses = responses
        self.call_count = 0
        self.calls = defaultdict(list)

    async def perform_request(self, method, url, params=None, headers=None, body=None):
        resp = 200, {}
        if self.responses:
            resp = self.responses[self.call_count]
        self.call_count += 1
        self.calls[(method, url)].append((params, headers, body))
        return resp


class OpenSearchTestCase:
    def assert_call_count_equals(self, count):
        assert count == self.client.transport.call_count

    def assert_url_called(self, method, url, count=1):
        assert (method, url) in self.client.transport.calls
        calls = self.client.transport.calls[(method, url)]
        assert count == len(calls)
        return calls


class TestOpenSearchTestCase(OpenSearchTestCase):
    def setup_method(self):
        self.client = AsyncOpenSearch(transport_class=DummyTransport)

    async def test_our_transport_used(self):
        assert isinstance(self.client.transport, DummyTransport)

    async def test_start_with_0_call(self):
        self.assert_call_count_equals(0)

    async def test_each_call_is_recorded(self):
        await self.client.transport.perform_request("GET", "/")
        await self.client.transport.perform_request(
            "DELETE", "/42", params={}, body="body"
        )
        self.assert_call_count_equals(2)
        assert [({}, None, "body")] == self.assert_url_called("DELETE", "/42", 1)

    @pytest.mark.asyncio
    async def test_get(self):
        await self.client._get("/")
        self.assert_call_count_equals(1)
        assert [(None, None, None)] == self.assert_url_called("GET", "/", 1)

    async def test_head(self):
        await self.client._head("/")
        self.assert_call_count_equals(1)
        assert [(None, None, None)] == self.assert_url_called("HEAD", "/", 1)

    async def test_put(self):
        await self.client._put("/xyz", {"X": "Y"}, "body")
        self.assert_call_count_equals(1)
        assert [("body", {"X": " =="}, None)], self.assert_url_called("PUT", "/xyz", 1)

    async def test_post(self):
        await self.client._post("/xyz", {"X": "Y"}, "body")
        self.assert_call_count_equals(1)
        assert [("body", {"X": " =="}, None)], self.assert_url_called("POST", "/xyz", 1)

    async def test_delete(self):
        await self.client._delete("/xyz", {"X": "Y"}, "body")
        self.assert_call_count_equals(1)
        assert [("body", {"X": " =="}, None)], self.assert_url_called(
            "DELETE", "/xyz", 1
        )
