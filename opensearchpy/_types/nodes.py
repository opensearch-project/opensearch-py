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
    FieldCommonDateTime,
    FieldCommonDuration,
    FieldCommonDurationValueUnitMicros,
    FieldCommonDurationValueUnitMillis,
    FieldCommonDurationValueUnitNanos,
    FieldCommonEpochTimeUnitMillis,
    FieldCommonEpochTimeUnitSeconds,
    FieldCommonErrorCause,
    FieldCommonHost,
    FieldCommonHumanReadableByteCount,
    FieldCommonIndexRouting,
    FieldCommonIp,
    FieldCommonName,
    FieldCommonNodeRoles,
    FieldCommonNodeStatistics,
    FieldCommonPercentageNumber,
    FieldCommonPercentageString,
    FieldCommonPluginStats,
    FieldCommonStringifiedBoolean,
    FieldCommonStringifiedInteger,
    FieldCommonStringOrStringArray,
    FieldCommonTransportAddress,
    FieldCommonVersionString,
    StatsIndexShardStatsBase,
    StatsIndexStats,
    StatsIndexStatsBase,
)

FieldCommonSampleType: TypeAlias = Literal["block", "cpu", "wait"]


InfoMetric: TypeAlias = Literal[
    "_all",
    "aggregations",
    "http",
    "indices",
    "ingest",
    "jvm",
    "os",
    "plugins",
    "process",
    "search_pipelines",
    "settings",
    "thread_pool",
    "transport",
]


class InfoNodeInfoAction(TypedDict):
    destructive_requires_name: str


class InfoNodeInfoAggregation(TypedDict):
    types: list[str]


class InfoNodeInfoBootstrap(TypedDict):
    memory_lock: str


class InfoNodeInfoClient(TypedDict):
    type: str


class InfoNodeInfoDiscovery(TypedDict):
    type: NotRequired[str]
    seed_hosts: NotRequired[str]


class InfoNodeInfoHttp(TypedDict):
    bound_address: list[str]
    max_content_length: NotRequired[FieldCommonHumanReadableByteCount]
    max_content_length_in_bytes: FieldCommonByteCount
    publish_address: str


class InfoNodeInfoIngestDownloader(TypedDict):
    enabled: str


class InfoNodeInfoIngestInfo(TypedDict):
    downloader: InfoNodeInfoIngestDownloader


class InfoNodeInfoIngestProcessor(TypedDict):
    type: str


class InfoNodeInfoJvmMemory(TypedDict):
    direct_max: NotRequired[FieldCommonHumanReadableByteCount]
    direct_max_in_bytes: FieldCommonByteCount
    heap_init: NotRequired[FieldCommonHumanReadableByteCount]
    heap_init_in_bytes: FieldCommonByteCount
    heap_max: NotRequired[FieldCommonHumanReadableByteCount]
    heap_max_in_bytes: FieldCommonByteCount
    non_heap_init: NotRequired[FieldCommonHumanReadableByteCount]
    non_heap_init_in_bytes: FieldCommonByteCount
    non_heap_max: NotRequired[FieldCommonHumanReadableByteCount]
    non_heap_max_in_bytes: FieldCommonByteCount


class InfoNodeInfoMemory(TypedDict):
    total: FieldCommonHumanReadableByteCount
    total_in_bytes: FieldCommonByteCount


class InfoNodeInfoNetworkInterface(TypedDict):
    address: str
    mac_address: str
    name: FieldCommonName


class InfoNodeInfoOSCPU(TypedDict):
    cache_size: FieldCommonHumanReadableByteCount
    cache_size_in_bytes: FieldCommonByteCount
    cores_per_socket: int
    mhz: int
    model: str
    total_cores: int
    total_sockets: int
    vendor: str


class InfoNodeInfoPath(TypedDict):
    logs: str
    home: str
    repo: NotRequired[list[str]]
    data: NotRequired[list[str]]


class InfoNodeInfoRepositoriesUrl(TypedDict):
    allowed_urls: str


class InfoNodeInfoScript(TypedDict):
    allowed_types: str
    disable_max_compilations_rate: str


class InfoNodeInfoSearchPipelineProcessor(TypedDict):
    type: str


class InfoNodeInfoSearchPipelines(TypedDict):
    response_processors: NotRequired[list[InfoNodeInfoSearchPipelineProcessor]]
    request_processors: NotRequired[list[InfoNodeInfoSearchPipelineProcessor]]
    phase_results_processors: NotRequired[list[InfoNodeInfoSearchPipelineProcessor]]


class InfoNodeInfoSearchRemote(TypedDict):
    connect: str


class InfoNodeInfoSettingsClusterElection(TypedDict):
    strategy: FieldCommonName


class InfoNodeInfoSettingsDeprecationIndexing(TypedDict):
    enabled: FieldCommonStringifiedBoolean


class InfoNodeInfoSettingsHttpTypeConfig(TypedDict):
    default: NotRequired[str]


class InfoNodeInfoSettingsIndexStoreMmap(TypedDict):
    extensions: NotRequired[list[str]]


class InfoNodeInfoSettingsIngest(TypedDict):
    attachment: NotRequired[InfoNodeInfoIngestInfo]
    append: NotRequired[InfoNodeInfoIngestInfo]
    csv: NotRequired[InfoNodeInfoIngestInfo]
    convert: NotRequired[InfoNodeInfoIngestInfo]
    date: NotRequired[InfoNodeInfoIngestInfo]
    date_index_name: NotRequired[InfoNodeInfoIngestInfo]
    dot_expander: NotRequired[InfoNodeInfoIngestInfo]
    enrich: NotRequired[InfoNodeInfoIngestInfo]
    fail: NotRequired[InfoNodeInfoIngestInfo]
    foreach: NotRequired[InfoNodeInfoIngestInfo]
    json: NotRequired[InfoNodeInfoIngestInfo]
    user_agent: NotRequired[InfoNodeInfoIngestInfo]
    kv: NotRequired[InfoNodeInfoIngestInfo]
    geoip: NotRequired[InfoNodeInfoIngestInfo]
    grok: NotRequired[InfoNodeInfoIngestInfo]
    gsub: NotRequired[InfoNodeInfoIngestInfo]
    join: NotRequired[InfoNodeInfoIngestInfo]
    lowercase: NotRequired[InfoNodeInfoIngestInfo]
    remove: NotRequired[InfoNodeInfoIngestInfo]
    rename: NotRequired[InfoNodeInfoIngestInfo]
    script: NotRequired[InfoNodeInfoIngestInfo]
    set: NotRequired[InfoNodeInfoIngestInfo]
    sort: NotRequired[InfoNodeInfoIngestInfo]
    split: NotRequired[InfoNodeInfoIngestInfo]
    trim: NotRequired[InfoNodeInfoIngestInfo]
    uppercase: NotRequired[InfoNodeInfoIngestInfo]
    urldecode: NotRequired[InfoNodeInfoIngestInfo]
    bytes: NotRequired[InfoNodeInfoIngestInfo]
    dissect: NotRequired[InfoNodeInfoIngestInfo]
    set_security_user: NotRequired[InfoNodeInfoIngestInfo]
    pipeline: NotRequired[InfoNodeInfoIngestInfo]
    drop: NotRequired[InfoNodeInfoIngestInfo]
    circle: NotRequired[InfoNodeInfoIngestInfo]
    inference: NotRequired[InfoNodeInfoIngestInfo]


class InfoNodeInfoSettingsNetwork(TypedDict):
    host: FieldCommonHost


class InfoNodeInfoSettingsNode(TypedDict):
    name: FieldCommonName
    attr: NotRequired[dict[str, Any]]
    max_local_storage_nodes: NotRequired[str]


class InfoNodeInfoSettingsPlugins(TypedDict):
    pass


class InfoNodeInfoSettingsTransportTypeConfig(TypedDict):
    default: NotRequired[str]


class InfoNodeInfoTransport(TypedDict):
    bound_address: list[str]
    publish_address: str
    profiles: dict[str, str]


class InfoNodeThreadPoolInfo(TypedDict):
    core: NotRequired[int]
    keep_alive: NotRequired[FieldCommonDuration]
    max: NotRequired[int]
    queue_size: int
    size: NotRequired[int]
    type: str


class ReloadSecureSettingsNodeReloadResponse(TypedDict):
    name: FieldCommonName


class StatsBreaker(TypedDict):
    estimated_size: NotRequired[FieldCommonHumanReadableByteCount]
    estimated_size_in_bytes: NotRequired[FieldCommonByteCount]
    limit_size: NotRequired[FieldCommonHumanReadableByteCount]
    limit_size_in_bytes: NotRequired[FieldCommonByteCount]
    overhead: NotRequired[float]
    tripped: NotRequired[int]


class StatsCacheStatsBase(TypedDict):
    size: NotRequired[FieldCommonHumanReadableByteCount]
    size_in_bytes: NotRequired[FieldCommonByteCount]
    evictions: NotRequired[int]
    hit_count: NotRequired[int]
    miss_count: NotRequired[int]
    item_count: NotRequired[int]


class StatsCgroupMemoryStats(TypedDict):
    control_group: NotRequired[str]
    limit_in_bytes: NotRequired[str]
    usage_in_bytes: NotRequired[str]


class StatsClusterStateQueue(TypedDict):
    total: NotRequired[int]
    pending: NotRequired[int]
    committed: NotRequired[int]


class StatsDataPathStats(TypedDict):
    available: NotRequired[FieldCommonHumanReadableByteCount]
    available_in_bytes: NotRequired[FieldCommonByteCount]
    cache_reserved: NotRequired[FieldCommonHumanReadableByteCount]
    cache_reserved_in_bytes: NotRequired[FieldCommonByteCount]
    free: NotRequired[FieldCommonHumanReadableByteCount]
    free_in_bytes: NotRequired[FieldCommonByteCount]
    mount: NotRequired[str]
    path: NotRequired[str]
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_in_bytes: NotRequired[FieldCommonByteCount]
    type: NotRequired[str]


class StatsFileSystemTotal(TypedDict):
    available: NotRequired[FieldCommonHumanReadableByteCount]
    available_in_bytes: NotRequired[FieldCommonByteCount]
    free: NotRequired[FieldCommonHumanReadableByteCount]
    free_in_bytes: NotRequired[FieldCommonByteCount]
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_in_bytes: NotRequired[FieldCommonByteCount]
    cache_reserved: NotRequired[FieldCommonHumanReadableByteCount]
    cache_reserved_in_bytes: NotRequired[FieldCommonByteCount]


class StatsHttp(TypedDict):
    current_open: NotRequired[int]
    total_opened: NotRequired[int]


StatsIndexMetric: TypeAlias = Literal[
    "_all",
    "completion",
    "docs",
    "fielddata",
    "flush",
    "get",
    "indexing",
    "merge",
    "query_cache",
    "recovery",
    "refresh",
    "request_cache",
    "search",
    "segments",
    "store",
    "suggest",
    "translog",
    "warmer",
]


class StatsJvmClasses(TypedDict):
    current_loaded_count: NotRequired[int]
    total_loaded_count: NotRequired[int]
    total_unloaded_count: NotRequired[int]


class StatsJvmThreads(TypedDict):
    count: NotRequired[int]
    peak_count: NotRequired[int]


class StatsLastGcStats(TypedDict):
    used: NotRequired[FieldCommonHumanReadableByteCount]
    used_in_bytes: NotRequired[FieldCommonByteCount]
    max: NotRequired[FieldCommonHumanReadableByteCount]
    max_in_bytes: NotRequired[FieldCommonByteCount]
    usage_percent: NotRequired[FieldCommonPercentageNumber]


class StatsMemoryStatsBase(TypedDict):
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_in_bytes: NotRequired[FieldCommonByteCount]
    free: NotRequired[FieldCommonHumanReadableByteCount]
    free_in_bytes: NotRequired[FieldCommonByteCount]
    used: NotRequired[FieldCommonHumanReadableByteCount]
    used_in_bytes: NotRequired[FieldCommonByteCount]


StatsMetric: TypeAlias = Literal[
    "_all",
    "adaptive_selection",
    "admission_control",
    "breaker",
    "caches",
    "cluster_manager_throttling",
    "discovery",
    "file_cache",
    "fs",
    "http",
    "indexing_pressure",
    "indices",
    "ingest",
    "jvm",
    "os",
    "process",
    "repositories",
    "resource_usage_stats",
    "script",
    "script_cache",
    "search_backpressure",
    "search_pipeline",
    "segment_replication_backpressure",
    "shard_indexing_pressure",
    "task_cancellation",
    "thread_pool",
    "transport",
    "weighted_routing",
]


class StatsNodeBufferPool(TypedDict):
    count: NotRequired[int]
    total_capacity: NotRequired[FieldCommonHumanReadableByteCount]
    total_capacity_in_bytes: NotRequired[FieldCommonByteCount]
    used: NotRequired[FieldCommonHumanReadableByteCount]
    used_in_bytes: NotRequired[FieldCommonByteCount]


class StatsOperatingSystemCpuStats(TypedDict):
    percent: NotRequired[FieldCommonPercentageNumber]
    load_average: NotRequired[dict[str, float]]


class StatsPool(TypedDict):
    used: NotRequired[FieldCommonHumanReadableByteCount]
    used_in_bytes: NotRequired[FieldCommonByteCount]
    max: NotRequired[FieldCommonHumanReadableByteCount]
    max_in_bytes: NotRequired[FieldCommonByteCount]
    peak_used: NotRequired[FieldCommonHumanReadableByteCount]
    peak_used_in_bytes: NotRequired[FieldCommonByteCount]
    peak_max: NotRequired[FieldCommonHumanReadableByteCount]
    peak_max_in_bytes: NotRequired[FieldCommonByteCount]
    last_gc_stats: NotRequired[StatsLastGcStats]


class StatsPressureMemory(TypedDict):
    all: NotRequired[FieldCommonHumanReadableByteCount]
    all_in_bytes: NotRequired[FieldCommonByteCount]
    combined_coordinating_and_primary: NotRequired[FieldCommonHumanReadableByteCount]
    combined_coordinating_and_primary_in_bytes: NotRequired[FieldCommonByteCount]
    coordinating: NotRequired[FieldCommonHumanReadableByteCount]
    coordinating_in_bytes: NotRequired[FieldCommonByteCount]
    primary: NotRequired[FieldCommonHumanReadableByteCount]
    primary_in_bytes: NotRequired[FieldCommonByteCount]
    replica: NotRequired[FieldCommonHumanReadableByteCount]
    replica_in_bytes: NotRequired[FieldCommonByteCount]
    coordinating_rejections: NotRequired[int]
    primary_rejections: NotRequired[int]
    replica_rejections: NotRequired[int]


class StatsProcessMemoryStats(TypedDict):
    total_virtual: NotRequired[FieldCommonHumanReadableByteCount]
    total_virtual_in_bytes: NotRequired[FieldCommonByteCount]


class StatsPublishedClusterStates(TypedDict):
    full_states: NotRequired[int]
    incompatible_diffs: NotRequired[int]
    compatible_diffs: NotRequired[int]


class StatsRepositoryStatsSnapshot(TypedDict):
    repository_name: NotRequired[str]
    repository_type: NotRequired[str]
    repository_location: NotRequired[dict[str, str]]
    request_counts: NotRequired[dict[str, int]]
    request_success_total: NotRequired[dict[str, int]]
    request_failures_total: NotRequired[dict[str, int]]
    request_time_in_millis: NotRequired[dict[str, int]]
    request_retry_count_total: NotRequired[dict[str, int]]


class StatsScriptStatsBase(TypedDict):
    cache_evictions: int
    compilations: int
    compilation_limit_triggered: int


class StatsShardClusterManagerThrottlingStatsDetail(TypedDict):
    total_throttled_tasks: int
    throttled_tasks_per_task_type: dict[str, int]


class StatsShardIndexingPressurePerShardMemoryAllocationCurrentStats(TypedDict):
    current_coordinating_and_primary_bytes: FieldCommonByteCount
    current_replica_bytes: FieldCommonByteCount


class StatsShardIndexingPressurePerShardMemoryAllocationLimitStats(TypedDict):
    current_coordinating_and_primary_limits_in_bytes: FieldCommonByteCount
    current_replica_limits_in_bytes: FieldCommonByteCount


class StatsShardIndexingPressurePerShardMemoryAllocationStats(TypedDict):
    current: StatsShardIndexingPressurePerShardMemoryAllocationCurrentStats
    limit: StatsShardIndexingPressurePerShardMemoryAllocationLimitStats


class StatsShardIndexingPressurePerShardMemoryStatsDetails(TypedDict):
    coordinating: NotRequired[FieldCommonHumanReadableByteCount]
    coordinating_in_bytes: FieldCommonByteCount
    primary: NotRequired[FieldCommonHumanReadableByteCount]
    primary_in_bytes: FieldCommonByteCount
    replica: NotRequired[FieldCommonHumanReadableByteCount]
    replica_in_bytes: FieldCommonByteCount


class StatsShardIndexingPressureRejectionsBreakupStats(TypedDict):
    node_limits: NotRequired[int]
    no_successful_request_limits: NotRequired[int]
    throughput_degradation_limits: NotRequired[int]


StatsShardRepositoriesStats: TypeAlias = list[StatsRepositoryStatsSnapshot]


class StatsShardResourceUsageStatsIoUsageStats(TypedDict):
    max_io_utilization_percent: NotRequired[FieldCommonPercentageString]


StatsShardSearchBackpressureMode: TypeAlias = Literal[
    "disabled", "enforced", "monitor_only"
]


class StatsShardSearchBackpressureTaskCancellationStats(TypedDict):
    cancellation_count: NotRequired[int]
    cancellation_limit_reached_count: NotRequired[int]
    cancelled_task_percentage: NotRequired[FieldCommonPercentageNumber]
    current_cancellation_eligible_tasks_count: NotRequired[int]


class StatsShardSearchBackpressureTaskResourceTrackerHeapUsageTrackerStats(TypedDict):
    cancellation_count: NotRequired[int]
    current_max: NotRequired[FieldCommonHumanReadableByteCount]
    current_max_bytes: NotRequired[FieldCommonByteCount]
    current_avg: NotRequired[FieldCommonHumanReadableByteCount]
    current_avg_bytes: NotRequired[FieldCommonByteCount]
    rolling_avg: NotRequired[FieldCommonHumanReadableByteCount]
    rolling_avg_bytes: NotRequired[FieldCommonByteCount]


class StatsShardSegmentReplicationBackpressureStats(TypedDict):
    total_rejected_requests: NotRequired[int]


class StatsShardTaskCancellationStatsDetail(TypedDict):
    current_count_post_cancel: NotRequired[int]
    total_count_post_cancel: NotRequired[int]


class StatsShardWeightedRoutingStatsDetail(TypedDict):
    fail_open_count: NotRequired[int]


class StatsTransport(TypedDict):
    rx_count: NotRequired[int]
    rx_size: NotRequired[FieldCommonHumanReadableByteCount]
    rx_size_in_bytes: NotRequired[FieldCommonByteCount]
    server_open: NotRequired[int]
    tx_count: NotRequired[int]
    tx_size: NotRequired[FieldCommonHumanReadableByteCount]
    tx_size_in_bytes: NotRequired[FieldCommonByteCount]
    total_outbound_connections: NotRequired[int]


class StatsTransportUsageStats(TypedDict):
    rejection_count: NotRequired[dict[str, int]]


class StatsUsageStats(TypedDict):
    transport: NotRequired[StatsTransportUsageStats]


UsageMetric: TypeAlias = Literal["_all", "aggregations", "rest_actions"]


class FieldCommonNodesResponseBase(TypedDict):
    field_nodes: NotRequired[FieldCommonNodeStatistics]


class InfoNodeInfoIngest(TypedDict):
    processors: list[InfoNodeInfoIngestProcessor]


class InfoNodeInfoNetwork(TypedDict):
    primary_interface: InfoNodeInfoNetworkInterface
    refresh_interval: int


class InfoNodeInfoRepositories(TypedDict):
    url: InfoNodeInfoRepositoriesUrl


class InfoNodeInfoSearch(TypedDict):
    remote: InfoNodeInfoSearchRemote


InfoNodeInfoSettingsHttpType: TypeAlias = str | InfoNodeInfoSettingsHttpTypeConfig


class InfoNodeInfoSettingsIndexHybrid(TypedDict):
    mmap: NotRequired[InfoNodeInfoSettingsIndexStoreMmap]


class InfoNodeInfoSettingsIndexStore(TypedDict):
    hybrid: NotRequired[InfoNodeInfoSettingsIndexHybrid]


InfoNodeInfoSettingsTransportType: TypeAlias = (
    str | InfoNodeInfoSettingsTransportTypeConfig
)


class InfoNodeOperatingSystemInfo(TypedDict):
    arch: NotRequired[str]
    available_processors: int
    allocated_processors: NotRequired[int]
    name: NotRequired[FieldCommonName]
    pretty_name: NotRequired[FieldCommonName]
    refresh_interval: NotRequired[FieldCommonDuration]
    refresh_interval_in_millis: FieldCommonDurationValueUnitMillis
    version: NotRequired[FieldCommonVersionString]
    cpu: NotRequired[InfoNodeInfoOSCPU]
    mem: NotRequired[InfoNodeInfoMemory]
    swap: NotRequired[InfoNodeInfoMemory]


class InfoNodeProcessInfo(TypedDict):
    id: int
    mlockall: bool
    refresh_interval: NotRequired[FieldCommonDuration]
    refresh_interval_in_millis: FieldCommonDurationValueUnitMillis


class ReloadSecureSettingsNodeReloadError(ReloadSecureSettingsNodeReloadResponse):
    reload_exception: NotRequired[FieldCommonErrorCause]


ReloadSecureSettingsNodeReloadResult: TypeAlias = (
    ReloadSecureSettingsNodeReloadResponse | ReloadSecureSettingsNodeReloadError
)


class StatsAdaptiveSelection(TypedDict):
    avg_queue_size: NotRequired[int]
    avg_response_time: NotRequired[FieldCommonDuration]
    avg_response_time_ns: NotRequired[FieldCommonDurationValueUnitNanos]
    avg_service_time: NotRequired[FieldCommonDuration]
    avg_service_time_ns: NotRequired[FieldCommonDurationValueUnitNanos]
    outgoing_searches: NotRequired[int]
    rank: NotRequired[str]


class StatsCacheIndicesStats(StatsCacheStatsBase):
    pass


class StatsCacheShardStats(StatsCacheStatsBase):
    pass


class StatsCacheStats(StatsCacheStatsBase):
    store_name: NotRequired[str]
    indices: NotRequired[dict[str, StatsCacheIndicesStats]]
    shards: NotRequired[dict[str, StatsCacheShardStats]]


class StatsCgroupCpuAcctStats(TypedDict):
    control_group: NotRequired[str]
    usage_nanos: NotRequired[FieldCommonDurationValueUnitNanos]


class StatsCgroupCpuStat(TypedDict):
    number_of_elapsed_periods: NotRequired[int]
    number_of_times_throttled: NotRequired[int]
    time_throttled_nanos: NotRequired[FieldCommonDurationValueUnitNanos]


class StatsCgroupCpuStats(TypedDict):
    control_group: NotRequired[str]
    cfs_period_micros: NotRequired[FieldCommonDurationValueUnitMicros]
    cfs_quota_micros: NotRequired[FieldCommonDurationValueUnitMicros]
    stat: NotRequired[StatsCgroupCpuStat]


class StatsCgroupStats(TypedDict):
    cpuacct: NotRequired[StatsCgroupCpuAcctStats]
    cpu: NotRequired[StatsCgroupCpuStats]
    memory: NotRequired[StatsCgroupMemoryStats]


class StatsClusterStateOverallStats(TypedDict):
    update_count: NotRequired[int]
    total_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    failed_count: NotRequired[int]


class StatsClusterStateStats(TypedDict):
    overall: NotRequired[StatsClusterStateOverallStats]


class StatsDiscovery(TypedDict):
    cluster_state_queue: NotRequired[StatsClusterStateQueue]
    cluster_state_stats: NotRequired[StatsClusterStateStats]
    published_cluster_states: NotRequired[StatsPublishedClusterStates]


class StatsExtendedMemoryStats(StatsMemoryStatsBase):
    free_percent: NotRequired[FieldCommonPercentageNumber]
    used_percent: NotRequired[FieldCommonPercentageNumber]


class StatsGarbageCollectorTotal(TypedDict):
    collection_count: NotRequired[int]
    collection_time: NotRequired[FieldCommonDuration]
    collection_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class StatsIndexingPressureMemory(TypedDict):
    limit: NotRequired[FieldCommonHumanReadableByteCount]
    limit_in_bytes: NotRequired[FieldCommonByteCount]
    current: NotRequired[StatsPressureMemory]
    total: NotRequired[StatsPressureMemory]


class StatsIoStatDevice(TypedDict):
    device_name: NotRequired[str]
    operations: NotRequired[int]
    read_kilobytes: NotRequired[int]
    read_operations: NotRequired[int]
    write_kilobytes: NotRequired[int]
    write_operations: NotRequired[int]
    read_time: NotRequired[int]
    write_time: NotRequired[int]
    queue_size: NotRequired[int]
    io_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class StatsIoStats(TypedDict):
    devices: NotRequired[list[StatsIoStatDevice]]
    total: NotRequired[StatsIoStatDevice]


class StatsJvmMemoryStats(TypedDict):
    heap_used: NotRequired[FieldCommonHumanReadableByteCount]
    heap_used_in_bytes: NotRequired[FieldCommonByteCount]
    heap_used_percent: NotRequired[FieldCommonPercentageNumber]
    heap_committed: NotRequired[FieldCommonHumanReadableByteCount]
    heap_committed_in_bytes: NotRequired[FieldCommonByteCount]
    heap_max: NotRequired[FieldCommonHumanReadableByteCount]
    heap_max_in_bytes: NotRequired[FieldCommonByteCount]
    non_heap_used: NotRequired[FieldCommonHumanReadableByteCount]
    non_heap_used_in_bytes: NotRequired[FieldCommonByteCount]
    non_heap_committed: NotRequired[FieldCommonHumanReadableByteCount]
    non_heap_committed_in_bytes: NotRequired[FieldCommonByteCount]
    pools: NotRequired[dict[str, StatsPool]]


class StatsMemoryStats(StatsMemoryStatsBase):
    pass


class StatsOperatingSystem(TypedDict):
    cpu: NotRequired[StatsOperatingSystemCpuStats]
    mem: NotRequired[StatsExtendedMemoryStats]
    swap: NotRequired[StatsMemoryStats]
    cgroup: NotRequired[StatsCgroupStats]
    timestamp: NotRequired[FieldCommonEpochTimeUnitMillis]


class StatsProcessCpuStats(TypedDict):
    percent: FieldCommonPercentageNumber
    total: NotRequired[FieldCommonDuration]
    total_in_millis: FieldCommonDurationValueUnitMillis


class StatsProcessor(TypedDict):
    count: NotRequired[int]
    current: NotRequired[int]
    failed: NotRequired[int]
    time: NotRequired[FieldCommonDuration]
    time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class StatsRemoteStoreStats(TypedDict):
    last_successful_fetch_of_pinned_timestamps: NotRequired[
        FieldCommonEpochTimeUnitSeconds
    ]


class StatsScriptContextStats(StatsScriptStatsBase):
    context: str


class StatsScriptStats(StatsScriptStatsBase):
    pass


class StatsShardAdmissionControlStats(TypedDict):
    global_io_usage: NotRequired[StatsUsageStats]
    global_cpu_usage: NotRequired[StatsUsageStats]


class StatsShardClusterManagerThrottlingStats(TypedDict):
    stats: NotRequired[StatsShardClusterManagerThrottlingStatsDetail]


class StatsShardIndexingPressurePerShardIndexingStats(TypedDict):
    coordinating_time_in_millis: FieldCommonDurationValueUnitMillis
    coordinating_count: int
    primary_time_in_millis: FieldCommonDurationValueUnitMillis
    primary_count: int
    replica_time_in_millis: FieldCommonDurationValueUnitMillis
    replica_count: int


class StatsShardIndexingPressurePerShardLastSuccessfulTimestamp(TypedDict):
    coordinating_last_successful_request_timestamp_in_millis: (
        FieldCommonEpochTimeUnitMillis
    )
    primary_last_successful_request_timestamp_in_millis: FieldCommonEpochTimeUnitMillis
    replica_last_successful_request_timestamp_in_millis: FieldCommonEpochTimeUnitMillis


class StatsShardIndexingPressurePerShardMemoryStats(TypedDict):
    current: StatsShardIndexingPressurePerShardMemoryStatsDetails
    total: StatsShardIndexingPressurePerShardMemoryStatsDetails


class StatsShardIndexingPressurePerShardRejectionCoordinatingStats(TypedDict):
    coordinating_rejections: int
    breakup: NotRequired[StatsShardIndexingPressureRejectionsBreakupStats]
    breakup_shadow_mode: NotRequired[StatsShardIndexingPressureRejectionsBreakupStats]


class StatsShardIndexingPressurePerShardRejectionPrimaryStats(TypedDict):
    primary_rejections: int
    breakup: NotRequired[StatsShardIndexingPressureRejectionsBreakupStats]
    breakup_shadow_mode: NotRequired[StatsShardIndexingPressureRejectionsBreakupStats]


class StatsShardIndexingPressurePerShardRejectionReplicaStats(TypedDict):
    replica_rejections: int
    breakup: NotRequired[StatsShardIndexingPressureRejectionsBreakupStats]
    breakup_shadow_mode: NotRequired[StatsShardIndexingPressureRejectionsBreakupStats]


class StatsShardIndexingPressurePerShardRejectionStats(TypedDict):
    coordinating: StatsShardIndexingPressurePerShardRejectionCoordinatingStats
    primary: StatsShardIndexingPressurePerShardRejectionPrimaryStats
    replica: StatsShardIndexingPressurePerShardRejectionReplicaStats


class StatsShardIndexingPressurePerShardStats(TypedDict):
    memory: StatsShardIndexingPressurePerShardMemoryStats
    rejection: StatsShardIndexingPressurePerShardRejectionStats
    last_successful_timestamp: StatsShardIndexingPressurePerShardLastSuccessfulTimestamp
    indexing: StatsShardIndexingPressurePerShardIndexingStats
    memory_allocation: StatsShardIndexingPressurePerShardMemoryAllocationStats


class StatsShardIndexingPressureStats(TypedDict):
    stats: NotRequired[dict[str, StatsShardIndexingPressurePerShardStats]]
    enabled: NotRequired[bool]
    enforced: NotRequired[bool]
    total_rejections_breakup: NotRequired[
        StatsShardIndexingPressureRejectionsBreakupStats
    ]
    total_rejections_breakup_shadow_mode: NotRequired[
        StatsShardIndexingPressureRejectionsBreakupStats
    ]


class StatsShardResourceUsageStatsDetail(TypedDict):
    timestamp: NotRequired[FieldCommonEpochTimeUnitMillis]
    cpu_utilization_percent: NotRequired[FieldCommonPercentageString]
    memory_utilization_percent: NotRequired[FieldCommonPercentageString]
    io_usage_stats: NotRequired[StatsShardResourceUsageStatsIoUsageStats]


class StatsShardSearchBackpressureTaskResourceTrackerCpuUsageTrackerStats(TypedDict):
    cancellation_count: NotRequired[int]
    current_max: NotRequired[FieldCommonDuration]
    current_max_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    current_avg: NotRequired[FieldCommonDuration]
    current_avg_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class StatsShardSearchBackpressureTaskResourceTrackerElapsedTimeTrackerStats(TypedDict):
    cancellation_count: NotRequired[int]
    current_max: NotRequired[FieldCommonDuration]
    current_max_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    current_avg: NotRequired[FieldCommonDuration]
    current_avg_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class StatsShardSearchBackpressureTaskResourceTrackerStats(TypedDict):
    heap_usage_tracker: NotRequired[
        StatsShardSearchBackpressureTaskResourceTrackerHeapUsageTrackerStats
    ]
    elapsed_time_tracker: NotRequired[
        StatsShardSearchBackpressureTaskResourceTrackerElapsedTimeTrackerStats
    ]
    cpu_usage_tracker: NotRequired[
        StatsShardSearchBackpressureTaskResourceTrackerCpuUsageTrackerStats
    ]


class StatsShardSearchBackpressureTaskStats(TypedDict):
    resource_tracker_stats: NotRequired[
        StatsShardSearchBackpressureTaskResourceTrackerStats
    ]
    cancellation_stats: NotRequired[StatsShardSearchBackpressureTaskCancellationStats]
    completion_count: NotRequired[int]


class StatsShardSearchPipelineOperationStats(TypedDict):
    count: NotRequired[int]
    time: NotRequired[FieldCommonDuration]
    time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    current: NotRequired[int]
    failed: NotRequired[int]


class StatsShardSearchPipelinePerPipelineProcessorStats(TypedDict):
    type: NotRequired[str]
    stats: NotRequired[StatsShardSearchPipelineOperationStats]


class StatsShardSearchPipelinePerPipelineStats(TypedDict):
    request: NotRequired[StatsShardSearchPipelineOperationStats]
    response: NotRequired[StatsShardSearchPipelineOperationStats]
    request_processors: NotRequired[
        list[StatsShardSearchPipelinePerPipelineProcessorStats]
    ]
    response_processors: NotRequired[
        list[dict[str, StatsShardSearchPipelinePerPipelineProcessorStats]]
    ]


class StatsShardSearchPipelineStats(TypedDict):
    total_request: NotRequired[StatsShardSearchPipelineOperationStats]
    total_response: NotRequired[StatsShardSearchPipelineOperationStats]
    pipelines: NotRequired[dict[str, StatsShardSearchPipelinePerPipelineStats]]


class StatsShardTaskCancellationStats(TypedDict):
    search_shard_task: NotRequired[StatsShardTaskCancellationStatsDetail]
    search_task: NotRequired[StatsShardTaskCancellationStatsDetail]


class StatsShardWeightedRoutingStats(TypedDict):
    stats: NotRequired[StatsShardWeightedRoutingStatsDetail]


class StatsThreadCount(TypedDict):
    active: NotRequired[int]
    completed: NotRequired[int]
    largest: NotRequired[int]
    queue: NotRequired[int]
    rejected: NotRequired[int]
    threads: NotRequired[int]
    total_wait_time: NotRequired[FieldCommonDuration]
    total_wait_time_in_nanos: NotRequired[FieldCommonDurationValueUnitNanos]


class UsageNodeUsage(TypedDict):
    rest_actions: NotRequired[dict[str, int]]
    since: FieldCommonEpochTimeUnitMillis
    timestamp: FieldCommonEpochTimeUnitMillis
    aggregations: NotRequired[dict[str, Any]]


class InfoNodeInfoSettingsCluster(TypedDict):
    name: FieldCommonName
    routing: NotRequired[FieldCommonIndexRouting]
    election: NotRequired[InfoNodeInfoSettingsClusterElection]
    initial_cluster_manager_nodes: NotRequired[FieldCommonStringOrStringArray]
    initial_master_nodes: NotRequired[FieldCommonStringOrStringArray]
    deprecation_indexing: NotRequired[InfoNodeInfoSettingsDeprecationIndexing]


InfoNodeInfoSettingsHttp = TypedDict(
    "InfoNodeInfoSettingsHttp",
    {
        "type": InfoNodeInfoSettingsHttpType,
        "type.default": NotRequired[str],
        "compression": NotRequired[FieldCommonStringifiedBoolean],
        "port": NotRequired[FieldCommonStringifiedInteger],
    },
)


class InfoNodeInfoSettingsIndex(TypedDict):
    store: NotRequired[InfoNodeInfoSettingsIndexStore]


InfoNodeInfoSettingsTransport = TypedDict(
    "InfoNodeInfoSettingsTransport",
    {
        "type": InfoNodeInfoSettingsTransportType,
        "type.default": NotRequired[str],
    },
)


class InfoNodeJvmInfo(TypedDict):
    gc_collectors: NotRequired[list[str]]
    mem: InfoNodeInfoJvmMemory
    memory_pools: NotRequired[list[str]]
    pid: int
    start_time: NotRequired[FieldCommonDateTime]
    start_time_in_millis: FieldCommonEpochTimeUnitMillis
    version: NotRequired[FieldCommonVersionString]
    vm_name: NotRequired[FieldCommonName]
    vm_vendor: NotRequired[str]
    vm_version: NotRequired[FieldCommonVersionString]
    bundled_jdk: bool
    using_bundled_jdk: NotRequired[bool | None]
    using_compressed_ordinary_object_pointers: NotRequired[
        FieldCommonStringifiedBoolean
    ]
    input_arguments: NotRequired[list[str]]


StatsCachesStats: TypeAlias = dict[str, StatsCacheStats]


class StatsFileSystem(TypedDict):
    data: NotRequired[list[StatsDataPathStats]]
    timestamp: NotRequired[FieldCommonEpochTimeUnitMillis]
    total: NotRequired[StatsFileSystemTotal]
    io_stats: NotRequired[StatsIoStats]


class StatsGarbageCollector(TypedDict):
    collectors: NotRequired[dict[str, StatsGarbageCollectorTotal]]


class StatsIndexingPressure(TypedDict):
    memory: NotRequired[StatsIndexingPressureMemory]


class StatsJvm(TypedDict):
    buffer_pools: NotRequired[dict[str, StatsNodeBufferPool]]
    classes: NotRequired[StatsJvmClasses]
    gc: NotRequired[StatsGarbageCollector]
    mem: NotRequired[StatsJvmMemoryStats]
    threads: NotRequired[StatsJvmThreads]
    timestamp: NotRequired[FieldCommonEpochTimeUnitMillis]
    uptime: NotRequired[FieldCommonDuration]
    uptime_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class StatsKeyedProcessor(TypedDict):
    stats: NotRequired[StatsProcessor]
    type: NotRequired[str]


class StatsProcess(TypedDict):
    cpu: NotRequired[StatsProcessCpuStats]
    mem: NotRequired[StatsProcessMemoryStats]
    open_file_descriptors: NotRequired[int]
    max_file_descriptors: NotRequired[int]
    timestamp: NotRequired[FieldCommonEpochTimeUnitMillis]


class StatsScriptCacheStats(TypedDict):
    sum: StatsScriptStats
    contexts: NotRequired[list[StatsScriptContextStats]]


StatsShardResourceUsageStats: TypeAlias = dict[str, StatsShardResourceUsageStatsDetail]


class StatsShardSearchBackpressureStats(TypedDict):
    search_task: NotRequired[StatsShardSearchBackpressureTaskStats]
    search_shard_task: NotRequired[StatsShardSearchBackpressureTaskStats]
    mode: NotRequired[StatsShardSearchBackpressureMode]


class InfoNodeInfoSettings(TypedDict):
    cluster: InfoNodeInfoSettingsCluster
    node: InfoNodeInfoSettingsNode
    path: InfoNodeInfoPath
    repositories: NotRequired[InfoNodeInfoRepositories]
    discovery: NotRequired[InfoNodeInfoDiscovery]
    action: NotRequired[InfoNodeInfoAction]
    client: InfoNodeInfoClient
    http: InfoNodeInfoSettingsHttp
    bootstrap: NotRequired[InfoNodeInfoBootstrap]
    transport: InfoNodeInfoSettingsTransport
    network: NotRequired[InfoNodeInfoSettingsNetwork]
    script: NotRequired[InfoNodeInfoScript]
    search: NotRequired[InfoNodeInfoSearch]
    ingest: NotRequired[InfoNodeInfoSettingsIngest]
    index: NotRequired[InfoNodeInfoSettingsIndex]
    plugins: NotRequired[InfoNodeInfoSettingsPlugins]


class StatsIngestTotal(TypedDict):
    count: NotRequired[int]
    current: NotRequired[int]
    failed: NotRequired[int]
    processors: NotRequired[list[dict[str, StatsKeyedProcessor]]]
    time: NotRequired[FieldCommonDuration]
    time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]


class StatsNodeIndexShardStats(StatsIndexShardStatsBase):
    pass


class StatsNodeIndicesStats(StatsIndexStatsBase):
    indices: NotRequired[dict[str, StatsIndexStats]]
    shards: NotRequired[dict[str, list[dict[str, StatsNodeIndexShardStats]]]]


class InfoNodeInfo(TypedDict):
    attributes: NotRequired[dict[str, str]]
    build_flavor: NotRequired[str]
    build_hash: str
    build_type: str
    host: NotRequired[FieldCommonHost]
    http: NotRequired[InfoNodeInfoHttp]
    ip: NotRequired[FieldCommonIp]
    jvm: NotRequired[InfoNodeJvmInfo]
    name: FieldCommonName
    network: NotRequired[InfoNodeInfoNetwork]
    os: NotRequired[InfoNodeOperatingSystemInfo]
    plugins: NotRequired[list[FieldCommonPluginStats]]
    process: NotRequired[InfoNodeProcessInfo]
    roles: FieldCommonNodeRoles
    settings: NotRequired[InfoNodeInfoSettings]
    thread_pool: NotRequired[dict[str, InfoNodeThreadPoolInfo]]
    total_indexing_buffer: NotRequired[
        FieldCommonByteCount | FieldCommonHumanReadableByteCount
    ]
    total_indexing_buffer_in_bytes: NotRequired[
        FieldCommonHumanReadableByteCount | FieldCommonByteCount
    ]
    transport: NotRequired[InfoNodeInfoTransport]
    transport_address: NotRequired[FieldCommonTransportAddress]
    version: FieldCommonVersionString
    modules: NotRequired[list[FieldCommonPluginStats]]
    ingest: NotRequired[InfoNodeInfoIngest]
    aggregations: NotRequired[dict[str, InfoNodeInfoAggregation]]
    search_pipelines: NotRequired[InfoNodeInfoSearchPipelines]


class StatsIngest(TypedDict):
    pipelines: NotRequired[dict[str, StatsIngestTotal]]
    total: NotRequired[StatsIngestTotal]


class StatsStats(TypedDict):
    adaptive_selection: NotRequired[dict[str, StatsAdaptiveSelection]]
    breakers: NotRequired[dict[str, StatsBreaker]]
    fs: NotRequired[StatsFileSystem]
    host: NotRequired[FieldCommonHost]
    http: NotRequired[StatsHttp]
    ingest: NotRequired[StatsIngest]
    ip: NotRequired[FieldCommonIp | list[FieldCommonIp]]
    jvm: NotRequired[StatsJvm]
    name: NotRequired[FieldCommonName]
    os: NotRequired[StatsOperatingSystem]
    process: NotRequired[StatsProcess]
    roles: NotRequired[FieldCommonNodeRoles]
    script: NotRequired[StatsScriptStats]
    script_cache: NotRequired[StatsScriptCacheStats]
    thread_pool: NotRequired[dict[str, StatsThreadCount]]
    timestamp: NotRequired[FieldCommonEpochTimeUnitMillis]
    transport: NotRequired[StatsTransport]
    transport_address: NotRequired[FieldCommonTransportAddress]
    attributes: NotRequired[dict[str, str]]
    discovery: NotRequired[StatsDiscovery]
    indexing_pressure: NotRequired[StatsIndexingPressure]
    indices: NotRequired[StatsNodeIndicesStats]
    shard_indexing_pressure: NotRequired[StatsShardIndexingPressureStats]
    search_backpressure: NotRequired[StatsShardSearchBackpressureStats]
    cluster_manager_throttling: NotRequired[StatsShardClusterManagerThrottlingStats]
    weighted_routing: NotRequired[StatsShardWeightedRoutingStats]
    task_cancellation: NotRequired[StatsShardTaskCancellationStats]
    resource_usage_stats: NotRequired[StatsShardResourceUsageStats]
    search_pipeline: NotRequired[StatsShardSearchPipelineStats]
    segment_replication_backpressure: NotRequired[
        StatsShardSegmentReplicationBackpressureStats
    ]
    remote_store: NotRequired[StatsRemoteStoreStats]
    repositories: NotRequired[StatsShardRepositoriesStats]
    admission_control: NotRequired[StatsShardAdmissionControlStats]
    caches: NotRequired[StatsCachesStats]
