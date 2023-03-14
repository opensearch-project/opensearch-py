# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import pytest

from opensearchpy import Date, Text
from opensearchpy._async.helpers.document import AsyncDocument
from opensearchpy._async.helpers.index import AsyncIndex, AsyncIndexTemplate
from opensearchpy.helpers import analysis

pytestmark = pytest.mark.asyncio


class Post(AsyncDocument):
    title = Text(analyzer=analysis.analyzer("my_analyzer", tokenizer="keyword"))
    published_from = Date()


async def test_index_template_works(write_client):
    it = AsyncIndexTemplate("test-template", "test-*")
    it.document(Post)
    it.settings(number_of_replicas=0, number_of_shards=1)
    await it.save()

    i = AsyncIndex("test-blog")
    await i.create()

    assert {
        "test-blog": {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "my_analyzer"},
                    "published_from": {"type": "date"},
                }
            }
        }
    } == await write_client.indices.get_mapping(index="test-blog")


async def test_index_can_be_saved_even_with_settings(write_client):
    i = AsyncIndex("test-blog", using=write_client)
    i.settings(number_of_shards=3, number_of_replicas=0)
    await i.save()
    i.settings(number_of_replicas=1)
    await i.save()

    assert (
        "1"
        == (await i.get_settings())["test-blog"]["settings"]["index"][
            "number_of_replicas"
        ]
    )


async def test_index_exists(data_client):
    assert await AsyncIndex("git").exists()
    assert not await AsyncIndex("not-there").exists()


async def test_index_can_be_created_with_settings_and_mappings(write_client):
    i = AsyncIndex("test-blog", using=write_client)
    i.document(Post)
    i.settings(number_of_replicas=0, number_of_shards=1)
    await i.create()

    assert {
        "test-blog": {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "my_analyzer"},
                    "published_from": {"type": "date"},
                }
            }
        }
    } == await write_client.indices.get_mapping(index="test-blog")

    settings = await write_client.indices.get_settings(index="test-blog")
    assert settings["test-blog"]["settings"]["index"]["number_of_replicas"] == "0"
    assert settings["test-blog"]["settings"]["index"]["number_of_shards"] == "1"
    assert settings["test-blog"]["settings"]["index"]["analysis"] == {
        "analyzer": {"my_analyzer": {"type": "custom", "tokenizer": "keyword"}}
    }


async def test_delete(write_client):
    await write_client.indices.create(
        index="test-index",
        body={"settings": {"number_of_replicas": 0, "number_of_shards": 1}},
    )

    i = AsyncIndex("test-index", using=write_client)
    await i.delete()
    assert not await write_client.indices.exists(index="test-index")


async def test_multiple_indices_with_same_doc_type_work(write_client):
    i1 = AsyncIndex("test-index-1", using=write_client)
    i2 = AsyncIndex("test-index-2", using=write_client)

    for i in i1, i2:
        i.document(Post)
        await i.create()

    for i in ("test-index-1", "test-index-2"):
        settings = await write_client.indices.get_settings(index=i)
        assert settings[i]["settings"]["index"]["analysis"] == {
            "analyzer": {"my_analyzer": {"type": "custom", "tokenizer": "keyword"}}
        }
