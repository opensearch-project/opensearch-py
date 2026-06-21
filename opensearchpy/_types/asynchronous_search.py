# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

# ------------------------------------------------------------------------------------------
# THIS CODE IS AUTOMATICALLY GENERATED AND MANUAL EDITS WILL BE LOST
#
# To contribute, kindly make modifications in the opensearch-py client generator
# or in the OpenSearch API specification, and run `nox -rs generate`. See DEVELOPER_GUIDE.md
# and https://github.com/opensearch-project/opensearch-api-specification for details.
# -----------------------------------------------------------------------------------------+

from __future__ import annotations

from typing import Any, TypedDict

from typing_extensions import NotRequired

from ._internal import (
    AggregationsAggregationContainerModel43,
    FieldCommonFields,
    FieldCommonScriptField,
    FieldCommonSlicedScroll,
    FieldCommonSort,
    FieldCommonSortResults,
    QueryDslFieldAndFormatModel,
    QueryDslQueryContainer,
    SearchFieldCollapse,
    SearchHighlight,
    SearchPointInTimeReference,
    SearchSearchResponse,
    SearchSourceConfig,
    SearchSuggester,
    SearchTrackHits,
)
from .nodes import FieldCommonNodesResponseBase


class FieldCommonAsynchronousSearchStats(TypedDict):
    submitted: NotRequired[int]
    initialized: NotRequired[int]
    search_failed: NotRequired[int]
    search_completed: NotRequired[int]
    rejected: NotRequired[int]
    persist_failed: NotRequired[int]
    cancelled: NotRequired[int]
    running_current: NotRequired[int]
    persisted: NotRequired[int]


class FieldCommonNodesStats(TypedDict):
    asynchronous_search_stats: NotRequired[FieldCommonAsynchronousSearchStats]


class FieldCommonStatsResponse(FieldCommonNodesResponseBase):
    cluster_name: NotRequired[str]
    nodes: NotRequired[dict[str, FieldCommonNodesStats]]


class FieldCommonResponseBody(TypedDict):
    id: NotRequired[str]
    state: NotRequired[str]
    start_time_in_millis: NotRequired[float]
    expiration_time_in_millis: NotRequired[float]
    took: NotRequired[float]
    response: NotRequired[SearchSearchResponse]


FieldCommonSearch = TypedDict(
    "FieldCommonSearch",
    {
        "aggregations": NotRequired[dict[str, AggregationsAggregationContainerModel43]],
        "collapse": NotRequired[SearchFieldCollapse],
        "explain": NotRequired[bool],
        "ext": NotRequired[dict[str, dict[str, Any]]],
        "from": NotRequired[float],
        "highlight": NotRequired[SearchHighlight],
        "track_total_hits": NotRequired[SearchTrackHits],
        "indices_boost": NotRequired[list[dict[str, float]]],
        "docvalue_fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "min_score": NotRequired[float],
        "post_filter": NotRequired[QueryDslQueryContainer],
        "profile": NotRequired[bool],
        "query": NotRequired[QueryDslQueryContainer],
        "script_fields": NotRequired[dict[str, FieldCommonScriptField]],
        "search_after": NotRequired[FieldCommonSortResults],
        "size": NotRequired[float],
        "slice": NotRequired[FieldCommonSlicedScroll],
        "sort": NotRequired[FieldCommonSort],
        "_source": NotRequired[SearchSourceConfig],
        "fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "suggest": NotRequired[SearchSuggester],
        "terminate_after": NotRequired[int],
        "timeout": NotRequired[str],
        "track_scores": NotRequired[bool],
        "version": NotRequired[bool],
        "seq_no_primary_term": NotRequired[bool],
        "stored_fields": NotRequired[FieldCommonFields],
        "pit": NotRequired[SearchPointInTimeReference],
        "stats": NotRequired[list[str]],
    },
)
