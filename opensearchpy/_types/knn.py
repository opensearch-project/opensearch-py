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
    FieldCommonByteCount,
    FieldCommonDurationValueUnitMillis,
    FieldCommonDurationValueUnitNanos,
    FieldCommonHealthStatus,
    FieldCommonName,
    FieldCommonPercentageNumber,
)
from .nodes import FieldCommonNodesResponseBase

FieldCommonDeletionResult: TypeAlias = Literal["deleted", "error"]


class FieldCommonKnnMethod(TypedDict):
    name: str
    space_type: NotRequired[str]
    engine: NotRequired[str]
    parameters: NotRequired[dict[str, Any]]


FieldCommonKnnStatName: TypeAlias = Literal[
    "cache_capacity_reached",
    "circuit_breaker_triggered",
    "eviction_count",
    "faiss_initialized",
    "graph_index_errors",
    "graph_index_requests",
    "graph_memory_usage",
    "graph_memory_usage_percentage",
    "graph_query_errors",
    "graph_query_requests",
    "graph_stats",
    "hit_count",
    "indexing_from_model_degraded",
    "indices_in_cache",
    "knn_query_requests",
    "knn_query_with_filter_requests",
    "load_exception_count",
    "load_success_count",
    "lucene_initialized",
    "max_distance_query_requests",
    "max_distance_query_with_filter_requests",
    "min_score_query_requests",
    "min_score_query_with_filter_requests",
    "miss_count",
    "model_index_status",
    "nmslib_initialized",
    "script_compilation_errors",
    "script_compilations",
    "script_query_errors",
    "script_query_requests",
    "total_load_time",
    "training_errors",
    "training_memory_usage",
    "training_memory_usage_percentage",
    "training_requests",
]


class FieldCommonTrainedModel(TypedDict):
    training_index: str
    training_field: str
    dimension: int
    max_training_vector_count: NotRequired[int]
    search_size: NotRequired[int]
    description: NotRequired[str]
    mode: NotRequired[str]
    compression_level: NotRequired[str]
    method: NotRequired[FieldCommonKnnMethod]
    spaceType: NotRequired[str]


class FieldCommonDeletedModel(TypedDict):
    model_id: str
    result: FieldCommonDeletionResult


class FieldCommonGraphMergeStats(TypedDict):
    current: NotRequired[int]
    total: NotRequired[int]
    total_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    current_docs: NotRequired[int]
    total_docs: NotRequired[int]
    total_size_in_bytes: NotRequired[FieldCommonByteCount]
    current_size_in_bytes: NotRequired[FieldCommonByteCount]


class FieldCommonGraphRefreshStats(TypedDict):
    total: NotRequired[int]
    total_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class FieldCommonGraphStats(TypedDict):
    merge: NotRequired[FieldCommonGraphMergeStats]
    refresh: NotRequired[FieldCommonGraphRefreshStats]


class FieldCommonRemoteVectorIndexBuildStatsDetails(TypedDict):
    remote_index_build_current_flush_operations: NotRequired[int]
    remote_index_build_current_flush_size: NotRequired[FieldCommonByteCount]
    remote_index_build_current_merge_operations: NotRequired[int]
    remote_index_build_current_merge_size: NotRequired[FieldCommonByteCount]
    remote_index_build_flush_time_in_millis: NotRequired[
        FieldCommonDurationValueUnitMillis
    ]
    remote_index_build_merge_time_in_millis: NotRequired[
        FieldCommonDurationValueUnitMillis
    ]


class FieldCommonRemoteVectorIndexClientStats(TypedDict):
    build_request_failure_count: NotRequired[int]
    build_request_success_count: NotRequired[int]
    index_build_failure_count: NotRequired[int]
    index_build_success_count: NotRequired[int]
    status_request_failure_count: NotRequired[int]
    status_request_success_count: NotRequired[int]
    waiting_time_in_ms: NotRequired[FieldCommonDurationValueUnitMillis]


class FieldCommonRemoteVectorIndexRepositoryStats(TypedDict):
    read_success_count: NotRequired[int]
    read_failure_count: NotRequired[int]
    successful_read_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    successful_write_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    write_success_count: NotRequired[int]
    write_failure_count: NotRequired[int]


class FieldCommonRemoteVectorIndexBuildStats(TypedDict):
    repository_stats: NotRequired[FieldCommonRemoteVectorIndexRepositoryStats]
    client_stats: NotRequired[FieldCommonRemoteVectorIndexClientStats]
    build_stats: NotRequired[FieldCommonRemoteVectorIndexBuildStatsDetails]


class FieldCommonNodeStats(TypedDict):
    max_distance_query_with_filter_requests: NotRequired[int]
    graph_memory_usage_percentage: NotRequired[FieldCommonPercentageNumber]
    graph_query_requests: NotRequired[int]
    graph_memory_usage: NotRequired[FieldCommonByteCount]
    cache_capacity_reached: NotRequired[bool]
    load_success_count: NotRequired[int]
    training_memory_usage: NotRequired[FieldCommonByteCount]
    indices_in_cache: NotRequired[dict[str, Any]]
    script_query_errors: NotRequired[int]
    hit_count: NotRequired[int]
    knn_query_requests: NotRequired[int]
    total_load_time: NotRequired[FieldCommonDurationValueUnitNanos]
    miss_count: NotRequired[int]
    min_score_query_requests: NotRequired[int]
    knn_query_with_filter_requests: NotRequired[int]
    training_memory_usage_percentage: NotRequired[FieldCommonPercentageNumber]
    max_distance_query_requests: NotRequired[int]
    lucene_initialized: NotRequired[bool]
    graph_index_requests: NotRequired[int]
    faiss_initialized: NotRequired[bool]
    load_exception_count: NotRequired[int]
    training_errors: NotRequired[int]
    min_score_query_with_filter_requests: NotRequired[int]
    eviction_count: NotRequired[int]
    nmslib_initialized: NotRequired[bool]
    script_compilations: NotRequired[int]
    script_query_requests: NotRequired[int]
    graph_stats: NotRequired[FieldCommonGraphStats]
    graph_query_errors: NotRequired[int]
    indexing_from_model_degraded: NotRequired[bool]
    graph_index_errors: NotRequired[int]
    training_requests: NotRequired[int]
    script_compilation_errors: NotRequired[int]
    remote_vector_index_build_stats: NotRequired[FieldCommonRemoteVectorIndexBuildStats]


class FieldCommonStats(FieldCommonNodesResponseBase):
    cluster_name: NotRequired[FieldCommonName]
    circuit_breaker_triggered: NotRequired[bool]
    model_index_status: NotRequired[FieldCommonHealthStatus | None]
    nodes: NotRequired[dict[str, FieldCommonNodeStats]]
