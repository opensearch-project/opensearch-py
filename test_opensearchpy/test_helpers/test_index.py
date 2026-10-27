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

import string
from random import choice
from typing import Any

from pytest import raises

from opensearchpy import Date, Document, Index, IndexTemplate, Text, analyzer


class Post(Document):
    title = Text()
    published_from = Date()


def test_multiple_doc_types_will_combine_mappings() -> None:
    class User(Document):
        username = Text()

    i = Index("i")
    i.document(Post)
    i.document(User)
    assert {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "username": {"type": "text"},
                "published_from": {"type": "date"},
            }
        }
    } == i.to_dict()


def test_search_is_limited_to_index_name() -> None:
    i = Index("my-index")
    s = i.search()

    assert s._index == ["my-index"]


def test_cloned_index_has_copied_settings_and_using() -> None:
    client = object()
    i: Any = Index("my-index", using=client)
    i.settings(number_of_shards=1)

    i2 = i.clone("my-other-index")

    assert "my-other-index" == i2._name
    assert client is i2._using
    assert i._settings == i2._settings
    assert i._settings is not i2._settings


def test_cloned_index_has_analysis_attribute() -> None:
    """
    Regression test for Issue #582 in which `Index.clone()` was not copying
    over the `_analysis` attribute.
    """
    client = object()
    i: Any = Index("my-index", using=client)

    random_analyzer_name = "".join(choice(string.ascii_letters) for _ in range(100))
    random_analyzer = analyzer(
        random_analyzer_name, tokenizer="standard", filter="standard"
    )

    i.analyzer(random_analyzer)

    i2 = i.clone("my-clone-index")

    assert i.to_dict()["settings"]["analysis"] == i2.to_dict()["settings"]["analysis"]


def test_settings_are_saved() -> None:
    i: Any = Index("i")
    i.settings(number_of_replicas=0)
    i.settings(number_of_shards=1)

    assert {"settings": {"number_of_shards": 1, "number_of_replicas": 0}} == i.to_dict()


def test_registered_doc_type_included_in_to_dict() -> None:
    i: Any = Index("i", using="alias")
    i.document(Post)

    assert {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "published_from": {"type": "date"},
            }
        }
    } == i.to_dict()


def test_registered_doc_type_included_in_search() -> None:
    i: Any = Index("i", using="alias")
    i.document(Post)

    s = i.search()

    assert s._doc_type == [Post]


def test_aliases_add_to_object() -> None:
    random_alias = "".join(choice(string.ascii_letters) for _ in range(100))
    alias_dict: Any = {random_alias: {}}

    index: Any = Index("i", using="alias")
    index.aliases(**alias_dict)

    assert index._aliases == alias_dict


def test_aliases_returned_from_to_dict() -> None:
    random_alias = "".join(choice(string.ascii_letters) for _ in range(100))
    alias_dict: Any = {random_alias: {}}

    index: Any = Index("i", using="alias")
    index.aliases(**alias_dict)

    assert index._aliases == index.to_dict()["aliases"] == alias_dict


def test_analyzers_added_to_object() -> None:
    random_analyzer_name = "".join(choice(string.ascii_letters) for _ in range(100))
    random_analyzer = analyzer(
        random_analyzer_name, tokenizer="standard", filter="standard"
    )

    index: Any = Index("i", using="alias")
    index.analyzer(random_analyzer)

    assert index._analysis["analyzer"][random_analyzer_name] == {
        "filter": ["standard"],
        "type": "custom",
        "tokenizer": "standard",
    }


def test_analyzers_returned_from_to_dict() -> None:
    random_analyzer_name = "".join(choice(string.ascii_letters) for _ in range(100))
    random_analyzer = analyzer(
        random_analyzer_name, tokenizer="standard", filter="standard"
    )
    index: Any = Index("i", using="alias")
    index.analyzer(random_analyzer)

    assert index.to_dict()["settings"]["analysis"]["analyzer"][
        random_analyzer_name
    ] == {"filter": ["standard"], "type": "custom", "tokenizer": "standard"}


def test_conflicting_analyzer_raises_error() -> None:
    i: Any = Index("i")
    i.analyzer("my_analyzer", tokenizer="whitespace", filter=["lowercase", "stop"])

    with raises(ValueError):
        i.analyzer("my_analyzer", tokenizer="keyword", filter=["lowercase", "stop"])


def test_index_template_can_have_order() -> None:
    i: Any = Index("i-*")
    it = i.as_template("i", order=2)

    assert {"index_patterns": ["i-*"], "order": 2} == it.to_dict()


def test_index_template_save_result(mock_client: Any) -> None:
    it: Any = IndexTemplate("test-template", "test-*")

    assert it.save(using="mock") == mock_client.indices.put_template()


def test_save_does_not_raise_on_matching_analysis_with_string_typed_server_values(
    mock_client: Any,
) -> None:
    """
    Regression test for https://github.com/opensearch-project/opensearch-py/issues/882.

    OpenSearch returns analysis settings values as strings (e.g. ``'3'`` for the
    integer ``3``, ``'false'`` for the boolean ``False``).  Index.save() must not
    raise IllegalOperation when those string-typed server values logically match
    the Python-typed values defined in the index settings.
    """
    from opensearchpy.exceptions import IllegalOperation

    i: Any = Index("test-index", using="mock")
    i.settings(
        analysis={
            "filter": {
                "my_shingles": {
                    "type": "shingle",
                    "min_shingle_size": 2,
                    "max_shingle_size": 3,
                    "output_unigrams": False,
                }
            }
        }
    )

    # OpenSearch returns all numeric/boolean values as strings.
    mock_client.indices.exists.return_value = True
    mock_client.indices.get_settings.return_value = {
        "test-index": {
            "settings": {
                "index": {
                    "analysis": {
                        "filter": {
                            "my_shingles": {
                                "type": "shingle",
                                "min_shingle_size": "2",
                                "max_shingle_size": "3",
                                "output_unigrams": "false",
                            }
                        }
                    }
                }
            }
        }
    }
    mock_client.cluster.state.return_value = {
        "metadata": {"indices": {"test-index": {"state": "open"}}}
    }

    # Before the fix this raised IllegalOperation because "2" != 2 etc.
    try:
        i.save(using="mock")
    except IllegalOperation:
        raise AssertionError(
            "Index.save() raised IllegalOperation even though the analysis "
            "configuration already matches (types differed only as str vs int/bool)"
        )
