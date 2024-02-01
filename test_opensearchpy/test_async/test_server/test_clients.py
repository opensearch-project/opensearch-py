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


from __future__ import unicode_literals

from typing import Any

import pytest
from _pytest.mark.structures import MarkDecorator

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestUnicode:
    async def test_indices_analyze(self, async_client: Any) -> None:
        await async_client.indices.analyze(body='{"text": "привет"}')


class TestBulk:
    async def test_bulk_works_with_string_body(self, async_client: Any) -> None:
        docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
        response = await async_client.bulk(body=docs)

        assert response["errors"] is False
        assert len(response["items"]) == 1

    async def test_bulk_works_with_bytestring_body(self, async_client: Any) -> None:
        docs = b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}'
        response = await async_client.bulk(body=docs)

        assert response["errors"] is False
        assert len(response["items"]) == 1


class TestYarlMissing:
    async def test_aiohttp_connection_works_without_yarl(
        self, async_client: Any, monkeypatch: Any
    ) -> None:
        """
        This is a defensive test case for if aiohttp suddenly stops using yarl.
        """
        from opensearchpy._async import http_aiohttp

        monkeypatch.setattr(http_aiohttp, "yarl", False)

        resp = await async_client.info(pretty=True)
        assert isinstance(resp, dict)


class TestClose:
    async def test_close_doesnt_break_client(self, async_client: Any) -> None:
        await async_client.cluster.health()
        await async_client.close()
        await async_client.cluster.health()

    async def test_with_doesnt_break_client(self, async_client: Any) -> None:
        for _ in range(2):
            async with async_client as client:
                await client.cluster.health()
