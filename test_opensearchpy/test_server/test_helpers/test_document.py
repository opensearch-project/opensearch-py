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

from datetime import datetime
from ipaddress import ip_address
from typing import Any

import pytest
from pytest import raises
from pytz import timezone

from opensearchpy import (
    Binary,
    Boolean,
    ConflictError,
    Date,
    Document,
    Double,
    InnerDoc,
    Ip,
    Keyword,
    Long,
    Mapping,
    MetaField,
    Nested,
    NotFoundError,
    Object,
    Q,
    RankFeatures,
    Text,
    analyzer,
)
from opensearchpy.helpers.utils import AttrList

snowball = analyzer("my_snow", tokenizer="standard", filter=["lowercase", "snowball"])


class User(InnerDoc):
    name = Text(fields={"raw": Keyword()})


class Wiki(Document):
    owner = Object(User)
    views = Long()
    ranked = RankFeatures()

    class Index:
        name = "test-wiki"


class Repository(Document):
    owner = Object(User)
    created_at = Date()
    description = Text(analyzer=snowball)
    tags = Keyword()

    @classmethod
    def search(cls, using: Any = None, index: Any = None) -> Any:
        return super().search().filter("term", commit_repo="repo")

    class Index:
        name = "git"


class Commit(Document):
    committed_date = Date()
    authored_date = Date()
    description = Text(analyzer=snowball)

    class Index:
        name = "flat-git"

    class Meta:
        mapping = Mapping()


class History(InnerDoc):
    timestamp = Date()
    diff = Text()


class Comment(InnerDoc):
    content = Text()
    created_at = Date()
    author = Object(User)
    history = Nested(History)

    class Meta:
        dynamic = MetaField(False)


class PullRequest(Document):
    comments = Nested(Comment)
    created_at = Date()

    class Index:
        name = "test-prs"


class SerializationDoc(Document):
    i = Long()
    b = Boolean()
    d = Double()
    bin = Binary()
    ip = Ip()

    class Index:
        name = "test-serialization"


def test_serialization(write_client: Any) -> None:
    SerializationDoc.init()
    write_client.index(
        index="test-serialization",
        id=42,
        body={
            "i": [1, 2, "3", None],
            "b": [True, False, "true", "false", None],
            "d": [0.1, "-0.1", None],
            "bin": ["SGVsbG8gV29ybGQ=", None],
            "ip": ["::1", "127.0.0.1", None],
        },
    )
    sd = SerializationDoc.get(id=42)

    assert sd.i == [1, 2, 3, None]
    assert sd.b == [True, False, True, False, None]
    assert sd.d == [0.1, -0.1, None]
    assert sd.bin == [b"Hello World", None]
    assert sd.ip == [ip_address("::1"), ip_address("127.0.0.1"), None]

    assert sd.to_dict() == {
        "b": [True, False, True, False, None],
        "bin": ["SGVsbG8gV29ybGQ=", None],
        "d": [0.1, -0.1, None],
        "i": [1, 2, 3, None],
        "ip": ["::1", "127.0.0.1", None],
    }


def test_nested_inner_hits_are_wrapped_properly(pull_request: Any) -> None:
    history_query = Q(
        "nested",
        path="comments.history",
        inner_hits={},
        query=Q("match", comments__history__diff="ahoj"),
    )
    s = PullRequest.search().query(
        "nested", inner_hits={}, path="comments", query=history_query
    )

    response = s.execute()
    pr = response.hits[0]
    assert isinstance(pr, PullRequest)
    assert isinstance(pr.comments[0], Comment)
    assert isinstance(pr.comments[0].history[0], History)

    comment = pr.meta.inner_hits.comments.hits[0]
    assert isinstance(comment, Comment)
    assert comment.author.name == "honzakral"
    assert isinstance(comment.history[0], History)

    history = comment.meta.inner_hits["comments.history"].hits[0]
    assert isinstance(history, History)
    assert history.timestamp == datetime(2012, 1, 1)
    assert "score" in history.meta


def test_nested_inner_hits_are_deserialized_properly(pull_request: Any) -> None:
    s = PullRequest.search().query(
        "nested",
        inner_hits={},
        path="comments",
        query=Q("match", comments__content="hello"),
    )

    response = s.execute()
    pr = response.hits[0]
    assert isinstance(pr.created_at, datetime)
    assert isinstance(pr.comments[0], Comment)
    assert isinstance(pr.comments[0].created_at, datetime)


def test_nested_top_hits_are_wrapped_properly(pull_request: Any) -> None:
    s = PullRequest.search()
    s.aggs.bucket("comments", "nested", path="comments").metric(
        "hits", "top_hits", size=1
    )

    r = s.execute()

    print(r._d_)
    assert isinstance(r.aggregations.comments.hits.hits[0], Comment)


def test_update_object_field(write_client: Any) -> None:
    Wiki.init()
    w = Wiki(
        owner=User(name="Honza Kral"),
        _id="opensearch-py",
        ranked={"test1": 0.1, "topic2": 0.2},
    )
    w.save()

    assert "updated" == w.update(owner=[{"name": "Honza"}, {"name": "Nick"}])
    assert w.owner[0].name == "Honza"
    assert w.owner[1].name == "Nick"

    w = Wiki.get(id="opensearch-py")
    assert w.owner[0].name == "Honza"
    assert w.owner[1].name == "Nick"

    assert w.ranked == {"test1": 0.1, "topic2": 0.2}


def test_update_script(write_client: Any) -> None:
    Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    w.save()

    w.update(script="ctx._source.views += params.inc", inc=5)
    w = Wiki.get(id="opensearch-py")
    assert w.views == 47


def test_update_retry_on_conflict(write_client: Any) -> None:
    Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    w.save()

    w1 = Wiki.get(id="opensearch-py")
    w2 = Wiki.get(id="opensearch-py")
    w1.update(script="ctx._source.views += params.inc", inc=5, retry_on_conflict=1)
    w2.update(script="ctx._source.views += params.inc", inc=5, retry_on_conflict=1)

    w = Wiki.get(id="opensearch-py")
    assert w.views == 52


@pytest.mark.parametrize("retry_on_conflict", [None, 0])  # type: ignore
def test_update_conflicting_version(write_client: Any, retry_on_conflict: int) -> None:
    Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    w.save()

    w1 = Wiki.get(id="opensearch-py")
    w2 = Wiki.get(id="opensearch-py")
    w1.update(script="ctx._source.views += params.inc", inc=5)

    with raises(ConflictError):
        w2.update(
            script="ctx._source.views += params.inc",
            inc=5,
            retry_on_conflict=retry_on_conflict,
        )


def test_save_and_update_return_doc_meta(write_client: Any) -> None:
    Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    resp = w.save(return_doc_meta=True)
    assert resp["_index"] == "test-wiki"
    assert resp["result"] == "created"
    assert "_id" in resp.keys()
    assert "_primary_term" in resp.keys()
    assert "_seq_no" in resp.keys()
    assert "_shards" in resp.keys()
    assert "_version" in resp.keys()

    resp = w.update(
        script="ctx._source.views += params.inc", inc=5, return_doc_meta=True
    )
    assert resp["_index"] == "test-wiki"
    assert resp["result"] == "updated"
    assert "_id" in resp.keys()
    assert "_primary_term" in resp.keys()
    assert "_seq_no" in resp.keys()
    assert "_shards" in resp.keys()
    assert "_version" in resp.keys()


def test_init(write_client: Any) -> None:
    Repository.init(index="test-git")

    assert write_client.indices.exists(index="test-git")


def test_get_raises_404_on_index_missing(data_client: Any) -> None:
    with raises(NotFoundError):
        Repository.get("opensearch-dsl-php", index="not-there")


def test_get_raises_404_on_non_existent_id(data_client: Any) -> None:
    with raises(NotFoundError):
        Repository.get("opensearch-dsl-php")


def test_get_returns_none_if_404_ignored(data_client: Any) -> None:
    assert None is Repository.get("opensearch-dsl-php", ignore=404)


def test_get_returns_none_if_404_ignored_and_index_doesnt_exist(
    data_client: Any,
) -> None:
    assert None is Repository.get("42", index="not-there", ignore=404)


def test_get(data_client: Any) -> None:
    opensearch_repo = Repository.get("opensearch-py")

    assert isinstance(opensearch_repo, Repository)
    assert opensearch_repo.owner.name == "opensearch"
    assert datetime(2014, 3, 3) == opensearch_repo.created_at


def test_exists_return_true(data_client: Any) -> None:
    assert Repository.exists("opensearch-py")


def test_exists_false(data_client: Any) -> None:
    assert not Repository.exists("opensearch-dsl-php")


def test_get_with_tz_date(data_client: Any) -> None:
    first_commit = Commit.get(
        id="3ca6e1e73a071a705b4babd2f581c91a2a3e5037", routing="opensearch-py"
    )

    tzinfo = timezone("Europe/Prague")
    assert (
        tzinfo.localize(datetime(2014, 5, 2, 13, 47, 19, 123000))
        == first_commit.authored_date
    )


def test_save_with_tz_date(data_client: Any) -> None:
    tzinfo = timezone("Europe/Prague")
    first_commit = Commit.get(
        id="3ca6e1e73a071a705b4babd2f581c91a2a3e5037", routing="opensearch-py"
    )
    first_commit.committed_date = tzinfo.localize(
        datetime(2014, 5, 2, 13, 47, 19, 123456)
    )
    first_commit.save()

    first_commit = Commit.get(
        id="3ca6e1e73a071a705b4babd2f581c91a2a3e5037", routing="opensearch-py"
    )
    assert (
        tzinfo.localize(datetime(2014, 5, 2, 13, 47, 19, 123456))
        == first_commit.committed_date
    )


COMMIT_DOCS_WITH_MISSING = [
    {"_id": "0"},  # Missing
    {"_id": "3ca6e1e73a071a705b4babd2f581c91a2a3e5037"},  # Existing
    {"_id": "f"},  # Missing
    {"_id": "eb3e543323f189fd7b698e66295427204fff5755"},  # Existing
]


def test_mget(data_client: Any) -> None:
    commits = Commit.mget(docs=COMMIT_DOCS_WITH_MISSING)
    assert commits[0] is None
    assert commits[1].meta.id == "3ca6e1e73a071a705b4babd2f581c91a2a3e5037"
    assert commits[2] is None
    assert commits[3].meta.id == "eb3e543323f189fd7b698e66295427204fff5755"


def test_mget_raises_exception_when_missing_param_is_invalid(data_client: Any) -> None:
    with raises(ValueError):
        Commit.mget(docs=COMMIT_DOCS_WITH_MISSING, missing="raj")


def test_mget_raises_404_when_missing_param_is_raise(data_client: Any) -> None:
    with raises(NotFoundError):
        Commit.mget(docs=COMMIT_DOCS_WITH_MISSING, missing="raise")


def test_mget_ignores_missing_docs_when_missing_param_is_skip(data_client: Any) -> None:
    commits = Commit.mget(docs=COMMIT_DOCS_WITH_MISSING, missing="skip")
    assert commits[0].meta.id == "3ca6e1e73a071a705b4babd2f581c91a2a3e5037"
    assert commits[1].meta.id == "eb3e543323f189fd7b698e66295427204fff5755"


def test_update_works_from_search_response(data_client: Any) -> None:
    opensearch_repo = Repository.search().execute()[0]

    opensearch_repo.update(owner={"other_name": "opensearchpy"})
    assert "opensearchpy" == opensearch_repo.owner.other_name

    new_version = Repository.get("opensearch-py")
    assert "opensearchpy" == new_version.owner.other_name
    assert "opensearch" == new_version.owner.name


def test_update(data_client: Any) -> None:
    opensearch_repo = Repository.get("opensearch-py")
    v = opensearch_repo.meta.version

    old_seq_no = opensearch_repo.meta.seq_no
    opensearch_repo.update(
        owner={"new_name": "opensearchpy"}, new_field="testing-update"
    )

    assert "opensearchpy" == opensearch_repo.owner.new_name
    assert "testing-update" == opensearch_repo.new_field

    # assert version has been updated
    assert opensearch_repo.meta.version == v + 1

    new_version = Repository.get("opensearch-py")
    assert "testing-update" == new_version.new_field
    assert "opensearchpy" == new_version.owner.new_name
    assert "opensearch" == new_version.owner.name
    assert "seq_no" in new_version.meta
    assert new_version.meta.seq_no != old_seq_no
    assert "primary_term" in new_version.meta


def test_save_updates_existing_doc(data_client: Any) -> None:
    opensearch_repo = Repository.get("opensearch-py")

    opensearch_repo.new_field = "testing-save"
    old_seq_no = opensearch_repo.meta.seq_no
    assert "updated" == opensearch_repo.save()

    new_repo = data_client.get(index="git", id="opensearch-py")
    assert "testing-save" == new_repo["_source"]["new_field"]
    assert new_repo["_seq_no"] != old_seq_no
    assert new_repo["_seq_no"] == opensearch_repo.meta.seq_no


def test_save_automatically_uses_seq_no_and_primary_term(data_client: Any) -> None:
    opensearch_repo = Repository.get("opensearch-py")
    opensearch_repo.meta.seq_no += 1

    with raises(ConflictError):
        opensearch_repo.save()


def test_delete_automatically_uses_seq_no_and_primary_term(data_client: Any) -> None:
    opensearch_repo = Repository.get("opensearch-py")
    opensearch_repo.meta.seq_no += 1

    with raises(ConflictError):
        opensearch_repo.delete()


def assert_doc_equals(expected: Any, actual: Any) -> None:
    for f in expected:
        assert f in actual
        assert actual[f] == expected[f]


def test_can_save_to_different_index(write_client: Any) -> None:
    test_repo = Repository(description="testing", meta={"id": 42})
    assert test_repo.save(index="test-document")

    assert_doc_equals(
        {
            "found": True,
            "_index": "test-document",
            "_id": "42",
            "_source": {"description": "testing"},
        },
        write_client.get(index="test-document", id=42),
    )


def test_save_without_skip_empty_will_include_empty_fields(write_client: Any) -> None:
    test_repo = Repository(field_1=[], field_2=None, field_3={}, meta={"id": 42})
    assert test_repo.save(index="test-document", skip_empty=False)

    assert_doc_equals(
        {
            "found": True,
            "_index": "test-document",
            "_id": "42",
            "_source": {"field_1": [], "field_2": None, "field_3": {}},
        },
        write_client.get(index="test-document", id=42),
    )


def test_delete(write_client: Any) -> None:
    write_client.create(
        index="test-document",
        id="opensearch-py",
        body={
            "organization": "opensearch",
            "created_at": "2014-03-03",
            "owner": {"name": "opensearch"},
        },
    )

    test_repo = Repository(meta={"id": "opensearch-py"})
    test_repo.meta.index = "test-document"
    test_repo.delete()

    assert not write_client.exists(
        index="test-document",
        id="opensearch-py",
    )


def test_search(data_client: Any) -> None:
    assert Repository.search().count() == 1


def test_search_returns_proper_doc_classes(data_client: Any) -> None:
    result = Repository.search().execute()

    opensearch_repo = result.hits[0]

    assert isinstance(opensearch_repo, Repository)
    assert opensearch_repo.owner.name == "opensearch"


def test_refresh_mapping(data_client: Any) -> None:
    class Commit(Document):
        class Index:
            name = "git"

        _index: Any

    Commit._index.load_mappings()

    assert "stats" in Commit._index._mapping
    assert "committer" in Commit._index._mapping
    assert "description" in Commit._index._mapping
    assert "committed_date" in Commit._index._mapping
    assert isinstance(Commit._index._mapping["committed_date"], Date)


def test_highlight_in_meta(data_client: Any) -> None:
    commit = (
        Commit.search()
        .query("match", description="inverting")
        .highlight("description")
        .execute()[0]
    )

    assert isinstance(commit, Commit)
    assert "description" in commit.meta.highlight
    assert isinstance(commit.meta.highlight["description"], AttrList)
    assert len(commit.meta.highlight["description"]) > 0
