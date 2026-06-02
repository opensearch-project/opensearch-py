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
    FieldCommonIndexAlias,
    FieldCommonIndexName,
    FieldCommonSequenceNumber,
    FieldCommonStringifiedEpochTimeUnitMillis,
)


class FieldCommonAutoFollowStats(TypedDict):
    name: NotRequired[str]
    pattern: NotRequired[str]
    num_success_start_replication: NotRequired[float]
    num_failed_start_replication: NotRequired[float]
    num_failed_leader_calls: NotRequired[float]
    failed_indices: NotRequired[list[str]]
    last_execution_time: NotRequired[float]


class FieldCommonAutoFollowStatus(TypedDict):
    num_success_start_replication: NotRequired[float]
    num_failed_start_replication: NotRequired[float]
    num_failed_leader_calls: NotRequired[float]
    failed_indices: NotRequired[list[str]]
    autofollow_stats: NotRequired[list[FieldCommonAutoFollowStats]]


class FieldCommonDeleteReplicationRule(TypedDict):
    leader_alias: NotRequired[FieldCommonIndexAlias]
    name: NotRequired[str]


class FieldCommonIndexSchema(TypedDict):
    number_of_shards: NotRequired[int]
    number_of_replicas: NotRequired[int]


FieldCommonReplicationStatus: TypeAlias = Literal[
    "BOOTSTRAPPING", "PAUSED", "REPLICATION NOT IN PROGRESS", "RUNNING", "SYNCING"
]


class FieldCommonSettingsBody(TypedDict):
    index: NotRequired[FieldCommonIndexSchema]


class FieldCommonSyncingDetails(TypedDict):
    leader_checkpoint: NotRequired[int]
    follower_checkpoint: NotRequired[int]
    seq_no: NotRequired[FieldCommonSequenceNumber]


Settings = TypedDict(
    "Settings",
    {
        "index": NotRequired[FieldCommonIndexSchema],
        "index.number_of_shards": NotRequired[int],
        "index.number_of_replicas": NotRequired[int],
    },
)


class FieldCommonUpdateSettings(TypedDict):
    settings: NotRequired[Settings]


class FieldCommonUseRoles(TypedDict):
    leader_cluster_role: NotRequired[str]
    follower_cluster_role: NotRequired[str]


class FieldCommonCreateReplicationRule(TypedDict):
    leader_alias: NotRequired[FieldCommonIndexAlias]
    name: NotRequired[str]
    pattern: NotRequired[str]
    use_roles: NotRequired[FieldCommonUseRoles]


class FieldCommonIndexFollowerStatus(TypedDict):
    operations_written: NotRequired[float]
    operations_read: NotRequired[float]
    failed_read_requests: NotRequired[float]
    throttled_read_requests: NotRequired[float]
    failed_write_requests: NotRequired[float]
    throttled_write_requests: NotRequired[float]
    follower_checkpoint: NotRequired[float]
    leader_checkpoint: NotRequired[float]
    total_write_time_millis: NotRequired[FieldCommonStringifiedEpochTimeUnitMillis]


class FieldCommonIndexStatus(TypedDict):
    operations_read: NotRequired[float]
    translog_size_bytes: NotRequired[FieldCommonByteCount]
    operations_read_lucene: NotRequired[float]
    operations_read_translog: NotRequired[float]
    total_read_time_lucene_millis: NotRequired[
        FieldCommonStringifiedEpochTimeUnitMillis
    ]
    total_read_time_translog_millis: NotRequired[
        FieldCommonStringifiedEpochTimeUnitMillis
    ]
    bytes_read: NotRequired[FieldCommonByteCount]


class FieldCommonLeaderStatus(TypedDict):
    num_replicated_indices: NotRequired[float]
    operations_read: NotRequired[float]
    translog_size_bytes: NotRequired[FieldCommonByteCount]
    operations_read_lucene: NotRequired[float]
    operations_read_translog: NotRequired[float]
    total_read_time_lucene_millis: NotRequired[
        FieldCommonStringifiedEpochTimeUnitMillis
    ]
    total_read_time_translog_millis: NotRequired[
        FieldCommonStringifiedEpochTimeUnitMillis
    ]
    bytes_read: NotRequired[FieldCommonByteCount]
    index_stats: NotRequired[dict[str, FieldCommonIndexStatus]]


class FieldCommonReplication(TypedDict):
    leader_alias: NotRequired[FieldCommonIndexAlias]
    leader_index: NotRequired[FieldCommonIndexName]
    use_roles: NotRequired[FieldCommonUseRoles]


class FieldCommonStatus(TypedDict):
    status: NotRequired[FieldCommonReplicationStatus]
    reason: NotRequired[str]
    leader_alias: NotRequired[FieldCommonIndexAlias]
    leader_index: NotRequired[FieldCommonIndexName]
    follower_index: NotRequired[FieldCommonIndexName]
    syncing_details: NotRequired[FieldCommonSyncingDetails]


class FieldCommonFollowerStatus(TypedDict):
    num_syncing_indices: NotRequired[float]
    num_bootstrapping_indices: NotRequired[float]
    num_paused_indices: NotRequired[float]
    num_failed_indices: NotRequired[float]
    num_shard_tasks: NotRequired[float]
    num_index_tasks: NotRequired[float]
    operations_written: NotRequired[float]
    operations_read: NotRequired[float]
    failed_read_requests: NotRequired[float]
    throttled_read_requests: NotRequired[float]
    failed_write_requests: NotRequired[float]
    throttled_write_requests: NotRequired[float]
    follower_checkpoint: NotRequired[float]
    leader_checkpoint: NotRequired[float]
    total_write_time_millis: NotRequired[FieldCommonStringifiedEpochTimeUnitMillis]
    index_stats: NotRequired[dict[str, FieldCommonIndexFollowerStatus]]
