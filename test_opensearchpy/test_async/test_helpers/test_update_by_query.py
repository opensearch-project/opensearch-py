# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from copy import deepcopy

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy import Q
from opensearchpy._async.helpers import update_by_query
from opensearchpy.helpers.response import UpdateByQueryResponse

pytestmark: MarkDecorator = pytest.mark.asyncio


async def test_ubq_starts_with_no_query() -> None:
    ubq = update_by_query.AsyncUpdateByQuery()

    assert ubq.query._proxied is None


async def test_ubq_to_dict() -> None:
    ubq = update_by_query.AsyncUpdateByQuery()
    assert {} == ubq.to_dict()

    ubq = ubq.query("match", f=42)
    assert {"query": {"match": {"f": 42}}} == ubq.to_dict()

    assert {"query": {"match": {"f": 42}}, "size": 10} == ubq.to_dict(size=10)

    ubq = update_by_query.AsyncUpdateByQuery(extra={"size": 5})
    assert {"size": 5} == ubq.to_dict()

    ubq = update_by_query.AsyncUpdateByQuery(
        extra={"extra_q": Q("term", category="conference")}
    )
    assert {"extra_q": {"term": {"category": "conference"}}} == ubq.to_dict()


async def test_complex_example() -> None:
    ubq = update_by_query.AsyncUpdateByQuery()
    ubq = (
        ubq.query("match", title="python")
        .query(~Q("match", title="ruby"))
        .filter(Q("term", category="meetup") | Q("term", category="conference"))
        .script(
            source="ctx._source.likes += params.f", lang="painless", params={"f": 3}
        )
    )

    ubq.query.minimum_should_match = 2
    assert {
        "query": {
            "bool": {
                "filter": [
                    {
                        "bool": {
                            "should": [
                                {"term": {"category": "meetup"}},
                                {"term": {"category": "conference"}},
                            ]
                        }
                    }
                ],
                "must": [{"match": {"title": "python"}}],
                "must_not": [{"match": {"title": "ruby"}}],
                "minimum_should_match": 2,
            }
        },
        "script": {
            "source": "ctx._source.likes += params.f",
            "lang": "painless",
            "params": {"f": 3},
        },
    } == ubq.to_dict()


async def test_exclude() -> None:
    ubq = update_by_query.AsyncUpdateByQuery()
    ubq = ubq.exclude("match", title="python")

    assert {
        "query": {
            "bool": {
                "filter": [{"bool": {"must_not": [{"match": {"title": "python"}}]}}]
            }
        }
    } == ubq.to_dict()


async def test_reverse() -> None:
    d = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "should": [
                            {"term": {"category": "meetup"}},
                            {"term": {"category": "conference"}},
                        ]
                    }
                },
                "query": {
                    "bool": {
                        "must": [{"match": {"title": "python"}}],
                        "must_not": [{"match": {"title": "ruby"}}],
                        "minimum_should_match": 2,
                    }
                },
            }
        },
        "script": {
            "source": "ctx._source.likes += params.f",
            "lang": "painless",
            "params": {"f": 3},
        },
    }

    d2 = deepcopy(d)

    ubq = update_by_query.AsyncUpdateByQuery.from_dict(d)

    assert d == d2
    assert d == ubq.to_dict()


async def test_from_dict_doesnt_need_query() -> None:
    ubq = update_by_query.AsyncUpdateByQuery.from_dict({"script": {"source": "test"}})

    assert {"script": {"source": "test"}} == ubq.to_dict()


async def test_overwrite_script() -> None:
    ubq = update_by_query.AsyncUpdateByQuery()
    ubq = ubq.script(
        source="ctx._source.likes += params.f", lang="painless", params={"f": 3}
    )
    assert {
        "script": {
            "source": "ctx._source.likes += params.f",
            "lang": "painless",
            "params": {"f": 3},
        }
    } == ubq.to_dict()
    ubq = ubq.script(source="ctx._source.likes++")
    assert {"script": {"source": "ctx._source.likes++"}} == ubq.to_dict()


async def test_update_by_query_response_success() -> None:
    ubqr = UpdateByQueryResponse({}, {"timed_out": False, "failures": []})
    assert ubqr.success()

    ubqr = UpdateByQueryResponse({}, {"timed_out": True, "failures": []})
    assert not ubqr.success()

    ubqr = UpdateByQueryResponse({}, {"timed_out": False, "failures": [{}]})
    assert not ubqr.success()
