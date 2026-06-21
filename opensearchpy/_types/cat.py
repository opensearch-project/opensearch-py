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

from typing import TypedDict

from typing_extensions import NotRequired

from ._internal import (
    FieldCommonDateTime,
    FieldCommonDuration,
    FieldCommonHost,
    FieldCommonHumanReadableByteCount,
    FieldCommonId,
    FieldCommonIndexName,
    FieldCommonIp,
    FieldCommonName,
    FieldCommonNodeId,
    FieldCommonPercentageString,
    FieldCommonStringifiedEpochTimeUnitMillis,
    FieldCommonStringifiedEpochTimeUnitSeconds,
    FieldCommonTimeOfDay,
    FieldCommonVersionString,
)

AliasesAliasesRecord = TypedDict(
    "AliasesAliasesRecord",
    {
        "alias": NotRequired[str],
        "index": NotRequired[FieldCommonIndexName],
        "filter": NotRequired[str],
        "routing.index": NotRequired[str],
        "routing.search": NotRequired[str],
        "is_write_index": NotRequired[str],
    },
)


AllocationAllocationRecord = TypedDict(
    "AllocationAllocationRecord",
    {
        "shards": NotRequired[str],
        "disk.indices": NotRequired[str | None],
        "disk.used": NotRequired[str | None],
        "disk.avail": NotRequired[str | None],
        "disk.total": NotRequired[str | None],
        "disk.percent": NotRequired[FieldCommonPercentageString | None],
        "host": NotRequired[FieldCommonHost | None],
        "ip": NotRequired[FieldCommonIp | None],
        "node": NotRequired[str],
    },
)


class ClusterManagerClusterManagerRecord(TypedDict):
    id: NotRequired[str]
    host: NotRequired[str]
    ip: NotRequired[str]
    node: NotRequired[str]


class FielddataFielddataRecord(TypedDict):
    id: NotRequired[str]
    host: NotRequired[str]
    ip: NotRequired[str]
    node: NotRequired[str]
    field: NotRequired[str]
    size: NotRequired[str]


IndicesIndicesRecord = TypedDict(
    "IndicesIndicesRecord",
    {
        "health": NotRequired[str],
        "status": NotRequired[str],
        "index": NotRequired[str],
        "uuid": NotRequired[str],
        "pri": NotRequired[str],
        "rep": NotRequired[str],
        "docs.count": NotRequired[str | None],
        "docs.deleted": NotRequired[str | None],
        "creation.date": NotRequired[str],
        "creation.date.string": NotRequired[str],
        "store.size": NotRequired[str | None],
        "pri.store.size": NotRequired[str | None],
        "completion.size": NotRequired[str | None],
        "pri.completion.size": NotRequired[str | None],
        "fielddata.memory_size": NotRequired[str | None],
        "pri.fielddata.memory_size": NotRequired[str | None],
        "fielddata.evictions": NotRequired[str | None],
        "pri.fielddata.evictions": NotRequired[str | None],
        "query_cache.memory_size": NotRequired[str | None],
        "pri.query_cache.memory_size": NotRequired[str | None],
        "query_cache.evictions": NotRequired[str | None],
        "pri.query_cache.evictions": NotRequired[str | None],
        "request_cache.memory_size": NotRequired[str | None],
        "pri.request_cache.memory_size": NotRequired[str | None],
        "request_cache.evictions": NotRequired[str | None],
        "pri.request_cache.evictions": NotRequired[str | None],
        "request_cache.hit_count": NotRequired[str | None],
        "pri.request_cache.hit_count": NotRequired[str | None],
        "request_cache.miss_count": NotRequired[str | None],
        "pri.request_cache.miss_count": NotRequired[str | None],
        "flush.total": NotRequired[str | None],
        "pri.flush.total": NotRequired[str | None],
        "flush.total_time": NotRequired[str | None],
        "pri.flush.total_time": NotRequired[str | None],
        "get.current": NotRequired[str | None],
        "pri.get.current": NotRequired[str | None],
        "get.time": NotRequired[str | None],
        "pri.get.time": NotRequired[str | None],
        "get.total": NotRequired[str | None],
        "pri.get.total": NotRequired[str | None],
        "get.exists_time": NotRequired[str | None],
        "pri.get.exists_time": NotRequired[str | None],
        "get.exists_total": NotRequired[str | None],
        "pri.get.exists_total": NotRequired[str | None],
        "get.missing_time": NotRequired[str | None],
        "pri.get.missing_time": NotRequired[str | None],
        "get.missing_total": NotRequired[str | None],
        "pri.get.missing_total": NotRequired[str | None],
        "indexing.delete_current": NotRequired[str | None],
        "pri.indexing.delete_current": NotRequired[str | None],
        "indexing.delete_time": NotRequired[str | None],
        "pri.indexing.delete_time": NotRequired[str | None],
        "indexing.delete_total": NotRequired[str | None],
        "pri.indexing.delete_total": NotRequired[str | None],
        "indexing.index_current": NotRequired[str | None],
        "pri.indexing.index_current": NotRequired[str | None],
        "indexing.index_time": NotRequired[str | None],
        "pri.indexing.index_time": NotRequired[str | None],
        "indexing.index_total": NotRequired[str | None],
        "pri.indexing.index_total": NotRequired[str | None],
        "indexing.index_failed": NotRequired[str | None],
        "pri.indexing.index_failed": NotRequired[str | None],
        "merges.current": NotRequired[str | None],
        "pri.merges.current": NotRequired[str | None],
        "merges.current_docs": NotRequired[str | None],
        "pri.merges.current_docs": NotRequired[str | None],
        "merges.current_size": NotRequired[str | None],
        "pri.merges.current_size": NotRequired[str | None],
        "merges.total": NotRequired[str | None],
        "pri.merges.total": NotRequired[str | None],
        "merges.total_docs": NotRequired[str | None],
        "pri.merges.total_docs": NotRequired[str | None],
        "merges.total_size": NotRequired[str | None],
        "pri.merges.total_size": NotRequired[str | None],
        "merges.total_time": NotRequired[str | None],
        "pri.merges.total_time": NotRequired[str | None],
        "refresh.total": NotRequired[str | None],
        "pri.refresh.total": NotRequired[str | None],
        "refresh.time": NotRequired[str | None],
        "pri.refresh.time": NotRequired[str | None],
        "refresh.external_total": NotRequired[str | None],
        "pri.refresh.external_total": NotRequired[str | None],
        "refresh.external_time": NotRequired[str | None],
        "pri.refresh.external_time": NotRequired[str | None],
        "refresh.listeners": NotRequired[str | None],
        "pri.refresh.listeners": NotRequired[str | None],
        "search.fetch_current": NotRequired[str | None],
        "pri.search.fetch_current": NotRequired[str | None],
        "search.fetch_time": NotRequired[str | None],
        "pri.search.fetch_time": NotRequired[str | None],
        "search.fetch_total": NotRequired[str | None],
        "pri.search.fetch_total": NotRequired[str | None],
        "search.open_contexts": NotRequired[str | None],
        "pri.search.open_contexts": NotRequired[str | None],
        "search.query_current": NotRequired[str | None],
        "pri.search.query_current": NotRequired[str | None],
        "search.query_time": NotRequired[str | None],
        "pri.search.query_time": NotRequired[str | None],
        "search.query_total": NotRequired[str | None],
        "pri.search.query_total": NotRequired[str | None],
        "search.concurrent_query_current": NotRequired[str | None],
        "pri.search.concurrent_query_current": NotRequired[str | None],
        "search.concurrent_query_time": NotRequired[str | None],
        "pri.search.concurrent_query_time": NotRequired[str | None],
        "search.concurrent_query_total": NotRequired[str | None],
        "pri.search.concurrent_query_total": NotRequired[str | None],
        "search.concurrent_avg_slice_count": NotRequired[str | None],
        "pri.search.concurrent_avg_slice_count": NotRequired[str | None],
        "search.scroll_current": NotRequired[str | None],
        "pri.search.scroll_current": NotRequired[str | None],
        "search.scroll_time": NotRequired[str | None],
        "pri.search.scroll_time": NotRequired[str | None],
        "search.scroll_total": NotRequired[str | None],
        "pri.search.scroll_total": NotRequired[str | None],
        "search.point_in_time_current": NotRequired[str | None],
        "pri.search.point_in_time_current": NotRequired[str | None],
        "search.point_in_time_time": NotRequired[str | None],
        "pri.search.point_in_time_time": NotRequired[str | None],
        "search.point_in_time_total": NotRequired[str | None],
        "pri.search.point_in_time_total": NotRequired[str | None],
        "segments.count": NotRequired[str | None],
        "pri.segments.count": NotRequired[str | None],
        "segments.memory": NotRequired[str | None],
        "pri.segments.memory": NotRequired[str | None],
        "segments.index_writer_memory": NotRequired[str | None],
        "pri.segments.index_writer_memory": NotRequired[str | None],
        "segments.version_map_memory": NotRequired[str | None],
        "pri.segments.version_map_memory": NotRequired[str | None],
        "segments.fixed_bitset_memory": NotRequired[str | None],
        "pri.segments.fixed_bitset_memory": NotRequired[str | None],
        "warmer.current": NotRequired[str | None],
        "pri.warmer.current": NotRequired[str | None],
        "warmer.total": NotRequired[str | None],
        "pri.warmer.total": NotRequired[str | None],
        "warmer.total_time": NotRequired[str | None],
        "pri.warmer.total_time": NotRequired[str | None],
        "suggest.current": NotRequired[str | None],
        "pri.suggest.current": NotRequired[str | None],
        "suggest.time": NotRequired[str | None],
        "pri.suggest.time": NotRequired[str | None],
        "suggest.total": NotRequired[str | None],
        "pri.suggest.total": NotRequired[str | None],
        "memory.total": NotRequired[str],
        "pri.memory.total": NotRequired[str],
        "search.throttled": NotRequired[str],
    },
)


class MasterMasterRecord(TypedDict):
    id: NotRequired[str]
    host: NotRequired[str]
    ip: NotRequired[str]
    node: NotRequired[str]


class NodeattrsNodeAttributesRecord(TypedDict):
    node: NotRequired[str]
    id: NotRequired[str]
    pid: NotRequired[str]
    host: NotRequired[str]
    ip: NotRequired[str]
    port: NotRequired[str]
    attr: NotRequired[str]
    value: NotRequired[str]


NodesNodesRecord = TypedDict(
    "NodesNodesRecord",
    {
        "id": NotRequired[FieldCommonId],
        "pid": NotRequired[str],
        "ip": NotRequired[str],
        "port": NotRequired[str],
        "http_address": NotRequired[str],
        "version": NotRequired[FieldCommonVersionString],
        "flavor": NotRequired[str],
        "type": NotRequired[str],
        "build": NotRequired[str],
        "jdk": NotRequired[str],
        "disk.total": NotRequired[str],
        "disk.used": NotRequired[str],
        "disk.avail": NotRequired[str],
        "disk.used_percent": NotRequired[FieldCommonPercentageString],
        "heap.current": NotRequired[str],
        "heap.percent": NotRequired[FieldCommonPercentageString],
        "heap.max": NotRequired[str],
        "ram.current": NotRequired[str],
        "ram.percent": NotRequired[FieldCommonPercentageString],
        "ram.max": NotRequired[str],
        "file_desc.current": NotRequired[str],
        "file_desc.percent": NotRequired[FieldCommonPercentageString],
        "file_desc.max": NotRequired[str],
        "cpu": NotRequired[str],
        "load_1m": NotRequired[str],
        "load_5m": NotRequired[str],
        "load_15m": NotRequired[str],
        "uptime": NotRequired[str],
        "node.role": NotRequired[str],
        "node.roles": NotRequired[str],
        "cluster_manager": NotRequired[str],
        "master": NotRequired[str],
        "name": NotRequired[FieldCommonName],
        "completion.size": NotRequired[str],
        "fielddata.memory_size": NotRequired[str],
        "fielddata.evictions": NotRequired[str],
        "query_cache.memory_size": NotRequired[str],
        "query_cache.evictions": NotRequired[str],
        "query_cache.hit_count": NotRequired[str],
        "query_cache.miss_count": NotRequired[str],
        "request_cache.memory_size": NotRequired[str],
        "request_cache.evictions": NotRequired[str],
        "request_cache.hit_count": NotRequired[str],
        "request_cache.miss_count": NotRequired[str],
        "flush.total": NotRequired[str],
        "flush.total_time": NotRequired[str],
        "get.current": NotRequired[str],
        "get.time": NotRequired[str],
        "get.total": NotRequired[str],
        "get.exists_time": NotRequired[str],
        "get.exists_total": NotRequired[str],
        "get.missing_time": NotRequired[str],
        "get.missing_total": NotRequired[str],
        "indexing.delete_current": NotRequired[str],
        "indexing.delete_time": NotRequired[str],
        "indexing.delete_total": NotRequired[str],
        "indexing.index_current": NotRequired[str],
        "indexing.index_time": NotRequired[str],
        "indexing.index_total": NotRequired[str],
        "indexing.index_failed": NotRequired[str],
        "merges.current": NotRequired[str],
        "merges.current_docs": NotRequired[str],
        "merges.current_size": NotRequired[str],
        "merges.total": NotRequired[str],
        "merges.total_docs": NotRequired[str],
        "merges.total_size": NotRequired[str],
        "merges.total_time": NotRequired[str],
        "refresh.total": NotRequired[str],
        "refresh.time": NotRequired[str],
        "refresh.external_total": NotRequired[str],
        "refresh.external_time": NotRequired[str],
        "refresh.listeners": NotRequired[str],
        "script.compilations": NotRequired[str],
        "script.cache_evictions": NotRequired[str],
        "script.compilation_limit_triggered": NotRequired[str],
        "search.fetch_current": NotRequired[str],
        "search.fetch_time": NotRequired[str],
        "search.fetch_total": NotRequired[str],
        "search.open_contexts": NotRequired[str],
        "search.query_current": NotRequired[str],
        "search.query_time": NotRequired[str],
        "search.query_total": NotRequired[str],
        "search.concurrent_query_current": NotRequired[str],
        "search.concurrent_query_time": NotRequired[str],
        "search.concurrent_query_total": NotRequired[str],
        "search.concurrent_avg_slice_count": NotRequired[str],
        "search.scroll_current": NotRequired[str],
        "search.scroll_time": NotRequired[str],
        "search.scroll_total": NotRequired[str],
        "search.point_in_time_current": NotRequired[str],
        "search.point_in_time_time": NotRequired[str],
        "search.point_in_time_total": NotRequired[str],
        "segments.count": NotRequired[str],
        "segments.memory": NotRequired[str],
        "segments.index_writer_memory": NotRequired[str],
        "segments.version_map_memory": NotRequired[str],
        "segments.fixed_bitset_memory": NotRequired[str],
        "suggest.current": NotRequired[str],
        "suggest.time": NotRequired[str],
        "suggest.total": NotRequired[str],
        "bulk.total_operations": NotRequired[str],
        "bulk.total_time": NotRequired[str],
        "bulk.total_size_in_bytes": NotRequired[str],
        "bulk.avg_time": NotRequired[str],
        "bulk.avg_size_in_bytes": NotRequired[str],
    },
)


class PendingTasksPendingTasksRecord(TypedDict):
    insertOrder: NotRequired[str]
    timeInQueue: NotRequired[str]
    priority: NotRequired[str]
    source: NotRequired[str]


class PluginsPluginsRecord(TypedDict):
    id: NotRequired[FieldCommonNodeId]
    name: NotRequired[FieldCommonName]
    component: NotRequired[str]
    version: NotRequired[FieldCommonVersionString]
    description: NotRequired[str]
    type: NotRequired[str]


class RepositoriesRepositoriesRecord(TypedDict):
    id: NotRequired[str]
    type: NotRequired[str]


class SegmentReplicationSegmentReplicationRecord(TypedDict):
    shardId: NotRequired[str]
    target_node: NotRequired[str]
    target_host: NotRequired[str]
    checkpoints_behind: NotRequired[str]
    bytes_behind: NotRequired[str]
    current_lag: NotRequired[str]
    last_completed_lag: NotRequired[str]
    rejected_requests: NotRequired[str]
    stage: NotRequired[str]
    time: NotRequired[str]
    files_fetched: NotRequired[str]
    files_percent: NotRequired[FieldCommonPercentageString]
    bytes_fetched: NotRequired[str]
    bytes_percent: NotRequired[FieldCommonPercentageString]
    start_time: NotRequired[str]
    stop_time: NotRequired[str]
    files: NotRequired[str]
    files_total: NotRequired[str]
    bytes: NotRequired[str]
    bytes_total: NotRequired[str]
    replicating_stage_time_taken: NotRequired[str]
    get_checkpoint_info_stage_time_taken: NotRequired[str]
    file_diff_stage_time_taken: NotRequired[str]
    get_files_stage_time_taken: NotRequired[str]
    finalize_replication_stage_time_taken: NotRequired[str]


SegmentsSegmentsRecord = TypedDict(
    "SegmentsSegmentsRecord",
    {
        "index": NotRequired[FieldCommonIndexName],
        "shard": NotRequired[str],
        "prirep": NotRequired[str],
        "ip": NotRequired[str],
        "id": NotRequired[FieldCommonNodeId],
        "segment": NotRequired[str],
        "generation": NotRequired[str],
        "docs.count": NotRequired[str],
        "docs.deleted": NotRequired[str],
        "size": NotRequired[FieldCommonHumanReadableByteCount],
        "size.memory": NotRequired[str],
        "committed": NotRequired[str],
        "searchable": NotRequired[str],
        "version": NotRequired[FieldCommonVersionString],
        "compound": NotRequired[str],
    },
)


ShardsShardsRecord = TypedDict(
    "ShardsShardsRecord",
    {
        "index": NotRequired[str],
        "shard": NotRequired[str],
        "prirep": NotRequired[str],
        "state": NotRequired[str],
        "docs": NotRequired[str | None],
        "store": NotRequired[str | None],
        "ip": NotRequired[str | None],
        "id": NotRequired[str | None],
        "node": NotRequired[str | None],
        "sync_id": NotRequired[str | None],
        "unassigned.reason": NotRequired[str | None],
        "unassigned.at": NotRequired[str | None],
        "unassigned.for": NotRequired[str | None],
        "unassigned.details": NotRequired[str | None],
        "recoverysource.type": NotRequired[str | None],
        "completion.size": NotRequired[str | None],
        "fielddata.memory_size": NotRequired[str | None],
        "fielddata.evictions": NotRequired[str | None],
        "query_cache.memory_size": NotRequired[str | None],
        "query_cache.evictions": NotRequired[str | None],
        "flush.total": NotRequired[str | None],
        "flush.total_time": NotRequired[str | None],
        "get.current": NotRequired[str | None],
        "get.time": NotRequired[str | None],
        "get.total": NotRequired[str | None],
        "get.exists_time": NotRequired[str | None],
        "get.exists_total": NotRequired[str | None],
        "get.missing_time": NotRequired[str | None],
        "get.missing_total": NotRequired[str | None],
        "indexing.delete_current": NotRequired[str | None],
        "indexing.delete_time": NotRequired[str | None],
        "indexing.delete_total": NotRequired[str | None],
        "indexing.index_current": NotRequired[str | None],
        "indexing.index_time": NotRequired[str | None],
        "indexing.index_total": NotRequired[str | None],
        "indexing.index_failed": NotRequired[str | None],
        "merges.current": NotRequired[str | None],
        "merges.current_docs": NotRequired[str | None],
        "merges.current_size": NotRequired[str | None],
        "merges.total": NotRequired[str | None],
        "merges.total_docs": NotRequired[str | None],
        "merges.total_size": NotRequired[str | None],
        "merges.total_time": NotRequired[str | None],
        "refresh.total": NotRequired[str | None],
        "refresh.time": NotRequired[str | None],
        "refresh.external_total": NotRequired[str | None],
        "refresh.external_time": NotRequired[str | None],
        "refresh.listeners": NotRequired[str | None],
        "search.fetch_current": NotRequired[str | None],
        "search.fetch_time": NotRequired[str | None],
        "search.fetch_total": NotRequired[str | None],
        "search.open_contexts": NotRequired[str | None],
        "search.query_current": NotRequired[str | None],
        "search.query_time": NotRequired[str | None],
        "search.query_total": NotRequired[str | None],
        "search.concurrent_query_current": NotRequired[str | None],
        "search.concurrent_query_time": NotRequired[str | None],
        "search.concurrent_query_total": NotRequired[str | None],
        "search.concurrent_avg_slice_count": NotRequired[str | None],
        "search.scroll_current": NotRequired[str | None],
        "search.scroll_time": NotRequired[str | None],
        "search.scroll_total": NotRequired[str | None],
        "search.point_in_time_current": NotRequired[str | None],
        "search.point_in_time_time": NotRequired[str | None],
        "search.point_in_time_total": NotRequired[str | None],
        "search.search_idle_reactivate_count_total": NotRequired[str | None],
        "segments.count": NotRequired[str | None],
        "segments.memory": NotRequired[str | None],
        "segments.index_writer_memory": NotRequired[str | None],
        "segments.version_map_memory": NotRequired[str | None],
        "segments.fixed_bitset_memory": NotRequired[str | None],
        "seq_no.max": NotRequired[str | None],
        "seq_no.local_checkpoint": NotRequired[str | None],
        "seq_no.global_checkpoint": NotRequired[str | None],
        "warmer.current": NotRequired[str | None],
        "warmer.total": NotRequired[str | None],
        "warmer.total_time": NotRequired[str | None],
        "path.data": NotRequired[str | None],
        "path.state": NotRequired[str | None],
        "bulk.total_operations": NotRequired[str | None],
        "bulk.total_time": NotRequired[str | None],
        "bulk.total_size_in_bytes": NotRequired[str | None],
        "bulk.avg_time": NotRequired[str | None],
        "bulk.avg_size_in_bytes": NotRequired[str | None],
        "docs.deleted": NotRequired[str | None],
    },
)


class TasksTasksRecord(TypedDict):
    id: NotRequired[FieldCommonId]
    action: NotRequired[str]
    task_id: NotRequired[FieldCommonId]
    parent_task_id: NotRequired[str]
    type: NotRequired[str]
    start_time: NotRequired[str]
    timestamp: NotRequired[str]
    running_time_ns: NotRequired[str]
    running_time: NotRequired[str]
    node_id: NotRequired[FieldCommonNodeId]
    ip: NotRequired[str]
    port: NotRequired[str]
    node: NotRequired[str]
    version: NotRequired[FieldCommonVersionString]
    x_opaque_id: NotRequired[str]
    description: NotRequired[str]


class TemplatesTemplatesRecord(TypedDict):
    name: NotRequired[FieldCommonName]
    index_patterns: NotRequired[str]
    order: NotRequired[str]
    version: NotRequired[FieldCommonVersionString | None]
    composed_of: NotRequired[str]


class ThreadPoolThreadPoolRecord(TypedDict):
    node_name: NotRequired[str]
    node_id: NotRequired[FieldCommonNodeId]
    ephemeral_node_id: NotRequired[str]
    pid: NotRequired[str]
    host: NotRequired[str]
    ip: NotRequired[str]
    port: NotRequired[str]
    name: NotRequired[str]
    type: NotRequired[str]
    active: NotRequired[str]
    pool_size: NotRequired[str]
    queue: NotRequired[str]
    queue_size: NotRequired[str]
    rejected: NotRequired[str]
    largest: NotRequired[str]
    completed: NotRequired[str]
    total_wait_time: NotRequired[str]
    core: NotRequired[str | None]
    max: NotRequired[str | None]
    size: NotRequired[str | None]
    keep_alive: NotRequired[str | None]


class CountCountRecord(TypedDict):
    epoch: NotRequired[FieldCommonStringifiedEpochTimeUnitSeconds]
    timestamp: NotRequired[FieldCommonTimeOfDay]
    count: NotRequired[str]


HealthHealthRecord = TypedDict(
    "HealthHealthRecord",
    {
        "epoch": NotRequired[FieldCommonStringifiedEpochTimeUnitSeconds],
        "timestamp": NotRequired[FieldCommonTimeOfDay],
        "cluster": NotRequired[str],
        "status": NotRequired[str],
        "node.total": NotRequired[str],
        "node.data": NotRequired[str],
        "shards": NotRequired[str],
        "pri": NotRequired[str],
        "relo": NotRequired[str],
        "init": NotRequired[str],
        "unassign": NotRequired[str],
        "pending_tasks": NotRequired[str],
        "max_task_wait_time": NotRequired[str],
        "active_shards_percent": NotRequired[FieldCommonPercentageString],
        "discovered_cluster_manager": NotRequired[str],
        "discovered_master": NotRequired[str],
    },
)


class SnapshotsSnapshotsRecord(TypedDict):
    id: NotRequired[str]
    repository: NotRequired[str]
    status: NotRequired[str]
    start_epoch: NotRequired[FieldCommonStringifiedEpochTimeUnitSeconds]
    start_time: NotRequired[FieldCommonTimeOfDay]
    end_epoch: NotRequired[FieldCommonStringifiedEpochTimeUnitSeconds]
    end_time: NotRequired[FieldCommonTimeOfDay]
    duration: NotRequired[FieldCommonDuration]
    indices: NotRequired[str]
    successful_shards: NotRequired[str]
    failed_shards: NotRequired[str]
    total_shards: NotRequired[str]
    reason: NotRequired[str]


class RecoveryRecoveryRecord(TypedDict):
    index: NotRequired[FieldCommonIndexName]
    shard: NotRequired[str]
    start_time: NotRequired[FieldCommonDateTime]
    start_time_millis: NotRequired[FieldCommonStringifiedEpochTimeUnitMillis]
    stop_time: NotRequired[FieldCommonDateTime]
    stop_time_millis: NotRequired[FieldCommonStringifiedEpochTimeUnitMillis]
    time: NotRequired[FieldCommonDuration]
    type: NotRequired[str]
    stage: NotRequired[str]
    source_host: NotRequired[str]
    source_node: NotRequired[str]
    target_host: NotRequired[str]
    target_node: NotRequired[str]
    repository: NotRequired[str]
    snapshot: NotRequired[str]
    files: NotRequired[str]
    files_recovered: NotRequired[str]
    files_percent: NotRequired[FieldCommonPercentageString]
    files_total: NotRequired[str]
    bytes: NotRequired[str]
    bytes_recovered: NotRequired[str]
    bytes_percent: NotRequired[FieldCommonPercentageString]
    bytes_total: NotRequired[str]
    translog_ops: NotRequired[str]
    translog_ops_recovered: NotRequired[str]
    translog_ops_percent: NotRequired[FieldCommonPercentageString]
