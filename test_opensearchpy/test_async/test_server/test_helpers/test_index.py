# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy import Date, Text
from opensearchpy._async.helpers.document import AsyncDocument
from opensearchpy._async.helpers.index import AsyncIndex, AsyncIndexTemplate
from opensearchpy.exceptions import ValidationException
from opensearchpy.helpers import analysis

pytestmark: MarkDecorator = pytest.mark.asyncio


class Post(AsyncDocument):
    title = Text(analyzer=analysis.analyzer("my_analyzer", tokenizer="keyword"))
    published_from = Date()


async def test_index_template_works(write_client: Any) -> None:
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


async def test_index_can_be_saved_even_with_settings(write_client: Any) -> None:
    i = AsyncIndex(name="test-blog", using=write_client)
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


async def test_index_exists(data_client: Any) -> None:
    assert await AsyncIndex("git").exists()
    assert not await AsyncIndex("not-there").exists()


async def test_index_can_be_created_with_settings_and_mappings(
    write_client: Any,
) -> None:
    i = AsyncIndex(name="test-blog", using=write_client)
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


async def test_delete(write_client: Any) -> None:
    await write_client.indices.create(
        index="test-index",
        body={"settings": {"number_of_replicas": 0, "number_of_shards": 1}},
    )

    i = AsyncIndex("test-index", using=write_client)
    await i.delete()
    assert not await write_client.indices.exists(index="test-index")


async def test_multiple_indices_with_same_doc_type_work(write_client: Any) -> None:
    i1: Any = AsyncIndex("test-index-1", using=write_client)
    i2: Any = AsyncIndex("test-index-2", using=write_client)

    for i in i1, i2:
        i.document(Post)
        await i.create()

    for i in ("test-index-1", "test-index-2"):
        settings = await write_client.indices.get_settings(index=i)
        assert settings[i]["settings"]["index"]["analysis"] == {
            "analyzer": {"my_analyzer": {"type": "custom", "tokenizer": "keyword"}}
        }


async def test_index_can_be_saved_through_alias_with_settings(
    write_client: Any,
) -> None:
    raw_index = AsyncIndex("test-blog", using=write_client)
    raw_index.settings(number_of_shards=3, number_of_replicas=0)
    raw_index.aliases(**{"blog-alias": {}})
    await raw_index.save()

    i = AsyncIndex("blog-alias", using=write_client)
    i.settings(number_of_replicas=1)
    await i.save()

    settings = await write_client.indices.get_settings(index="test-blog")
    assert "1" == settings["test-blog"]["settings"]["index"]["number_of_replicas"]


async def test_validation_alias_has_many_indices(write_client: Any) -> None:
    raw_index_1 = AsyncIndex("test-blog-1", using=write_client)
    raw_index_1.settings(number_of_shards=3, number_of_replicas=0)
    raw_index_1.aliases(**{"blog-alias": {}})
    await raw_index_1.save()

    raw_index_2 = AsyncIndex("test-blog-2", using=write_client)
    raw_index_2.settings(number_of_shards=3, number_of_replicas=0)
    raw_index_2.aliases(**{"blog-alias": {}})
    await raw_index_2.save()

    i = AsyncIndex("blog-alias", using=write_client)
    with pytest.raises(ValidationException) as e:
        await i.save()

    message, indices = e.value.args[0][:-1].split(": ")
    assert message == "Settings for blog-alias point to multiple indices"
    assert set(indices.split(", ")) == {"test-blog-1", "test-blog-2"}
