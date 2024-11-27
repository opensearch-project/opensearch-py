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


from typing import Any

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy.exceptions import RequestError

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestSpecialCharacters:
    async def test_index_with_slash(self, async_client: Any) -> None:
        index_name = "movies/shmovies"
        with pytest.raises(RequestError) as e:
            await async_client.indices.create(index=index_name)
        assert (
            str(e.value)
            == "RequestError(400, 'invalid_index_name_exception', 'Invalid index name [movies/shmovies], must not contain the following characters [ , \", *, \\\\, <, |, ,, >, /, ?]')"
        )


class TestUnicode:
    async def test_indices_lifecycle_english(self, async_client: Any) -> None:
        index_name = "movies"

        index_create_result = await async_client.indices.create(index=index_name)
        assert index_create_result["acknowledged"] is True
        assert index_name == index_create_result["index"]

        document = {"name": "Solaris", "director": "Andrei Tartakovsky", "year": "2011"}
        id = "solaris@2011"
        doc_insert_result = await async_client.index(
            index=index_name, body=document, id=id, refresh=True
        )
        assert "created" == doc_insert_result["result"]
        assert index_name == doc_insert_result["_index"]
        assert id == doc_insert_result["_id"]

        doc_delete_result = await async_client.delete(index=index_name, id=id)
        assert "deleted" == doc_delete_result["result"]
        assert index_name == doc_delete_result["_index"]
        assert id == doc_delete_result["_id"]

        index_delete_result = await async_client.indices.delete(index=index_name)
        assert index_delete_result["acknowledged"] is True

    async def test_indices_lifecycle_russian(self, async_client: Any) -> None:
        index_name = "кино"
        index_create_result = await async_client.indices.create(index=index_name)
        assert index_create_result["acknowledged"] is True
        assert index_name == index_create_result["index"]

        document = {"название": "Солярис", "автор": "Андрей Тарковский", "год": "2011"}
        id = "соларис@2011"
        doc_insert_result = await async_client.index(
            index=index_name, body=document, id=id, refresh=True
        )
        assert "created" == doc_insert_result["result"]
        assert index_name == doc_insert_result["_index"]
        assert id == doc_insert_result["_id"]

        doc_delete_result = await async_client.delete(index=index_name, id=id)
        assert "deleted" == doc_delete_result["result"]
        assert index_name == doc_delete_result["_index"]
        assert id == doc_delete_result["_id"]

        index_delete_result = await async_client.indices.delete(index=index_name)
        assert index_delete_result["acknowledged"] is True

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
