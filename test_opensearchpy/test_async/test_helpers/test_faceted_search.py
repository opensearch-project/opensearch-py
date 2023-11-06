# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from datetime import datetime

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy._async.helpers.faceted_search import AsyncFacetedSearch
from opensearchpy.helpers.faceted_search import DateHistogramFacet, TermsFacet

pytestmark: MarkDecorator = pytest.mark.asyncio


class BlogSearch(AsyncFacetedSearch):
    doc_types = ["user", "post"]
    fields = (
        "title^5",
        "body",
    )

    facets = {
        "category": TermsFacet(field="category.raw"),
        "tags": TermsFacet(field="tags"),
    }


async def test_query_is_created_properly() -> None:
    bs = BlogSearch("python search")
    s = bs.build_search()

    assert s._doc_type == ["user", "post"]
    assert {
        "aggs": {
            "_filter_tags": {
                "filter": {"match_all": {}},
                "aggs": {"tags": {"terms": {"field": "tags"}}},
            },
            "_filter_category": {
                "filter": {"match_all": {}},
                "aggs": {"category": {"terms": {"field": "category.raw"}}},
            },
        },
        "query": {
            "multi_match": {"fields": ("title^5", "body"), "query": "python search"}
        },
        "highlight": {"fields": {"body": {}, "title": {}}},
    } == s.to_dict()


async def test_query_is_created_properly_with_sort_tuple():
    bs = BlogSearch("python search", sort=("category", "-title"))
    s = bs.build_search()

    assert s._doc_type == ["user", "post"]
    assert {
        "aggs": {
            "_filter_tags": {
                "filter": {"match_all": {}},
                "aggs": {"tags": {"terms": {"field": "tags"}}},
            },
            "_filter_category": {
                "filter": {"match_all": {}},
                "aggs": {"category": {"terms": {"field": "category.raw"}}},
            },
        },
        "query": {
            "multi_match": {"fields": ("title^5", "body"), "query": "python search"}
        },
        "highlight": {"fields": {"body": {}, "title": {}}},
        "sort": ["category", {"title": {"order": "desc"}}],
    } == s.to_dict()


async def test_filter_is_applied_to_search_but_not_relevant_facet():
    bs = BlogSearch("python search", filters={"category": "opensearch"})
    s = bs.build_search()

    assert {
        "aggs": {
            "_filter_tags": {
                "filter": {"terms": {"category.raw": ["opensearch"]}},
                "aggs": {"tags": {"terms": {"field": "tags"}}},
            },
            "_filter_category": {
                "filter": {"match_all": {}},
                "aggs": {"category": {"terms": {"field": "category.raw"}}},
            },
        },
        "post_filter": {"terms": {"category.raw": ["opensearch"]}},
        "query": {
            "multi_match": {"fields": ("title^5", "body"), "query": "python search"}
        },
        "highlight": {"fields": {"body": {}, "title": {}}},
    } == s.to_dict()


async def test_filters_are_applied_to_search_ant_relevant_facets():
    bs = BlogSearch(
        "python search",
        filters={"category": "opensearch", "tags": ["python", "django"]},
    )
    s = bs.build_search()

    d = s.to_dict()

    # we need to test post_filter without relying on order
    f = d["post_filter"]["bool"].pop("must")
    assert len(f) == 2
    assert {"terms": {"category.raw": ["opensearch"]}} in f
    assert {"terms": {"tags": ["python", "django"]}} in f

    assert {
        "aggs": {
            "_filter_tags": {
                "filter": {"terms": {"category.raw": ["opensearch"]}},
                "aggs": {"tags": {"terms": {"field": "tags"}}},
            },
            "_filter_category": {
                "filter": {"terms": {"tags": ["python", "django"]}},
                "aggs": {"category": {"terms": {"field": "category.raw"}}},
            },
        },
        "query": {
            "multi_match": {"fields": ("title^5", "body"), "query": "python search"}
        },
        "post_filter": {"bool": {}},
        "highlight": {"fields": {"body": {}, "title": {}}},
    } == d


async def test_date_histogram_facet_with_1970_01_01_date() -> None:
    dhf = DateHistogramFacet()
    assert dhf.get_value({"key": None}) == datetime(1970, 1, 1, 0, 0)
    assert dhf.get_value({"key": 0}) == datetime(1970, 1, 1, 0, 0)


@pytest.mark.parametrize(
    ["interval_type", "interval"],
    [
        ("interval", "year"),
        ("calendar_interval", "year"),
        ("interval", "month"),
        ("calendar_interval", "month"),
        ("interval", "week"),
        ("calendar_interval", "week"),
        ("interval", "day"),
        ("calendar_interval", "day"),
        ("fixed_interval", "day"),
        ("interval", "hour"),
        ("fixed_interval", "hour"),
        ("interval", "1Y"),
        ("calendar_interval", "1Y"),
        ("interval", "1M"),
        ("calendar_interval", "1M"),
        ("interval", "1w"),
        ("calendar_interval", "1w"),
        ("interval", "1d"),
        ("calendar_interval", "1d"),
        ("fixed_interval", "1d"),
        ("interval", "1h"),
        ("fixed_interval", "1h"),
    ],
)
async def test_date_histogram_interval_types(interval_type, interval) -> None:
    dhf = DateHistogramFacet(field="@timestamp", **{interval_type: interval})
    assert dhf.get_aggregation().to_dict() == {
        "date_histogram": {
            "field": "@timestamp",
            interval_type: interval,
            "min_doc_count": 0,
        }
    }
    dhf.get_value_filter(datetime.now())


async def test_date_histogram_no_interval_keyerror() -> None:
    dhf = DateHistogramFacet(field="@timestamp")
    with pytest.raises(KeyError) as e:
        dhf.get_value_filter(datetime.now())
    assert str(e.value) == "'interval'"
