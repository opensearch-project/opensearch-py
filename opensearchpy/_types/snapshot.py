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

from typing import Literal, TypeAlias, TypedDict

from typing_extensions import NotRequired

from ._internal import (
    FieldCommonByteCount,
    FieldCommonDateTime,
    FieldCommonDuration,
    FieldCommonDurationValueUnitMillis,
    FieldCommonEpochTimeUnitMillis,
    FieldCommonId,
    FieldCommonIndexName,
    FieldCommonMetadata,
    FieldCommonName,
    FieldCommonNodeId,
    FieldCommonShardStatistics,
    FieldCommonStringifiedBoolean,
    FieldCommonStringifiedInteger,
    FieldCommonUuid,
    FieldCommonVersionNumber,
    FieldCommonVersionString,
)


class FieldCommonFileCountSnapshotStats(TypedDict):
    file_count: NotRequired[int]
    size_in_bytes: NotRequired[FieldCommonByteCount]


class FieldCommonRepositorySettings(TypedDict):
    chunk_size: NotRequired[str]
    compress: NotRequired[FieldCommonStringifiedBoolean]
    concurrent_streams: NotRequired[FieldCommonStringifiedInteger]
    location: NotRequired[str]
    read_only: NotRequired[FieldCommonStringifiedBoolean]


class FieldCommonSnapshotShardFailure(TypedDict):
    index: NotRequired[FieldCommonIndexName]
    node_id: NotRequired[FieldCommonId]
    reason: NotRequired[str]
    shard_id: NotRequired[FieldCommonId]
    status: NotRequired[str]


class FieldCommonSnapshotShardsStats(TypedDict):
    done: NotRequired[int]
    failed: NotRequired[int]
    finalizing: NotRequired[int]
    initializing: NotRequired[int]
    started: NotRequired[int]
    total: NotRequired[int]


FieldCommonSnapshotShardsStatsStage: TypeAlias = Literal[
    "DONE", "FAILURE", "FINALIZE", "INIT", "STARTED"
]


class FieldCommonSnapshotShardsStatsSummaryItem(TypedDict):
    file_count: NotRequired[int]
    size_in_bytes: NotRequired[FieldCommonByteCount]


class CleanupRepositoryCleanupRepositoryResults(TypedDict):
    deleted_blobs: int
    deleted_bytes: int


class VerifyRepositoryCompactNodeInfo(TypedDict):
    name: FieldCommonName


class FieldCommonRepository(TypedDict):
    type: NotRequired[str]
    uuid: NotRequired[FieldCommonUuid]
    settings: NotRequired[FieldCommonRepositorySettings]


class FieldCommonSnapshotShardsStatsSummary(TypedDict):
    incremental: NotRequired[FieldCommonSnapshotShardsStatsSummaryItem]
    processed: NotRequired[FieldCommonSnapshotShardsStatsSummaryItem]
    total: NotRequired[FieldCommonSnapshotShardsStatsSummaryItem]
    start_time_in_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    time: NotRequired[FieldCommonDuration]
    time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class FieldCommonSnapshotShardsStatus(TypedDict):
    node: NotRequired[FieldCommonNodeId]
    reason: NotRequired[str]
    stage: FieldCommonSnapshotShardsStatsStage
    stats: FieldCommonSnapshotShardsStatsSummary


class FieldCommonSnapshotStats(TypedDict):
    incremental: NotRequired[FieldCommonFileCountSnapshotStats]
    processed: NotRequired[FieldCommonFileCountSnapshotStats]
    start_time_in_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    time: NotRequired[FieldCommonDuration]
    time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    total: NotRequired[FieldCommonFileCountSnapshotStats]


class RestoreSnapshotRestore(TypedDict):
    indices: list[FieldCommonIndexName]
    snapshot: str
    shards: FieldCommonShardStatistics


class FieldCommonSnapshotIndexStats(TypedDict):
    shards: NotRequired[dict[str, FieldCommonSnapshotShardsStatus]]
    shards_stats: NotRequired[FieldCommonSnapshotShardsStats]
    stats: NotRequired[FieldCommonSnapshotStats]


class FieldCommonSnapshotInfo(TypedDict):
    data_streams: NotRequired[list[str]]
    duration: NotRequired[FieldCommonDuration]
    duration_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    end_time: NotRequired[FieldCommonDateTime]
    end_time_in_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    failures: NotRequired[list[FieldCommonSnapshotShardFailure]]
    include_global_state: NotRequired[bool]
    indices: NotRequired[list[FieldCommonIndexName]]
    metadata: NotRequired[FieldCommonMetadata]
    pinned_timestamp: NotRequired[FieldCommonEpochTimeUnitMillis]
    reason: NotRequired[str]
    remote_store_index_shallow_copy: NotRequired[bool]
    snapshot: NotRequired[FieldCommonName]
    shards: NotRequired[FieldCommonShardStatistics]
    start_time: NotRequired[FieldCommonDateTime]
    start_time_in_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    state: NotRequired[str]
    uuid: NotRequired[FieldCommonUuid]
    version: NotRequired[FieldCommonVersionString]
    version_id: NotRequired[FieldCommonVersionNumber]


class FieldCommonSnapshotStatus(TypedDict):
    include_global_state: NotRequired[bool]
    indices: NotRequired[dict[str, FieldCommonSnapshotIndexStats]]
    repository: NotRequired[str]
    shards_stats: NotRequired[FieldCommonSnapshotShardsStats]
    snapshot: NotRequired[str]
    state: NotRequired[str]
    stats: NotRequired[FieldCommonSnapshotStats]
    uuid: NotRequired[FieldCommonUuid]
