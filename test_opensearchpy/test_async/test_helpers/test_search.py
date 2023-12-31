# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from copy import deepcopy
from typing import Any

import pytest
from _pytest.mark.structures import MarkDecorator
from pytest import raises

from opensearchpy._async.helpers import search
from opensearchpy._async.helpers.document import AsyncDocument
from opensearchpy.exceptions import IllegalOperation
from opensearchpy.helpers import query
from opensearchpy.helpers.query import Q

pytestmark: MarkDecorator = pytest.mark.asyncio


async def test_expand__to_dot_is_respected() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch().query("match", a__b=42, _expand__to_dot=False)

    assert {"query": {"match": {"a__b": 42}}} == s.to_dict()


async def test_execute_uses_cache() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    r = object()
    s._response = r

    assert r is await s.execute()


async def test_cache_isnt_cloned() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    s._response = object()

    assert not hasattr(s._clone(), "_response")


async def test_search_starts_with_no_query() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()

    assert s.query._proxied is None


async def test_search_query_combines_query() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()

    s2 = s.query("match", f=42)
    assert s2.query._proxied == query.Match(f=42)
    assert s.query._proxied is None

    s3 = s2.query("match", f=43)
    assert s2.query._proxied == query.Match(f=42)
    assert s3.query._proxied == query.Bool(must=[query.Match(f=42), query.Match(f=43)])


async def test_query_can_be_assigned_to() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()

    q = Q("match", title="python")
    s.query = q

    assert s.query._proxied is q


async def test_query_can_be_wrapped() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch().query("match", title="python")

    s.query = Q("function_score", query=s.query, field_value_factor={"field": "rating"})

    assert {
        "query": {
            "function_score": {
                "functions": [{"field_value_factor": {"field": "rating"}}],
                "query": {"match": {"title": "python"}},
            }
        }
    } == s.to_dict()


async def test_using() -> None:
    # pylint: disable=missing-function-docstring
    o = object()
    o2 = object()
    s = search.AsyncSearch(using=o)
    assert s._using is o
    s2 = s.using(o2)
    assert s._using is o
    assert s2._using is o2


async def test_methods_are_proxied_to_the_query() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch().query("match_all")

    assert s.query.to_dict() == {"match_all": {}}


async def test_query_always_returns_search() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()

    assert isinstance(s.query("match", f=42), search.AsyncSearch)


async def test_source_copied_on_clone() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch().source(False)
    assert s._clone()._source == s._source
    assert s._clone()._source is False

    s2 = search.AsyncSearch().source([])
    assert s2._clone()._source == s2._source
    assert s2._source == []

    s3 = search.AsyncSearch().source(["some", "fields"])
    assert s3._clone()._source == s3._source
    assert s3._clone()._source == ["some", "fields"]


async def test_copy_clones() -> None:
    # pylint: disable=missing-function-docstring
    from copy import copy

    s1 = search.AsyncSearch().source(["some", "fields"])
    s2 = copy(s1)

    assert s1 == s2
    assert s1 is not s2


async def test_aggs_allow_two_metric() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()

    s.aggs.metric("a", "max", field="a").metric("b", "max", field="b")

    assert s.to_dict() == {
        "aggs": {"a": {"max": {"field": "a"}}, "b": {"max": {"field": "b"}}}
    }


async def test_aggs_get_copied_on_change() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch().query("match_all")
    s.aggs.bucket("per_tag", "terms", field="f").metric(
        "max_score", "max", field="score"
    )

    s2 = s.query("match_all")
    s2.aggs.bucket("per_month", "date_histogram", field="date", interval="month")
    s3 = s2.query("match_all")
    s3.aggs["per_month"].metric("max_score", "max", field="score")
    s4 = s3._clone()
    s4.aggs.metric("max_score", "max", field="score")

    d: Any = {
        "query": {"match_all": {}},
        "aggs": {
            "per_tag": {
                "terms": {"field": "f"},
                "aggs": {"max_score": {"max": {"field": "score"}}},
            }
        },
    }

    assert d == s.to_dict()
    d["aggs"]["per_month"] = {"date_histogram": {"field": "date", "interval": "month"}}
    assert d == s2.to_dict()
    d["aggs"]["per_month"]["aggs"] = {"max_score": {"max": {"field": "score"}}}
    assert d == s3.to_dict()
    d["aggs"]["max_score"] = {"max": {"field": "score"}}
    assert d == s4.to_dict()


async def test_search_index() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch(index="i")
    assert s._index == ["i"]
    s = s.index("i2")
    assert s._index == ["i", "i2"]
    s = s.index("i3")
    assert s._index == ["i", "i2", "i3"]
    s = s.index()
    assert s._index is None
    s = search.AsyncSearch(index=("i", "i2"))
    assert s._index == ["i", "i2"]
    s = search.AsyncSearch(index=["i", "i2"])
    assert s._index == ["i", "i2"]
    s = search.AsyncSearch()
    s = s.index("i", "i2")
    assert s._index == ["i", "i2"]
    s2 = s.index("i3")
    assert s._index == ["i", "i2"]
    assert s2._index == ["i", "i2", "i3"]
    s = search.AsyncSearch()
    s = s.index(["i", "i2"], "i3")
    assert s._index == ["i", "i2", "i3"]
    s2 = s.index("i4")
    assert s._index == ["i", "i2", "i3"]
    assert s2._index == ["i", "i2", "i3", "i4"]
    s2 = s.index(["i4"])
    assert s2._index == ["i", "i2", "i3", "i4"]
    s2 = s.index(("i4", "i5"))
    assert s2._index == ["i", "i2", "i3", "i4", "i5"]


async def test_doc_type_document_class() -> None:
    # pylint: disable=missing-function-docstring
    class MyDocument(AsyncDocument):
        pass

    s = search.AsyncSearch(doc_type=MyDocument)
    assert s._doc_type == [MyDocument]
    assert s._doc_type_map == {}

    s = search.AsyncSearch().doc_type(MyDocument)
    assert s._doc_type == [MyDocument]
    assert s._doc_type_map == {}


async def test_sort() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    s = s.sort("fielda", "-fieldb")

    assert ["fielda", {"fieldb": {"order": "desc"}}] == s._sort
    assert {"sort": ["fielda", {"fieldb": {"order": "desc"}}]} == s.to_dict()

    s = s.sort()
    assert [] == s._sort
    assert search.AsyncSearch().to_dict() == s.to_dict()


async def test_sort_by_score() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    s = s.sort("_score")
    assert {"sort": ["_score"]} == s.to_dict()

    s = search.AsyncSearch()
    with raises(IllegalOperation):
        s.sort("-_score")


async def test_slice() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    assert {"from": 3, "size": 7} == s[3:10].to_dict()
    assert {"from": 0, "size": 5} == s[:5].to_dict()
    assert {"from": 3, "size": 10} == s[3:].to_dict()
    assert {"from": 0, "size": 0} == s[0:0].to_dict()
    assert {"from": 20, "size": 0} == s[20:0].to_dict()


async def test_index() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    assert {"from": 3, "size": 1} == s[3].to_dict()


async def test_search_to_dict() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    assert {} == s.to_dict()

    s = s.query("match", f=42)
    assert {"query": {"match": {"f": 42}}} == s.to_dict()

    assert {"query": {"match": {"f": 42}}, "size": 10} == s.to_dict(size=10)

    s.aggs.bucket("per_tag", "terms", field="f").metric(
        "max_score", "max", field="score"
    )
    d = {
        "aggs": {
            "per_tag": {
                "terms": {"field": "f"},
                "aggs": {"max_score": {"max": {"field": "score"}}},
            }
        },
        "query": {"match": {"f": 42}},
    }
    assert d == s.to_dict()

    s = search.AsyncSearch(extra={"size": 5})
    assert {"size": 5} == s.to_dict()
    s = s.extra(from_=42)
    assert {"size": 5, "from": 42} == s.to_dict()


async def test_complex_example() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    s = (
        s.query("match", title="python")
        .query(~Q("match", title="ruby"))
        .filter(Q("term", category="meetup") | Q("term", category="conference"))
        .post_filter("terms", tags=["prague", "czech"])
        .script_fields(more_attendees="doc['attendees'].value + 42")
    )

    s.aggs.bucket("per_country", "terms", field="country").metric(
        "avg_attendees", "avg", field="attendees"
    )

    s.query.minimum_should_match = 2

    s = s.highlight_options(order="score").highlight("title", "body", fragment_size=50)

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
        "post_filter": {"terms": {"tags": ["prague", "czech"]}},
        "aggs": {
            "per_country": {
                "terms": {"field": "country"},
                "aggs": {"avg_attendees": {"avg": {"field": "attendees"}}},
            }
        },
        "highlight": {
            "order": "score",
            "fields": {"title": {"fragment_size": 50}, "body": {"fragment_size": 50}},
        },
        "script_fields": {"more_attendees": {"script": "doc['attendees'].value + 42"}},
    } == s.to_dict()


async def test_reverse() -> None:
    # pylint: disable=missing-function-docstring
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
        "post_filter": {"bool": {"must": [{"terms": {"tags": ["prague", "czech"]}}]}},
        "aggs": {
            "per_country": {
                "terms": {"field": "country"},
                "aggs": {"avg_attendees": {"avg": {"field": "attendees"}}},
            }
        },
        "sort": ["title", {"category": {"order": "desc"}}, "_score"],
        "size": 5,
        "highlight": {"order": "score", "fields": {"title": {"fragment_size": 50}}},
        "suggest": {
            "my-title-suggestions-1": {
                "text": "devloping distibutd saerch engies",
                "term": {"size": 3, "field": "title"},
            }
        },
        "script_fields": {"more_attendees": {"script": "doc['attendees'].value + 42"}},
    }

    d2 = deepcopy(d)

    s = search.AsyncSearch.from_dict(d)

    # make sure we haven't modified anything in place
    assert d == d2
    assert {"size": 5} == s._extra
    assert d == s.to_dict()


async def test_from_dict_doesnt_need_query() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch.from_dict({"size": 5})

    assert {"size": 5} == s.to_dict()


async def test_source() -> None:
    # pylint: disable=missing-function-docstring
    assert {} == search.AsyncSearch().source().to_dict()

    assert {
        "_source": {"includes": ["foo.bar.*"], "excludes": ["foo.one"]}
    } == search.AsyncSearch().source(
        includes=["foo.bar.*"], excludes=["foo.one"]
    ).to_dict()

    assert {"_source": False} == search.AsyncSearch().source(False).to_dict()

    assert {"_source": ["f1", "f2"]} == search.AsyncSearch().source(
        includes=["foo.bar.*"], excludes=["foo.one"]
    ).source(["f1", "f2"]).to_dict()


async def test_source_on_clone() -> None:
    # pylint: disable=missing-function-docstring
    assert {
        "_source": {"includes": ["foo.bar.*"], "excludes": ["foo.one"]},
        "query": {"bool": {"filter": [{"term": {"title": "python"}}]}},
    } == search.AsyncSearch().source(includes=["foo.bar.*"]).source(
        excludes=["foo.one"]
    ).filter(
        "term", title="python"
    ).to_dict()
    assert {
        "_source": False,
        "query": {"bool": {"filter": [{"term": {"title": "python"}}]}},
    } == search.AsyncSearch().source(False).filter("term", title="python").to_dict()


async def test_source_on_clear() -> None:
    # pylint: disable=missing-function-docstring
    assert (
        {}
        == search.AsyncSearch()
        .source(includes=["foo.bar.*"])
        .source(includes=None, excludes=None)
        .to_dict()
    )


async def test_suggest_accepts_global_text() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch.from_dict(
        {
            "suggest": {
                "text": "the amsterdma meetpu",
                "my-suggest-1": {"term": {"field": "title"}},
                "my-suggest-2": {"text": "other", "term": {"field": "body"}},
            }
        }
    )

    assert {
        "suggest": {
            "my-suggest-1": {
                "term": {"field": "title"},
                "text": "the amsterdma meetpu",
            },
            "my-suggest-2": {"term": {"field": "body"}, "text": "other"},
        }
    } == s.to_dict()


async def test_suggest() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    s = s.suggest("my_suggestion", "pyhton", term={"field": "title"})

    assert {
        "suggest": {"my_suggestion": {"term": {"field": "title"}, "text": "pyhton"}}
    } == s.to_dict()


async def test_exclude() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    s = s.exclude("match", title="python")

    assert {
        "query": {
            "bool": {
                "filter": [{"bool": {"must_not": [{"match": {"title": "python"}}]}}]
            }
        }
    } == s.to_dict()


async def test_update_from_dict() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch()
    s.update_from_dict({"indices_boost": [{"important-documents": 2}]})
    s.update_from_dict({"_source": ["id", "name"]})

    assert {
        "indices_boost": [{"important-documents": 2}],
        "_source": ["id", "name"],
    } == s.to_dict()


async def test_rescore_query_to_dict() -> None:
    # pylint: disable=missing-function-docstring
    s = search.AsyncSearch(index="index-name")

    positive_query = Q(
        "function_score",
        query=Q("term", tags="a"),
        script_score={"script": "_score * 1"},
    )

    negative_query = Q(
        "function_score",
        query=Q("term", tags="b"),
        script_score={"script": "_score * -100"},
    )

    s = s.query(positive_query)
    s = s.extra(
        rescore={"window_size": 100, "query": {"rescore_query": negative_query}}
    )
    assert s.to_dict() == {
        "query": {
            "function_score": {
                "query": {"term": {"tags": "a"}},
                "functions": [{"script_score": {"script": "_score * 1"}}],
            }
        },
        "rescore": {
            "window_size": 100,
            "query": {
                "rescore_query": {
                    "function_score": {
                        "query": {"term": {"tags": "b"}},
                        "functions": [{"script_score": {"script": "_score * -100"}}],
                    }
                }
            },
        },
    }

    assert s.to_dict(
        rescore={"window_size": 10, "query": {"rescore_query": positive_query}}
    ) == {
        "query": {
            "function_score": {
                "query": {"term": {"tags": "a"}},
                "functions": [{"script_score": {"script": "_score * 1"}}],
            }
        },
        "rescore": {
            "window_size": 10,
            "query": {
                "rescore_query": {
                    "function_score": {
                        "query": {"term": {"tags": "a"}},
                        "functions": [{"script_score": {"script": "_score * 1"}}],
                    }
                }
            },
        },
    }
