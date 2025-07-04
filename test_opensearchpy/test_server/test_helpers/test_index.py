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

from opensearchpy import Date, Document, Index, IndexTemplate, Text
from opensearchpy.exceptions import ValidationException
from opensearchpy.helpers import analysis


class Post(Document):
    title = Text(analyzer=analysis.analyzer("my_analyzer", tokenizer="keyword"))
    published_from = Date()


def test_index_template_works(write_client: Any) -> None:
    it = IndexTemplate("test-template", "test-*")
    it.document(Post)
    it.settings(number_of_replicas=0, number_of_shards=1)
    it.save()

    i = Index("test-blog")
    i.create()

    assert {
        "test-blog": {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "my_analyzer"},
                    "published_from": {"type": "date"},
                }
            }
        }
    } == write_client.indices.get_mapping(index="test-blog")


def test_index_can_be_saved_even_with_settings(write_client: Any) -> None:
    i = Index(name="test-blog", using=write_client)
    i.settings(number_of_shards=3, number_of_replicas=0)
    i.save()
    i.settings(number_of_replicas=1)
    i.save()

    assert (
        "1" == i.get_settings()["test-blog"]["settings"]["index"]["number_of_replicas"]
    )


def test_index_exists(data_client: Any) -> None:
    assert Index("git").exists()
    assert not Index("not-there").exists()


def test_index_can_be_created_with_settings_and_mappings(write_client: Any) -> None:
    i = Index(name="test-blog", using=write_client)
    i.document(Post)
    i.settings(number_of_replicas=0, number_of_shards=1)
    i.create()

    assert {
        "test-blog": {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "my_analyzer"},
                    "published_from": {"type": "date"},
                }
            }
        }
    } == write_client.indices.get_mapping(index="test-blog")

    settings = write_client.indices.get_settings(index="test-blog")
    assert settings["test-blog"]["settings"]["index"]["number_of_replicas"] == "0"
    assert settings["test-blog"]["settings"]["index"]["number_of_shards"] == "1"
    assert settings["test-blog"]["settings"]["index"]["analysis"] == {
        "analyzer": {"my_analyzer": {"type": "custom", "tokenizer": "keyword"}}
    }


def test_delete(write_client: Any) -> None:
    write_client.indices.create(
        index="test-index",
        body={"settings": {"number_of_replicas": 0, "number_of_shards": 1}},
    )

    i = Index("test-index", using=write_client)
    i.delete()
    assert not write_client.indices.exists(index="test-index")


def test_multiple_indices_with_same_doc_type_work(write_client: Any) -> None:
    i1 = Index("test-index-1", using=write_client)
    i2 = Index("test-index-2", using=write_client)

    for i in (i1, i2):
        i.document(Post)
        i.create()

    for j in ("test-index-1", "test-index-2"):
        settings = write_client.indices.get_settings(index=j)
        assert settings[j]["settings"]["index"]["analysis"] == {
            "analyzer": {"my_analyzer": {"type": "custom", "tokenizer": "keyword"}}
        }


def test_index_can_be_saved_through_alias_with_settings(write_client: Any) -> None:
    raw_index = Index("test-blog", using=write_client)
    raw_index.settings(number_of_shards=3, number_of_replicas=0)
    raw_index.aliases(**{"blog-alias": {}})
    raw_index.save()

    i = Index("blog-alias", using=write_client)
    i.settings(number_of_replicas=1)
    i.save()

    assert (
        "1"
        == raw_index.get_settings()["test-blog"]["settings"]["index"][
            "number_of_replicas"
        ]
    )


def test_validation_alias_has_many_indices(write_client: Any) -> None:
    raw_index_1 = Index("test-blog-1", using=write_client)
    raw_index_1.settings(number_of_shards=3, number_of_replicas=0)
    raw_index_1.aliases(**{"blog-alias": {}})
    raw_index_1.save()

    raw_index_2 = Index("test-blog-2", using=write_client)
    raw_index_2.settings(number_of_shards=3, number_of_replicas=0)
    raw_index_2.aliases(**{"blog-alias": {}})
    raw_index_2.save()

    i = Index("blog-alias", using=write_client)
    with pytest.raises(ValidationException) as e:
        i.save()

    message, indices = e.value.args[0][:-1].split(": ")
    assert message == "Settings for blog-alias point to multiple indices"
    assert set(indices.split(", ")) == {"test-blog-1", "test-blog-2"}
