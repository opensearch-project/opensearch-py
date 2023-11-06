# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import pytest
from _pytest.mark.structures import MarkDecorator
from pytest import raises

from opensearchpy import exceptions
from opensearchpy._async.helpers import mapping
from opensearchpy.helpers import analysis

pytestmark: MarkDecorator = pytest.mark.asyncio


async def test_mapping_saved_into_opensearch(write_client) -> None:
    m = mapping.AsyncMapping()
    m.field(
        "name", "text", analyzer=analysis.analyzer("my_analyzer", tokenizer="keyword")
    )
    m.field("tags", "keyword")
    await m.save("test-mapping", using=write_client)

    assert {
        "test-mapping": {
            "mappings": {
                "properties": {
                    "name": {"type": "text", "analyzer": "my_analyzer"},
                    "tags": {"type": "keyword"},
                }
            }
        }
    } == await write_client.indices.get_mapping(index="test-mapping")


async def test_mapping_saved_into_opensearch_when_index_already_exists_closed(
    write_client,
) -> None:
    m = mapping.AsyncMapping()
    m.field(
        "name", "text", analyzer=analysis.analyzer("my_analyzer", tokenizer="keyword")
    )
    await write_client.indices.create(index="test-mapping")

    with raises(exceptions.IllegalOperation):
        await m.save("test-mapping", using=write_client)

    await write_client.cluster.health(index="test-mapping", wait_for_status="yellow")
    await write_client.indices.close(index="test-mapping")
    await m.save("test-mapping", using=write_client)

    assert {
        "test-mapping": {
            "mappings": {
                "properties": {"name": {"type": "text", "analyzer": "my_analyzer"}}
            }
        }
    } == await write_client.indices.get_mapping(index="test-mapping")


async def test_mapping_saved_into_opensearch_when_index_already_exists_with_analysis(
    write_client,
) -> None:
    m = mapping.AsyncMapping()
    analyzer = analysis.analyzer("my_analyzer", tokenizer="keyword")
    m.field("name", "text", analyzer=analyzer)

    new_analysis = analyzer.get_analysis_definition()
    new_analysis["analyzer"]["other_analyzer"] = {
        "type": "custom",
        "tokenizer": "whitespace",
    }
    await write_client.indices.create(
        index="test-mapping", body={"settings": {"analysis": new_analysis}}
    )

    m.field("title", "text", analyzer=analyzer)
    await m.save("test-mapping", using=write_client)

    assert {
        "test-mapping": {
            "mappings": {
                "properties": {
                    "name": {"type": "text", "analyzer": "my_analyzer"},
                    "title": {"type": "text", "analyzer": "my_analyzer"},
                }
            }
        }
    } == await write_client.indices.get_mapping(index="test-mapping")


async def test_mapping_gets_updated_from_opensearch(write_client):
    await write_client.indices.create(
        index="test-mapping",
        body={
            "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            "mappings": {
                "date_detection": False,
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "snowball",
                        "fields": {"raw": {"type": "keyword"}},
                    },
                    "created_at": {"type": "date"},
                    "comments": {
                        "type": "nested",
                        "properties": {
                            "created": {"type": "date"},
                            "author": {
                                "type": "text",
                                "analyzer": "snowball",
                                "fields": {"raw": {"type": "keyword"}},
                            },
                        },
                    },
                },
            },
        },
    )

    m = await mapping.AsyncMapping.from_opensearch("test-mapping", using=write_client)

    assert ["comments", "created_at", "title"] == list(
        sorted(m.properties.properties._d_.keys())
    )
    assert {
        "date_detection": False,
        "properties": {
            "comments": {
                "type": "nested",
                "properties": {
                    "created": {"type": "date"},
                    "author": {
                        "analyzer": "snowball",
                        "fields": {"raw": {"type": "keyword"}},
                        "type": "text",
                    },
                },
            },
            "created_at": {"type": "date"},
            "title": {
                "analyzer": "snowball",
                "fields": {"raw": {"type": "keyword"}},
                "type": "text",
            },
        },
    } == m.to_dict()

    # test same with alias
    await write_client.indices.put_alias(index="test-mapping", name="test-alias")

    m2 = await mapping.AsyncMapping.from_opensearch("test-alias", using=write_client)
    assert m2.to_dict() == m.to_dict()
