# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from datetime import datetime
from ipaddress import ip_address
from typing import Any, Optional

import pytest
from pytest import raises
from pytz import timezone

from opensearchpy import (
    Binary,
    Boolean,
    ConflictError,
    Date,
    Double,
    InnerDoc,
    Ip,
    Keyword,
    Long,
    MetaField,
    Nested,
    NotFoundError,
    Object,
    Q,
    RankFeatures,
    Text,
    analyzer,
)
from opensearchpy._async.helpers.actions import aiter
from opensearchpy._async.helpers.document import AsyncDocument
from opensearchpy._async.helpers.mapping import AsyncMapping
from opensearchpy.helpers.utils import AttrList

pytestmark = pytest.mark.asyncio
snowball = analyzer("my_snow", tokenizer="standard", filter=["lowercase", "snowball"])


class User(InnerDoc):
    name = Text(fields={"raw": Keyword()})


class Wiki(AsyncDocument):
    owner = Object(User)
    views = Long()
    ranked = RankFeatures()

    class Index:
        name = "test-wiki"


class Repository(AsyncDocument):
    owner = Object(User)
    created_at = Date()
    description = Text(analyzer=snowball)
    tags = Keyword()

    @classmethod
    def search(cls, using: Any = None, index: Optional[str] = None) -> Any:
        return super(Repository, cls).search().filter("term", commit_repo="repo")

    class Index:
        name = "git"


class Commit(AsyncDocument):
    committed_date = Date()
    authored_date = Date()
    description = Text(analyzer=snowball)

    class Index:
        name = "flat-git"

    class Meta:
        mapping = AsyncMapping()


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


class PullRequest(AsyncDocument):
    comments = Nested(Comment)
    created_at = Date()

    class Index:
        name = "test-prs"


class SerializationDoc(AsyncDocument):
    i = Long()
    b = Boolean()
    d = Double()
    bin = Binary()
    ip = Ip()

    class Index:
        name = "test-serialization"


async def test_serialization(write_client: Any) -> None:
    await SerializationDoc.init()
    await write_client.index(
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
    sd: Any = await SerializationDoc.get(id=42)

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


async def test_nested_inner_hits_are_wrapped_properly(pull_request: Any) -> None:
    history_query = Q(
        "nested",
        path="comments.history",
        inner_hits={},
        query=Q("match", comments__history__diff="ahoj"),
    )
    s = PullRequest.search().query(
        "nested", inner_hits={}, path="comments", query=history_query
    )

    response = await s.execute()
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


async def test_nested_inner_hits_are_deserialized_properly(pull_request: Any) -> None:
    s = PullRequest.search().query(
        "nested",
        inner_hits={},
        path="comments",
        query=Q("match", comments__content="hello"),
    )

    response = await s.execute()
    pr = response.hits[0]
    assert isinstance(pr.created_at, datetime)
    assert isinstance(pr.comments[0], Comment)
    assert isinstance(pr.comments[0].created_at, datetime)


async def test_nested_top_hits_are_wrapped_properly(pull_request: Any) -> None:
    s = PullRequest.search()
    s.aggs.bucket("comments", "nested", path="comments").metric(
        "hits", "top_hits", size=1
    )

    r = await s.execute()

    print(r._d_)
    assert isinstance(r.aggregations.comments.hits.hits[0], Comment)


async def test_update_object_field(write_client: Any) -> None:
    await Wiki.init()
    w = Wiki(
        owner=User(name="Honza Kral"),
        _id="opensearch-py",
        ranked={"test1": 0.1, "topic2": 0.2},
    )
    await w.save()

    assert "updated" == await w.update(owner=[{"name": "Honza"}, {"name": "Nick"}])
    assert w.owner[0].name == "Honza"
    assert w.owner[1].name == "Nick"

    w = await Wiki.get(id="opensearch-py")
    assert w.owner[0].name == "Honza"
    assert w.owner[1].name == "Nick"

    assert w.ranked == {"test1": 0.1, "topic2": 0.2}


async def test_update_script(write_client: Any) -> None:
    await Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    await w.save()

    await w.update(script="ctx._source.views += params.inc", inc=5)
    w = await Wiki.get(id="opensearch-py")
    assert w.views == 47


async def test_update_retry_on_conflict(write_client: Any) -> None:
    await Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    await w.save()

    w1 = await Wiki.get(id="opensearch-py")
    w2 = await Wiki.get(id="opensearch-py")
    await w1.update(
        script="ctx._source.views += params.inc", inc=5, retry_on_conflict=1
    )
    await w2.update(
        script="ctx._source.views += params.inc", inc=5, retry_on_conflict=1
    )

    w = await Wiki.get(id="opensearch-py")
    assert w.views == 52


@pytest.mark.parametrize("retry_on_conflict", [None, 0])  # type: ignore
async def test_update_conflicting_version(
    write_client: Any, retry_on_conflict: bool
) -> None:
    await Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    await w.save()

    w1 = await Wiki.get(id="opensearch-py")
    w2 = await Wiki.get(id="opensearch-py")
    await w1.update(script="ctx._source.views += params.inc", inc=5)

    with raises(ConflictError):
        await w2.update(
            script="ctx._source.views += params.inc",
            inc=5,
            retry_on_conflict=retry_on_conflict,
        )


async def test_save_and_update_return_doc_meta(write_client: Any) -> None:
    await Wiki.init()
    w = Wiki(owner=User(name="Honza Kral"), _id="opensearch-py", views=42)
    resp = await w.save(return_doc_meta=True)
    assert resp["_index"] == "test-wiki"
    assert resp["result"] == "created"
    assert resp.keys().__contains__("_id")
    assert resp.keys().__contains__("_primary_term")
    assert resp.keys().__contains__("_seq_no")
    assert resp.keys().__contains__("_shards")
    assert resp.keys().__contains__("_version")

    resp = await w.update(
        script="ctx._source.views += params.inc", inc=5, return_doc_meta=True
    )
    assert resp["_index"] == "test-wiki"
    assert resp["result"] == "updated"
    assert resp.keys().__contains__("_id")
    assert resp.keys().__contains__("_primary_term")
    assert resp.keys().__contains__("_seq_no")
    assert resp.keys().__contains__("_shards")
    assert resp.keys().__contains__("_version")


async def test_init(write_client: Any) -> None:
    await Repository.init(index="test-git")

    assert await write_client.indices.exists(index="test-git")


async def test_get_raises_404_on_index_missing(data_client: Any) -> None:
    with raises(NotFoundError):
        await Repository.get("opensearch-dsl-php", index="not-there")


async def test_get_raises_404_on_non_existent_id(data_client: Any) -> None:
    with raises(NotFoundError):
        await Repository.get("opensearch-dsl-php")


async def test_get_returns_none_if_404_ignored(data_client: Any) -> None:
    assert None is await Repository.get("opensearch-dsl-php", ignore=404)


async def test_get_returns_none_if_404_ignored_and_index_doesnt_exist(
    data_client: Any,
) -> None:
    assert None is await Repository.get("42", index="not-there", ignore=404)


async def test_get(data_client: Any) -> None:
    opensearch_repo = await Repository.get("opensearch-py")

    assert isinstance(opensearch_repo, Repository)
    assert opensearch_repo.owner.name == "opensearch"
    assert datetime(2014, 3, 3) == opensearch_repo.created_at


async def test_exists_return_true(data_client: Any) -> None:
    assert await Repository.exists("opensearch-py")


async def test_exists_false(data_client: Any) -> None:
    assert not await Repository.exists("opensearch-dsl-php")


async def test_get_with_tz_date(data_client: Any) -> None:
    first_commit = await Commit.get(
        id="3ca6e1e73a071a705b4babd2f581c91a2a3e5037", routing="opensearch-py"
    )

    tzinfo = timezone("Europe/Prague")
    assert (
        tzinfo.localize(datetime(2014, 5, 2, 13, 47, 19, 123000))
        == first_commit.authored_date
    )


async def test_save_with_tz_date(data_client: Any) -> None:
    tzinfo = timezone("Europe/Prague")
    first_commit = await Commit.get(
        id="3ca6e1e73a071a705b4babd2f581c91a2a3e5037", routing="opensearch-py"
    )
    first_commit.committed_date = tzinfo.localize(
        datetime(2014, 5, 2, 13, 47, 19, 123456)
    )
    await first_commit.save()

    first_commit = await Commit.get(
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


async def test_mget(data_client: Any) -> None:
    commits = await Commit.mget(COMMIT_DOCS_WITH_MISSING)
    assert commits[0] is None
    assert commits[1].meta.id == "3ca6e1e73a071a705b4babd2f581c91a2a3e5037"
    assert commits[2] is None
    assert commits[3].meta.id == "eb3e543323f189fd7b698e66295427204fff5755"


async def test_mget_raises_exception_when_missing_param_is_invalid(
    data_client: Any,
) -> None:
    with raises(ValueError):
        await Commit.mget(COMMIT_DOCS_WITH_MISSING, missing="raj")


async def test_mget_raises_404_when_missing_param_is_raise(data_client: Any) -> None:
    with raises(NotFoundError):
        await Commit.mget(COMMIT_DOCS_WITH_MISSING, missing="raise")


async def test_mget_ignores_missing_docs_when_missing_param_is_skip(
    data_client: Any,
) -> None:
    commits = await Commit.mget(COMMIT_DOCS_WITH_MISSING, missing="skip")
    assert commits[0].meta.id == "3ca6e1e73a071a705b4babd2f581c91a2a3e5037"
    assert commits[1].meta.id == "eb3e543323f189fd7b698e66295427204fff5755"


async def test_update_works_from_search_response(data_client: Any) -> None:
    opensearch_repo = (await Repository.search().execute())[0]

    await opensearch_repo.update(owner={"other_name": "opensearchpy"})
    assert "opensearchpy" == opensearch_repo.owner.other_name

    new_version = await Repository.get("opensearch-py")
    assert "opensearchpy" == new_version.owner.other_name
    assert "opensearch" == new_version.owner.name


async def test_update(data_client: Any) -> None:
    opensearch_repo = await Repository.get("opensearch-py")
    v = opensearch_repo.meta.version

    old_seq_no = opensearch_repo.meta.seq_no
    await opensearch_repo.update(
        owner={"new_name": "opensearchpy"}, new_field="testing-update"
    )

    assert "opensearchpy" == opensearch_repo.owner.new_name
    assert "testing-update" == opensearch_repo.new_field

    # assert version has been updated
    assert opensearch_repo.meta.version == v + 1

    new_version = await Repository.get("opensearch-py")
    assert "testing-update" == new_version.new_field
    assert "opensearchpy" == new_version.owner.new_name
    assert "opensearch" == new_version.owner.name
    assert "seq_no" in new_version.meta
    assert new_version.meta.seq_no != old_seq_no
    assert "primary_term" in new_version.meta


async def test_save_updates_existing_doc(data_client: Any) -> None:
    opensearch_repo = await Repository.get("opensearch-py")

    opensearch_repo.new_field = "testing-save"
    old_seq_no = opensearch_repo.meta.seq_no
    assert "updated" == await opensearch_repo.save()

    new_repo = await data_client.get(index="git", id="opensearch-py")
    assert "testing-save" == new_repo["_source"]["new_field"]
    assert new_repo["_seq_no"] != old_seq_no
    assert new_repo["_seq_no"] == opensearch_repo.meta.seq_no


async def test_save_automatically_uses_seq_no_and_primary_term(
    data_client: Any,
) -> None:
    opensearch_repo = await Repository.get("opensearch-py")
    opensearch_repo.meta.seq_no += 1

    with raises(ConflictError):
        await opensearch_repo.save()


async def test_delete_automatically_uses_seq_no_and_primary_term(
    data_client: Any,
) -> None:
    opensearch_repo = await Repository.get("opensearch-py")
    opensearch_repo.meta.seq_no += 1

    with raises(ConflictError):
        await opensearch_repo.delete()


async def assert_doc_equals(expected: Any, actual: Any) -> None:
    async for f in aiter(expected):
        assert f in actual
        assert actual[f] == expected[f]


async def test_can_save_to_different_index(write_client: Any) -> None:
    test_repo = Repository(description="testing", meta={"id": 42})
    assert await test_repo.save(index="test-document")

    await assert_doc_equals(
        {
            "found": True,
            "_index": "test-document",
            "_id": "42",
            "_source": {"description": "testing"},
        },
        await write_client.get(index="test-document", id=42),
    )


async def test_save_without_skip_empty_will_include_empty_fields(
    write_client: Any,
) -> None:
    test_repo = Repository(field_1=[], field_2=None, field_3={}, meta={"id": 42})
    assert await test_repo.save(index="test-document", skip_empty=False)

    await assert_doc_equals(
        {
            "found": True,
            "_index": "test-document",
            "_id": "42",
            "_source": {"field_1": [], "field_2": None, "field_3": {}},
        },
        await write_client.get(index="test-document", id=42),
    )


async def test_delete(write_client: Any) -> None:
    await write_client.create(
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
    await test_repo.delete()

    assert not await write_client.exists(
        index="test-document",
        id="opensearch-py",
    )


async def test_search(data_client: Any) -> None:
    assert await Repository.search().count() == 1


async def test_search_returns_proper_doc_classes(data_client: Any) -> None:
    result = await Repository.search().execute()

    opensearch_repo = result.hits[0]

    assert isinstance(opensearch_repo, Repository)
    assert opensearch_repo.owner.name == "opensearch"


async def test_refresh_mapping(data_client: Any) -> None:
    class Commit(AsyncDocument):
        _index: Any

        class Index:
            name = "git"

    await Commit._index.load_mappings()

    assert "stats" in Commit._index._mapping
    assert "committer" in Commit._index._mapping
    assert "description" in Commit._index._mapping
    assert "committed_date" in Commit._index._mapping
    assert isinstance(Commit._index._mapping["committed_date"], Date)


async def test_highlight_in_meta(data_client: Any) -> None:
    commit = (
        await Commit.search()
        .query("match", description="inverting")
        .highlight("description")
        .execute()
    )[0]

    assert isinstance(commit, Commit)
    assert "description" in commit.meta.highlight
    assert isinstance(commit.meta.highlight["description"], AttrList)
    assert len(commit.meta.highlight["description"]) > 0
