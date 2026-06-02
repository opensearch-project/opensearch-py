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

from typing import Any, Literal, TypeAlias, TypedDict

from typing_extensions import NotRequired

from ._internal import (
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
    SearchSourceConfig,
    SearchSuggester,
    SearchTrackHits,
)

FieldCommonGroupingType: TypeAlias = Literal["NONE", "SIMILARITY", "none", "similarity"]


class FieldCommonMeasurement(TypedDict):
    number: NotRequired[int]
    count: NotRequired[int]
    aggregationType: NotRequired[str]


class Latency(TypedDict):
    number: NotRequired[int]
    count: NotRequired[int]
    aggregationType: NotRequired[str]


class Cpu(TypedDict):
    number: NotRequired[int]
    count: NotRequired[int]
    aggregationType: NotRequired[str]


class Memory(TypedDict):
    number: NotRequired[int]
    count: NotRequired[int]
    aggregationType: NotRequired[str]


class FieldCommonMeasurements(TypedDict):
    latency: NotRequired[Latency]
    cpu: NotRequired[Cpu]
    memory: NotRequired[Memory]


FieldCommonMetricType: TypeAlias = Literal["cpu", "latency", "memory"]


class FieldCommonTaskResourceUsage(TypedDict):
    cpu_time_in_nanos: NotRequired[int]
    memory_in_bytes: NotRequired[int]


class TaskResourceUsage(TypedDict):
    cpu_time_in_nanos: NotRequired[int]
    memory_in_bytes: NotRequired[int]


class FieldCommonTaskResourceUsages(TypedDict):
    action: NotRequired[str]
    taskId: NotRequired[int]
    parentTaskId: NotRequired[int]
    nodeId: NotRequired[str]
    taskResourceUsage: NotRequired[TaskResourceUsage]


class TaskResourceUsageModel(TypedDict):
    action: NotRequired[str]
    taskId: NotRequired[int]
    parentTaskId: NotRequired[int]
    nodeId: NotRequired[str]
    taskResourceUsage: NotRequired[TaskResourceUsage]


class Measurements(TypedDict):
    latency: NotRequired[Latency]
    cpu: NotRequired[Cpu]
    memory: NotRequired[Memory]


class TaskResourceUsageModel1(TypedDict):
    cpu_time_in_nanos: NotRequired[int]
    memory_in_bytes: NotRequired[int]


class TaskResourceUsageModel2(TypedDict):
    action: NotRequired[str]
    taskId: NotRequired[int]
    parentTaskId: NotRequired[int]
    nodeId: NotRequired[str]
    taskResourceUsage: NotRequired[TaskResourceUsageModel1]


FieldCommonSource = TypedDict(
    "FieldCommonSource",
    {
        "aggregations": NotRequired[dict[str, Any]],
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


Source = TypedDict(
    "Source",
    {
        "aggregations": NotRequired[dict[str, Any]],
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


class TopQuery(TypedDict):
    id: NotRequired[str]
    group_by: NotRequired[FieldCommonGroupingType]
    timestamp: NotRequired[int]
    total_shards: NotRequired[int]
    task_resource_usages: NotRequired[list[TaskResourceUsageModel]]
    query_hashcode: NotRequired[str]
    labels: NotRequired[dict[str, Any]]
    search_type: NotRequired[str]
    source: NotRequired[Source]
    node_id: NotRequired[str]
    indices: NotRequired[list[str]]
    phase_latency_map: NotRequired[dict[str, Any]]
    measurements: NotRequired[Measurements]


class FieldCommonTopQueriesResponse(TypedDict):
    top_queries: list[TopQuery]


class FieldCommonTopQuery(TypedDict):
    id: NotRequired[str]
    group_by: NotRequired[FieldCommonGroupingType]
    timestamp: NotRequired[int]
    total_shards: NotRequired[int]
    task_resource_usages: NotRequired[list[TaskResourceUsageModel2]]
    query_hashcode: NotRequired[str]
    labels: NotRequired[dict[str, Any]]
    search_type: NotRequired[str]
    source: NotRequired[Source]
    node_id: NotRequired[str]
    indices: NotRequired[list[str]]
    phase_latency_map: NotRequired[dict[str, Any]]
    measurements: NotRequired[Measurements]
