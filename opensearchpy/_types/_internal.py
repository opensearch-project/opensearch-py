# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from __future__ import annotations

from typing import Any, Literal, TypeAlias, TypedDict, Union

from typing_extensions import NotRequired


class FieldCommonAcknowledgedResponseBase(TypedDict):
    acknowledged: bool


FieldCommonActionStatusOptions: TypeAlias = Literal[
    "failure", "simulated", "success", "throttled"
]

FieldCommonBatchSize: TypeAlias = int

FieldCommonBuiltinScriptLanguage: TypeAlias = Literal[
    "expression", "java", "mustache", "painless"
]

FieldCommonByte: TypeAlias = float

FieldCommonByteCount: TypeAlias = int

FieldCommonByteUnit: TypeAlias = (
    Literal["b"]
    | Literal["kb", "k"]
    | Literal["mb", "m"]
    | Literal["gb", "g"]
    | Literal["tb", "t"]
    | Literal["pb", "p"]
)


class FieldCommonClusterStatistics(TypedDict):
    skipped: int
    successful: int
    total: int


FieldCommonConflicts: TypeAlias = Literal["abort", "proceed"]


class FieldCommonCoordsGeoBounds(TypedDict):
    top: float
    bottom: float
    left: float
    right: float


FieldCommonDataStreamName: TypeAlias = str

FieldCommonDataStreamNames: TypeAlias = (
    FieldCommonDataStreamName | list[FieldCommonDataStreamName]
)

FieldCommonDateFormat: TypeAlias = str

FieldCommonDateMath: TypeAlias = str

FieldCommonDFIIndependenceMeasure: TypeAlias = Literal[
    "chisquared", "saturated", "standardized"
]

FieldCommonDFRAfterEffect: TypeAlias = Literal["b", "l", "no"]

FieldCommonDFRBasicModel: TypeAlias = Literal["be", "d", "g", "if", "in", "ine", "p"]

FieldCommonDistance: TypeAlias = str

FieldCommonDistanceUnit: TypeAlias = Literal[
    "cm", "ft", "in", "km", "m", "mi", "mm", "nmi", "yd"
]


class FieldCommonDocStats(TypedDict):
    count: int
    deleted: NotRequired[int]


FieldCommonDocStatus = TypedDict(
    "FieldCommonDocStatus",
    {
        "1xx": NotRequired[int],
        "2xx": NotRequired[int],
        "3xx": NotRequired[int],
        "4xx": NotRequired[int],
        "5xx": NotRequired[int],
    },
)

FieldCommonDuration: TypeAlias = str

FieldCommonDurationLarge: TypeAlias = str


class FieldCommonEmptyObject(TypedDict):
    pass


FieldCommonExpandWildcard: TypeAlias = Literal[
    "all", "closed", "hidden", "none", "open"
]

FieldCommonExpandWildcards: TypeAlias = (
    FieldCommonExpandWildcard | list[FieldCommonExpandWildcard]
)

FieldCommonField: TypeAlias = str

FieldCommonFields: TypeAlias = FieldCommonField | list[FieldCommonField]

FieldCommonFieldSortNumericType: TypeAlias = Literal[
    "date", "date_nanos", "double", "long"
]

FieldCommonFieldValue: TypeAlias = bool | float | str | None

FieldCommonFuzziness: TypeAlias = str | int

FieldCommonGeoDistanceType: TypeAlias = Literal["arc", "plane"]

FieldCommonGeoHash: TypeAlias = str


class FieldCommonGeoHashLocation(TypedDict):
    geohash: FieldCommonGeoHash


FieldCommonGeoHashPrecision: TypeAlias = int | str

FieldCommonGeoShapeRelation: TypeAlias = Literal[
    "contains", "disjoint", "intersects", "within"
]

FieldCommonGeoTile: TypeAlias = str

FieldCommonGeoTilePrecision: TypeAlias = float

FieldCommonHealthStatus: TypeAlias = (
    Literal["green", "GREEN"] | Literal["yellow", "YELLOW"] | Literal["red", "RED"]
)

FieldCommonHost: TypeAlias = str

FieldCommonHumanReadableByteCount: TypeAlias = str

FieldCommonIBDistribution: TypeAlias = Literal["ll", "spl"]

FieldCommonIBLambda: TypeAlias = Literal["df", "ttf"]

FieldCommonId: TypeAlias = str

FieldCommonIds: TypeAlias = FieldCommonId | list[FieldCommonId]

FieldCommonIndexAlias: TypeAlias = str

FieldCommonIndexName: TypeAlias = str

FieldCommonIndices: TypeAlias = FieldCommonIndexName | list[FieldCommonIndexName]

FieldCommonIp: TypeAlias = str


class FieldCommonLatLonGeoLocation(TypedDict):
    lat: float
    lon: float


FieldCommonLevel: TypeAlias = Literal["cluster", "indices", "shards"]


class FieldCommonMetadata(TypedDict):
    pass


FieldCommonMinimumShouldMatch: TypeAlias = int | str

FieldCommonMultiTermQueryRewrite: TypeAlias = str

FieldCommonName: TypeAlias = str

FieldCommonNames: TypeAlias = FieldCommonName | list[FieldCommonName]

FieldCommonNodeId: TypeAlias = str

FieldCommonNodeIds: TypeAlias = FieldCommonNodeId | list[FieldCommonNodeId]

FieldCommonNodeName: TypeAlias = str

FieldCommonNodeRole: TypeAlias = Literal[
    "client",
    "coordinating_only",
    "data",
    "data_cold",
    "data_content",
    "data_frozen",
    "data_hot",
    "data_warm",
    "ingest",
    "ml",
    "remote_cluster_client",
    "transform",
    "voting_only",
    "master",
    "cluster_manager",
]

FieldCommonNodeRoles: TypeAlias = list[FieldCommonNodeRole]

FieldCommonOpType: TypeAlias = Literal["create", "index"]

FieldCommonPassword: TypeAlias = str

FieldCommonPercentageNumber: TypeAlias = float

FieldCommonPercentageString: TypeAlias = str


class FieldCommonPhaseTook(TypedDict):
    dfs_pre_query: int
    query: int
    fetch: int
    dfs_query: int
    expand: int
    can_match: int


FieldCommonPipelineName: TypeAlias = str


class FieldCommonQueryCacheStats(TypedDict):
    cache_count: int
    cache_size: int
    evictions: int
    hit_count: int
    memory_size: NotRequired[FieldCommonHumanReadableByteCount]
    memory_size_in_bytes: FieldCommonByteCount
    miss_count: int
    total_count: int


FieldCommonRefresh: TypeAlias = (
    bool | Literal["false"] | Literal["true"] | Literal["wait_for"]
)

FieldCommonRelationName: TypeAlias = str


class FieldCommonRemoteStoreTranslogUploadTotalUploadSizeStats(TypedDict):
    failed: NotRequired[FieldCommonHumanReadableByteCount]
    failed_bytes: FieldCommonByteCount
    started: NotRequired[FieldCommonHumanReadableByteCount]
    started_bytes: FieldCommonByteCount
    succeeded: NotRequired[FieldCommonHumanReadableByteCount]
    succeeded_bytes: FieldCommonByteCount


class FieldCommonRemoteStoreTranslogUploadTotalUploadsStats(TypedDict):
    failed: int
    started: int
    succeeded: int


class FieldCommonRemoteStoreUploadDownloadStats(TypedDict):
    failed: NotRequired[FieldCommonHumanReadableByteCount]
    failed_bytes: FieldCommonByteCount
    started: NotRequired[FieldCommonHumanReadableByteCount]
    started_bytes: FieldCommonByteCount
    succeeded: NotRequired[FieldCommonHumanReadableByteCount]
    succeeded_bytes: FieldCommonByteCount


class FieldCommonRemoteStoreUploadPressureStats(TypedDict):
    total_rejections: int


class FieldCommonRemoteStoreUploadRefreshSizeLagStats(TypedDict):
    max: NotRequired[FieldCommonHumanReadableByteCount]
    max_bytes: FieldCommonByteCount
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_bytes: FieldCommonByteCount


class FieldCommonRequestCacheStats(TypedDict):
    evictions: int
    hit_count: int
    memory_size: NotRequired[FieldCommonHumanReadableByteCount]
    memory_size_in_bytes: FieldCommonByteCount
    miss_count: int


FieldCommonResult: TypeAlias = Literal[
    "created", "deleted", "noop", "not_found", "updated"
]


class FieldCommonRetries(TypedDict):
    bulk: int
    search: int


FieldCommonRouting: TypeAlias = str


class FieldCommonScriptBase(TypedDict):
    params: NotRequired[dict[str, Any]]


FieldCommonScriptLanguage: TypeAlias = FieldCommonBuiltinScriptLanguage | str

FieldCommonScriptSortType: TypeAlias = Literal["number", "string", "version"]

FieldCommonScrollId: TypeAlias = str

FieldCommonScrollIds: TypeAlias = FieldCommonScrollId | list[FieldCommonScrollId]

FieldCommonSearchType: TypeAlias = Literal["dfs_query_then_fetch", "query_then_fetch"]


class FieldCommonSegmentReplicationStats1(TypedDict):
    max_bytes_behind: FieldCommonHumanReadableByteCount
    max_replication_lag: FieldCommonDuration
    total_bytes_behind: FieldCommonHumanReadableByteCount


FieldCommonSequenceNumber: TypeAlias = int

FieldCommonShort: TypeAlias = float


class FieldCommonSlicedScroll(TypedDict):
    field: NotRequired[FieldCommonField]
    id: int
    max: int


FieldCommonSlicesCalculation: TypeAlias = Literal["auto"]

FieldCommonSortMode: TypeAlias = Literal["avg", "max", "median", "min", "sum"]

FieldCommonSortOrder: TypeAlias = Literal["asc", "desc"]

FieldCommonSortResults: TypeAlias = list[FieldCommonFieldValue]


class FieldCommonStoredScript(TypedDict):
    lang: FieldCommonScriptLanguage
    options: NotRequired[dict[str, str]]
    source: str


class FieldCommonStoredScriptId(FieldCommonScriptBase):
    id: FieldCommonId


class FieldCommonStoreStats(TypedDict):
    size: NotRequired[FieldCommonHumanReadableByteCount]
    size_in_bytes: FieldCommonByteCount
    reserved: NotRequired[FieldCommonHumanReadableByteCount]
    reserved_in_bytes: FieldCommonByteCount


FieldCommonStringifiedBoolean: TypeAlias = bool | str

FieldCommonStringifiedDouble: TypeAlias = float | str

FieldCommonStringifiedInteger: TypeAlias = int | str

FieldCommonStringifiedLong: TypeAlias = int | str

FieldCommonStringOrStringArray: TypeAlias = str | list[str]

FieldCommonSuggestMode: TypeAlias = Literal["always", "missing", "popular"]

FieldCommonTaskId: TypeAlias = str

FieldCommonTDocument: TypeAlias = Any

FieldCommonTermFrequencyNormalization: TypeAlias = Literal["h1", "h2", "h3", "no", "z"]


class FieldCommonThreadInfo(TypedDict):
    thread_executions: float
    active_threads: float


FieldCommonTimeOfDay: TypeAlias = str

FieldCommonTimeUnit: TypeAlias = Literal["nanos", "micros", "ms", "s", "m", "h", "d"]

FieldCommonTimeZone: TypeAlias = str

FieldCommonTransportAddress: TypeAlias = str

FieldCommonTResult: TypeAlias = Any

FieldCommonType: TypeAlias = str

FieldCommonUint: TypeAlias = int

FieldCommonUlong: TypeAlias = float

FieldCommonUnitMicros: TypeAlias = int

FieldCommonUnitMillis: TypeAlias = int

FieldCommonUnitNanos: TypeAlias = int

FieldCommonUnitSeconds: TypeAlias = int

FieldCommonUsername: TypeAlias = str

FieldCommonUuid: TypeAlias = str

FieldCommonVersionNumber: TypeAlias = int

FieldCommonVersionString: TypeAlias = str

FieldCommonVersionType: TypeAlias = Literal["external", "external_gte", "internal"]


class FieldCommonVoid(TypedDict):
    pass


FieldCommonWaitForActiveShardOptions: TypeAlias = Literal["all"] | None

FieldCommonWaitForActiveShards: TypeAlias = (
    FieldCommonStringifiedInteger | FieldCommonWaitForActiveShardOptions
)

FieldCommonWaitForEvents: TypeAlias = Literal[
    "immediate", "urgent", "high", "normal", "low", "languid"
]


class FieldCommonWktGeoBounds(TypedDict):
    wkt: str


class FieldCommonXyCartesianCoordinates(TypedDict):
    x: float
    y: float


FieldCommonXyLocation: TypeAlias = FieldCommonXyCartesianCoordinates | list[float] | str


class MLExecuteAgentStreamRequestBody(TypedDict):
    parameters: FieldCommonParameters


class MLPredictModelStreamRequestBody(TypedDict):
    parameters: FieldCommonParameters


class FieldCommonBaseNode(TypedDict):
    attributes: NotRequired[dict[str, str]]
    host: NotRequired[FieldCommonHost]
    ip: NotRequired[FieldCommonIp]
    name: FieldCommonName
    roles: NotRequired[FieldCommonNodeRoles]
    transport_address: NotRequired[FieldCommonTransportAddress]


FieldCommonDurationValueUnitMicros: TypeAlias = FieldCommonUnitMicros

FieldCommonDurationValueUnitMillis: TypeAlias = FieldCommonUnitMillis

FieldCommonDurationValueUnitNanos: TypeAlias = FieldCommonUnitNanos

FieldCommonEpochTimeUnitMillis: TypeAlias = FieldCommonUnitMillis

FieldCommonEpochTimeUnitSeconds: TypeAlias = FieldCommonUnitSeconds


class FieldCommonErrorCause(TypedDict):
    type: str
    reason: NotRequired[str]
    stack_trace: NotRequired[str]
    caused_by: NotRequired[FieldCommonErrorCause]
    root_cause: NotRequired[list[FieldCommonErrorCause]]
    suppressed: NotRequired[list[FieldCommonErrorCause]]
    header: NotRequired[dict[str, FieldCommonStringOrStringArray]]


class FieldCommonErrorResponseBase(TypedDict):
    error: FieldCommonErrorCause
    status: int


class FieldCommonFieldMemoryUsage(TypedDict):
    memory_size: NotRequired[FieldCommonHumanReadableByteCount]
    memory_size_in_bytes: FieldCommonByteCount


class FieldCommonFieldSizeUsage(TypedDict):
    size: NotRequired[FieldCommonHumanReadableByteCount]
    size_in_bytes: FieldCommonByteCount


FieldCommonFieldWithDirection: TypeAlias = dict[str, FieldCommonSortOrder]


class FieldCommonFlushStats(TypedDict):
    periodic: int
    total: int
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis


FieldCommonGeoLocation: TypeAlias = (
    FieldCommonLatLonGeoLocation | FieldCommonGeoHashLocation | list[float] | str
)


class FieldCommonGetStats(TypedDict):
    total: int
    getTime: NotRequired[FieldCommonDuration]
    time: NotRequired[FieldCommonDuration]
    time_in_millis: FieldCommonDurationValueUnitMillis
    exists_total: int
    exists_time: NotRequired[FieldCommonDuration]
    exists_time_in_millis: FieldCommonDurationValueUnitMillis
    missing_total: int
    missing_time: NotRequired[FieldCommonDuration]
    missing_time_in_millis: FieldCommonDurationValueUnitMillis
    current: int


FieldCommonHttpHeaders: TypeAlias = dict[str, FieldCommonStringOrStringArray]


class FieldCommonIndexingStats(TypedDict):
    index_total: int
    index_time: NotRequired[FieldCommonDuration]
    index_time_in_millis: FieldCommonDurationValueUnitMillis
    index_current: int
    index_failed: int
    delete_total: int
    delete_time: NotRequired[FieldCommonDuration]
    delete_time_in_millis: FieldCommonDurationValueUnitMillis
    delete_current: int
    noop_update_total: int
    is_throttled: bool
    throttle_time: NotRequired[FieldCommonDuration]
    throttle_time_in_millis: FieldCommonDurationValueUnitMillis
    doc_status: NotRequired[FieldCommonDocStatus]
    types: NotRequired[dict[str, FieldCommonIndexingStats]]


class FieldCommonInlineGet(TypedDict):
    fields: NotRequired[dict[str, Any]]
    found: bool
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_primary_term: NotRequired[int]
    field_routing: NotRequired[FieldCommonRouting]
    field_source: NotRequired[FieldCommonTDocument]


class FieldCommonInlineGetDictUserDefined(TypedDict):
    fields: NotRequired[dict[str, dict[str, Any]]]
    found: bool
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_primary_term: NotRequired[int]
    field_routing: NotRequired[FieldCommonRouting]
    field_source: NotRequired[dict[str, Any]]


class FieldCommonInlineScript1(FieldCommonScriptBase):
    lang: NotRequired[FieldCommonScriptLanguage]
    options: NotRequired[dict[str, str]]
    source: str


FieldCommonInlineScript: TypeAlias = str | FieldCommonInlineScript1


class FieldCommonMergesStats(TypedDict):
    current: int
    current_docs: int
    current_size: NotRequired[FieldCommonHumanReadableByteCount]
    current_size_in_bytes: FieldCommonByteCount
    total: int
    total_auto_throttle: NotRequired[FieldCommonHumanReadableByteCount]
    total_auto_throttle_in_bytes: FieldCommonByteCount
    total_docs: int
    total_size: NotRequired[FieldCommonHumanReadableByteCount]
    total_size_in_bytes: FieldCommonByteCount
    total_stopped_time: NotRequired[FieldCommonDuration]
    total_stopped_time_in_millis: FieldCommonDurationValueUnitMillis
    total_throttled_time: NotRequired[FieldCommonDuration]
    total_throttled_time_in_millis: FieldCommonDurationValueUnitMillis
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis
    unreferenced_file_cleanups_performed: NotRequired[int]


class FieldCommonNodeAttributes(TypedDict):
    attributes: dict[str, str]
    ephemeral_id: FieldCommonId
    id: NotRequired[FieldCommonNodeId]
    name: FieldCommonNodeName
    transport_address: FieldCommonTransportAddress
    roles: NotRequired[FieldCommonNodeRoles]
    external_id: NotRequired[str]


class FieldCommonNodeStatistics(TypedDict):
    failures: NotRequired[list[FieldCommonErrorCause]]
    total: int
    successful: int
    failed: int


class FieldCommonPluginStats(TypedDict):
    classname: str
    description: str
    extended_plugins: list[str]
    has_native_controller: bool
    java_version: FieldCommonVersionString
    name: FieldCommonName
    version: FieldCommonVersionString
    licensed: NotRequired[bool]
    custom_foldername: NotRequired[str | None]
    opensearch_version: FieldCommonVersionString
    optional_extended_plugins: NotRequired[list[str]]


class FieldCommonRecoveryStats(TypedDict):
    current_as_source: int
    current_as_target: int
    throttle_time: NotRequired[FieldCommonDuration]
    throttle_time_in_millis: FieldCommonDurationValueUnitMillis


class FieldCommonRefreshStats(TypedDict):
    external_total: int
    external_total_time: NotRequired[FieldCommonDuration]
    external_total_time_in_millis: FieldCommonDurationValueUnitMillis
    listeners: int
    total: int
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis


class FieldCommonRemoteStoreDownloadStats(TypedDict):
    total_download_size: FieldCommonRemoteStoreUploadDownloadStats
    total_time_spent: NotRequired[FieldCommonDuration]
    total_time_spent_in_millis: FieldCommonDurationValueUnitMillis


class FieldCommonRemoteStoreTranslogUploadStats(TypedDict):
    total_uploads: FieldCommonRemoteStoreTranslogUploadTotalUploadsStats
    total_upload_size: FieldCommonRemoteStoreTranslogUploadTotalUploadSizeStats


class FieldCommonRemoteStoreUploadStats(TypedDict):
    max_refresh_time_lag: NotRequired[FieldCommonDuration]
    max_refresh_time_lag_in_millis: FieldCommonDurationValueUnitMillis
    pressure: NotRequired[FieldCommonRemoteStoreUploadPressureStats]
    refresh_size_lag: FieldCommonRemoteStoreUploadRefreshSizeLagStats
    total_time_spent: NotRequired[FieldCommonDuration]
    total_time_spent_in_millis: FieldCommonDurationValueUnitMillis
    total_upload_size: FieldCommonRemoteStoreUploadDownloadStats


class FieldCommonRequestStats(TypedDict):
    time: NotRequired[FieldCommonDuration]
    time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    current: NotRequired[int]
    total: NotRequired[int]


class FieldCommonResourceStat(TypedDict):
    cpu_time_in_nanos: FieldCommonDurationValueUnitNanos
    memory_in_bytes: FieldCommonByteCount


class FieldCommonResourceStats(TypedDict):
    average: FieldCommonResourceStat
    total: FieldCommonResourceStat
    min: FieldCommonResourceStat
    max: FieldCommonResourceStat
    thread_info: FieldCommonThreadInfo


FieldCommonRoutingInQueryString: TypeAlias = FieldCommonStringOrStringArray


class FieldCommonScoreSort(TypedDict):
    order: NotRequired[FieldCommonSortOrder]


FieldCommonScript: TypeAlias = FieldCommonInlineScript | FieldCommonStoredScriptId


class FieldCommonScriptField(TypedDict):
    script: FieldCommonScript
    ignore_failure: NotRequired[bool]


class FieldCommonScrollableHitSourceSearchFailure(TypedDict):
    index: NotRequired[FieldCommonIndexName]
    shard: NotRequired[int]
    node: NotRequired[str]
    status: int
    reason: FieldCommonErrorCause


class FieldCommonSearchStats(TypedDict):
    open_contexts: NotRequired[int]
    query_current: int
    query_time: NotRequired[FieldCommonDuration]
    query_time_in_millis: FieldCommonDurationValueUnitMillis
    query_total: int
    concurrent_query_total: NotRequired[int]
    concurrent_query_time: NotRequired[FieldCommonDuration]
    concurrent_query_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    concurrent_query_current: NotRequired[int]
    concurrent_avg_slice_count: NotRequired[float]
    fetch_current: int
    fetch_time: NotRequired[FieldCommonDuration]
    fetch_time_in_millis: FieldCommonDurationValueUnitMillis
    fetch_total: int
    scroll_current: int
    scroll_time: NotRequired[FieldCommonDuration]
    scroll_time_in_millis: FieldCommonDurationValueUnitMillis
    scroll_total: int
    point_in_time_total: NotRequired[int]
    point_in_time_time: NotRequired[FieldCommonDuration]
    point_in_time_time_in_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    point_in_time_current: NotRequired[int]
    suggest_current: int
    suggest_time: NotRequired[FieldCommonDuration]
    suggest_time_in_millis: FieldCommonDurationValueUnitMillis
    suggest_total: int
    search_idle_reactivate_count_total: NotRequired[int]
    request: NotRequired[dict[str, FieldCommonRequestStats]]
    groups: NotRequired[dict[str, FieldCommonSearchStats]]


class FieldCommonSegmentReplicationStats2(TypedDict):
    max_bytes_behind: FieldCommonByteCount
    max_replication_lag: FieldCommonDurationValueUnitMillis
    total_bytes_behind: FieldCommonByteCount


FieldCommonSegmentReplicationStats: TypeAlias = (
    FieldCommonSegmentReplicationStats1 | FieldCommonSegmentReplicationStats2
)


class FieldCommonShardFailure(TypedDict):
    index: NotRequired[FieldCommonIndexName]
    node: NotRequired[str]
    reason: FieldCommonErrorCause
    shard: int
    status: NotRequired[str]
    primary: bool


class FieldCommonShardInfo(TypedDict):
    failed: FieldCommonUint
    successful: FieldCommonUint
    total: FieldCommonUint
    failures: NotRequired[list[FieldCommonShardFailure]]


class FieldCommonShardSearchFailure(TypedDict):
    shard: int
    index: NotRequired[str]
    node: NotRequired[str]
    reason: FieldCommonErrorCause


class FieldCommonShardStatistics(TypedDict):
    failed: FieldCommonUint
    successful: FieldCommonUint
    total: FieldCommonUint
    failures: NotRequired[list[FieldCommonShardSearchFailure]]
    skipped: NotRequired[FieldCommonUint]


FieldCommonSlices: TypeAlias = int | FieldCommonSlicesCalculation

FieldCommonStringifiedEpochTimeUnitMillis: TypeAlias = (
    FieldCommonEpochTimeUnitMillis | str
)

FieldCommonStringifiedEpochTimeUnitSeconds: TypeAlias = (
    FieldCommonEpochTimeUnitSeconds | str
)

FieldCommonStringifiedVersionNumber: TypeAlias = FieldCommonVersionNumber | str


class FieldCommonTaskFailure(TypedDict):
    task_id: int
    node_id: FieldCommonNodeId
    status: str
    reason: FieldCommonErrorCause


class FieldCommonTopLeftBottomRightGeoBounds(TypedDict):
    top_left: FieldCommonGeoLocation
    bottom_right: FieldCommonGeoLocation


class FieldCommonTopRightBottomLeftGeoBounds(TypedDict):
    top_right: FieldCommonGeoLocation
    bottom_left: FieldCommonGeoLocation


class FieldCommonWarmerStats(TypedDict):
    current: int
    total: int
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis


class FieldCommonWriteResponseBase(TypedDict):
    field_type: NotRequired[FieldCommonType]
    field_id: FieldCommonId
    field_index: FieldCommonIndexName
    field_primary_term: int
    result: FieldCommonResult
    field_seq_no: FieldCommonSequenceNumber
    field_shards: FieldCommonShardStatistics
    field_version: FieldCommonVersionNumber
    forced_refresh: NotRequired[bool]


class FieldCommonBulkItemResponseFailure(TypedDict):
    cause: FieldCommonErrorCause
    id: NotRequired[FieldCommonId]
    index: FieldCommonIndexName
    status: int


class FieldCommonCompletionStats(TypedDict):
    size_in_bytes: FieldCommonByteCount
    size: NotRequired[FieldCommonHumanReadableByteCount]
    fields: NotRequired[dict[str, FieldCommonFieldSizeUsage]]


FieldCommonDateTime: TypeAlias = str | FieldCommonEpochTimeUnitMillis


class FieldCommonDerivedField(TypedDict):
    name: str
    type: str
    script: FieldCommonScript
    prefilter_field: NotRequired[str]
    properties: NotRequired[dict[str, Any]]
    ignore_malformed: NotRequired[bool]
    format: NotRequired[str]


class FieldCommonFielddataStats(TypedDict):
    evictions: NotRequired[int]
    memory_size: NotRequired[FieldCommonHumanReadableByteCount]
    memory_size_in_bytes: FieldCommonByteCount
    fields: NotRequired[dict[str, FieldCommonFieldMemoryUsage]]


FieldCommonGeoBounds: TypeAlias = (
    FieldCommonCoordsGeoBounds
    | FieldCommonTopLeftBottomRightGeoBounds
    | FieldCommonTopRightBottomLeftGeoBounds
    | FieldCommonWktGeoBounds
)


class FieldCommonIndicesResponseBase(FieldCommonAcknowledgedResponseBase):
    field_shards: NotRequired[FieldCommonShardStatistics]


class FieldCommonOpenSearchVersionInfo(TypedDict):
    build_date: FieldCommonDateTime
    build_flavor: NotRequired[str]
    build_hash: str
    build_snapshot: bool
    build_type: str
    distribution: str
    lucene_version: FieldCommonVersionString
    minimum_index_compatibility_version: FieldCommonVersionString
    minimum_wire_compatibility_version: FieldCommonVersionString
    number: str


class FieldCommonRemoteStoreStats(TypedDict):
    upload: FieldCommonRemoteStoreUploadStats
    download: FieldCommonRemoteStoreDownloadStats


class FieldCommonRemoteStoreTranslogStats(TypedDict):
    upload: FieldCommonRemoteStoreTranslogUploadStats


class FieldCommonSegmentsStats(TypedDict):
    count: int
    doc_values_memory: NotRequired[FieldCommonHumanReadableByteCount]
    doc_values_memory_in_bytes: FieldCommonByteCount
    file_sizes: dict[str, StatsShardFileSizeInfo]
    fixed_bit_set: NotRequired[FieldCommonHumanReadableByteCount]
    fixed_bit_set_memory_in_bytes: FieldCommonByteCount
    index_writer_memory: NotRequired[FieldCommonHumanReadableByteCount]
    index_writer_max_memory_in_bytes: NotRequired[FieldCommonByteCount]
    index_writer_memory_in_bytes: FieldCommonByteCount
    max_unsafe_auto_id_timestamp: FieldCommonEpochTimeUnitMillis
    memory: NotRequired[FieldCommonHumanReadableByteCount]
    memory_in_bytes: FieldCommonByteCount
    norms_memory: NotRequired[FieldCommonHumanReadableByteCount]
    norms_memory_in_bytes: FieldCommonByteCount
    points_memory: NotRequired[FieldCommonHumanReadableByteCount]
    points_memory_in_bytes: FieldCommonByteCount
    stored_fields_memory: NotRequired[FieldCommonHumanReadableByteCount]
    stored_fields_memory_in_bytes: FieldCommonByteCount
    terms_memory: NotRequired[FieldCommonHumanReadableByteCount]
    terms_memory_in_bytes: FieldCommonByteCount
    term_vectors_memory: NotRequired[FieldCommonHumanReadableByteCount]
    term_vectors_memory_in_bytes: FieldCommonByteCount
    version_map_memory: NotRequired[FieldCommonHumanReadableByteCount]
    version_map_memory_in_bytes: FieldCommonByteCount
    remote_store: NotRequired[FieldCommonRemoteStoreStats]
    segment_replication: NotRequired[FieldCommonSegmentReplicationStats]


class FieldCommonShardsOperationResponseBase(TypedDict):
    field_shards: FieldCommonShardStatistics


class FieldCommonTranslogStats(TypedDict):
    earliest_last_modified_age: int
    operations: int
    remote_store: NotRequired[FieldCommonRemoteStoreTranslogStats]
    size: NotRequired[FieldCommonHumanReadableByteCount]
    size_in_bytes: FieldCommonByteCount
    uncommitted_operations: int
    uncommitted_size: NotRequired[FieldCommonHumanReadableByteCount]
    uncommitted_size_in_bytes: FieldCommonByteCount


FieldCommonBulkByScrollFailure: TypeAlias = (
    FieldCommonBulkItemResponseFailure | FieldCommonScrollableHitSourceSearchFailure
)


class FieldCommonNodeShard(TypedDict):
    state: StatsShardRoutingState
    primary: bool
    node: NotRequired[FieldCommonNodeName]
    shard: int
    index: FieldCommonIndexName
    searchOnly: NotRequired[bool]
    allocation_id: NotRequired[dict[str, FieldCommonId]]
    recovery_source: NotRequired[dict[str, FieldCommonId]]
    unassigned_info: NotRequired[AllocationExplainUnassignedInformation]
    relocating_node: NotRequired[FieldCommonNodeId | None]


class FieldCommonBulkByScrollTaskStatus(TypedDict):
    slice_id: NotRequired[int]
    total: int
    updated: NotRequired[int]
    created: NotRequired[int]
    deleted: int
    batches: int
    version_conflicts: int
    noops: int
    retries: FieldCommonRetries
    throttled_millis: FieldCommonDurationValueUnitMillis
    throttled: NotRequired[FieldCommonDuration]
    requests_per_second: float
    canceled: NotRequired[str]
    throttled_until_millis: FieldCommonDurationValueUnitMillis
    throttled_until: NotRequired[FieldCommonDuration]
    slices: NotRequired[list[FieldCommonBulkByScrollTaskStatusOrException]]


FieldCommonBulkByScrollTaskStatusOrException: TypeAlias = (
    FieldCommonBulkByScrollTaskStatus | FieldCommonErrorCause
)


class FieldCommonFieldSort(TypedDict):
    missing: NotRequired[FieldCommonFieldValue]
    mode: NotRequired[FieldCommonSortMode]
    nested: NotRequired[FieldCommonNestedSortValue]
    order: NotRequired[FieldCommonSortOrder]
    unmapped_type: NotRequired[MappingFieldType]
    numeric_type: NotRequired[FieldCommonFieldSortNumericType]


FieldCommonFieldWithOrder: TypeAlias = dict[str, FieldCommonFieldSort]


class FieldCommonGeoDistanceSort(TypedDict):
    mode: NotRequired[FieldCommonSortMode]
    distance_type: NotRequired[FieldCommonGeoDistanceType]
    ignore_unmapped: NotRequired[bool]
    nested: NotRequired[FieldCommonNestedSortValue]
    order: NotRequired[FieldCommonSortOrder]
    unit: NotRequired[FieldCommonDistanceUnit]
    validation_method: NotRequired[QueryDslGeoValidationMethod]


class FieldCommonNestedSortValue(TypedDict):
    filter: NotRequired[QueryDslQueryContainer]
    max_children: NotRequired[int]
    nested: NotRequired[FieldCommonNestedSortValue]
    path: FieldCommonField


class FieldCommonScriptSort(TypedDict):
    order: NotRequired[FieldCommonSortOrder]
    script: FieldCommonScript
    type: NotRequired[FieldCommonScriptSortType]
    mode: NotRequired[FieldCommonSortMode]
    nested: NotRequired[FieldCommonNestedSortValue]


FieldCommonSort: TypeAlias = Union[
    "FieldCommonSortCombinations", list["FieldCommonSortCombinations"]
]

FieldCommonSortCombinations: TypeAlias = Union[
    FieldCommonField,
    FieldCommonFieldWithDirection,
    FieldCommonFieldWithOrder,
    "FieldCommonSortOptions",
]


class FieldCommonSortOptions(TypedDict):
    field_score: NotRequired[FieldCommonScoreSort]
    field_geo_distance: NotRequired[FieldCommonGeoDistanceSort]
    field_script: NotRequired[FieldCommonScriptSort]


class QueryDslFieldAndFormat(TypedDict):
    field: FieldCommonField
    format: NotRequired[str]


QueryDslFieldAndFormatModel: TypeAlias = FieldCommonField | QueryDslFieldAndFormat


class AggregationsAggregation(TypedDict):
    meta: NotRequired[FieldCommonMetadata]


class AggregationsAggregationContainer(AggregationsAggregation):
    pass


class AggregationsAggregationContainerModel(TypedDict):
    matrix_stats: AggregationsMatrixStatsAggregation


class AggregationsAggregationContainerModel2(
    AggregationsAggregationContainerModel, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel3(TypedDict):
    scripted_metric: AggregationsScriptedMetricAggregation


class AggregationsAggregationContainerModel7(
    AggregationsAggregationContainerModel3, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel8(TypedDict):
    avg_bucket: AggregationsAverageBucketAggregation


class AggregationsAggregationContainerModel35(
    AggregationsAggregationContainerModel8, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel36(TypedDict):
    avg: AggregationsAverageAggregation


class AggregationsAggregationContainerModel39(
    AggregationsAggregationContainerModel36, AggregationsAggregationContainer
):
    pass


AggregationsAggregationContainerModel43: TypeAlias = Union[
    "AggregationsAggregationContainerModel45",
    "AggregationsAggregationContainerModel46",
    AggregationsAggregationContainerModel39,
    AggregationsAggregationContainerModel35,
    "AggregationsAggregationContainerModel44",
    "AggregationsAggregationContainerModel47",
    "AggregationsAggregationContainerModel48",
    "AggregationsAggregationContainerModel49",
    "AggregationsAggregationContainerModel50",
    "AggregationsAggregationContainerModel51",
    "AggregationsAggregationContainerModel52",
    "AggregationsAggregationContainerModel53",
    "AggregationsAggregationContainerModel54",
    "AggregationsAggregationContainerModel55",
    "AggregationsAggregationContainerModel56",
    "AggregationsAggregationContainerModel57",
    "AggregationsAggregationContainerModel58",
    "AggregationsAggregationContainerModel59",
    AggregationsAggregationContainerModel2,
    "AggregationsAggregationContainerModel60",
    "AggregationsAggregationContainerModel61",
    "AggregationsAggregationContainerModel62",
    "AggregationsAggregationContainerModel63",
    "AggregationsAggregationContainerModel64",
    "AggregationsAggregationContainerModel65",
    "AggregationsAggregationContainerModel66",
    "AggregationsAggregationContainerModel67",
    AggregationsAggregationContainerModel7,
    "AggregationsAggregationContainerModel68",
    "AggregationsAggregationContainerModel69",
    "AggregationsAggregationContainerModel70",
]


class QueryDslQueryContainer(TypedDict):
    agentic: NotRequired[QueryDslAgenticQuery]
    bool: NotRequired[QueryDslBoolQuery]
    boosting: NotRequired[QueryDslBoostingQuery]
    common: NotRequired[dict[FieldCommonField, QueryDslCommonTermsQueryModel]]
    combined_fields: NotRequired[QueryDslCombinedFieldsQuery]
    constant_score: NotRequired[QueryDslConstantScoreQuery]
    dis_max: NotRequired[QueryDslDisMaxQuery]
    distance_feature: NotRequired[QueryDslDistanceFeatureQueryModel1]
    exists: NotRequired[QueryDslExistsQuery]
    function_score: NotRequired[QueryDslFunctionScoreQuery]
    fuzzy: NotRequired[dict[FieldCommonField, QueryDslFuzzyQueryModel]]
    geo_bounding_box: NotRequired[QueryDslGeoBoundingBoxQuery]
    geo_distance: NotRequired[QueryDslGeoDistanceQuery]
    geo_polygon: NotRequired[QueryDslGeoPolygonQuery]
    geo_shape: NotRequired[QueryDslGeoShapeQuery]
    has_child: NotRequired[QueryDslHasChildQuery]
    has_parent: NotRequired[QueryDslHasParentQuery]
    hybrid: NotRequired[QueryDslHybridQuery]
    ids: NotRequired[QueryDslIdsQuery]
    intervals: NotRequired[dict[FieldCommonField, QueryDslIntervalsQuery]]
    knn: NotRequired[dict[FieldCommonField, QueryDslKnnQuery]]
    match: NotRequired[dict[FieldCommonField, QueryDslMatchQueryModel]]
    match_all: NotRequired[QueryDslMatchAllQuery]
    match_bool_prefix: NotRequired[
        dict[FieldCommonField, QueryDslMatchBoolPrefixQueryModel]
    ]
    match_none: NotRequired[QueryDslMatchNoneQuery]
    match_phrase: NotRequired[dict[FieldCommonField, QueryDslMatchPhraseQueryModel]]
    match_phrase_prefix: NotRequired[
        dict[FieldCommonField, QueryDslMatchPhrasePrefixQueryModel]
    ]
    more_like_this: NotRequired[QueryDslMoreLikeThisQuery]
    multi_match: NotRequired[QueryDslMultiMatchQuery]
    nested: NotRequired[QueryDslNestedQuery]
    neural: NotRequired[dict[FieldCommonField, QueryDslNeuralQuery]]
    parent_id: NotRequired[QueryDslParentIdQuery]
    percolate: NotRequired[QueryDslPercolateQuery]
    prefix: NotRequired[dict[FieldCommonField, QueryDslPrefixQueryModel]]
    query_string: NotRequired[QueryDslQueryStringQuery]
    range: NotRequired[dict[FieldCommonField, QueryDslRangeQuery]]
    rank_feature: NotRequired[QueryDslRankFeatureQuery]
    regexp: NotRequired[dict[FieldCommonField, QueryDslRegexpQueryModel]]
    script: NotRequired[QueryDslScriptQuery]
    script_score: NotRequired[QueryDslScriptScoreQuery]
    simple_query_string: NotRequired[QueryDslSimpleQueryStringQuery]
    span_containing: NotRequired[QueryDslSpanContainingQuery]
    field_masking_span: NotRequired[QueryDslSpanFieldMaskingQuery]
    span_first: NotRequired[QueryDslSpanFirstQuery]
    span_multi: NotRequired[QueryDslSpanMultiTermQuery]
    span_near: NotRequired[QueryDslSpanNearQuery]
    span_not: NotRequired[QueryDslSpanNotQuery]
    span_or: NotRequired[QueryDslSpanOrQuery]
    span_term: NotRequired[dict[FieldCommonField, QueryDslSpanTermQueryModel]]
    span_within: NotRequired[QueryDslSpanWithinQuery]
    template: NotRequired[dict[str, Any]]
    term: NotRequired[dict[FieldCommonField, QueryDslTermQueryModel]]
    terms: NotRequired[QueryDslTermsQuery]
    terms_set: NotRequired[dict[FieldCommonField, QueryDslTermsSetQuery]]
    type: NotRequired[QueryDslTypeQuery]
    wildcard: NotRequired[dict[FieldCommonField, QueryDslWildcardQueryModel]]
    wrapper: NotRequired[QueryDslWrapperQuery]
    xy_shape: NotRequired[QueryDslXyShapeQuery]


class SearchPointInTimeReference(TypedDict):
    id: FieldCommonId
    keep_alive: NotRequired[FieldCommonDuration]


class SearchSuggester(TypedDict):
    text: NotRequired[str]


SearchTrackHits: TypeAlias = bool | int


class SearchSourceFilter(TypedDict):
    excludes: NotRequired[FieldCommonFields]
    includes: NotRequired[FieldCommonFields]


SearchSourceFilterModel: TypeAlias = FieldCommonFields | SearchSourceFilter

SearchSourceConfig: TypeAlias = bool | SearchSourceFilterModel


class SearchFieldCollapse(TypedDict):
    field: FieldCommonField
    inner_hits: NotRequired[SearchInnerHits | list[SearchInnerHits]]
    max_concurrent_group_searches: NotRequired[int]


class SearchRescore(TypedDict):
    query: SearchRescoreQuery
    window_size: NotRequired[int]


class SearchHighlightBase(TypedDict):
    type: NotRequired[SearchHighlighterType]
    boundary_chars: NotRequired[str]
    boundary_max_scan: NotRequired[int]
    boundary_scanner: NotRequired[SearchBoundaryScanner]
    boundary_scanner_locale: NotRequired[str]
    force_source: NotRequired[bool]
    fragmenter: NotRequired[SearchHighlighterFragmenter]
    fragment_offset: NotRequired[int]
    fragment_size: NotRequired[int]
    highlight_filter: NotRequired[bool]
    highlight_query: NotRequired[QueryDslQueryContainer]
    max_fragment_length: NotRequired[int]
    max_analyzer_offset: NotRequired[int]
    no_match_size: NotRequired[int]
    number_of_fragments: NotRequired[int]
    options: NotRequired[dict[str, dict[str, Any]]]
    order: NotRequired[SearchHighlighterOrder]
    phrase_limit: NotRequired[int]
    post_tags: NotRequired[list[str]]
    pre_tags: NotRequired[list[str]]
    require_field_match: NotRequired[bool]
    tags_schema: NotRequired[SearchHighlighterTagsSchema]


class SearchHighlight(SearchHighlightBase):
    encoder: NotRequired[SearchHighlighterEncoder]
    fields: SearchHighlightFields


SearchRequestBody = TypedDict(
    "SearchRequestBody",
    {
        "aggregations": NotRequired[dict[str, AggregationsAggregationContainerModel43]],
        "aggs": NotRequired[dict[str, AggregationsAggregationContainerModel43]],
        "collapse": NotRequired[SearchFieldCollapse],
        "explain": NotRequired[bool],
        "ext": NotRequired[dict[str, Any]],
        "from": NotRequired[int],
        "highlight": NotRequired[SearchHighlight],
        "track_total_hits": NotRequired[SearchTrackHits],
        "indices_boost": NotRequired[list[dict[str, float]]],
        "docvalue_fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "min_score": NotRequired[float],
        "post_filter": NotRequired[QueryDslQueryContainer],
        "profile": NotRequired[bool],
        "search_pipeline": NotRequired[str],
        "verbose_pipeline": NotRequired[bool],
        "query": NotRequired[QueryDslQueryContainer],
        "rescore": NotRequired[SearchRescore | list[SearchRescore]],
        "script_fields": NotRequired[dict[str, FieldCommonScriptField]],
        "search_after": NotRequired[FieldCommonSortResults],
        "size": NotRequired[int],
        "slice": NotRequired[FieldCommonSlicedScroll],
        "sort": NotRequired[FieldCommonSort],
        "_source": NotRequired[SearchSourceConfig],
        "fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "suggest": NotRequired[SearchSuggester],
        "terminate_after": NotRequired[int],
        "timeout": NotRequired[str],
        "track_scores": NotRequired[bool],
        "include_named_queries_score": NotRequired[bool],
        "version": NotRequired[bool],
        "seq_no_primary_term": NotRequired[bool],
        "stored_fields": NotRequired[FieldCommonFields],
        "pit": NotRequired[SearchPointInTimeReference],
        "stats": NotRequired[list[str]],
        "derived": NotRequired[dict[str, FieldCommonDerivedField]],
    },
)


class FieldCommonBulkByScrollResponseBase(FieldCommonBulkByScrollTaskStatus):
    took: int
    timed_out: bool
    failures: list[FieldCommonBulkByScrollFailure]


FieldCommonWaitForNodes: TypeAlias = int | str

AllocationExplainAllocationExplainDecision: TypeAlias = Literal[
    "ALWAYS", "NO", "THROTTLE", "YES"
]


class AllocationExplainAllocationStore(TypedDict):
    allocation_id: str
    found: bool
    in_sync: bool
    matching_size_in_bytes: FieldCommonByteCount
    matching_sync_id: bool
    store_exception: str


class AllocationExplainCurrentNode(TypedDict):
    id: FieldCommonId
    name: FieldCommonName
    attributes: dict[str, str]
    transport_address: FieldCommonTransportAddress
    weight_ranking: int


AllocationExplainDecision: TypeAlias = Literal[
    "allocation_delayed",
    "awaiting_info",
    "no",
    "no_attempt",
    "no_valid_shard_copy",
    "throttled",
    "worse_balance",
    "yes",
]


class AllocationExplainDiskUsage(TypedDict):
    path: str
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_bytes: FieldCommonByteCount
    used: NotRequired[FieldCommonHumanReadableByteCount]
    used_bytes: FieldCommonByteCount
    free: NotRequired[FieldCommonHumanReadableByteCount]
    free_bytes: FieldCommonByteCount
    free_disk_percent: FieldCommonPercentageNumber
    used_disk_percent: FieldCommonPercentageNumber


class AllocationExplainNodeDiskUsage(TypedDict):
    node_name: FieldCommonName
    least_available: AllocationExplainDiskUsage
    most_available: AllocationExplainDiskUsage


class AllocationExplainReservedSize(TypedDict):
    node_id: FieldCommonId
    path: str
    total: int
    shards: list[str]


AllocationExplainUnassignedInformationReason: TypeAlias = Literal[
    "ALLOCATION_FAILED",
    "CLUSTER_RECOVERED",
    "DANGLING_INDEX_IMPORTED",
    "EXISTING_INDEX_RESTORED",
    "FORCED_EMPTY_PRIMARY",
    "INDEX_CREATED",
    "INDEX_REOPENED",
    "MANUAL_ALLOCATION",
    "NEW_INDEX_RESTORED",
    "NODE_LEFT",
    "PRIMARY_FAILED",
    "REALLOCATED_REPLICA",
    "REINITIALIZED",
    "REPLICA_ADDED",
    "REROUTE_CANCELLED",
]

DecommissionAwarenessDecommissionStatus: TypeAlias = Literal[
    "INIT", "DRAINING", "IN_PROGRESS", "SUCCESSFUL", "FAILED"
]


class HealthAwarenessAttributeStats(TypedDict):
    active_shards: NotRequired[int]
    initializing_shards: NotRequired[int]
    relocating_shards: NotRequired[int]
    unassigned_shards: NotRequired[int]
    data_nodes: NotRequired[int]
    weight: NotRequired[int]


HealthLevel: TypeAlias = Literal["awareness_attributes", "cluster", "indices", "shards"]


class HealthShardHealthStats(TypedDict):
    active_shards: int
    initializing_shards: int
    primary_active: bool
    relocating_shards: int
    status: FieldCommonHealthStatus
    unassigned_shards: int


class RemoteInfoClusterRemoteProxyInfo(TypedDict):
    mode: Literal["proxy"]
    connected: bool
    initial_connect_timeout: FieldCommonDuration
    skip_unavailable: bool
    proxy_address: str
    server_name: str
    num_proxy_sockets_connected: int
    max_proxy_socket_connections: int


class RemoteInfoClusterRemoteSniffInfo(TypedDict):
    mode: Literal["sniff"]
    connected: bool
    max_connections_per_cluster: int
    num_nodes_connected: int
    initial_connect_timeout: FieldCommonDuration
    skip_unavailable: bool
    seeds: list[str]


class RerouteCommandAllocatePrimaryAction(TypedDict):
    index: FieldCommonIndexName
    shard: int
    node: str
    accept_data_loss: bool


class RerouteCommandAllocateReplicaAction(TypedDict):
    index: FieldCommonIndexName
    shard: int
    node: str


class RerouteCommandCancelAction(TypedDict):
    index: FieldCommonIndexName
    shard: int
    node: str
    allow_primary: NotRequired[bool]


class RerouteCommandMoveAction(TypedDict):
    index: FieldCommonIndexName
    shard: int
    from_node: str
    to_node: str


RerouteMetric: TypeAlias = Literal[
    "_all",
    "blocks",
    "cluster_manager_node",
    "master_node",
    "metadata",
    "nodes",
    "routing_nodes",
    "routing_table",
    "version",
]


class RerouteRerouteDecision(TypedDict):
    decider: str
    decision: str
    explanation: str


class RerouteRerouteParameters(TypedDict):
    allow_primary: bool
    index: FieldCommonIndexName
    node: FieldCommonNodeName
    shard: int
    from_node: NotRequired[FieldCommonNodeName]
    to_node: NotRequired[FieldCommonNodeName]


StateMetric: TypeAlias = Literal[
    "_all",
    "blocks",
    "cluster_manager_node",
    "master_node",
    "metadata",
    "nodes",
    "routing_nodes",
    "routing_table",
    "version",
]


class StatsClusterFileSystem(TypedDict):
    available: NotRequired[FieldCommonHumanReadableByteCount]
    available_in_bytes: FieldCommonByteCount
    free: NotRequired[FieldCommonHumanReadableByteCount]
    free_in_bytes: FieldCommonByteCount
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_in_bytes: FieldCommonByteCount
    cache_reserved: NotRequired[FieldCommonHumanReadableByteCount]
    cache_reserved_in_bytes: NotRequired[FieldCommonByteCount]


class StatsClusterJvmMemory(TypedDict):
    heap_max: NotRequired[FieldCommonHumanReadableByteCount]
    heap_max_in_bytes: FieldCommonByteCount
    heap_used: NotRequired[FieldCommonHumanReadableByteCount]
    heap_used_in_bytes: FieldCommonByteCount


class StatsClusterJvmVersion(TypedDict):
    bundled_jdk: bool
    count: int
    using_bundled_jdk: bool
    version: FieldCommonVersionString
    vm_name: str
    vm_vendor: str
    vm_version: FieldCommonVersionString


class StatsClusterNetworkTypes(TypedDict):
    http_types: dict[str, int]
    transport_types: dict[str, int]


class StatsClusterNodeCount(TypedDict):
    coordinating_only: int
    data: int
    data_cold: NotRequired[int]
    data_content: NotRequired[int]
    data_frozen: NotRequired[int]
    data_hot: NotRequired[int]
    data_warm: NotRequired[int]
    ingest: int
    master: int
    cluster_manager: NotRequired[int]
    ml: NotRequired[int]
    remote_cluster_client: int
    search: NotRequired[int]
    total: int
    transform: NotRequired[int]
    voting_only: NotRequired[int]
    warm: NotRequired[int]


class StatsClusterOperatingSystemArchitecture(TypedDict):
    arch: str
    count: int


class StatsClusterOperatingSystemName(TypedDict):
    count: int
    name: NotRequired[FieldCommonName]


class StatsClusterOperatingSystemPrettyName(TypedDict):
    count: int
    pretty_name: NotRequired[FieldCommonName]


class StatsClusterProcessCpu(TypedDict):
    percent: FieldCommonPercentageNumber


class StatsClusterProcessOpenFileDescriptors(TypedDict):
    avg: int
    max: int
    min: int


class StatsClusterShardMetrics(TypedDict):
    avg: float
    max: float
    min: float


class StatsFieldTypes(TypedDict):
    name: FieldCommonName
    count: int
    index_count: int


class StatsFieldTypesMappings(TypedDict):
    field_types: list[StatsFieldTypes]


class StatsIndexingPressureMemorySummary(TypedDict):
    all_in_bytes: FieldCommonByteCount
    combined_coordinating_and_primary_in_bytes: FieldCommonByteCount
    coordinating_in_bytes: FieldCommonByteCount
    coordinating_rejections: NotRequired[float]
    primary_in_bytes: FieldCommonByteCount
    primary_rejections: NotRequired[float]
    replica_in_bytes: FieldCommonByteCount
    replica_rejections: NotRequired[float]


StatsIndexMetric: TypeAlias = Literal[
    "_all",
    "analysis",
    "completion",
    "docs",
    "fielddata",
    "mappings",
    "query_cache",
    "segments",
    "shards",
    "store",
]


class StatsIndicesVersions(TypedDict):
    index_count: int
    primary_shard_count: int
    total_primary_bytes: FieldCommonByteCount
    version: FieldCommonVersionString


StatsMetric: TypeAlias = Literal[
    "_all",
    "discovery_type",
    "fs",
    "indices",
    "ingest",
    "jvm",
    "network_types",
    "os",
    "packaging_types",
    "plugins",
    "process",
]


class StatsNodePackagingType(TypedDict):
    count: int
    flavor: NotRequired[str]
    type: str


class StatsOperatingSystemMemoryInfo(TypedDict):
    adjusted_total_in_bytes: NotRequired[FieldCommonByteCount]
    free: NotRequired[FieldCommonHumanReadableByteCount]
    free_in_bytes: FieldCommonByteCount
    free_percent: FieldCommonPercentageNumber
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_in_bytes: FieldCommonByteCount
    used: NotRequired[FieldCommonHumanReadableByteCount]
    used_in_bytes: FieldCommonByteCount
    used_percent: FieldCommonPercentageNumber


class WeightedRoutingWeightsBase(TypedDict):
    field_version: NotRequired[FieldCommonVersionNumber]
    weights: NotRequired[dict[str, str]]


class AllocationExplainAllocationDecision(TypedDict):
    decider: str
    decision: AllocationExplainAllocationExplainDecision
    explanation: str


class AllocationExplainClusterInfo(TypedDict):
    nodes: dict[str, AllocationExplainNodeDiskUsage]
    shard_sizes: dict[str, FieldCommonByteCount | FieldCommonHumanReadableByteCount]
    shard_data_set_sizes: NotRequired[dict[str, str]]
    shard_paths: dict[str, str]
    reserved_sizes: list[AllocationExplainReservedSize]


class AllocationExplainNodeAllocationExplanation(TypedDict):
    deciders: list[AllocationExplainAllocationDecision]
    node_attributes: dict[str, str]
    node_decision: AllocationExplainDecision
    node_id: FieldCommonId
    node_name: FieldCommonName
    store: NotRequired[AllocationExplainAllocationStore]
    transport_address: FieldCommonTransportAddress
    weight_ranking: NotRequired[int]


class HealthIndexHealthStats(TypedDict):
    active_primary_shards: int
    active_shards: int
    initializing_shards: int
    number_of_replicas: int
    number_of_shards: int
    relocating_shards: int
    shards: NotRequired[dict[str, HealthShardHealthStats]]
    status: FieldCommonHealthStatus
    unassigned_shards: int


class PendingTasksPendingTask(TypedDict):
    executing: bool
    insert_order: int
    priority: str
    source: str
    time_in_queue: NotRequired[FieldCommonDuration]
    time_in_queue_millis: FieldCommonDurationValueUnitMillis
    time_in_execution: NotRequired[FieldCommonDuration]
    time_in_execution_millis: NotRequired[FieldCommonDurationValueUnitMillis]


RemoteInfoClusterRemoteInfo: TypeAlias = (
    RemoteInfoClusterRemoteSniffInfo | RemoteInfoClusterRemoteProxyInfo
)


class RerouteCommand(TypedDict):
    cancel: NotRequired[RerouteCommandCancelAction]
    move: NotRequired[RerouteCommandMoveAction]
    allocate_replica: NotRequired[RerouteCommandAllocateReplicaAction]
    allocate_stale_primary: NotRequired[RerouteCommandAllocatePrimaryAction]
    allocate_empty_primary: NotRequired[RerouteCommandAllocatePrimaryAction]


class RerouteRerouteExplanation(TypedDict):
    command: str
    decisions: list[RerouteRerouteDecision]
    parameters: RerouteRerouteParameters


class StatsCharFilterTypes(TypedDict):
    analyzer_types: list[StatsFieldTypes]
    built_in_analyzers: list[StatsFieldTypes]
    built_in_char_filters: list[StatsFieldTypes]
    built_in_filters: list[StatsFieldTypes]
    built_in_tokenizers: list[StatsFieldTypes]
    char_filter_types: list[StatsFieldTypes]
    filter_types: list[StatsFieldTypes]
    tokenizer_types: list[StatsFieldTypes]


class StatsClusterIndicesShardsIndex(TypedDict):
    primaries: StatsClusterShardMetrics
    replication: StatsClusterShardMetrics
    shards: StatsClusterShardMetrics


class StatsClusterJvm(TypedDict):
    max_uptime: NotRequired[FieldCommonDuration]
    max_uptime_in_millis: FieldCommonDurationValueUnitMillis
    mem: StatsClusterJvmMemory
    threads: int
    versions: NotRequired[list[StatsClusterJvmVersion]]


class StatsClusterOperatingSystem(TypedDict):
    allocated_processors: int
    architectures: NotRequired[list[StatsClusterOperatingSystemArchitecture]]
    available_processors: int
    mem: StatsOperatingSystemMemoryInfo
    names: list[StatsClusterOperatingSystemName]
    pretty_names: list[StatsClusterOperatingSystemPrettyName]


class StatsClusterProcess(TypedDict):
    cpu: StatsClusterProcessCpu
    open_file_descriptors: StatsClusterProcessOpenFileDescriptors


class StatsClusterProcessor(TypedDict):
    count: int
    current: int
    failed: int
    time: NotRequired[FieldCommonDuration]
    time_in_millis: FieldCommonDurationValueUnitMillis


class StatsIndexingPressureMemory(TypedDict):
    current: StatsIndexingPressureMemorySummary
    limit_in_bytes: FieldCommonByteCount
    total: StatsIndexingPressureMemorySummary


class AllocationExplainUnassignedInformation(TypedDict):
    at: FieldCommonDateTime
    last_allocation_status: NotRequired[str]
    reason: AllocationExplainUnassignedInformationReason
    details: NotRequired[str]
    failed_allocation_attempts: NotRequired[int]
    delayed: NotRequired[bool]
    allocation_status: NotRequired[str]


class HealthHealthResponseBody(TypedDict):
    active_primary_shards: int
    active_shards: int
    active_shards_percent: NotRequired[FieldCommonPercentageString]
    active_shards_percent_as_number: FieldCommonPercentageNumber
    awareness_attributes: NotRequired[dict[str, HealthAwarenessAttributeStats]]
    cluster_name: FieldCommonName
    delayed_unassigned_shards: int
    discovered_master: NotRequired[bool]
    discovered_cluster_manager: NotRequired[bool]
    indices: NotRequired[dict[str, HealthIndexHealthStats]]
    initializing_shards: int
    number_of_data_nodes: int
    number_of_in_flight_fetch: int
    number_of_nodes: int
    number_of_pending_tasks: int
    relocating_shards: int
    status: FieldCommonHealthStatus
    task_max_waiting_in_queue: NotRequired[FieldCommonDuration]
    task_max_waiting_in_queue_millis: FieldCommonDurationValueUnitMillis
    timed_out: bool
    unassigned_shards: int


class StatsClusterIndicesShards(TypedDict):
    index: NotRequired[StatsClusterIndicesShardsIndex]
    primaries: NotRequired[int]
    replication: NotRequired[int]
    total: NotRequired[int]


class StatsClusterIngest(TypedDict):
    number_of_pipelines: int
    processor_stats: dict[str, StatsClusterProcessor]


class StatsIndexingPressure(TypedDict):
    memory: StatsIndexingPressureMemory


class StatsClusterIndices(TypedDict):
    analysis: NotRequired[StatsCharFilterTypes]
    completion: NotRequired[FieldCommonCompletionStats]
    count: NotRequired[int]
    docs: NotRequired[FieldCommonDocStats]
    fielddata: NotRequired[FieldCommonFielddataStats]
    query_cache: NotRequired[FieldCommonQueryCacheStats]
    segments: NotRequired[FieldCommonSegmentsStats]
    shards: NotRequired[StatsClusterIndicesShards]
    store: NotRequired[FieldCommonStoreStats]
    mappings: NotRequired[StatsFieldTypesMappings]
    versions: NotRequired[list[StatsIndicesVersions]]


class StatsClusterNodes(TypedDict):
    count: NotRequired[StatsClusterNodeCount]
    discovery_types: NotRequired[dict[str, int]]
    fs: NotRequired[StatsClusterFileSystem]
    indexing_pressure: NotRequired[StatsIndexingPressure]
    ingest: NotRequired[StatsClusterIngest]
    jvm: NotRequired[StatsClusterJvm]
    network_types: NotRequired[StatsClusterNetworkTypes]
    os: NotRequired[StatsClusterOperatingSystem]
    packaging_types: NotRequired[list[StatsNodePackagingType]]
    plugins: NotRequired[list[FieldCommonPluginStats]]
    process: NotRequired[StatsClusterProcess]
    versions: NotRequired[list[FieldCommonVersionString]]


class FieldCommonComponentTemplate(TypedDict):
    name: FieldCommonName
    component_template: FieldCommonComponentTemplateNode


class FieldCommonComponentTemplateNode(TypedDict):
    template: FieldCommonComponentTemplateSummary
    version: NotRequired[FieldCommonVersionNumber]
    field_meta: NotRequired[FieldCommonMetadata]


class FieldCommonComponentTemplateSummary(TypedDict):
    field_meta: NotRequired[FieldCommonMetadata]
    version: NotRequired[FieldCommonVersionNumber]
    settings: NotRequired[dict[str, FieldCommonIndexSettings]]
    mappings: NotRequired[MappingTypeMapping]
    aliases: NotRequired[dict[str, FieldCommonAliasDefinition]]


class AggregationsAggregateBase(TypedDict):
    meta: NotRequired[FieldCommonMetadata]


AggregationsAggregateOrder: TypeAlias = (
    dict[str, FieldCommonSortOrder] | list[dict[str, FieldCommonSortOrder]]
)

AggregationsAggregationRange = TypedDict(
    "AggregationsAggregationRange",
    {
        "from": NotRequired[float | str | None],
        "key": NotRequired[str],
        "to": NotRequired[float | str | None],
    },
)


class AggregationsArrayPercentilesItem(TypedDict):
    key: str
    value: float | None
    value_as_string: NotRequired[str]


class AggregationsBoxPlotAggregate(AggregationsAggregateBase):
    min: float
    max: float
    q1: float
    q2: float
    q3: float
    lower: float
    upper: float
    min_as_string: NotRequired[str]
    max_as_string: NotRequired[str]
    q1_as_string: NotRequired[str]
    q2_as_string: NotRequired[str]
    q3_as_string: NotRequired[str]
    lower_as_string: NotRequired[str]
    upper_as_string: NotRequired[str]


AggregationsBucketsPath: TypeAlias = str | list[str] | dict[str, str]


class AggregationsBucketsQueryContainer(TypedDict):
    pass


AggregationsCalendarInterval: TypeAlias = (
    Literal["second", "1s"]
    | Literal["minute", "1m"]
    | Literal["hour", "1h"]
    | Literal["day", "1d"]
    | Literal["week", "1w"]
    | Literal["month", "1M"]
    | Literal["quarter", "1q"]
    | Literal["year", "1Y"]
)


class AggregationsCardinalityAggregate(AggregationsAggregateBase):
    value: int


AggregationsCardinalityExecutionMode: TypeAlias = Literal[
    "direct", "global_ordinals", "segment_ordinals"
]


class AggregationsChildrenAggregationFields(TypedDict):
    type: NotRequired[FieldCommonRelationName]


class AggregationsChiSquareHeuristic(TypedDict):
    background_is_superset: bool
    include_negatives: bool


AggregationsCompositeAggregateKey: TypeAlias = dict[str, FieldCommonFieldValue]


class AggregationsCumulativeCardinalityAggregate(AggregationsAggregateBase):
    value: int
    value_as_string: NotRequired[str]


class AggregationsEwmaModelSettings(TypedDict):
    alpha: NotRequired[float]


AggregationsFieldDateMath: TypeAlias = FieldCommonDateMath | float


class AggregationsFiltersAggregationFields(TypedDict):
    filters: NotRequired[AggregationsBucketsQueryContainer]
    other_bucket: NotRequired[bool]
    other_bucket_key: NotRequired[str]
    keyed: NotRequired[bool]


AggregationsGapPolicy: TypeAlias = Literal["insert_zeros", "keep_values", "skip"]


class AggregationsGlobalAggregationFields(TypedDict):
    pass


class AggregationsGoogleNormalizedDistanceHeuristic(TypedDict):
    background_is_superset: NotRequired[bool]


class AggregationsHdrMethod(TypedDict):
    number_of_significant_value_digits: NotRequired[int]


class AggregationsHistogramOrder(TypedDict):
    field_count: NotRequired[FieldCommonSortOrder]
    field_key: NotRequired[FieldCommonSortOrder]


class AggregationsHoltLinearModelSettings(TypedDict):
    alpha: NotRequired[float]
    beta: NotRequired[float]


AggregationsHoltWintersType: TypeAlias = Literal["add", "mult"]

AggregationsIpRangeAggregationRange = TypedDict(
    "AggregationsIpRangeAggregationRange",
    {
        "from": NotRequired[str | None],
        "mask": NotRequired[str],
        "to": NotRequired[str | None],
    },
)

AggregationsKeyedPercentiles: TypeAlias = dict[str, float | str | None] | None

AggregationsLongTermsBucketKey: TypeAlias = int | str


class AggregationsMatrixAggregation(TypedDict):
    fields: NotRequired[FieldCommonFields]
    missing: NotRequired[dict[str, float]]


class AggregationsMatrixStatsAggregation(AggregationsMatrixAggregation):
    mode: NotRequired[FieldCommonSortMode]


class AggregationsMatrixStatsFields(TypedDict):
    name: FieldCommonField
    count: int
    mean: float
    variance: float
    skewness: float
    kurtosis: float
    covariance: dict[str, float]
    correlation: dict[str, float]


class AggregationsMetricAggregationBase(TypedDict):
    field: NotRequired[FieldCommonField]


class AggregationsMetricAggregationBaseModel(TypedDict):
    missing: NotRequired[FieldCommonFieldValue]


class AggregationsMetricAggregationBaseModel1(
    AggregationsMetricAggregationBase, AggregationsMetricAggregationBaseModel
):
    pass


AggregationsMinimumInterval: TypeAlias = Literal[
    "day", "hour", "minute", "month", "second", "year"
]


class AggregationsMissingAggregationFields(TypedDict):
    field: NotRequired[FieldCommonField]
    missing: NotRequired[FieldCommonFieldValue]


AggregationsMissingOrder: TypeAlias = Literal["default", "first", "last"]


class Buckets(TypedDict):
    pass


class AggregationsMultiBucketAggregateBase(AggregationsAggregateBase):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseAdjacencyMatrixBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseCompositeBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseDateHistogramBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseFiltersBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseGeoHashGridBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseGeoTileGridBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseHistogramBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseIpRangeBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseLongRareTermsBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: NotRequired[Buckets]


class AggregationsMultiBucketAggregateBaseRangeBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseStringRareTermsBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: NotRequired[Buckets]


class AggregationsMultiBucketAggregateBaseVariableWidthHistogramBucket(
    AggregationsMultiBucketAggregateBase
):
    buckets: Buckets


class AggregationsMultiBucketAggregateBaseVoid(AggregationsMultiBucketAggregateBase):
    buckets: NotRequired[Buckets]


class AggregationsMultiBucketBase(TypedDict):
    doc_count: int


class AggregationsMultiTermLookup(TypedDict):
    field: FieldCommonField
    missing: NotRequired[FieldCommonFieldValue]


class AggregationsMultiTermsBucket(AggregationsMultiBucketBase):
    key: list[FieldCommonFieldValue]
    key_as_string: NotRequired[str]
    doc_count_error_upper_bound: NotRequired[int]


class AggregationsMutualInformationHeuristic(TypedDict):
    background_is_superset: NotRequired[bool]
    include_negatives: NotRequired[bool]


class AggregationsNestedAggregationFields(TypedDict):
    path: NotRequired[FieldCommonField]


AggregationsNormalizeMethod: TypeAlias = Literal[
    "mean", "percent_of_sum", "rescale_0_1", "rescale_0_100", "softmax", "z-score"
]


class AggregationsParentAggregationFields(TypedDict):
    type: NotRequired[FieldCommonRelationName]


class AggregationsPercentageScoreHeuristic(TypedDict):
    pass


AggregationsPercentiles: TypeAlias = (
    AggregationsKeyedPercentiles | list[AggregationsArrayPercentilesItem]
)


class AggregationsPercentilesAggregateBase(AggregationsAggregateBase):
    values: AggregationsPercentiles


class AggregationsPercentilesBucketAggregate(AggregationsPercentilesAggregateBase):
    pass


class AggregationsRangeAggregateBase(AggregationsMultiBucketAggregateBaseRangeBucket):
    pass


AggregationsRangeBucket = TypedDict(
    "AggregationsRangeBucket",
    {
        "doc_count": int,
        "from": NotRequired[float],
        "to": NotRequired[float],
        "from_as_string": NotRequired[str],
        "to_as_string": NotRequired[str],
        "key": NotRequired[str],
    },
)


class AggregationsRateAggregate(AggregationsAggregateBase):
    value: float
    value_as_string: NotRequired[str]


AggregationsRateMode: TypeAlias = Literal["sum", "value_count"]


class AggregationsReverseNestedAggregationFields(TypedDict):
    path: NotRequired[FieldCommonField]


AggregationsSamplerAggregationExecutionHint: TypeAlias = Literal[
    "bytes_hash", "global_ordinals", "map"
]


class AggregationsSamplerAggregationFields(TypedDict):
    shard_size: NotRequired[int]


class AggregationsScriptedMetricAggregate(AggregationsAggregateBase):
    value: Any


class AggregationsSignificantTermsAggregateBase(AggregationsMultiBucketAggregateBase):
    bg_count: NotRequired[int]
    doc_count: NotRequired[int]


class AggregationsSignificantTermsAggregateBaseSignificantLongTermsBucket(
    AggregationsSignificantTermsAggregateBase
):
    buckets: NotRequired[Buckets]


class AggregationsSignificantTermsAggregateBaseSignificantStringTermsBucket(
    AggregationsSignificantTermsAggregateBase
):
    buckets: NotRequired[Buckets]


class AggregationsSignificantTermsAggregateBaseVoid(
    AggregationsSignificantTermsAggregateBase
):
    buckets: NotRequired[Buckets]


class AggregationsSignificantTermsBucketBase(AggregationsMultiBucketBase):
    score: float
    bg_count: int


class AggregationsSingleBucketAggregateBase(AggregationsAggregateBase):
    doc_count: int


class AggregationsSingleMetricAggregateBase(AggregationsAggregateBase):
    value: float | None
    value_as_string: NotRequired[str]


class AggregationsStandardDeviationBounds(TypedDict):
    upper: float | None
    lower: float | None
    upper_population: float | None
    lower_population: float | None
    upper_sampling: float | None
    lower_sampling: float | None


class AggregationsStandardDeviationBoundsAsString(TypedDict):
    upper: str
    lower: str
    upper_population: str
    lower_population: str
    upper_sampling: str
    lower_sampling: str


class AggregationsStatsAggregateBase(AggregationsAggregateBase):
    count: int
    min: float | None
    max: float | None
    avg: float | None
    sum: float
    min_as_string: NotRequired[str]
    max_as_string: NotRequired[str]
    avg_as_string: NotRequired[str]
    sum_as_string: NotRequired[str]


class AggregationsStatsBucketAggregate(AggregationsStatsAggregateBase):
    pass


class AggregationsStringRareTermsAggregate(
    AggregationsMultiBucketAggregateBaseStringRareTermsBucket
):
    pass


class AggregationsStringRareTermsBucket(AggregationsMultiBucketBase):
    key: str


class AggregationsSumAggregate(AggregationsSingleMetricAggregateBase):
    pass


AggregationsT: TypeAlias = Any

AggregationsTBucket: TypeAlias = Any


class AggregationsTDigest(TypedDict):
    compression: NotRequired[int]


class AggregationsTDigestPercentileRanksAggregate(AggregationsPercentilesAggregateBase):
    pass


class AggregationsTDigestPercentilesAggregate(AggregationsPercentilesAggregateBase):
    pass


class AggregationsTermsAggregateBase(AggregationsMultiBucketAggregateBase):
    doc_count_error_upper_bound: NotRequired[int]
    sum_other_doc_count: NotRequired[int]


class AggregationsTermsAggregateBaseMultiTermsBucket(AggregationsTermsAggregateBase):
    buckets: NotRequired[Buckets]


class AggregationsTermsAggregateBaseVoid(AggregationsTermsAggregateBase):
    buckets: list[FieldCommonVoid]


AggregationsTermsAggregationCollectMode: TypeAlias = Literal[
    "breadth_first", "depth_first"
]

AggregationsTermsAggregationExecutionHint: TypeAlias = Literal[
    "global_ordinals", "global_ordinals_hash", "global_ordinals_low_cardinality", "map"
]


class AggregationsTermsAggregationFields(TypedDict):
    field: NotRequired[FieldCommonField]


class AggregationsTermsBucketBase(AggregationsMultiBucketBase):
    doc_count_error_upper_bound: NotRequired[int]


AggregationsTermsExclude: TypeAlias = str | list[str]


class AggregationsTermsPartition(TypedDict):
    num_partitions: int
    partition: int


class AggregationsTTestAggregate(AggregationsAggregateBase):
    value: float | None
    value_as_string: NotRequired[str]


AggregationsTTestType: TypeAlias = Literal["heteroscedastic", "homoscedastic", "paired"]


class AggregationsUnmappedRareTermsAggregate(AggregationsMultiBucketAggregateBaseVoid):
    pass


class AggregationsUnmappedSignificantTermsAggregate(
    AggregationsSignificantTermsAggregateBaseVoid
):
    pass


class AggregationsUnmappedTermsAggregate(AggregationsTermsAggregateBaseVoid):
    pass


class AggregationsUnsignedLongTermsBucket(AggregationsTermsBucketBase):
    key: float
    key_as_string: NotRequired[str]


class AggregationsValueCountAggregate(AggregationsSingleMetricAggregateBase):
    pass


AggregationsValueType: TypeAlias = Literal[
    "boolean",
    "byte",
    "date",
    "double",
    "float",
    "integer",
    "ip",
    "long",
    "number",
    "numeric",
    "short",
    "string",
    "unsigned_long",
]


class AggregationsVariableWidthHistogramAggregate(
    AggregationsMultiBucketAggregateBaseVariableWidthHistogramBucket
):
    pass


class AggregationsVariableWidthHistogramAggregation(TypedDict):
    field: NotRequired[FieldCommonField]
    buckets: NotRequired[int]
    shard_size: NotRequired[int]
    initial_buffer: NotRequired[int]


class AggregationsVariableWidthHistogramBucket(AggregationsMultiBucketBase):
    min: float
    key: float
    max: float
    min_as_string: NotRequired[str]
    key_as_string: NotRequired[str]
    max_as_string: NotRequired[str]


class AggregationsWeightedAvgAggregate(AggregationsSingleMetricAggregateBase):
    pass


class AnalysisCharFilterBase(TypedDict):
    version: NotRequired[FieldCommonVersionString]


class AnalysisCustomAnalyzer(TypedDict):
    type: Literal["custom"]
    char_filter: NotRequired[list[str]]
    filter: NotRequired[list[str]]
    position_increment_gap: NotRequired[int]
    position_offset_gap: NotRequired[int]
    tokenizer: str


class AnalysisCustomNormalizer(TypedDict):
    type: Literal["custom"]
    char_filter: NotRequired[list[str]]
    filter: NotRequired[list[str]]


AnalysisDelimitedPayloadEncoding: TypeAlias = Literal["float", "identity", "int"]

AnalysisEdgeNGramSide: TypeAlias = Literal["back", "front"]


class AnalysisHtmlStripCharFilter(AnalysisCharFilterBase):
    type: Literal["html_strip"]


AnalysisIcuCollationAlternate: TypeAlias = Literal["non-ignorable", "shifted"]

AnalysisIcuCollationCaseFirst: TypeAlias = Literal["lower", "upper"]

AnalysisIcuCollationDecomposition: TypeAlias = Literal["canonical", "no"]

AnalysisIcuCollationStrength: TypeAlias = Literal[
    "identical", "primary", "quaternary", "secondary", "tertiary"
]

AnalysisIcuNormalizationMode: TypeAlias = Literal["compose", "decompose"]

AnalysisIcuNormalizationType: TypeAlias = Literal["nfc", "nfkc", "nfkc_cf"]

AnalysisIcuTransformDirection: TypeAlias = Literal["forward", "reverse"]

AnalysisKeepTypesMode: TypeAlias = Literal["exclude", "include"]


class AnalysisKeywordAnalyzer(TypedDict):
    type: Literal["keyword"]
    version: NotRequired[FieldCommonVersionString]


class AnalysisKuromojiIterationMarkCharFilter(AnalysisCharFilterBase):
    type: Literal["kuromoji_iteration_mark"]
    normalize_kana: bool
    normalize_kanji: bool


AnalysisKuromojiTokenizationMode: TypeAlias = Literal["extended", "normal", "search"]

AnalysisLanguage: TypeAlias = Literal[
    "Arabic",
    "Armenian",
    "Basque",
    "Brazilian",
    "Bulgarian",
    "Catalan",
    "Chinese",
    "Cjk",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Estonian",
    "Finnish",
    "French",
    "Galician",
    "German",
    "Greek",
    "Hindi",
    "Hungarian",
    "Indonesian",
    "Irish",
    "Italian",
    "Latvian",
    "Norwegian",
    "Persian",
    "Portuguese",
    "Romanian",
    "Russian",
    "Sorani",
    "Spanish",
    "Swedish",
    "Thai",
    "Turkish",
]


class AnalysisLowercaseNormalizer(TypedDict):
    type: Literal["lowercase"]


class AnalysisMappingCharFilter(AnalysisCharFilterBase):
    type: Literal["mapping"]
    mappings: NotRequired[list[str]]
    mappings_path: NotRequired[str]


AnalysisNoriDecompoundMode: TypeAlias = Literal["discard", "mixed", "none"]

AnalysisNormalizer: TypeAlias = AnalysisLowercaseNormalizer | AnalysisCustomNormalizer


class AnalysisPatternReplaceCharFilter(AnalysisCharFilterBase):
    type: Literal["pattern_replace"]
    flags: NotRequired[str]
    pattern: str
    replacement: NotRequired[str]


AnalysisPhoneAnalyzerBase = TypedDict(
    "AnalysisPhoneAnalyzerBase",
    {
        "phone-region": NotRequired[str],
    },
)


class AnalysisPhoneSearchAnalyzer(AnalysisPhoneAnalyzerBase):
    type: Literal["phone-search"]


AnalysisPhoneticEncoder: TypeAlias = Literal[
    "beider_morse",
    "caverphone1",
    "caverphone2",
    "cologne",
    "daitch_mokotoff",
    "double_metaphone",
    "haasephonetik",
    "koelnerphonetik",
    "metaphone",
    "nysiis",
    "refined_soundex",
    "soundex",
]

AnalysisPhoneticLanguage: TypeAlias = Literal[
    "any",
    "common",
    "cyrillic",
    "english",
    "french",
    "german",
    "hebrew",
    "hungarian",
    "polish",
    "romanian",
    "russian",
    "spanish",
]

AnalysisPhoneticNameType: TypeAlias = Literal["ashkenazi", "generic", "sephardic"]

AnalysisPhoneticRuleType: TypeAlias = Literal["approx", "exact"]


class AnalysisSimpleAnalyzer(TypedDict):
    type: Literal["simple"]
    version: NotRequired[FieldCommonVersionString]


class AnalysisSmartcnAnalyzer(TypedDict):
    type: NotRequired[Literal["smartcn"]]


AnalysisSnowballLanguage: TypeAlias = Literal[
    "Armenian",
    "Basque",
    "Catalan",
    "Danish",
    "Dutch",
    "English",
    "Finnish",
    "French",
    "German",
    "German2",
    "Hungarian",
    "Italian",
    "Kp",
    "Lovins",
    "Norwegian",
    "Porter",
    "Portuguese",
    "Romanian",
    "Russian",
    "Spanish",
    "Swedish",
    "Turkish",
]

AnalysisStopWords: TypeAlias = FieldCommonStringOrStringArray

AnalysisSynonymFormat: TypeAlias = Literal["solr", "wordnet"]

AnalysisTokenChar: TypeAlias = Literal[
    "custom", "digit", "letter", "punctuation", "symbol", "whitespace"
]


class AnalysisTokenFilterBase(TypedDict):
    version: NotRequired[FieldCommonVersionString]


class AnalysisTokenizerBase(TypedDict):
    version: NotRequired[FieldCommonVersionString]


class AnalysisTrimTokenFilter(AnalysisTokenFilterBase):
    type: Literal["trim"]


class AnalysisTruncateTokenFilter(AnalysisTokenFilterBase):
    type: Literal["truncate"]
    length: NotRequired[int]


class AnalysisUaxEmailUrlTokenizer(AnalysisTokenizerBase):
    type: Literal["uax_url_email"]
    max_token_length: NotRequired[int]


class AnalysisUniqueTokenFilter(AnalysisTokenFilterBase):
    type: Literal["unique"]
    only_on_same_position: NotRequired[bool]


class AnalysisUppercaseTokenFilter(AnalysisTokenFilterBase):
    type: Literal["uppercase"]


class AnalysisWhitespaceAnalyzer(TypedDict):
    type: Literal["whitespace"]
    version: NotRequired[FieldCommonVersionString]


class AnalysisWhitespaceTokenizer(AnalysisTokenizerBase):
    type: Literal["whitespace"]
    max_token_length: NotRequired[int]


class AnalysisWordDelimiterGraphTokenFilter(AnalysisTokenFilterBase):
    type: Literal["word_delimiter_graph"]
    adjust_offsets: NotRequired[bool]
    catenate_all: NotRequired[bool]
    catenate_numbers: NotRequired[bool]
    catenate_words: NotRequired[bool]
    generate_number_parts: NotRequired[bool]
    generate_word_parts: NotRequired[bool]
    ignore_keywords: NotRequired[bool]
    preserve_original: NotRequired[FieldCommonStringifiedBoolean]
    protected_words: NotRequired[list[str]]
    protected_words_path: NotRequired[str]
    split_on_case_change: NotRequired[bool]
    split_on_numerics: NotRequired[bool]
    stem_english_possessive: NotRequired[bool]
    type_table: NotRequired[list[str]]
    type_table_path: NotRequired[str]


class AnalysisWordDelimiterTokenFilter(AnalysisTokenFilterBase):
    type: Literal["word_delimiter"]
    catenate_all: NotRequired[bool]
    catenate_numbers: NotRequired[bool]
    catenate_words: NotRequired[bool]
    generate_number_parts: NotRequired[bool]
    generate_word_parts: NotRequired[bool]
    preserve_original: NotRequired[FieldCommonStringifiedBoolean]
    protected_words: NotRequired[list[str]]
    protected_words_path: NotRequired[str]
    split_on_case_change: NotRequired[bool]
    split_on_numerics: NotRequired[bool]
    stem_english_possessive: NotRequired[bool]
    type_table: NotRequired[list[str]]
    type_table_path: NotRequired[str]


class MappingAllField(TypedDict):
    analyzer: str
    enabled: bool
    omit_norms: bool
    search_analyzer: str
    similarity: str
    store: bool
    store_term_vector_offsets: bool
    store_term_vector_payloads: bool
    store_term_vector_positions: bool
    store_term_vectors: bool


class MappingDataStreamTimestamp(TypedDict):
    enabled: bool


MappingDynamicMapping: TypeAlias = (
    Literal["false", "strict", "strict_allow_templates", "true"] | bool
)


class MappingFieldNamesField(TypedDict):
    enabled: bool


MappingFieldType: TypeAlias = Literal[
    "aggregate_metric_double",
    "alias",
    "binary",
    "boolean",
    "byte",
    "completion",
    "constant_keyword",
    "date",
    "date_nanos",
    "date_range",
    "double",
    "double_range",
    "flat_object",
    "float",
    "float_range",
    "geo_point",
    "geo_shape",
    "half_float",
    "histogram",
    "icu_collation_keyword",
    "integer",
    "integer_range",
    "ip",
    "ip_range",
    "join",
    "keyword",
    "knn_vector",
    "long",
    "long_range",
    "match_only_text",
    "murmur3",
    "nested",
    "object",
    "percolator",
    "rank_feature",
    "rank_features",
    "scaled_float",
    "search_as_you_type",
    "semantic",
    "short",
    "text",
    "token_count",
    "unsigned_long",
    "version",
    "wildcard",
    "xy_point",
    "xy_shape",
]

MappingGeoOrientation: TypeAlias = (
    Literal["left", "LEFT", "clockwise", "cw"]
    | Literal["right", "RIGHT", "counterclockwise", "ccw"]
)

MappingGeoStrategy: TypeAlias = Literal["recursive", "term"]


class MappingIndexField(TypedDict):
    enabled: bool


MappingIndexOptions: TypeAlias = Literal["docs", "freqs", "offsets", "positions"]


class MappingKnnVectorMethod(TypedDict):
    name: str
    space_type: NotRequired[str]
    engine: NotRequired[str]
    parameters: NotRequired[dict[str, Any]]


MappingMatchType: TypeAlias = Literal["regex", "simple"]


class MappingRoutingField(TypedDict):
    required: bool


class MappingSemanticChunkingStrategy(TypedDict):
    algorithm: str
    parameters: NotRequired[dict[str, Any]]


class MappingSemanticDenseEmbeddingConfig(TypedDict):
    data_type: NotRequired[str]
    mode: NotRequired[str]
    compression_level: NotRequired[str]
    method: NotRequired[MappingKnnVectorMethod]


class MappingSemanticSparseEncodingConfig(TypedDict):
    prune_type: NotRequired[str]
    prune_ratio: NotRequired[float]


class MappingSizeField(TypedDict):
    enabled: bool


class MappingSourceField(TypedDict):
    compress: NotRequired[bool]
    compress_threshold: NotRequired[str]
    enabled: NotRequired[bool]
    excludes: NotRequired[list[str]]
    includes: NotRequired[list[str]]


class MappingSuggestContext(TypedDict):
    name: FieldCommonName
    path: NotRequired[FieldCommonField]
    type: str
    precision: NotRequired[float | str]


MappingTermVectorOption: TypeAlias = Literal[
    "no",
    "with_offsets",
    "with_positions",
    "with_positions_offsets",
    "with_positions_offsets_payloads",
    "with_positions_payloads",
    "yes",
]


class MappingTextIndexPrefixes(TypedDict):
    max_chars: int
    min_chars: int


QueryDslChildScoreMode: TypeAlias = Literal["avg", "max", "min", "none", "sum"]

QueryDslCombinedFieldsOperator: TypeAlias = Literal["and", "or"]

QueryDslCombinedFieldsZeroTerms: TypeAlias = Literal["all", "none"]


class QueryDslFieldLookup(TypedDict):
    id: FieldCommonId
    index: NotRequired[FieldCommonIndexName]
    path: NotRequired[FieldCommonField]
    routing: NotRequired[FieldCommonRouting]


QueryDslFieldValueFactorModifier: TypeAlias = Literal[
    "ln",
    "ln1p",
    "ln2p",
    "log",
    "log1p",
    "log2p",
    "none",
    "reciprocal",
    "sqrt",
    "square",
]


class QueryDslFieldValueFactorScoreFunction(TypedDict):
    field: FieldCommonField
    factor: NotRequired[float]
    missing: NotRequired[float]
    modifier: NotRequired[QueryDslFieldValueFactorModifier]


QueryDslFunctionBoostMode: TypeAlias = Literal[
    "avg", "max", "min", "multiply", "replace", "sum"
]

QueryDslFunctionScoreMode: TypeAlias = Literal[
    "avg", "first", "max", "min", "multiply", "sum"
]

QueryDslGeoExecution: TypeAlias = Literal["indexed", "memory"]


class QueryDslGeoShape(TypedDict):
    type: NotRequired[str]
    coordinates: NotRequired[list[Any]]


class QueryDslGeoShapeQueryField(TypedDict):
    indexed_shape: NotRequired[QueryDslFieldLookup]
    shape: QueryDslGeoShape
    relation: NotRequired[FieldCommonGeoShapeRelation]


QueryDslGeoValidationMethod: TypeAlias = Literal["coerce", "ignore_malformed", "strict"]

QueryDslIgnoreUnmapped: TypeAlias = bool


class QueryDslIntervalsFuzzy(TypedDict):
    analyzer: NotRequired[str]
    fuzziness: NotRequired[FieldCommonFuzziness]
    prefix_length: NotRequired[int]
    term: str
    transpositions: NotRequired[bool]
    use_field: NotRequired[FieldCommonField]


class QueryDslIntervalsPrefix(TypedDict):
    analyzer: NotRequired[str]
    prefix: str
    use_field: NotRequired[FieldCommonField]


class QueryDslIntervalsWildcard(TypedDict):
    analyzer: NotRequired[str]
    pattern: str
    use_field: NotRequired[FieldCommonField]


class QueryDslLikeDocument(TypedDict):
    doc: NotRequired[Any]
    fields: NotRequired[list[FieldCommonField]]
    field_id: NotRequired[FieldCommonId]
    field_index: NotRequired[FieldCommonIndexName]
    field_type: NotRequired[FieldCommonType]
    per_field_analyzer: NotRequired[dict[str, str]]
    routing: NotRequired[FieldCommonRouting]
    version: NotRequired[FieldCommonVersionNumber]
    version_type: NotRequired[FieldCommonVersionType]


QueryDslMultiValueMode: TypeAlias = Literal["avg", "max", "min", "sum"]


class QueryDslNumericDecayPlacement(TypedDict):
    decay: NotRequired[float]
    offset: NotRequired[float]
    origin: float
    scale: float


QueryDslOperator: TypeAlias = Literal["and", "AND", "or", "OR"]


class QueryDslQueryBase(TypedDict):
    boost: NotRequired[float]
    field_name: NotRequired[str]


QueryDslQueryVector: TypeAlias = list[float]


class QueryDslRandomScoreFunction(TypedDict):
    field: NotRequired[FieldCommonField]
    seed: NotRequired[int | str]


QueryDslRangeRelation: TypeAlias = Literal["contains", "intersects", "within"]


class QueryDslRankFeatureFunction(TypedDict):
    pass


class QueryDslRankFeatureFunctionLinear(QueryDslRankFeatureFunction):
    pass


class QueryDslRankFeatureFunctionLogarithm(QueryDslRankFeatureFunction):
    scaling_factor: float


class QueryDslRankFeatureFunctionSaturation(QueryDslRankFeatureFunction):
    pivot: NotRequired[float]


class QueryDslRankFeatureFunctionSigmoid(QueryDslRankFeatureFunction):
    pivot: float
    exponent: float


class QueryDslRankFeatureQuery(QueryDslQueryBase):
    field: FieldCommonField
    saturation: NotRequired[QueryDslRankFeatureFunctionSaturation]
    log: NotRequired[QueryDslRankFeatureFunctionLogarithm]
    linear: NotRequired[QueryDslRankFeatureFunctionLinear]
    sigmoid: NotRequired[QueryDslRankFeatureFunctionSigmoid]


class QueryDslRegexpQuery(QueryDslQueryBase):
    case_insensitive: NotRequired[bool]
    flags: NotRequired[str]
    max_determinized_states: NotRequired[int]
    rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    value: str


QueryDslRegexpQueryModel: TypeAlias = str | QueryDslRegexpQuery


class QueryDslRescoreContext(TypedDict):
    oversample_factor: NotRequired[float]


QueryDslSimpleQueryStringFlag: TypeAlias = Literal[
    "ALL",
    "AND",
    "ESCAPE",
    "FUZZY",
    "NEAR",
    "NONE",
    "NOT",
    "OR",
    "PHRASE",
    "PRECEDENCE",
    "PREFIX",
    "SLOP",
    "WHITESPACE",
]

QueryDslSimpleQueryStringFlags: TypeAlias = QueryDslSimpleQueryStringFlag | str


class QueryDslSimpleQueryStringQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    analyze_wildcard: NotRequired[bool]
    auto_generate_synonyms_phrase_query: NotRequired[bool]
    default_operator: NotRequired[QueryDslOperator]
    fields: NotRequired[list[FieldCommonField]]
    flags: NotRequired[QueryDslSimpleQueryStringFlags]
    fuzzy_max_expansions: NotRequired[int]
    fuzzy_prefix_length: NotRequired[int]
    fuzzy_transpositions: NotRequired[bool]
    lenient: NotRequired[bool]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    query: str
    quote_field_suffix: NotRequired[str]


QueryDslSpanGapQuery: TypeAlias = dict[FieldCommonField, int]


class QueryDslSpanTermQuery(QueryDslQueryBase):
    value: str


QueryDslSpanTermQueryModel: TypeAlias = str | QueryDslSpanTermQuery


class QueryDslTermQuery(QueryDslQueryBase):
    value: FieldCommonFieldValue
    case_insensitive: NotRequired[bool]


QueryDslTermQueryModel: TypeAlias = FieldCommonFieldValue | QueryDslTermQuery


class QueryDslTermsLookup(TypedDict):
    index: FieldCommonIndexName
    id: FieldCommonId
    path: FieldCommonField
    routing: NotRequired[FieldCommonRouting]
    store: NotRequired[bool]


QueryDslTermsQueryField: TypeAlias = list[FieldCommonFieldValue] | QueryDslTermsLookup

QueryDslTermsQueryValueType: TypeAlias = Literal["bitmap", "default"]

QueryDslTextQueryType: TypeAlias = Literal[
    "best_fields",
    "bool_prefix",
    "cross_fields",
    "most_fields",
    "phrase",
    "phrase_prefix",
]


class QueryDslTypeQuery(QueryDslQueryBase):
    value: str


class QueryDslWildcardQuery(QueryDslQueryBase):
    case_insensitive: NotRequired[bool]
    rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    value: NotRequired[str]
    wildcard: NotRequired[str]


QueryDslWildcardQueryModel: TypeAlias = str | QueryDslWildcardQuery


class QueryDslWrapperQuery(QueryDslQueryBase):
    query: str


class QueryDslXyShape(TypedDict):
    type: NotRequired[str]
    coordinates: NotRequired[list[Any]]


class QueryDslXyShapeQuery(QueryDslQueryBase):
    ignore_unmapped: NotRequired[bool]


class QueryDslXyShapeQueryField(TypedDict):
    indexed_shape: NotRequired[QueryDslFieldLookup]
    shape: QueryDslXyShape
    relation: NotRequired[FieldCommonGeoShapeRelation]


QueryDslZeroTermsQuery: TypeAlias = Literal["all", "ALL", "none", "NONE"]


class AggregationsAdjacencyMatrixAggregate(
    AggregationsMultiBucketAggregateBaseAdjacencyMatrixBucket
):
    pass


class AggregationsAdjacencyMatrixBucket(AggregationsMultiBucketBase):
    key: str


class AggregationsAggregationContainerModel1(TypedDict):
    variable_width_histogram: AggregationsVariableWidthHistogramAggregation


class AggregationsAutoDateHistogramAggregate(
    AggregationsMultiBucketAggregateBaseDateHistogramBucket
):
    interval: FieldCommonDurationLarge


class AggregationsAvgAggregate(AggregationsSingleMetricAggregateBase):
    pass


class AggregationsBucketMetricValueAggregate(AggregationsSingleMetricAggregateBase):
    keys: list[str]


class AggregationsBucketPathAggregation(TypedDict):
    buckets_path: NotRequired[AggregationsBucketsPath]


AggregationsBuckets: TypeAlias = (
    dict[str, AggregationsTBucket] | list[AggregationsTBucket]
)


class AggregationsChildrenAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsCompositeAggregate(
    AggregationsMultiBucketAggregateBaseCompositeBucket
):
    after_key: NotRequired[AggregationsCompositeAggregateKey]


class AggregationsCompositeBucket(AggregationsMultiBucketBase):
    key: AggregationsCompositeAggregateKey


class AggregationsCompositeValuesSource(TypedDict):
    field: NotRequired[FieldCommonField]
    missing_bucket: NotRequired[bool]
    missing_order: NotRequired[AggregationsMissingOrder]
    script: NotRequired[FieldCommonScript]
    value_type: NotRequired[AggregationsValueType]
    order: NotRequired[FieldCommonSortOrder]


class AggregationsDateHistogramAggregate(
    AggregationsMultiBucketAggregateBaseDateHistogramBucket
):
    pass


class AggregationsDateHistogramBucket(AggregationsMultiBucketBase):
    key_as_string: NotRequired[str]
    key: FieldCommonEpochTimeUnitMillis


class AggregationsDateRangeAggregate(AggregationsRangeAggregateBase):
    pass


AggregationsDateRangeExpression = TypedDict(
    "AggregationsDateRangeExpression",
    {
        "from": NotRequired[AggregationsFieldDateMath],
        "key": NotRequired[str],
        "to": NotRequired[AggregationsFieldDateMath],
    },
)


class AggregationsDerivativeAggregate(AggregationsSingleMetricAggregateBase):
    normalized_value: NotRequired[float]
    normalized_value_as_string: NotRequired[str]


class AggregationsDiversifiedSamplerAggregationFields(TypedDict):
    execution_hint: NotRequired[AggregationsSamplerAggregationExecutionHint]
    max_docs_per_value: NotRequired[int]
    script: NotRequired[FieldCommonScript]
    shard_size: NotRequired[int]
    field: NotRequired[FieldCommonField]


class AggregationsDoubleTermsBucket(AggregationsTermsBucketBase):
    key: float
    key_as_string: NotRequired[str]


class AggregationsExtendedBounds(TypedDict):
    max: AggregationsT
    min: AggregationsT


class AggregationsExtendedBoundsDouble(AggregationsExtendedBounds):
    max: NotRequired[float]
    min: NotRequired[float]


class AggregationsExtendedBoundsFieldDateMath(AggregationsExtendedBounds):
    max: NotRequired[AggregationsFieldDateMath]
    min: NotRequired[AggregationsFieldDateMath]


class AggregationsExtendedStatsAggregateBase(AggregationsStatsAggregateBase):
    sum_of_squares: float | None
    variance: float | None
    variance_population: float | None
    variance_sampling: float | None
    std_deviation: float | None
    std_deviation_population: float | None
    std_deviation_sampling: float | None
    std_deviation_bounds: NotRequired[AggregationsStandardDeviationBounds]
    sum_of_squares_as_string: NotRequired[str]
    variance_as_string: NotRequired[str]
    variance_population_as_string: NotRequired[str]
    variance_sampling_as_string: NotRequired[str]
    std_deviation_as_string: NotRequired[str]
    std_deviation_bounds_as_string: NotRequired[
        AggregationsStandardDeviationBoundsAsString
    ]


class AggregationsExtendedStatsBucketAggregate(AggregationsExtendedStatsAggregateBase):
    pass


class AggregationsFilterAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsFiltersAggregate(AggregationsMultiBucketAggregateBaseFiltersBucket):
    pass


class AggregationsFiltersBucket(AggregationsMultiBucketBase):
    pass


class AggregationsGeoCentroidAggregate(AggregationsAggregateBase):
    count: int
    location: NotRequired[FieldCommonGeoLocation]


class AggregationsGeoDistanceAggregate(AggregationsRangeAggregateBase):
    pass


class AggregationsGeoDistanceAggregationFields(TypedDict):
    distance_type: NotRequired[FieldCommonGeoDistanceType]
    field: NotRequired[FieldCommonField]
    origin: NotRequired[FieldCommonGeoLocation]
    ranges: NotRequired[list[AggregationsAggregationRange]]
    unit: NotRequired[FieldCommonDistanceUnit]


class AggregationsGeoHashGridAggregate(
    AggregationsMultiBucketAggregateBaseGeoHashGridBucket
):
    pass


class AggregationsGeoHashGridBucket(AggregationsMultiBucketBase):
    key: FieldCommonGeoHash


class AggregationsGeoTileGridAggregate(
    AggregationsMultiBucketAggregateBaseGeoTileGridBucket
):
    pass


class AggregationsGeoTileGridBucket(AggregationsMultiBucketBase):
    key: FieldCommonGeoTile


class AggregationsGlobalAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsHdrPercentileRanksAggregate(AggregationsPercentilesAggregateBase):
    pass


class AggregationsHdrPercentilesAggregate(AggregationsPercentilesAggregateBase):
    pass


class AggregationsHistogramAggregate(
    AggregationsMultiBucketAggregateBaseHistogramBucket
):
    pass


class AggregationsHistogramAggregationFields(TypedDict):
    extended_bounds: NotRequired[AggregationsExtendedBoundsDouble]
    hard_bounds: NotRequired[AggregationsExtendedBoundsDouble]
    field: NotRequired[FieldCommonField]
    interval: NotRequired[float]
    min_doc_count: NotRequired[int]
    missing: NotRequired[float]
    offset: NotRequired[float]
    order: NotRequired[AggregationsHistogramOrder]
    script: NotRequired[FieldCommonScript]
    format: NotRequired[str]
    keyed: NotRequired[bool]


class AggregationsHistogramBucket(AggregationsMultiBucketBase):
    key_as_string: NotRequired[str]
    key: float


class AggregationsHoltWintersModelSettings(TypedDict):
    alpha: NotRequired[float]
    beta: NotRequired[float]
    gamma: NotRequired[float]
    pad: NotRequired[bool]
    period: NotRequired[int]
    type: NotRequired[AggregationsHoltWintersType]


class AggregationsIpRangeAggregate(AggregationsMultiBucketAggregateBaseIpRangeBucket):
    pass


class AggregationsIpRangeAggregationFields(TypedDict):
    field: NotRequired[FieldCommonField]
    ranges: NotRequired[list[AggregationsIpRangeAggregationRange]]


AggregationsIpRangeBucket = TypedDict(
    "AggregationsIpRangeBucket",
    {
        "doc_count": int,
        "key": NotRequired[str],
        "from": NotRequired[str],
        "to": NotRequired[str],
    },
)


class AggregationsLongRareTermsAggregate(
    AggregationsMultiBucketAggregateBaseLongRareTermsBucket
):
    pass


class AggregationsLongRareTermsBucket(AggregationsMultiBucketBase):
    key: int
    key_as_string: NotRequired[str]


class AggregationsLongTermsBucket(AggregationsTermsBucketBase):
    key: AggregationsLongTermsBucketKey
    key_as_string: NotRequired[str]


class AggregationsMatrixStatsAggregate(AggregationsAggregateBase):
    doc_count: int
    fields: NotRequired[list[AggregationsMatrixStatsFields]]


class AggregationsMaxAggregate(AggregationsSingleMetricAggregateBase):
    pass


class AggregationsMedianAbsoluteDeviationAggregate(
    AggregationsSingleMetricAggregateBase
):
    pass


class AggregationsMetricAggregationBaseModel2(TypedDict):
    script: NotRequired[FieldCommonScript]


class AggregationsMetricAggregationBaseModel3(
    AggregationsMetricAggregationBaseModel2, AggregationsMetricAggregationBaseModel
):
    pass


AggregationsMetricAggregationBaseModel4: TypeAlias = (
    AggregationsMetricAggregationBaseModel1 | AggregationsMetricAggregationBaseModel3
)


class AggregationsMinAggregate(AggregationsSingleMetricAggregateBase):
    pass


class AggregationsMissingAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsMultiTermsAggregate(AggregationsTermsAggregateBaseMultiTermsBucket):
    pass


class AggregationsMultiTermsAggregationFields(TypedDict):
    collect_mode: NotRequired[AggregationsTermsAggregationCollectMode]
    order: NotRequired[AggregationsHistogramOrder]
    min_doc_count: NotRequired[int]
    shard_min_doc_count: NotRequired[int]
    shard_size: NotRequired[int]
    show_term_doc_count_error: NotRequired[bool]
    size: NotRequired[int]
    terms: list[AggregationsMultiTermLookup]


class AggregationsNestedAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsParentAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsPipelineAggregationBase(AggregationsBucketPathAggregation):
    format: NotRequired[str]
    gap_policy: NotRequired[AggregationsGapPolicy]


class AggregationsRangeAggregate(AggregationsRangeAggregateBase):
    pass


class AggregationsRangeAggregationFields(TypedDict):
    field: NotRequired[FieldCommonField]
    missing: NotRequired[int]
    ranges: NotRequired[list[AggregationsAggregationRange]]
    script: NotRequired[FieldCommonScript]
    keyed: NotRequired[bool]
    format: NotRequired[str]


class AggregationsReverseNestedAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsSamplerAggregate(AggregationsSingleBucketAggregateBase):
    pass


class AggregationsScriptedHeuristic(TypedDict):
    script: FieldCommonScript


class AggregationsScriptedMetricAggregation(TypedDict):
    combine_script: NotRequired[FieldCommonScript]
    init_script: NotRequired[FieldCommonScript]
    map_script: NotRequired[FieldCommonScript]
    params: NotRequired[dict[str, Any]]
    reduce_script: NotRequired[FieldCommonScript]


class AggregationsSerialDifferencingAggregation(AggregationsPipelineAggregationBase):
    lag: NotRequired[int]


class AggregationsSignificantLongTermsAggregate(
    AggregationsSignificantTermsAggregateBaseSignificantLongTermsBucket
):
    pass


class AggregationsSignificantLongTermsBucket(AggregationsSignificantTermsBucketBase):
    key: int
    key_as_string: NotRequired[str]


class AggregationsSignificantStringTermsAggregate(
    AggregationsSignificantTermsAggregateBaseSignificantStringTermsBucket
):
    pass


class AggregationsSignificantStringTermsBucket(AggregationsSignificantTermsBucketBase):
    key: str


class AggregationsSimpleValueAggregate(AggregationsSingleMetricAggregateBase):
    pass


class AggregationsStatsAggregate(AggregationsStatsAggregateBase):
    pass


class AggregationsStatsBucketAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsStringTermsBucket(AggregationsTermsBucketBase):
    key: str


class AggregationsSumBucketAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsTermsAggregateBaseDoubleTermsBucket(AggregationsTermsAggregateBase):
    buckets: list[AggregationsDoubleTermsBucket]


class AggregationsTermsAggregateBaseLongTermsBucket(AggregationsTermsAggregateBase):
    buckets: list[AggregationsLongTermsBucket]


class AggregationsTermsAggregateBaseStringTermsBucket(AggregationsTermsAggregateBase):
    buckets: list[AggregationsStringTermsBucket]


class AggregationsTermsAggregateBaseUnsignedLongTermsBucket(
    AggregationsTermsAggregateBase
):
    buckets: list[AggregationsUnsignedLongTermsBucket]


class AggregationsTermsAggregationFieldsModel(TypedDict):
    script: NotRequired[FieldCommonScript]


AggregationsTermsInclude: TypeAlias = str | list[str] | AggregationsTermsPartition


class AggregationsUnsignedLongTermsAggregate(
    AggregationsTermsAggregateBaseUnsignedLongTermsBucket
):
    pass


class AggregationsWeightedAverageValue(TypedDict):
    field: NotRequired[FieldCommonField]
    missing: NotRequired[float]
    script: NotRequired[FieldCommonScript]


class AnalysisAsciiFoldingTokenFilter(AnalysisTokenFilterBase):
    type: Literal["asciifolding"]
    preserve_original: NotRequired[FieldCommonStringifiedBoolean]


class AnalysisCharGroupTokenizer(AnalysisTokenizerBase):
    type: Literal["char_group"]
    tokenize_on_chars: list[str]
    max_token_length: NotRequired[int]


class AnalysisCjkAnalyzer(TypedDict):
    type: NotRequired[Literal["cjk"]]
    stopwords: NotRequired[AnalysisStopWords]
    stopwords_path: NotRequired[str]


class AnalysisCommonGramsTokenFilter(AnalysisTokenFilterBase):
    type: Literal["common_grams"]
    common_words: NotRequired[list[str]]
    common_words_path: NotRequired[str]
    ignore_case: NotRequired[bool]
    query_mode: NotRequired[bool]


class AnalysisCompoundWordTokenFilterBase(AnalysisTokenFilterBase):
    hyphenation_patterns_path: NotRequired[str]
    max_subword_size: NotRequired[int]
    min_subword_size: NotRequired[int]
    min_word_size: NotRequired[int]
    only_longest_match: NotRequired[bool]
    word_list: NotRequired[list[str]]
    word_list_path: NotRequired[str]


class AnalysisConditionTokenFilter(AnalysisTokenFilterBase):
    type: Literal["condition"]
    filter: list[str]
    script: FieldCommonScript


class AnalysisDelimitedPayloadTokenFilter(AnalysisTokenFilterBase):
    type: Literal["delimited_payload"]
    delimiter: NotRequired[str]
    encoding: NotRequired[AnalysisDelimitedPayloadEncoding]


class AnalysisDictionaryDecompounderTokenFilter(AnalysisCompoundWordTokenFilterBase):
    type: Literal["dictionary_decompounder"]


class AnalysisDutchAnalyzer(TypedDict):
    type: Literal["dutch"]
    stopwords: NotRequired[AnalysisStopWords]


class AnalysisEdgeNGramTokenFilter(AnalysisTokenFilterBase):
    type: Literal["edge_ngram"]
    max_gram: NotRequired[int]
    min_gram: NotRequired[int]
    side: NotRequired[AnalysisEdgeNGramSide]
    preserve_original: NotRequired[FieldCommonStringifiedBoolean]


class AnalysisEdgeNGramTokenizer(AnalysisTokenizerBase):
    type: Literal["edge_ngram"]
    custom_token_chars: NotRequired[str]
    max_gram: int
    min_gram: int
    token_chars: list[AnalysisTokenChar]


class AnalysisElisionTokenFilter(AnalysisTokenFilterBase):
    type: Literal["elision"]
    articles: NotRequired[list[str]]
    articles_path: NotRequired[str]
    articles_case: NotRequired[FieldCommonStringifiedBoolean]


class AnalysisFingerprintAnalyzer(TypedDict):
    type: Literal["fingerprint"]
    version: NotRequired[FieldCommonVersionString]
    max_output_size: int
    preserve_original: bool
    separator: str
    stopwords: NotRequired[AnalysisStopWords]
    stopwords_path: NotRequired[str]


class AnalysisFingerprintTokenFilter(AnalysisTokenFilterBase):
    type: Literal["fingerprint"]
    max_output_size: NotRequired[int]
    separator: NotRequired[str]


class AnalysisHunspellTokenFilter(AnalysisTokenFilterBase):
    type: Literal["hunspell"]
    dedup: NotRequired[bool]
    dictionary: NotRequired[str]
    locale: str
    longest_only: NotRequired[bool]


class AnalysisHyphenationDecompounderTokenFilter(AnalysisCompoundWordTokenFilterBase):
    type: Literal["hyphenation_decompounder"]


class AnalysisIcuAnalyzer(TypedDict):
    type: Literal["icu_analyzer"]
    method: AnalysisIcuNormalizationType
    mode: AnalysisIcuNormalizationMode


class AnalysisIcuCollationTokenFilter(AnalysisTokenFilterBase):
    type: Literal["icu_collation"]
    alternate: NotRequired[AnalysisIcuCollationAlternate]
    caseFirst: NotRequired[AnalysisIcuCollationCaseFirst]
    caseLevel: NotRequired[bool]
    country: NotRequired[str]
    decomposition: NotRequired[AnalysisIcuCollationDecomposition]
    hiraganaQuaternaryMode: NotRequired[bool]
    language: NotRequired[str]
    numeric: NotRequired[bool]
    rules: NotRequired[str]
    strength: NotRequired[AnalysisIcuCollationStrength]
    variableTop: NotRequired[str]
    variant: NotRequired[str]


class AnalysisIcuFoldingTokenFilter(AnalysisTokenFilterBase):
    type: Literal["icu_folding"]
    unicode_set_filter: str


class AnalysisIcuNormalizationCharFilter(AnalysisCharFilterBase):
    type: Literal["icu_normalizer"]
    mode: NotRequired[AnalysisIcuNormalizationMode]
    name: NotRequired[AnalysisIcuNormalizationType]


class AnalysisIcuNormalizationTokenFilter(AnalysisTokenFilterBase):
    type: Literal["icu_normalizer"]
    name: AnalysisIcuNormalizationType


class AnalysisIcuTokenizer(AnalysisTokenizerBase):
    type: Literal["icu_tokenizer"]
    rule_files: str


class AnalysisIcuTransformTokenFilter(AnalysisTokenFilterBase):
    type: Literal["icu_transform"]
    dir: NotRequired[AnalysisIcuTransformDirection]
    id: str


class AnalysisKeepTypesTokenFilter(AnalysisTokenFilterBase):
    type: Literal["keep_types"]
    mode: NotRequired[AnalysisKeepTypesMode]
    types: NotRequired[list[str]]


class AnalysisKeepWordsTokenFilter(AnalysisTokenFilterBase):
    type: Literal["keep"]
    keep_words: NotRequired[list[str]]
    keep_words_case: NotRequired[bool]
    keep_words_path: NotRequired[str]


class AnalysisKeywordMarkerTokenFilter(AnalysisTokenFilterBase):
    type: Literal["keyword_marker"]
    ignore_case: NotRequired[bool]
    keywords: NotRequired[list[str]]
    keywords_path: NotRequired[str]
    keywords_pattern: NotRequired[str]


class AnalysisKeywordTokenizer(AnalysisTokenizerBase):
    type: Literal["keyword"]
    buffer_size: int


class AnalysisKStemTokenFilter(AnalysisTokenFilterBase):
    type: Literal["kstem"]


class AnalysisKuromojiAnalyzer(TypedDict):
    type: Literal["kuromoji"]
    mode: AnalysisKuromojiTokenizationMode
    user_dictionary: NotRequired[str]


class AnalysisKuromojiPartOfSpeechTokenFilter(AnalysisTokenFilterBase):
    type: Literal["kuromoji_part_of_speech"]
    stoptags: list[str]


class AnalysisKuromojiReadingFormTokenFilter(AnalysisTokenFilterBase):
    type: Literal["kuromoji_readingform"]
    use_romaji: bool


class AnalysisKuromojiStemmerTokenFilter(AnalysisTokenFilterBase):
    type: Literal["kuromoji_stemmer"]
    minimum_length: int


class AnalysisKuromojiTokenizer(AnalysisTokenizerBase):
    type: Literal["kuromoji_tokenizer"]
    discard_punctuation: NotRequired[bool]
    mode: AnalysisKuromojiTokenizationMode
    nbest_cost: NotRequired[int]
    nbest_examples: NotRequired[str]
    user_dictionary: NotRequired[str]
    user_dictionary_rules: NotRequired[list[str]]
    discard_compound_token: NotRequired[bool]


class AnalysisLanguageAnalyzer(TypedDict):
    type: Literal["language"]
    version: NotRequired[FieldCommonVersionString]
    language: AnalysisLanguage
    stem_exclusion: list[str]
    stopwords: NotRequired[AnalysisStopWords]
    stopwords_path: NotRequired[str]


class AnalysisLengthTokenFilter(AnalysisTokenFilterBase):
    type: Literal["length"]
    max: NotRequired[int]
    min: NotRequired[int]


class AnalysisLetterTokenizer(AnalysisTokenizerBase):
    type: Literal["letter"]


class AnalysisLimitTokenCountTokenFilter(AnalysisTokenFilterBase):
    type: Literal["limit"]
    consume_all_tokens: NotRequired[bool]
    max_token_count: NotRequired[FieldCommonStringifiedInteger]


class AnalysisLowercaseTokenFilter(AnalysisTokenFilterBase):
    type: Literal["lowercase"]
    language: NotRequired[str]


class AnalysisLowercaseTokenizer(AnalysisTokenizerBase):
    type: Literal["lowercase"]


class AnalysisMultiplexerTokenFilter(AnalysisTokenFilterBase):
    type: Literal["multiplexer"]
    filters: list[str]
    preserve_original: NotRequired[FieldCommonStringifiedBoolean]


class AnalysisNGramTokenFilter(AnalysisTokenFilterBase):
    type: Literal["ngram"]
    max_gram: NotRequired[int]
    min_gram: NotRequired[int]
    preserve_original: NotRequired[FieldCommonStringifiedBoolean]


class AnalysisNGramTokenizer(AnalysisTokenizerBase):
    type: Literal["ngram"]
    custom_token_chars: NotRequired[str]
    max_gram: int
    min_gram: int
    token_chars: list[AnalysisTokenChar]


class AnalysisNoriAnalyzer(TypedDict):
    type: Literal["nori"]
    version: NotRequired[FieldCommonVersionString]
    decompound_mode: NotRequired[AnalysisNoriDecompoundMode]
    stoptags: NotRequired[list[str]]
    user_dictionary: NotRequired[str]


class AnalysisNoriPartOfSpeechTokenFilter(AnalysisTokenFilterBase):
    type: Literal["nori_part_of_speech"]
    stoptags: NotRequired[list[str]]


class AnalysisNoriTokenizer(AnalysisTokenizerBase):
    type: Literal["nori_tokenizer"]
    decompound_mode: NotRequired[AnalysisNoriDecompoundMode]
    discard_punctuation: NotRequired[bool]
    user_dictionary: NotRequired[str]
    user_dictionary_rules: NotRequired[list[str]]


class AnalysisPathHierarchyTokenizer(AnalysisTokenizerBase):
    type: Literal["path_hierarchy"]
    buffer_size: FieldCommonStringifiedInteger
    delimiter: str
    replacement: NotRequired[str]
    reverse: FieldCommonStringifiedBoolean
    skip: FieldCommonStringifiedInteger


class AnalysisPatternAnalyzer(TypedDict):
    type: Literal["pattern"]
    version: NotRequired[FieldCommonVersionString]
    flags: NotRequired[str]
    lowercase: NotRequired[bool]
    pattern: str
    stopwords: NotRequired[AnalysisStopWords]


class AnalysisPatternCaptureTokenFilter(AnalysisTokenFilterBase):
    type: Literal["pattern_capture"]
    patterns: list[str]
    preserve_original: NotRequired[FieldCommonStringifiedBoolean]


class AnalysisPatternReplaceTokenFilter(AnalysisTokenFilterBase):
    type: Literal["pattern_replace"]
    all: NotRequired[bool]
    flags: NotRequired[str]
    pattern: str
    replacement: NotRequired[str]


class AnalysisPatternTokenizer(AnalysisTokenizerBase):
    type: Literal["pattern"]
    flags: NotRequired[str]
    group: NotRequired[int]
    pattern: NotRequired[str]


class AnalysisPersianStemTokenFilter(AnalysisTokenFilterBase):
    type: Literal["persian_stem"]


class AnalysisPhoneAnalyzer(AnalysisPhoneAnalyzerBase):
    type: Literal["phone"]


class AnalysisPhoneticTokenFilter(AnalysisTokenFilterBase):
    type: Literal["phonetic"]
    encoder: AnalysisPhoneticEncoder
    languageset: list[AnalysisPhoneticLanguage]
    max_code_len: NotRequired[int]
    name_type: AnalysisPhoneticNameType
    replace: NotRequired[bool]
    rule_type: AnalysisPhoneticRuleType


class AnalysisPorterStemTokenFilter(AnalysisTokenFilterBase):
    type: Literal["porter_stem"]


class AnalysisPredicateTokenFilter(AnalysisTokenFilterBase):
    type: Literal["predicate_token_filter"]
    script: FieldCommonScript


class AnalysisRemoveDuplicatesTokenFilter(AnalysisTokenFilterBase):
    type: Literal["remove_duplicates"]


class AnalysisReverseTokenFilter(AnalysisTokenFilterBase):
    type: Literal["reverse"]


class AnalysisShingleTokenFilter(AnalysisTokenFilterBase):
    type: Literal["shingle"]
    filler_token: NotRequired[str]
    max_shingle_size: NotRequired[FieldCommonStringifiedInteger]
    min_shingle_size: NotRequired[FieldCommonStringifiedInteger]
    output_unigrams: NotRequired[bool]
    output_unigrams_if_no_shingles: NotRequired[bool]
    token_separator: NotRequired[str]


class AnalysisSimplePatternSplitTokenizer(AnalysisTokenizerBase):
    type: Literal["simple_pattern_split"]
    pattern: NotRequired[str]


class AnalysisSimplePatternTokenizer(AnalysisTokenizerBase):
    type: Literal["simple_pattern"]
    pattern: NotRequired[str]


class AnalysisSmartcnStopTokenFilter(AnalysisTokenFilterBase):
    type: Literal["smartcn_stop"]


class AnalysisSmartcnTokenizer(AnalysisTokenizerBase):
    type: Literal["smartcn_tokenizer"]


class AnalysisSnowballAnalyzer(TypedDict):
    type: Literal["snowball"]
    version: NotRequired[FieldCommonVersionString]
    language: AnalysisSnowballLanguage
    stopwords: NotRequired[AnalysisStopWords]


class AnalysisSnowballTokenFilter(AnalysisTokenFilterBase):
    type: Literal["snowball"]
    language: AnalysisSnowballLanguage


class AnalysisStandardAnalyzer(TypedDict):
    type: Literal["standard"]
    max_token_length: NotRequired[int]
    stopwords: NotRequired[AnalysisStopWords]


class AnalysisStandardTokenizer(AnalysisTokenizerBase):
    type: Literal["standard"]
    max_token_length: NotRequired[int]


class AnalysisStemmerOverrideTokenFilter(AnalysisTokenFilterBase):
    type: Literal["stemmer_override"]
    rules: NotRequired[list[str]]
    rules_path: NotRequired[str]


class AnalysisStemmerTokenFilter(AnalysisTokenFilterBase):
    type: Literal["stemmer"]
    language: NotRequired[str]


class AnalysisStopAnalyzer(TypedDict):
    type: Literal["stop"]
    version: NotRequired[FieldCommonVersionString]
    stopwords: NotRequired[AnalysisStopWords]
    stopwords_path: NotRequired[str]


class AnalysisStopTokenFilter(AnalysisTokenFilterBase):
    type: Literal["stop"]
    ignore_case: NotRequired[bool]
    remove_trailing: NotRequired[bool]
    stopwords: NotRequired[AnalysisStopWords]
    stopwords_path: NotRequired[str]


class AnalysisSynonymGraphTokenFilter(AnalysisTokenFilterBase):
    type: Literal["synonym_graph"]
    expand: NotRequired[bool]
    format: NotRequired[AnalysisSynonymFormat]
    lenient: NotRequired[bool]
    synonyms: NotRequired[list[str]]
    synonyms_path: NotRequired[str]
    tokenizer: NotRequired[str]
    updateable: NotRequired[bool]


class AnalysisSynonymTokenFilter(AnalysisTokenFilterBase):
    type: Literal["synonym"]
    expand: NotRequired[bool]
    format: NotRequired[AnalysisSynonymFormat]
    lenient: NotRequired[bool]
    synonyms: NotRequired[list[str]]
    synonyms_path: NotRequired[str]
    tokenizer: NotRequired[str]
    updateable: NotRequired[bool]


AnalysisTokenFilterDefinition: TypeAlias = (
    AnalysisAsciiFoldingTokenFilter
    | AnalysisCommonGramsTokenFilter
    | AnalysisConditionTokenFilter
    | AnalysisDelimitedPayloadTokenFilter
    | AnalysisEdgeNGramTokenFilter
    | AnalysisElisionTokenFilter
    | AnalysisFingerprintTokenFilter
    | AnalysisHunspellTokenFilter
    | AnalysisHyphenationDecompounderTokenFilter
    | AnalysisKeepTypesTokenFilter
    | AnalysisKeepWordsTokenFilter
    | AnalysisKeywordMarkerTokenFilter
    | AnalysisKStemTokenFilter
    | AnalysisLengthTokenFilter
    | AnalysisLimitTokenCountTokenFilter
    | AnalysisLowercaseTokenFilter
    | AnalysisMultiplexerTokenFilter
    | AnalysisNGramTokenFilter
    | AnalysisNoriPartOfSpeechTokenFilter
    | AnalysisPatternCaptureTokenFilter
    | AnalysisPatternReplaceTokenFilter
    | AnalysisPersianStemTokenFilter
    | AnalysisPorterStemTokenFilter
    | AnalysisPredicateTokenFilter
    | AnalysisRemoveDuplicatesTokenFilter
    | AnalysisReverseTokenFilter
    | AnalysisShingleTokenFilter
    | AnalysisSnowballTokenFilter
    | AnalysisStemmerOverrideTokenFilter
    | AnalysisStemmerTokenFilter
    | AnalysisStopTokenFilter
    | AnalysisSynonymGraphTokenFilter
    | AnalysisSynonymTokenFilter
    | AnalysisTrimTokenFilter
    | AnalysisTruncateTokenFilter
    | AnalysisUniqueTokenFilter
    | AnalysisUppercaseTokenFilter
    | AnalysisWordDelimiterGraphTokenFilter
    | AnalysisWordDelimiterTokenFilter
    | AnalysisKuromojiStemmerTokenFilter
    | AnalysisKuromojiReadingFormTokenFilter
    | AnalysisKuromojiPartOfSpeechTokenFilter
    | AnalysisIcuTokenizer
    | AnalysisIcuCollationTokenFilter
    | AnalysisIcuFoldingTokenFilter
    | AnalysisIcuNormalizationTokenFilter
    | AnalysisIcuTransformTokenFilter
    | AnalysisPhoneticTokenFilter
    | AnalysisDictionaryDecompounderTokenFilter
    | AnalysisSmartcnStopTokenFilter
)

AnalysisTokenizerDefinition: TypeAlias = (
    AnalysisCharGroupTokenizer
    | AnalysisEdgeNGramTokenizer
    | AnalysisKeywordTokenizer
    | AnalysisLetterTokenizer
    | AnalysisLowercaseTokenizer
    | AnalysisNGramTokenizer
    | AnalysisNoriTokenizer
    | AnalysisPathHierarchyTokenizer
    | AnalysisStandardTokenizer
    | AnalysisUaxEmailUrlTokenizer
    | AnalysisWhitespaceTokenizer
    | AnalysisKuromojiTokenizer
    | AnalysisPatternTokenizer
    | AnalysisSimplePatternTokenizer
    | AnalysisSimplePatternSplitTokenizer
    | AnalysisIcuTokenizer
    | AnalysisSmartcnTokenizer
)


class MappingSemanticProperty(TypedDict):
    type: Literal["semantic"]
    raw_field_type: NotRequired[str]
    model_id: str
    search_model_id: NotRequired[str]
    semantic_info_field_name: NotRequired[str]
    chunking: NotRequired[bool | list[MappingSemanticChunkingStrategy]]
    semantic_field_search_analyzer: NotRequired[str]
    dense_embedding_config: NotRequired[MappingSemanticDenseEmbeddingConfig]
    sparse_encoding_config: NotRequired[MappingSemanticSparseEncodingConfig]
    skip_existing_embedding: NotRequired[bool]


class QueryDslAgenticQuery(QueryDslQueryBase):
    query_text: str
    query_fields: NotRequired[list[FieldCommonField]]
    memory_id: NotRequired[str]


class QueryDslCombinedFieldsQuery(QueryDslQueryBase):
    fields: list[FieldCommonField]
    query: str
    auto_generate_synonyms_phrase_query: NotRequired[bool]
    operator: NotRequired[QueryDslCombinedFieldsOperator]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    zero_terms_query: NotRequired[QueryDslCombinedFieldsZeroTerms]


class QueryDslCommonTermsQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    cutoff_frequency: NotRequired[float]
    high_freq_operator: NotRequired[QueryDslOperator]
    low_freq_operator: NotRequired[QueryDslOperator]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    query: str


QueryDslCommonTermsQueryModel: TypeAlias = str | QueryDslCommonTermsQuery


class QueryDslDecayFunctionBase(TypedDict):
    multi_value_mode: NotRequired[QueryDslMultiValueMode]


class QueryDslDistanceFeatureQuery(QueryDslQueryBase):
    origin: FieldCommonGeoLocation
    pivot: FieldCommonDistance
    field: FieldCommonField


class QueryDslDistanceFeatureQueryModel(QueryDslQueryBase):
    origin: FieldCommonDateMath
    pivot: FieldCommonDuration
    field: FieldCommonField


QueryDslDistanceFeatureQueryModel1: TypeAlias = (
    QueryDslDistanceFeatureQuery | QueryDslDistanceFeatureQueryModel
)


class QueryDslExistsQuery(QueryDslQueryBase):
    field: FieldCommonField


class QueryDslFuzzyQuery(QueryDslQueryBase):
    max_expansions: NotRequired[int]
    prefix_length: NotRequired[int]
    rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    transpositions: NotRequired[bool]
    fuzziness: NotRequired[FieldCommonFuzziness]
    value: FieldCommonFieldValue


QueryDslFuzzyQueryModel: TypeAlias = FieldCommonFieldValue | QueryDslFuzzyQuery


class QueryDslGeoBoundingBoxQuery(QueryDslQueryBase):
    type: NotRequired[QueryDslGeoExecution]
    validation_method: NotRequired[QueryDslGeoValidationMethod]
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]


class QueryDslGeoDecayPlacement(TypedDict):
    decay: NotRequired[float]
    offset: NotRequired[FieldCommonDistance]
    origin: FieldCommonGeoLocation
    scale: FieldCommonDistance


class QueryDslGeoDistanceQuery(QueryDslQueryBase):
    distance: FieldCommonDistance
    distance_type: NotRequired[FieldCommonGeoDistanceType]
    validation_method: NotRequired[QueryDslGeoValidationMethod]
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]
    unit: NotRequired[FieldCommonDistanceUnit]


class QueryDslGeoPolygonPoints(TypedDict):
    points: list[FieldCommonGeoLocation]


class QueryDslGeoPolygonQuery(QueryDslQueryBase):
    validation_method: NotRequired[QueryDslGeoValidationMethod]
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]


class QueryDslGeoShapeQuery(QueryDslQueryBase):
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]


class QueryDslIdsQuery(QueryDslQueryBase):
    values: NotRequired[FieldCommonIds]


QueryDslKnnQueryRescore: TypeAlias = bool | QueryDslRescoreContext

QueryDslLike: TypeAlias = str | QueryDslLikeDocument


class QueryDslMatchAllQuery(QueryDslQueryBase):
    pass


class QueryDslMatchBoolPrefixQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    fuzziness: NotRequired[FieldCommonFuzziness]
    fuzzy_rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    fuzzy_transpositions: NotRequired[bool]
    max_expansions: NotRequired[int]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    operator: NotRequired[QueryDslOperator]
    prefix_length: NotRequired[int]
    query: str


QueryDslMatchBoolPrefixQueryModel: TypeAlias = str | QueryDslMatchBoolPrefixQuery


class QueryDslMatchNoneQuery(QueryDslQueryBase):
    pass


class QueryDslMatchPhrasePrefixQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    max_expansions: NotRequired[int]
    query: str
    slop: NotRequired[int]
    zero_terms_query: NotRequired[QueryDslZeroTermsQuery]


QueryDslMatchPhrasePrefixQueryModel: TypeAlias = str | QueryDslMatchPhrasePrefixQuery


class QueryDslMatchPhraseQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    query: str
    slop: NotRequired[int]
    zero_terms_query: NotRequired[QueryDslZeroTermsQuery]


QueryDslMatchPhraseQueryModel: TypeAlias = str | QueryDslMatchPhraseQuery


class QueryDslMatchQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    auto_generate_synonyms_phrase_query: NotRequired[bool]
    cutoff_frequency: NotRequired[float]
    fuzziness: NotRequired[FieldCommonFuzziness]
    fuzzy_rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    fuzzy_transpositions: NotRequired[bool]
    lenient: NotRequired[bool]
    max_expansions: NotRequired[int]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    operator: NotRequired[QueryDslOperator]
    prefix_length: NotRequired[int]
    query: FieldCommonFieldValue
    zero_terms_query: NotRequired[QueryDslZeroTermsQuery]


QueryDslMatchQueryModel: TypeAlias = FieldCommonFieldValue | QueryDslMatchQuery


class QueryDslMoreLikeThisQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    boost_terms: NotRequired[float]
    fail_on_unsupported_field: NotRequired[bool]
    fields: NotRequired[list[FieldCommonField]]
    include: NotRequired[bool]
    like: QueryDslLike | list[QueryDslLike]
    max_doc_freq: NotRequired[int]
    max_query_terms: NotRequired[int]
    max_word_length: NotRequired[int]
    min_doc_freq: NotRequired[int]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    min_term_freq: NotRequired[int]
    min_word_length: NotRequired[int]
    per_field_analyzer: NotRequired[dict[str, str]]
    routing: NotRequired[FieldCommonRouting]
    stop_words: NotRequired[AnalysisStopWords]
    unlike: NotRequired[QueryDslLike | list[QueryDslLike]]
    version: NotRequired[FieldCommonVersionNumber]
    version_type: NotRequired[FieldCommonVersionType]


class QueryDslMultiMatchQuery(QueryDslQueryBase):
    analyzer: NotRequired[str]
    auto_generate_synonyms_phrase_query: NotRequired[bool]
    cutoff_frequency: NotRequired[float]
    fields: NotRequired[FieldCommonFields]
    fuzziness: NotRequired[FieldCommonFuzziness]
    fuzzy_rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    fuzzy_transpositions: NotRequired[bool]
    lenient: NotRequired[bool]
    max_expansions: NotRequired[int]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    operator: NotRequired[QueryDslOperator]
    prefix_length: NotRequired[int]
    query: str
    slop: NotRequired[int]
    tie_breaker: NotRequired[float]
    type: NotRequired[QueryDslTextQueryType]
    zero_terms_query: NotRequired[QueryDslZeroTermsQuery]


class QueryDslParentIdQuery(QueryDslQueryBase):
    id: NotRequired[FieldCommonId]
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]
    type: NotRequired[FieldCommonRelationName]


class QueryDslPercolateQuery(QueryDslQueryBase):
    document: NotRequired[Any]
    documents: NotRequired[list[Any]]
    field: FieldCommonField
    id: NotRequired[FieldCommonId]
    index: NotRequired[FieldCommonIndexName]
    name: NotRequired[str]
    preference: NotRequired[str]
    routing: NotRequired[FieldCommonRouting]
    version: NotRequired[FieldCommonVersionNumber]


class QueryDslPrefixQuery(QueryDslQueryBase):
    rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    value: str
    case_insensitive: NotRequired[bool]


QueryDslPrefixQueryModel: TypeAlias = str | QueryDslPrefixQuery


class QueryDslQueryStringQuery(QueryDslQueryBase):
    allow_leading_wildcard: NotRequired[bool]
    analyzer: NotRequired[str]
    analyze_wildcard: NotRequired[bool]
    auto_generate_synonyms_phrase_query: NotRequired[bool]
    default_field: NotRequired[FieldCommonField]
    default_operator: NotRequired[QueryDslOperator]
    enable_position_increments: NotRequired[bool]
    escape: NotRequired[bool]
    fields: NotRequired[list[FieldCommonField]]
    fuzziness: NotRequired[FieldCommonFuzziness]
    fuzzy_max_expansions: NotRequired[int]
    fuzzy_prefix_length: NotRequired[int]
    fuzzy_rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    fuzzy_transpositions: NotRequired[bool]
    lenient: NotRequired[bool]
    max_determinized_states: NotRequired[int]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    phrase_slop: NotRequired[int]
    query: str
    quote_analyzer: NotRequired[str]
    quote_field_suffix: NotRequired[str]
    rewrite: NotRequired[FieldCommonMultiTermQueryRewrite]
    tie_breaker: NotRequired[float]
    time_zone: NotRequired[FieldCommonTimeZone]
    type: NotRequired[QueryDslTextQueryType]


class QueryDslRangeQueryBase(QueryDslQueryBase):
    relation: NotRequired[QueryDslRangeRelation]


class QueryDslScriptQuery(QueryDslQueryBase):
    script: FieldCommonScript


class QueryDslScriptScoreFunction(TypedDict):
    script: FieldCommonScript


class QueryDslTermsQuery(TypedDict):
    field_name: NotRequired[str]
    boost: NotRequired[float]
    value_type: NotRequired[QueryDslTermsQueryValueType]


class QueryDslTermsSetQuery(QueryDslQueryBase):
    minimum_should_match_field: NotRequired[FieldCommonField]
    minimum_should_match_script: NotRequired[FieldCommonScript]
    terms: list[str]


class AggregationsAggregationContainerModel4(TypedDict):
    serial_diff: AggregationsSerialDifferencingAggregation


class AggregationsAggregationContainerModel5(TypedDict):
    stats_bucket: AggregationsStatsBucketAggregation


class AggregationsAggregationContainerModel6(TypedDict):
    sum_bucket: AggregationsSumBucketAggregation


class AggregationsAutoDateHistogramAggregationFields(TypedDict):
    buckets: NotRequired[int]
    field: NotRequired[FieldCommonField]
    format: NotRequired[str]
    minimum_interval: NotRequired[AggregationsMinimumInterval]
    missing: NotRequired[FieldCommonDateTime]
    offset: NotRequired[str]
    params: NotRequired[dict[str, Any]]
    script: NotRequired[FieldCommonScript]
    time_zone: NotRequired[FieldCommonTimeZone]


class AggregationsAverageBucketAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsBoxplotAggregation(TypedDict):
    compression: NotRequired[float]


class AggregationsBucketScriptAggregation(AggregationsPipelineAggregationBase):
    script: NotRequired[FieldCommonScript]


class AggregationsBucketSelectorAggregation(AggregationsPipelineAggregationBase):
    script: NotRequired[FieldCommonScript]


class AggregationsCardinalityAggregation(TypedDict):
    precision_threshold: NotRequired[int]
    execution_hint: NotRequired[AggregationsCardinalityExecutionMode]


class AggregationsCompositeDateHistogramAggregationSource(
    AggregationsCompositeValuesSource
):
    format: NotRequired[str]
    calendar_interval: NotRequired[FieldCommonDurationLarge]
    fixed_interval: NotRequired[FieldCommonDurationLarge]
    offset: NotRequired[FieldCommonDuration]
    time_zone: NotRequired[FieldCommonTimeZone]


class AggregationsCompositeGeoTileGridAggregationSource(
    AggregationsCompositeValuesSource
):
    precision: NotRequired[int]
    bounds: NotRequired[FieldCommonGeoBounds]


class AggregationsCompositeHistogramAggregationSource(
    AggregationsCompositeValuesSource
):
    interval: float


class AggregationsCompositeTermsAggregationSource(AggregationsCompositeValuesSource):
    pass


class AggregationsCumulativeCardinalityAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsCumulativeSumAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsDateHistogramAggregationFields(TypedDict):
    calendar_interval: NotRequired[AggregationsCalendarInterval]
    extended_bounds: NotRequired[AggregationsExtendedBoundsFieldDateMath]
    hard_bounds: NotRequired[AggregationsExtendedBoundsFieldDateMath]
    field: NotRequired[FieldCommonField]
    fixed_interval: NotRequired[FieldCommonDuration]
    format: NotRequired[str]
    interval: NotRequired[FieldCommonDuration]
    min_doc_count: NotRequired[int]
    missing: NotRequired[FieldCommonDateTime]
    offset: NotRequired[FieldCommonDuration]
    order: NotRequired[AggregationsHistogramOrder]
    params: NotRequired[dict[str, Any]]
    script: NotRequired[FieldCommonScript]
    time_zone: NotRequired[FieldCommonTimeZone]
    keyed: NotRequired[bool]


class AggregationsDateRangeAggregationFields(TypedDict):
    field: NotRequired[FieldCommonField]
    format: NotRequired[str]
    missing: NotRequired[FieldCommonFieldValue]
    ranges: NotRequired[list[AggregationsDateRangeExpression]]
    time_zone: NotRequired[FieldCommonTimeZone]
    keyed: NotRequired[bool]


class AggregationsDerivativeAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsDoubleTermsAggregate(AggregationsTermsAggregateBaseDoubleTermsBucket):
    pass


class AggregationsExtendedStatsAggregate(AggregationsExtendedStatsAggregateBase):
    pass


class AggregationsExtendedStatsBucketAggregation(AggregationsPipelineAggregationBase):
    sigma: NotRequired[float]


class AggregationsFormatMetricAggregationBase(TypedDict):
    format: NotRequired[str]


class AggregationsFormattableMetricAggregation(TypedDict):
    format: NotRequired[str]


class AggregationsGeoBoundsAggregate(AggregationsAggregateBase):
    bounds: NotRequired[FieldCommonGeoBounds]


class AggregationsGeoBoundsAggregation(TypedDict):
    wrap_longitude: NotRequired[bool]


class AggregationsGeoCentroidAggregation(TypedDict):
    count: NotRequired[int]
    location: NotRequired[FieldCommonGeoLocation]


class AggregationsGeoHashGridAggregationFields(TypedDict):
    bounds: NotRequired[FieldCommonGeoBounds]
    field: NotRequired[FieldCommonField]
    precision: NotRequired[FieldCommonGeoHashPrecision]
    shard_size: NotRequired[int]
    size: NotRequired[int]


class AggregationsGeoTileGridAggregationFields(TypedDict):
    field: NotRequired[FieldCommonField]
    precision: NotRequired[FieldCommonGeoTilePrecision]
    shard_size: NotRequired[int]
    size: NotRequired[int]
    bounds: NotRequired[FieldCommonGeoBounds]


class AggregationsLongTermsAggregate(AggregationsTermsAggregateBaseLongTermsBucket):
    pass


class AggregationsMaxAggregation(AggregationsFormatMetricAggregationBase):
    value_type: NotRequired[AggregationsValueType]


class AggregationsMaxBucketAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsMedianAbsoluteDeviationAggregation(
    AggregationsFormatMetricAggregationBase
):
    compression: NotRequired[float]


class AggregationsMinAggregation(AggregationsFormatMetricAggregationBase):
    value_type: NotRequired[AggregationsValueType]


class AggregationsMinBucketAggregation(AggregationsPipelineAggregationBase):
    pass


class AggregationsMovingAverageAggregationBase(AggregationsPipelineAggregationBase):
    minimize: NotRequired[bool]
    predict: NotRequired[int]
    window: NotRequired[int]


class AggregationsMovingFunctionAggregation(AggregationsPipelineAggregationBase):
    script: NotRequired[str]
    shift: NotRequired[int]
    window: NotRequired[int]


class AggregationsMovingPercentilesAggregation(AggregationsPipelineAggregationBase):
    window: NotRequired[int]
    shift: NotRequired[int]
    keyed: NotRequired[bool]


class AggregationsNormalizeAggregation(AggregationsPipelineAggregationBase):
    method: NotRequired[AggregationsNormalizeMethod]


class AggregationsPercentileRanksAggregation(AggregationsFormatMetricAggregationBase):
    keyed: NotRequired[bool]
    values: NotRequired[list[float]]
    hdr: NotRequired[AggregationsHdrMethod]
    tdigest: NotRequired[AggregationsTDigest]


class AggregationsPercentilesAggregation(AggregationsFormatMetricAggregationBase):
    keyed: NotRequired[bool]
    percents: NotRequired[list[float]]
    hdr: NotRequired[AggregationsHdrMethod]
    tdigest: NotRequired[AggregationsTDigest]


class AggregationsPercentilesBucketAggregation(AggregationsPipelineAggregationBase):
    percents: NotRequired[list[float]]


class AggregationsRareTermsAggregationFields(TypedDict):
    exclude: NotRequired[AggregationsTermsExclude]
    field: NotRequired[FieldCommonField]
    include: NotRequired[AggregationsTermsInclude]
    max_doc_count: NotRequired[int]
    missing: NotRequired[FieldCommonFieldValue]
    precision: NotRequired[float]
    value_type: NotRequired[str]


class AggregationsRateAggregation(AggregationsFormatMetricAggregationBase):
    unit: NotRequired[AggregationsCalendarInterval]
    mode: NotRequired[AggregationsRateMode]


class AggregationsSimpleMovingAverageAggregation(
    AggregationsMovingAverageAggregationBase
):
    model: Literal["simple"]
    settings: FieldCommonEmptyObject


class AggregationsStatsAggregation(AggregationsFormatMetricAggregationBase):
    pass


class AggregationsStringTermsAggregate(AggregationsTermsAggregateBaseStringTermsBucket):
    pass


class AggregationsSumAggregation(AggregationsFormatMetricAggregationBase):
    pass


class AggregationsTermsAggregationFieldsModel1(TypedDict):
    collect_mode: NotRequired[AggregationsTermsAggregationCollectMode]
    exclude: NotRequired[AggregationsTermsExclude]
    execution_hint: NotRequired[AggregationsTermsAggregationExecutionHint]
    include: NotRequired[AggregationsTermsInclude]
    min_doc_count: NotRequired[int]
    missing: NotRequired[FieldCommonFieldValue]
    value_type: NotRequired[AggregationsValueType]
    order: NotRequired[AggregationsAggregateOrder]
    shard_size: NotRequired[int]
    shard_min_doc_count: NotRequired[int]
    show_term_doc_count_error: NotRequired[bool]
    size: NotRequired[int]
    format: NotRequired[str]


class AggregationsTermsAggregationFieldsModel2(
    AggregationsTermsAggregationFields, AggregationsTermsAggregationFieldsModel1
):
    pass


AggregationsTermsAggregationFieldsModel3: TypeAlias = (
    AggregationsTermsAggregationFieldsModel2
)


class AggregationsValueCountAggregation(AggregationsFormattableMetricAggregation):
    pass


class AggregationsWeightedAverageAggregation(TypedDict):
    format: NotRequired[str]
    value: NotRequired[AggregationsWeightedAverageValue]
    value_type: NotRequired[AggregationsValueType]
    weight: NotRequired[AggregationsWeightedAverageValue]


AnalysisAnalyzer: TypeAlias = (
    AnalysisCustomAnalyzer
    | AnalysisFingerprintAnalyzer
    | AnalysisKeywordAnalyzer
    | AnalysisLanguageAnalyzer
    | AnalysisNoriAnalyzer
    | AnalysisPatternAnalyzer
    | AnalysisSimpleAnalyzer
    | AnalysisStandardAnalyzer
    | AnalysisStopAnalyzer
    | AnalysisWhitespaceAnalyzer
    | AnalysisIcuAnalyzer
    | AnalysisKuromojiAnalyzer
    | AnalysisSnowballAnalyzer
    | AnalysisDutchAnalyzer
    | AnalysisSmartcnAnalyzer
    | AnalysisCjkAnalyzer
    | AnalysisPhoneAnalyzer
    | AnalysisPhoneSearchAnalyzer
)

AnalysisCharFilterDefinition: TypeAlias = (
    AnalysisHtmlStripCharFilter
    | AnalysisMappingCharFilter
    | AnalysisPatternReplaceCharFilter
    | AnalysisIcuNormalizationCharFilter
    | AnalysisKuromojiIterationMarkCharFilter
)

AnalysisTokenFilter: TypeAlias = str | AnalysisTokenFilterDefinition

AnalysisTokenizer: TypeAlias = str | AnalysisTokenizerDefinition


class QueryDslDateDecayPlacement(TypedDict):
    decay: NotRequired[float]
    offset: NotRequired[FieldCommonDuration]
    origin: NotRequired[FieldCommonDateTime]
    scale: FieldCommonDuration


QueryDslDateRangeQuery = TypedDict(
    "QueryDslDateRangeQuery",
    {
        "boost": NotRequired[float],
        "_name": NotRequired[str],
        "relation": NotRequired[QueryDslRangeRelation],
        "gt": NotRequired[FieldCommonDateMath],
        "gte": NotRequired[FieldCommonDateMath],
        "lt": NotRequired[FieldCommonDateMath],
        "lte": NotRequired[FieldCommonDateMath],
        "from": NotRequired[FieldCommonDateMath | None],
        "to": NotRequired[FieldCommonDateMath | None],
        "format": NotRequired[FieldCommonDateFormat],
        "time_zone": NotRequired[FieldCommonTimeZone],
        "include_lower": NotRequired[bool],
        "include_upper": NotRequired[bool],
    },
)


class QueryDslDecayFunction(QueryDslDecayFunctionBase):
    pass


QueryDslDecayPlacement: TypeAlias = (
    QueryDslDateDecayPlacement
    | QueryDslGeoDecayPlacement
    | QueryDslNumericDecayPlacement
)

QueryDslNumberRangeQuery = TypedDict(
    "QueryDslNumberRangeQuery",
    {
        "boost": NotRequired[float],
        "_name": NotRequired[str],
        "relation": NotRequired[QueryDslRangeRelation],
        "gt": NotRequired[float],
        "gte": NotRequired[float],
        "lt": NotRequired[float],
        "lte": NotRequired[float],
        "from": NotRequired[float | str | None],
        "to": NotRequired[float | str | None],
        "include_lower": NotRequired[bool],
        "include_upper": NotRequired[bool],
    },
)

QueryDslRangeQuery: TypeAlias = QueryDslNumberRangeQuery | QueryDslDateRangeQuery


class AggregationsAggregationContainerModel9(TypedDict):
    boxplot: AggregationsBoxplotAggregation


class AggregationsAggregationContainerModel10(TypedDict):
    bucket_script: AggregationsBucketScriptAggregation


class AggregationsAggregationContainerModel11(TypedDict):
    bucket_selector: AggregationsBucketSelectorAggregation


class AggregationsAggregationContainerModel12(TypedDict):
    cardinality: AggregationsCardinalityAggregation


class AggregationsAggregationContainerModel13(TypedDict):
    cumulative_cardinality: AggregationsCumulativeCardinalityAggregation


class AggregationsAggregationContainerModel14(TypedDict):
    cumulative_sum: AggregationsCumulativeSumAggregation


class AggregationsAggregationContainerModel15(TypedDict):
    derivative: AggregationsDerivativeAggregation


class AggregationsAggregationContainerModel16(TypedDict):
    extended_stats_bucket: AggregationsExtendedStatsBucketAggregation


class AggregationsAggregationContainerModel17(TypedDict):
    geo_bounds: AggregationsGeoBoundsAggregation


class AggregationsAggregationContainerModel18(TypedDict):
    geo_centroid: AggregationsGeoCentroidAggregation


class AggregationsAggregationContainerModel19(TypedDict):
    max: AggregationsMaxAggregation


class AggregationsAggregationContainerModel20(TypedDict):
    max_bucket: AggregationsMaxBucketAggregation


class AggregationsAggregationContainerModel21(TypedDict):
    median_absolute_deviation: AggregationsMedianAbsoluteDeviationAggregation


class AggregationsAggregationContainerModel22(TypedDict):
    min: AggregationsMinAggregation


class AggregationsAggregationContainerModel23(TypedDict):
    min_bucket: AggregationsMinBucketAggregation


class AggregationsAggregationContainerModel24(TypedDict):
    moving_percentiles: AggregationsMovingPercentilesAggregation


class AggregationsAggregationContainerModel25(TypedDict):
    moving_fn: AggregationsMovingFunctionAggregation


class AggregationsAggregationContainerModel26(TypedDict):
    normalize: AggregationsNormalizeAggregation


class AggregationsAggregationContainerModel27(TypedDict):
    percentile_ranks: AggregationsPercentileRanksAggregation


class AggregationsAggregationContainerModel28(TypedDict):
    percentiles: AggregationsPercentilesAggregation


class AggregationsAggregationContainerModel29(TypedDict):
    percentiles_bucket: AggregationsPercentilesBucketAggregation


class AggregationsAggregationContainerModel30(TypedDict):
    rate: AggregationsRateAggregation


class AggregationsAggregationContainerModel31(TypedDict):
    stats: AggregationsStatsAggregation


class AggregationsAggregationContainerModel32(TypedDict):
    sum: AggregationsSumAggregation


class AggregationsAggregationContainerModel33(TypedDict):
    value_count: AggregationsValueCountAggregation


class AggregationsAggregationContainerModel34(TypedDict):
    weighted_avg: AggregationsWeightedAverageAggregation


class AggregationsAverageAggregation(AggregationsFormatMetricAggregationBase):
    pass


class AggregationsCompositeAggregationSource(TypedDict):
    terms: NotRequired[AggregationsCompositeTermsAggregationSource]
    histogram: NotRequired[AggregationsCompositeHistogramAggregationSource]
    date_histogram: NotRequired[AggregationsCompositeDateHistogramAggregationSource]
    geotile_grid: NotRequired[AggregationsCompositeGeoTileGridAggregationSource]


class AggregationsEwmaMovingAverageAggregation(
    AggregationsMovingAverageAggregationBase
):
    model: Literal["ewma"]
    settings: AggregationsEwmaModelSettings


class AggregationsExtendedStatsAggregation(AggregationsFormatMetricAggregationBase):
    sigma: NotRequired[float]


class AggregationsHoltMovingAverageAggregation(
    AggregationsMovingAverageAggregationBase
):
    model: Literal["holt"]
    settings: AggregationsHoltLinearModelSettings


class AggregationsHoltWintersMovingAverageAggregation(
    AggregationsMovingAverageAggregationBase
):
    model: Literal["holt_winters"]
    settings: AggregationsHoltWintersModelSettings


class AggregationsLinearMovingAverageAggregation(
    AggregationsMovingAverageAggregationBase
):
    model: Literal["linear"]
    settings: FieldCommonEmptyObject


AggregationsMovingAverageAggregation: TypeAlias = (
    AggregationsLinearMovingAverageAggregation
    | AggregationsSimpleMovingAverageAggregation
    | AggregationsEwmaMovingAverageAggregation
    | AggregationsHoltMovingAverageAggregation
    | AggregationsHoltWintersMovingAverageAggregation
)

AnalysisCharFilter: TypeAlias = str | AnalysisCharFilterDefinition


class AggregationsAggregationContainerModel37(TypedDict):
    extended_stats: AggregationsExtendedStatsAggregation


class AggregationsAggregationContainerModel38(TypedDict):
    moving_avg: AggregationsMovingAverageAggregation


class AggregationsCompositeAggregationFields(TypedDict):
    after: NotRequired[AggregationsCompositeAggregateKey]
    size: NotRequired[int]
    sources: NotRequired[list[dict[str, AggregationsCompositeAggregationSource]]]


class AggregationsAdjacencyMatrixAggregationFields(TypedDict):
    filters: NotRequired[dict[str, QueryDslQueryContainer]]


AggregationsAggregate: TypeAlias = Union[
    AggregationsAdjacencyMatrixAggregate,
    AggregationsAutoDateHistogramAggregate,
    AggregationsAvgAggregate,
    AggregationsBoxPlotAggregate,
    AggregationsBucketMetricValueAggregate,
    AggregationsCardinalityAggregate,
    AggregationsChildrenAggregate,
    AggregationsCompositeAggregate,
    AggregationsDateHistogramAggregate,
    AggregationsDateRangeAggregate,
    AggregationsDerivativeAggregate,
    AggregationsDoubleTermsAggregate,
    AggregationsExtendedStatsAggregate,
    AggregationsExtendedStatsBucketAggregate,
    AggregationsFilterAggregate,
    AggregationsFiltersAggregate,
    AggregationsGeoBoundsAggregate,
    AggregationsGeoCentroidAggregate,
    AggregationsGeoDistanceAggregate,
    AggregationsGeoHashGridAggregate,
    AggregationsGeoTileGridAggregate,
    AggregationsGlobalAggregate,
    AggregationsHdrPercentilesAggregate,
    AggregationsHdrPercentileRanksAggregate,
    AggregationsHistogramAggregate,
    AggregationsIpRangeAggregate,
    AggregationsLongRareTermsAggregate,
    AggregationsLongTermsAggregate,
    AggregationsMatrixStatsAggregate,
    AggregationsMaxAggregate,
    AggregationsMedianAbsoluteDeviationAggregate,
    AggregationsMinAggregate,
    AggregationsMissingAggregate,
    AggregationsMultiTermsAggregate,
    AggregationsNestedAggregate,
    AggregationsParentAggregate,
    AggregationsPercentilesBucketAggregate,
    AggregationsRangeAggregate,
    AggregationsRateAggregate,
    AggregationsReverseNestedAggregate,
    AggregationsSamplerAggregate,
    AggregationsScriptedMetricAggregate,
    AggregationsSignificantLongTermsAggregate,
    AggregationsSignificantStringTermsAggregate,
    AggregationsCumulativeCardinalityAggregate,
    AggregationsSimpleValueAggregate,
    AggregationsStatsAggregate,
    AggregationsStatsBucketAggregate,
    AggregationsStringRareTermsAggregate,
    AggregationsStringTermsAggregate,
    AggregationsSumAggregate,
    AggregationsTDigestPercentilesAggregate,
    AggregationsTDigestPercentileRanksAggregate,
    AggregationsTTestAggregate,
    "AggregationsTopHitsAggregate",
    AggregationsUnsignedLongTermsAggregate,
    AggregationsUnmappedRareTermsAggregate,
    AggregationsUnmappedSignificantTermsAggregate,
    AggregationsUnmappedTermsAggregate,
    AggregationsValueCountAggregate,
    AggregationsVariableWidthHistogramAggregate,
    AggregationsWeightedAvgAggregate,
]


class AggregationsAggregationContainerModel40(TypedDict):
    bucket_sort: AggregationsBucketSortAggregation


class AggregationsAggregationContainerModel41(TypedDict):
    top_hits: AggregationsTopHitsAggregation


class AggregationsAggregationContainerModel42(TypedDict):
    t_test: AggregationsTTestAggregation


class AggregationsBucketAggregationBase(TypedDict):
    aggregations: NotRequired[dict[str, AggregationsAggregationContainerModel43]]
    aggs: NotRequired[dict[str, AggregationsAggregationContainerModel43]]


AggregationsBucketSortAggregation = TypedDict(
    "AggregationsBucketSortAggregation",
    {
        "from": NotRequired[int],
        "gap_policy": NotRequired[AggregationsGapPolicy],
        "size": NotRequired[int],
        "sort": NotRequired[FieldCommonSort],
    },
)


class AggregationsSignificantTermsAggregationFields(TypedDict):
    background_filter: NotRequired[QueryDslQueryContainer]
    chi_square: NotRequired[AggregationsChiSquareHeuristic]
    exclude: NotRequired[AggregationsTermsExclude]
    execution_hint: NotRequired[AggregationsTermsAggregationExecutionHint]
    field: NotRequired[FieldCommonField]
    gnd: NotRequired[AggregationsGoogleNormalizedDistanceHeuristic]
    include: NotRequired[AggregationsTermsInclude]
    jlh: NotRequired[FieldCommonEmptyObject]
    min_doc_count: NotRequired[int]
    mutual_information: NotRequired[AggregationsMutualInformationHeuristic]
    percentage: NotRequired[AggregationsPercentageScoreHeuristic]
    script_heuristic: NotRequired[AggregationsScriptedHeuristic]
    shard_min_doc_count: NotRequired[int]
    shard_size: NotRequired[int]
    size: NotRequired[int]


class AggregationsSignificantTextAggregationFields(TypedDict):
    background_filter: NotRequired[QueryDslQueryContainer]
    chi_square: NotRequired[AggregationsChiSquareHeuristic]
    exclude: NotRequired[AggregationsTermsExclude]
    execution_hint: NotRequired[AggregationsTermsAggregationExecutionHint]
    field: NotRequired[FieldCommonField]
    filter_duplicate_text: NotRequired[bool]
    gnd: NotRequired[AggregationsGoogleNormalizedDistanceHeuristic]
    include: NotRequired[AggregationsTermsInclude]
    jlh: NotRequired[FieldCommonEmptyObject]
    min_doc_count: NotRequired[int]
    mutual_information: NotRequired[AggregationsMutualInformationHeuristic]
    percentage: NotRequired[AggregationsPercentageScoreHeuristic]
    script_heuristic: NotRequired[AggregationsScriptedHeuristic]
    shard_min_doc_count: NotRequired[int]
    shard_size: NotRequired[int]
    size: NotRequired[int]
    source_fields: NotRequired[FieldCommonFields]


class AggregationsTestPopulation(TypedDict):
    field: FieldCommonField
    script: NotRequired[FieldCommonScript]
    filter: NotRequired[QueryDslQueryContainer]


class AggregationsTopHitsAggregate(AggregationsAggregateBase):
    hits: SearchHitsMetadataJsonValue


AggregationsTopHitsAggregation = TypedDict(
    "AggregationsTopHitsAggregation",
    {
        "docvalue_fields": NotRequired[FieldCommonFields],
        "explain": NotRequired[bool],
        "from": NotRequired[int],
        "highlight": NotRequired[SearchHighlight],
        "script_fields": NotRequired[dict[str, FieldCommonScriptField]],
        "size": NotRequired[int],
        "sort": NotRequired[FieldCommonSort],
        "_source": NotRequired[SearchSourceConfig],
        "stored_fields": NotRequired[FieldCommonFields],
        "track_scores": NotRequired[bool],
        "version": NotRequired[bool],
        "seq_no_primary_term": NotRequired[bool],
    },
)


class AggregationsTTestAggregation(TypedDict):
    a: NotRequired[AggregationsTestPopulation]
    b: NotRequired[AggregationsTestPopulation]
    type: NotRequired[AggregationsTTestType]


class MappingDynamicTemplate(TypedDict):
    mapping: NotRequired[MappingProperty]
    match: NotRequired[str]
    match_mapping_type: NotRequired[str]
    match_pattern: NotRequired[MappingMatchType]
    path_match: NotRequired[str]
    path_unmatch: NotRequired[str]
    unmatch: NotRequired[str]


class MappingFieldMapping(TypedDict):
    full_name: str
    mapping: dict[str, MappingProperty]


class MappingMatchOnlyTextProperty(TypedDict):
    type: Literal["match_only_text"]
    fields: NotRequired[dict[str, MappingProperty]]
    meta: NotRequired[dict[str, str]]
    copy_to: NotRequired[FieldCommonFields]


MappingProperty: TypeAlias = Union[
    "MappingBinaryProperty",
    "MappingBooleanProperty",
    "MappingJoinProperty",
    "MappingKeywordProperty",
    MappingMatchOnlyTextProperty,
    "MappingPercolatorProperty",
    "MappingRankFeatureProperty",
    "MappingRankFeaturesProperty",
    "MappingSearchAsYouTypeProperty",
    "MappingTextProperty",
    "MappingVersionProperty",
    "MappingWildcardProperty",
    "MappingDateNanosProperty",
    "MappingDateProperty",
    "MappingAggregateMetricDoubleProperty",
    "MappingFlatObjectProperty",
    "MappingNestedProperty",
    "MappingObjectProperty",
    "MappingCompletionProperty",
    "MappingConstantKeywordProperty",
    "MappingFieldAliasProperty",
    "MappingHistogramProperty",
    "MappingIpProperty",
    "MappingMurmur3HashProperty",
    "MappingTokenCountProperty",
    "MappingGeoPointProperty",
    "MappingGeoShapeProperty",
    "MappingXyPointProperty",
    "MappingXyShapeProperty",
    "MappingByteNumberProperty",
    "MappingDoubleNumberProperty",
    "MappingFloatNumberProperty",
    "MappingHalfFloatNumberProperty",
    "MappingIntegerNumberProperty",
    "MappingLongNumberProperty",
    "MappingScaledFloatNumberProperty",
    MappingSemanticProperty,
    "MappingShortNumberProperty",
    "MappingUnsignedLongNumberProperty",
    "MappingDateRangeProperty",
    "MappingDoubleRangeProperty",
    "MappingFloatRangeProperty",
    "MappingIntegerRangeProperty",
    "MappingIpRangeProperty",
    "MappingLongRangeProperty",
    "MappingKnnVectorProperty",
    "MappingIcuCollationKeywordProperty",
]


class MappingPropertyBase(TypedDict):
    meta: NotRequired[dict[str, str]]
    properties: NotRequired[dict[str, MappingProperty]]
    ignore_above: NotRequired[int]
    dynamic: NotRequired[MappingDynamicMapping]
    fields: NotRequired[dict[str, MappingProperty]]


class MappingTypeMapping(TypedDict):
    all_field: NotRequired[MappingAllField]
    date_detection: NotRequired[bool]
    dynamic: NotRequired[MappingDynamicMapping]
    dynamic_date_formats: NotRequired[list[str]]
    dynamic_templates: NotRequired[list[dict[str, MappingDynamicTemplate]]]
    field_field_names: NotRequired[MappingFieldNamesField]
    index_field: NotRequired[MappingIndexField]
    field_meta: NotRequired[FieldCommonMetadata]
    numeric_detection: NotRequired[bool]
    properties: NotRequired[dict[str, MappingProperty]]
    field_routing: NotRequired[MappingRoutingField]
    field_size: NotRequired[MappingSizeField]
    field_source: NotRequired[MappingSourceField]
    enabled: NotRequired[bool]
    field_data_stream_timestamp: NotRequired[MappingDataStreamTimestamp]


class QueryDslBoolQuery(QueryDslQueryBase):
    filter: NotRequired[QueryDslQueryContainer | list[QueryDslQueryContainer]]
    minimum_should_match: NotRequired[FieldCommonMinimumShouldMatch]
    must: NotRequired[QueryDslQueryContainer | list[QueryDslQueryContainer]]
    must_not: NotRequired[QueryDslQueryContainer | list[QueryDslQueryContainer]]
    should: NotRequired[QueryDslQueryContainer | list[QueryDslQueryContainer]]
    adjust_pure_negative: NotRequired[bool]


class QueryDslBoostingQuery(QueryDslQueryBase):
    negative_boost: float
    negative: QueryDslQueryContainer
    positive: QueryDslQueryContainer


class QueryDslConstantScoreQuery(QueryDslQueryBase):
    filter: QueryDslQueryContainer


class QueryDslDisMaxQuery(QueryDslQueryBase):
    queries: list[QueryDslQueryContainer]
    tie_breaker: NotRequired[float]


class QueryDslFunctionScoreContainer(TypedDict):
    filter: NotRequired[QueryDslQueryContainer]
    weight: NotRequired[float]
    exp: NotRequired[QueryDslDecayFunction]
    gauss: NotRequired[QueryDslDecayFunction]
    linear: NotRequired[QueryDslDecayFunction]
    field_value_factor: NotRequired[QueryDslFieldValueFactorScoreFunction]
    random_score: NotRequired[QueryDslRandomScoreFunction]
    script_score: NotRequired[QueryDslScriptScoreFunction]


class QueryDslFunctionScoreQuery(QueryDslQueryBase):
    boost_mode: NotRequired[QueryDslFunctionBoostMode]
    functions: NotRequired[list[QueryDslFunctionScoreContainer]]
    max_boost: NotRequired[float]
    min_score: NotRequired[float]
    query: NotRequired[QueryDslQueryContainer]
    score_mode: NotRequired[QueryDslFunctionScoreMode]


class QueryDslHasChildQuery(QueryDslQueryBase):
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]
    inner_hits: NotRequired[SearchInnerHits]
    max_children: NotRequired[int]
    min_children: NotRequired[int]
    query: QueryDslQueryContainer
    score_mode: NotRequired[QueryDslChildScoreMode]
    type: FieldCommonRelationName


class QueryDslHasParentQuery(QueryDslQueryBase):
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]
    inner_hits: NotRequired[SearchInnerHits]
    parent_type: FieldCommonRelationName
    query: QueryDslQueryContainer
    score: NotRequired[bool]


class QueryDslHybridQuery(QueryDslQueryBase):
    queries: NotRequired[list[QueryDslQueryContainer]]
    pagination_depth: NotRequired[int]
    filter: NotRequired[QueryDslQueryContainer]


class QueryDslIntervalsAllOf(TypedDict):
    intervals: list[QueryDslIntervalsContainer]
    max_gaps: NotRequired[int]
    ordered: NotRequired[bool]
    filter: NotRequired[QueryDslIntervalsFilter]


class QueryDslIntervalsAnyOf(TypedDict):
    intervals: list[QueryDslIntervalsContainer]
    filter: NotRequired[QueryDslIntervalsFilter]


class QueryDslIntervalsContainer(TypedDict):
    all_of: NotRequired[QueryDslIntervalsAllOf]
    any_of: NotRequired[QueryDslIntervalsAnyOf]
    fuzzy: NotRequired[QueryDslIntervalsFuzzy]
    match: NotRequired[QueryDslIntervalsMatch]
    prefix: NotRequired[QueryDslIntervalsPrefix]
    wildcard: NotRequired[QueryDslIntervalsWildcard]


class QueryDslIntervalsFilter(TypedDict):
    after: NotRequired[QueryDslIntervalsContainer]
    before: NotRequired[QueryDslIntervalsContainer]
    contained_by: NotRequired[QueryDslIntervalsContainer]
    containing: NotRequired[QueryDslIntervalsContainer]
    not_contained_by: NotRequired[QueryDslIntervalsContainer]
    not_containing: NotRequired[QueryDslIntervalsContainer]
    not_overlapping: NotRequired[QueryDslIntervalsContainer]
    overlapping: NotRequired[QueryDslIntervalsContainer]
    script: NotRequired[FieldCommonScript]


class QueryDslIntervalsMatch(TypedDict):
    analyzer: NotRequired[str]
    max_gaps: NotRequired[int]
    ordered: NotRequired[bool]
    query: str
    use_field: NotRequired[FieldCommonField]
    filter: NotRequired[QueryDslIntervalsFilter]


class QueryDslIntervalsQuery(QueryDslQueryBase):
    all_of: NotRequired[QueryDslIntervalsAllOf]
    any_of: NotRequired[QueryDslIntervalsAnyOf]
    fuzzy: NotRequired[QueryDslIntervalsFuzzy]
    match: NotRequired[QueryDslIntervalsMatch]
    prefix: NotRequired[QueryDslIntervalsPrefix]
    wildcard: NotRequired[QueryDslIntervalsWildcard]


class QueryDslKnnQuery(QueryDslQueryBase):
    vector: QueryDslQueryVector
    k: NotRequired[int]
    min_score: NotRequired[float]
    max_distance: NotRequired[float]
    filter: NotRequired[QueryDslQueryContainer]
    method_parameters: NotRequired[dict[str, Any]]
    rescore: NotRequired[QueryDslKnnQueryRescore]
    expand_nested_docs: NotRequired[bool]


class QueryDslNestedQuery(QueryDslQueryBase):
    ignore_unmapped: NotRequired[QueryDslIgnoreUnmapped]
    inner_hits: NotRequired[SearchInnerHits]
    path: FieldCommonField
    query: QueryDslQueryContainer
    score_mode: NotRequired[QueryDslChildScoreMode]


class QueryDslNeuralQuery(QueryDslQueryBase):
    query_text: NotRequired[str]
    query_image: NotRequired[str]
    model_id: NotRequired[str]
    k: NotRequired[int]
    min_score: NotRequired[float]
    max_distance: NotRequired[float]
    filter: NotRequired[QueryDslQueryContainer]


class QueryDslScriptScoreQuery(QueryDslQueryBase):
    min_score: NotRequired[float]
    query: QueryDslQueryContainer
    script: FieldCommonScript


class QueryDslSpanContainingQuery(QueryDslQueryBase):
    big: QueryDslSpanQuery
    little: QueryDslSpanQuery


class QueryDslSpanFieldMaskingQuery(QueryDslQueryBase):
    field: FieldCommonField
    query: QueryDslSpanQuery


class QueryDslSpanFirstQuery(QueryDslQueryBase):
    end: int
    match: QueryDslSpanQuery


class QueryDslSpanMultiTermQuery(QueryDslQueryBase):
    match: QueryDslQueryContainer


class QueryDslSpanNearQuery(QueryDslQueryBase):
    clauses: list[QueryDslSpanQuery]
    in_order: NotRequired[bool]
    slop: NotRequired[int]


class QueryDslSpanNotQuery(QueryDslQueryBase):
    dist: NotRequired[int]
    exclude: QueryDslSpanQuery
    include: QueryDslSpanQuery
    post: NotRequired[int]
    pre: NotRequired[int]


class QueryDslSpanOrQuery(QueryDslQueryBase):
    clauses: list[QueryDslSpanQuery]


class QueryDslSpanQuery(TypedDict):
    span_containing: NotRequired[QueryDslSpanContainingQuery]
    field_masking_span: NotRequired[QueryDslSpanFieldMaskingQuery]
    span_first: NotRequired[QueryDslSpanFirstQuery]
    span_gap: NotRequired[QueryDslSpanGapQuery]
    span_multi: NotRequired[QueryDslSpanMultiTermQuery]
    span_near: NotRequired[QueryDslSpanNearQuery]
    span_not: NotRequired[QueryDslSpanNotQuery]
    span_or: NotRequired[QueryDslSpanOrQuery]
    span_term: NotRequired[dict[str, QueryDslSpanTermQueryModel]]
    span_within: NotRequired[QueryDslSpanWithinQuery]


class QueryDslSpanWithinQuery(QueryDslQueryBase):
    big: QueryDslSpanQuery
    little: QueryDslSpanQuery


class AggregationsAggregationContainerModel44(
    AggregationsAggregationContainerModel40, AggregationsAggregationContainer
):
    pass


class AggregationsAdjacencyMatrixAggregation(AggregationsBucketAggregationBase):
    adjacency_matrix: AggregationsAdjacencyMatrixAggregationFields


class AggregationsAutoDateHistogramAggregation(AggregationsBucketAggregationBase):
    auto_date_histogram: AggregationsAutoDateHistogramAggregationFields


class AggregationsChildrenAggregation(AggregationsBucketAggregationBase):
    children: AggregationsChildrenAggregationFields


class AggregationsCompositeAggregation(AggregationsBucketAggregationBase):
    composite: AggregationsCompositeAggregationFields


class AggregationsDateHistogramAggregation(AggregationsBucketAggregationBase):
    date_histogram: AggregationsDateHistogramAggregationFields


class AggregationsDateRangeAggregation(AggregationsBucketAggregationBase):
    date_range: AggregationsDateRangeAggregationFields


class AggregationsDiversifiedSamplerAggregation(AggregationsBucketAggregationBase):
    diversified_sampler: AggregationsDiversifiedSamplerAggregationFields


class AggregationsFilterAggregation(AggregationsBucketAggregationBase):
    filter: AggregationsFilterAggregationFields


class AggregationsFiltersAggregation(AggregationsBucketAggregationBase):
    filters: AggregationsFiltersAggregationFields


class AggregationsGeoDistanceAggregation(AggregationsBucketAggregationBase):
    geo_distance: AggregationsGeoDistanceAggregationFields


class AggregationsGeoHashGridAggregation(AggregationsBucketAggregationBase):
    geohash_grid: AggregationsGeoHashGridAggregationFields


class AggregationsGeoTileGridAggregation(AggregationsBucketAggregationBase):
    geotile_grid: AggregationsGeoTileGridAggregationFields


AggregationsGlobalAggregation = TypedDict(
    "AggregationsGlobalAggregation",
    {
        "aggregations": NotRequired[dict[str, AggregationsAggregationContainerModel43]],
        "aggs": NotRequired[dict[str, AggregationsAggregationContainerModel43]],
        "global": AggregationsGlobalAggregationFields,
    },
)


class AggregationsHistogramAggregation(AggregationsBucketAggregationBase):
    histogram: AggregationsHistogramAggregationFields


class AggregationsIpRangeAggregation(AggregationsBucketAggregationBase):
    ip_range: AggregationsIpRangeAggregationFields


class AggregationsMissingAggregation(AggregationsBucketAggregationBase):
    missing: AggregationsMissingAggregationFields


class AggregationsMultiTermsAggregation(AggregationsBucketAggregationBase):
    multi_terms: AggregationsMultiTermsAggregationFields


class AggregationsNestedAggregation(AggregationsBucketAggregationBase):
    nested: AggregationsNestedAggregationFields


class AggregationsParentAggregation(AggregationsBucketAggregationBase):
    parent: AggregationsParentAggregationFields


class AggregationsRangeAggregation(AggregationsBucketAggregationBase):
    range: AggregationsRangeAggregationFields


class AggregationsRareTermsAggregation(AggregationsBucketAggregationBase):
    rare_terms: AggregationsRareTermsAggregationFields


class AggregationsReverseNestedAggregation(AggregationsBucketAggregationBase):
    reverse_nested: AggregationsReverseNestedAggregationFields


class AggregationsSamplerAggregation(AggregationsBucketAggregationBase):
    sampler: AggregationsSamplerAggregationFields


class AggregationsSignificantTermsAggregation(AggregationsBucketAggregationBase):
    significant_terms: AggregationsSignificantTermsAggregationFields


class AggregationsSignificantTextAggregation(AggregationsBucketAggregationBase):
    significant_text: AggregationsSignificantTextAggregationFields


class AggregationsTermsAggregation(AggregationsBucketAggregationBase):
    terms: AggregationsTermsAggregationFieldsModel3


class MappingAggregateMetricDoubleProperty(MappingPropertyBase):
    type: Literal["aggregate_metric_double"]
    default_metric: str
    metrics: list[str]


class MappingConstantKeywordProperty(MappingPropertyBase):
    value: NotRequired[Any]
    type: Literal["constant_keyword"]


class MappingCorePropertyBase(MappingPropertyBase):
    copy_to: NotRequired[FieldCommonFields]
    similarity: NotRequired[str]
    store: NotRequired[bool]


class MappingFieldAliasProperty(MappingPropertyBase):
    path: NotRequired[FieldCommonField]
    type: Literal["alias"]


class MappingFlatObjectProperty(MappingPropertyBase):
    searchable: NotRequired[bool]
    aggregatable: NotRequired[bool]
    type: Literal["flat_object"]


class MappingHistogramProperty(MappingPropertyBase):
    ignore_malformed: NotRequired[bool]
    type: Literal["histogram"]


class MappingJoinProperty(MappingPropertyBase):
    relations: NotRequired[
        dict[str, FieldCommonRelationName | list[FieldCommonRelationName]]
    ]
    eager_global_ordinals: NotRequired[bool]
    type: Literal["join"]


class MappingPercolatorProperty(MappingPropertyBase):
    type: Literal["percolator"]


class MappingRankFeatureProperty(MappingPropertyBase):
    positive_score_impact: NotRequired[bool]
    type: Literal["rank_feature"]


class MappingRankFeaturesProperty(MappingPropertyBase):
    type: Literal["rank_features"]


class AggregationsFilterAggregationFields(QueryDslQueryContainer):
    pass


class AggregationsAggregationContainerModel45(
    AggregationsAdjacencyMatrixAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel46(
    AggregationsAutoDateHistogramAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel47(
    AggregationsChildrenAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel48(
    AggregationsCompositeAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel49(
    AggregationsDateHistogramAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel50(
    AggregationsDateRangeAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel51(
    AggregationsDiversifiedSamplerAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel52(
    AggregationsFilterAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel53(
    AggregationsFiltersAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel54(
    AggregationsGeoDistanceAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel55(
    AggregationsGeoHashGridAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel56(
    AggregationsGeoTileGridAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel57(
    AggregationsGlobalAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel58(
    AggregationsHistogramAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel59(
    AggregationsIpRangeAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel60(
    AggregationsMissingAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel61(
    AggregationsMultiTermsAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel62(
    AggregationsNestedAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel63(
    AggregationsParentAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel64(
    AggregationsRangeAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel65(
    AggregationsRareTermsAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel66(
    AggregationsReverseNestedAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel67(
    AggregationsSamplerAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel68(
    AggregationsSignificantTermsAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel69(
    AggregationsSignificantTextAggregation, AggregationsAggregationContainer
):
    pass


class AggregationsAggregationContainerModel70(
    AggregationsTermsAggregation, AggregationsAggregationContainer
):
    pass


class MappingDocValuesPropertyBase(MappingCorePropertyBase):
    doc_values: NotRequired[bool]


class MappingNestedProperty(MappingCorePropertyBase):
    enabled: NotRequired[bool]
    include_in_parent: NotRequired[bool]
    include_in_root: NotRequired[bool]
    type: Literal["nested"]


class MappingObjectProperty(MappingCorePropertyBase):
    enabled: NotRequired[bool]
    type: NotRequired[Literal["object"]]


class MappingSearchAsYouTypeProperty(MappingCorePropertyBase):
    analyzer: NotRequired[str]
    index: NotRequired[bool]
    index_options: NotRequired[MappingIndexOptions]
    max_shingle_size: NotRequired[int]
    norms: NotRequired[bool]
    search_analyzer: NotRequired[str]
    search_quote_analyzer: NotRequired[str]
    term_vector: NotRequired[MappingTermVectorOption]
    type: Literal["search_as_you_type"]


class MappingTextProperty(MappingCorePropertyBase):
    analyzer: NotRequired[str]
    boost: NotRequired[float]
    eager_global_ordinals: NotRequired[bool]
    fielddata: NotRequired[bool]
    fielddata_frequency_filter: NotRequired[FieldCommonFielddataFrequencyFilter]
    index: NotRequired[bool]
    index_options: NotRequired[MappingIndexOptions]
    index_phrases: NotRequired[bool]
    index_prefixes: NotRequired[MappingTextIndexPrefixes]
    norms: NotRequired[bool]
    position_increment_gap: NotRequired[int]
    search_analyzer: NotRequired[str]
    search_quote_analyzer: NotRequired[str]
    term_vector: NotRequired[MappingTermVectorOption]
    type: Literal["text"]


class MappingBinaryProperty(MappingDocValuesPropertyBase):
    type: Literal["binary"]


class MappingBooleanProperty(MappingDocValuesPropertyBase):
    boost: NotRequired[float]
    fielddata: NotRequired[FieldCommonNumericFielddata]
    index: NotRequired[bool]
    null_value: NotRequired[bool]
    type: Literal["boolean"]


class MappingCompletionProperty(MappingDocValuesPropertyBase):
    analyzer: NotRequired[str]
    contexts: NotRequired[list[MappingSuggestContext]]
    max_input_length: NotRequired[int]
    preserve_position_increments: NotRequired[bool]
    preserve_separators: NotRequired[bool]
    search_analyzer: NotRequired[str]
    type: Literal["completion"]


class MappingDateNanosProperty(MappingDocValuesPropertyBase):
    boost: NotRequired[float]
    format: NotRequired[str]
    ignore_malformed: NotRequired[bool]
    index: NotRequired[bool]
    null_value: NotRequired[FieldCommonDateTime]
    precision_step: NotRequired[int]
    type: Literal["date_nanos"]


class MappingDateProperty(MappingDocValuesPropertyBase):
    boost: NotRequired[float]
    fielddata: NotRequired[FieldCommonNumericFielddata]
    format: NotRequired[str]
    ignore_malformed: NotRequired[bool]
    index: NotRequired[bool]
    null_value: NotRequired[FieldCommonDateTime]
    precision_step: NotRequired[int]
    locale: NotRequired[str]
    type: Literal["date"]


class MappingGeoPointProperty(MappingDocValuesPropertyBase):
    ignore_malformed: NotRequired[bool]
    ignore_z_value: NotRequired[bool]
    null_value: NotRequired[FieldCommonGeoLocation]
    type: Literal["geo_point"]


class MappingGeoShapeProperty(MappingDocValuesPropertyBase):
    coerce: NotRequired[bool]
    ignore_malformed: NotRequired[bool]
    ignore_z_value: NotRequired[bool]
    orientation: NotRequired[MappingGeoOrientation]
    strategy: NotRequired[MappingGeoStrategy]
    distance_error_pct: NotRequired[float]
    type: Literal["geo_shape"]


class MappingIcuCollationKeywordProperty(MappingDocValuesPropertyBase):
    type: Literal["icu_collation_keyword"]
    index: NotRequired[bool]
    null_value: NotRequired[str]
    alternate: NotRequired[AnalysisIcuCollationAlternate]
    case_level: NotRequired[bool]
    case_first: NotRequired[AnalysisIcuCollationCaseFirst]
    decomposition: NotRequired[AnalysisIcuCollationDecomposition]
    hiragana_quaternary_mode: NotRequired[bool]
    numeric: NotRequired[bool]
    strength: NotRequired[AnalysisIcuCollationStrength]
    variable_top: NotRequired[str]
    country: NotRequired[str]
    language: NotRequired[str]
    variant: NotRequired[str]


class MappingIpProperty(MappingDocValuesPropertyBase):
    boost: NotRequired[float]
    index: NotRequired[bool]
    ignore_malformed: NotRequired[bool]
    null_value: NotRequired[str]
    type: Literal["ip"]


class MappingKeywordProperty(MappingDocValuesPropertyBase):
    boost: NotRequired[float]
    eager_global_ordinals: NotRequired[bool]
    index: NotRequired[bool]
    index_options: NotRequired[MappingIndexOptions]
    normalizer: NotRequired[str]
    norms: NotRequired[bool]
    null_value: NotRequired[str]
    split_queries_on_whitespace: NotRequired[bool]
    type: Literal["keyword"]


class MappingKnnVectorProperty(MappingDocValuesPropertyBase):
    type: Literal["knn_vector"]
    dimension: int
    space_type: NotRequired[str]
    data_type: NotRequired[str]
    mode: NotRequired[str]
    compression_level: NotRequired[str]
    method: NotRequired[MappingKnnVectorMethod]
    model_id: NotRequired[str]


class MappingMurmur3HashProperty(MappingDocValuesPropertyBase):
    type: Literal["murmur3"]


class MappingNumberPropertyBase(MappingDocValuesPropertyBase):
    boost: NotRequired[float]
    coerce: NotRequired[bool]
    ignore_malformed: NotRequired[bool]
    index: NotRequired[bool]


class MappingRangePropertyBase(MappingDocValuesPropertyBase):
    boost: NotRequired[float]
    coerce: NotRequired[bool]
    index: NotRequired[bool]


class MappingTokenCountProperty(MappingDocValuesPropertyBase):
    analyzer: NotRequired[str]
    boost: NotRequired[float]
    index: NotRequired[bool]
    null_value: NotRequired[float]
    enable_position_increments: NotRequired[bool]
    type: Literal["token_count"]


class MappingVersionProperty(MappingDocValuesPropertyBase):
    type: Literal["version"]


class MappingWildcardProperty(MappingDocValuesPropertyBase):
    type: Literal["wildcard"]
    null_value: NotRequired[str]
    normalizer: NotRequired[str]


class MappingXyPointProperty(MappingDocValuesPropertyBase):
    ignore_malformed: NotRequired[bool]
    ignore_z_value: NotRequired[bool]
    null_value: NotRequired[FieldCommonXyLocation]
    type: Literal["xy_point"]


class MappingXyShapeProperty(MappingDocValuesPropertyBase):
    coerce: NotRequired[bool]
    ignore_malformed: NotRequired[bool]
    ignore_z_value: NotRequired[bool]
    orientation: NotRequired[MappingGeoOrientation]
    type: Literal["xy_shape"]


class MappingByteNumberProperty(MappingNumberPropertyBase):
    type: Literal["byte"]
    null_value: NotRequired[FieldCommonByte]


class MappingDoubleNumberProperty(MappingNumberPropertyBase):
    type: Literal["double"]
    null_value: NotRequired[float]


class MappingFloatNumberProperty(MappingNumberPropertyBase):
    type: Literal["float"]
    null_value: NotRequired[float]


class MappingHalfFloatNumberProperty(MappingNumberPropertyBase):
    type: Literal["half_float"]
    null_value: NotRequired[float]


class MappingIntegerNumberProperty(MappingNumberPropertyBase):
    type: Literal["integer"]
    null_value: NotRequired[int]


class MappingLongNumberProperty(MappingNumberPropertyBase):
    type: Literal["long"]
    null_value: NotRequired[int]


class MappingScaledFloatNumberProperty(MappingNumberPropertyBase):
    type: Literal["scaled_float"]
    null_value: NotRequired[float]
    scaling_factor: NotRequired[float]


class MappingShortNumberProperty(MappingNumberPropertyBase):
    type: Literal["short"]
    null_value: NotRequired[FieldCommonShort]


class MappingUnsignedLongNumberProperty(MappingNumberPropertyBase):
    type: Literal["unsigned_long"]
    null_value: NotRequired[FieldCommonUlong]


class MappingDateRangeProperty(MappingRangePropertyBase):
    format: NotRequired[str]
    type: Literal["date_range"]


class MappingDoubleRangeProperty(MappingRangePropertyBase):
    type: Literal["double_range"]


class MappingFloatRangeProperty(MappingRangePropertyBase):
    type: Literal["float_range"]


class MappingIntegerRangeProperty(MappingRangePropertyBase):
    type: Literal["integer_range"]


class MappingIpRangeProperty(MappingRangePropertyBase):
    type: Literal["ip_range"]


class MappingLongRangeProperty(MappingRangePropertyBase):
    type: Literal["long_range"]


class BulkOperationBase(TypedDict):
    field_id: NotRequired[FieldCommonId]
    field_index: NotRequired[FieldCommonIndexName]
    routing: NotRequired[FieldCommonRouting]


class BulkUpdateOperation(BulkOperationBase):
    if_primary_term: NotRequired[int]
    if_seq_no: NotRequired[FieldCommonSequenceNumber]
    require_alias: NotRequired[bool]
    retry_on_conflict: NotRequired[int]


class BulkWriteOperation(BulkOperationBase):
    pipeline: NotRequired[str]
    require_alias: NotRequired[bool]


class ExplainExplanation(TypedDict):
    description: str
    details: NotRequired[list[ExplainExplanation]]
    value: float


class FieldCapsFieldCapability(TypedDict):
    aggregatable: bool
    indices: NotRequired[FieldCommonIndices]
    meta: NotRequired[dict[str, list[str]]]
    non_aggregatable_indices: NotRequired[FieldCommonIndices]
    non_searchable_indices: NotRequired[FieldCommonIndices]
    searchable: bool
    type: str
    metadata_field: NotRequired[bool]


class GetScriptContextContextMethodParam(TypedDict):
    name: FieldCommonName
    type: str


class GetScriptLanguagesLanguageContext(TypedDict):
    contexts: list[str]
    language: FieldCommonScriptLanguage


class GetGetResultBase(TypedDict):
    field_type: NotRequired[FieldCommonType]
    field_index: FieldCommonIndexName
    fields: NotRequired[dict[str, Any]]
    found: bool
    field_id: FieldCommonId
    field_primary_term: NotRequired[int]
    field_routing: NotRequired[str]
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_source: NotRequired[FieldCommonTDocument]
    field_version: NotRequired[FieldCommonVersionNumber]


class MsearchTemplateTemplateConfig(TypedDict):
    explain: NotRequired[bool]
    id: NotRequired[FieldCommonId]
    params: NotRequired[dict[str, str | dict[str, Any]]]
    profile: NotRequired[bool]
    source: NotRequired[str]


class MsearchMultisearchHeader(TypedDict):
    allow_no_indices: NotRequired[bool]
    expand_wildcards: NotRequired[FieldCommonExpandWildcards]
    ignore_unavailable: NotRequired[bool]
    index: NotRequired[FieldCommonIndices]
    preference: NotRequired[str]
    request_cache: NotRequired[bool]
    routing: NotRequired[FieldCommonRouting]
    search_type: NotRequired[FieldCommonSearchType]
    ccs_minimize_roundtrips: NotRequired[bool]
    allow_partial_search_results: NotRequired[bool]
    ignore_throttled: NotRequired[bool]


class PitDeletedPit(TypedDict):
    successful: NotRequired[bool]
    pit_id: NotRequired[str]


class PitPitDetail(TypedDict):
    pit_id: NotRequired[str]
    creation_time: NotRequired[int]
    keep_alive: NotRequired[int]


class RankEvalDocumentRating(TypedDict):
    field_id: FieldCommonId
    field_index: FieldCommonIndexName
    rating: int


class RankEvalRankEvalHit(TypedDict):
    field_id: FieldCommonId
    field_index: FieldCommonIndexName
    field_score: float
    field_type: NotRequired[FieldCommonType]


class RankEvalRankEvalHitItem(TypedDict):
    hit: RankEvalRankEvalHit
    rating: NotRequired[int]


class RankEvalRankEvalMetricBase(TypedDict):
    k: NotRequired[int]


class RankEvalRankEvalMetricDiscountedCumulativeGain(RankEvalRankEvalMetricBase):
    normalize: NotRequired[bool]


class RankEvalRankEvalMetricExpectedReciprocalRank(RankEvalRankEvalMetricBase):
    maximum_relevance: int


class RankEvalRankEvalMetricRatingThreshold(RankEvalRankEvalMetricBase):
    relevant_rating_threshold: NotRequired[int]


class RankEvalRankEvalMetricRecall(RankEvalRankEvalMetricRatingThreshold):
    pass


class RankEvalUnratedDocument(TypedDict):
    field_id: FieldCommonId
    field_index: FieldCommonIndexName


class ReindexDestination(TypedDict):
    index: FieldCommonIndexName
    op_type: NotRequired[FieldCommonOpType]
    pipeline: NotRequired[str]
    routing: NotRequired[FieldCommonRouting]
    version_type: NotRequired[FieldCommonVersionType]


class ReindexRemoteSource(TypedDict):
    connect_timeout: NotRequired[FieldCommonDuration]
    headers: NotRequired[dict[str, str]]
    host: FieldCommonHost
    username: NotRequired[FieldCommonUsername]
    password: NotRequired[FieldCommonPassword]
    socket_timeout: NotRequired[FieldCommonDuration]


class SearchAggregationBreakdown(TypedDict):
    build_aggregation: int
    build_aggregation_count: int
    build_leaf_collector: int
    build_leaf_collector_count: int
    collect: int
    collect_count: int
    initialize: int
    initialize_count: int
    post_collection: NotRequired[int]
    post_collection_count: NotRequired[int]
    reduce: int
    reduce_count: int


class SearchAggregationProfileDelegateDebugFilter(TypedDict):
    results_from_metadata: NotRequired[int]
    query: NotRequired[str]
    specialized_for: NotRequired[str]
    segments_counted_in_constant_time: NotRequired[int]


SearchBoundaryScanner: TypeAlias = Literal["chars", "sentence", "word"]

SearchBuiltinHighlighterType: TypeAlias = Literal["plain", "fvh", "unified"]


class SearchDirectGenerator(TypedDict):
    field: str
    max_edits: NotRequired[int]
    max_inspections: NotRequired[float]
    max_term_freq: NotRequired[float]
    min_doc_freq: NotRequired[float]
    min_word_length: NotRequired[int]
    post_filter: NotRequired[str]
    pre_filter: NotRequired[str]
    prefix_length: NotRequired[int]
    size: NotRequired[int]
    suggest_mode: NotRequired[FieldCommonSuggestMode]


class SearchFetchProfileBreakdown(TypedDict):
    load_source: NotRequired[int]
    load_source_count: NotRequired[int]
    load_stored_fields: NotRequired[int]
    load_stored_fields_count: NotRequired[int]
    next_reader: NotRequired[int]
    next_reader_count: NotRequired[int]
    process_count: NotRequired[int]
    process: NotRequired[int]


class SearchFetchProfileDebug(TypedDict):
    stored_fields: NotRequired[list[str]]
    fast_path: NotRequired[int]


SearchHighlighterEncoder: TypeAlias = Literal["default", "html"]

SearchHighlighterFragmenter: TypeAlias = Literal["simple", "span"]

SearchHighlighterOrder: TypeAlias = Literal["score"]

SearchHighlighterTagsSchema: TypeAlias = Literal["default", "styled"]

SearchHighlighterType: TypeAlias = SearchBuiltinHighlighterType | str


class SearchLaplaceSmoothingModel(TypedDict):
    alpha: float


class SearchLinearInterpolationSmoothingModel(TypedDict):
    bigram_lambda: float
    trigram_lambda: float
    unigram_lambda: float


class SearchNestedIdentity(TypedDict):
    field: FieldCommonField
    offset: int
    field_nested: NotRequired[SearchNestedIdentity]


class SearchPhraseSuggestCollateQuery(TypedDict):
    id: NotRequired[str]
    source: NotRequired[str]


class SearchPhraseSuggestHighlight(TypedDict):
    post_tag: str
    pre_tag: str


class SearchPhraseSuggestOption(TypedDict):
    text: str
    score: float
    highlighted: NotRequired[str]
    collate_match: NotRequired[bool]


class SearchProcessorExecutionDetail(TypedDict):
    processor_name: NotRequired[str]
    duration_millis: NotRequired[int]
    input_data: NotRequired[Any]
    output_data: NotRequired[Any]
    status: NotRequired[str]
    tag: NotRequired[str]
    error: NotRequired[str]


class SearchQueryBreakdown(TypedDict):
    advance: int
    advance_count: int
    build_scorer: int
    build_scorer_count: int
    create_weight: int
    create_weight_count: int
    match: int
    match_count: int
    shallow_advance: int
    shallow_advance_count: int
    next_doc: int
    next_doc_count: int
    score: int
    score_count: int
    compute_max_score: int
    compute_max_score_count: int
    set_min_competitive_score: int
    set_min_competitive_score_count: int


SearchScoreMode: TypeAlias = Literal["avg", "max", "min", "multiply", "total"]


class Hit(TypedDict):
    field_source: NotRequired[Any]


class Options(TypedDict):
    field_source: NotRequired[Any]


class Option(TypedDict):
    field_source: NotRequired[Any]


class Suggest(TypedDict):
    options: NotRequired[Options | list[Option]]


SearchSourceConfigParam: TypeAlias = bool | FieldCommonFields

SearchStringDistance: TypeAlias = Literal[
    "damerau_levenshtein", "internal", "jaro_winkler", "levenshtein", "ngram"
]


class SearchStupidBackoffSmoothingModel(TypedDict):
    discount: float


class SearchSuggestBase(TypedDict):
    length: int
    offset: int
    text: str


class SearchSuggesterBase(TypedDict):
    analyzer: NotRequired[str]
    field: str
    size: NotRequired[int]


class SearchSuggestFuzziness(TypedDict):
    fuzziness: str
    min_length: int
    prefix_length: int
    transpositions: bool
    unicode_aware: bool


SearchSuggestSort: TypeAlias = Literal["frequency", "score"]

SearchTDocument: TypeAlias = Any


class SearchTermSuggester(SearchSuggesterBase):
    lowercase_terms: NotRequired[bool]
    max_edits: NotRequired[int]
    max_inspections: NotRequired[int]
    max_term_freq: NotRequired[float]
    min_doc_freq: NotRequired[float]
    min_word_length: NotRequired[int]
    prefix_length: NotRequired[int]
    shard_size: NotRequired[int]
    sort: NotRequired[SearchSuggestSort]
    string_distance: NotRequired[SearchStringDistance]
    suggest_mode: NotRequired[FieldCommonSuggestMode]
    text: NotRequired[str]


class SearchTermSuggestOption(TypedDict):
    text: str
    score: float
    freq: NotRequired[int]
    highlighted: NotRequired[str]
    collate_match: NotRequired[bool]


SearchTotalHitsRelation: TypeAlias = Literal["eq", "gte"]


class TermvectorsFieldStatistics(TypedDict):
    doc_count: int
    sum_doc_freq: int
    sum_ttf: int


class TermvectorsFilter(TypedDict):
    max_doc_freq: NotRequired[int]
    max_num_terms: NotRequired[int]
    max_term_freq: NotRequired[int]
    max_word_length: NotRequired[int]
    min_doc_freq: NotRequired[int]
    min_term_freq: NotRequired[int]
    min_word_length: NotRequired[int]


class TermvectorsToken(TypedDict):
    end_offset: NotRequired[int]
    payload: NotRequired[str]
    position: int
    start_offset: NotRequired[int]


BulkCreateOperation: TypeAlias = BulkWriteOperation


class BulkDeleteOperation(BulkOperationBase):
    if_primary_term: NotRequired[int]
    if_seq_no: NotRequired[FieldCommonSequenceNumber]
    version: NotRequired[FieldCommonVersionNumber]
    version_type: NotRequired[FieldCommonVersionType]


class BulkIndexOperation(BulkWriteOperation):
    if_primary_term: NotRequired[int]
    if_seq_no: NotRequired[FieldCommonSequenceNumber]
    op_type: NotRequired[FieldCommonOpType]
    version: NotRequired[FieldCommonVersionNumber]
    version_type: NotRequired[FieldCommonVersionType]


class BulkOperationContainer(TypedDict):
    index: NotRequired[BulkIndexOperation]
    create: NotRequired[BulkCreateOperation]
    update: NotRequired[BulkUpdateOperation]
    delete: NotRequired[BulkDeleteOperation]


class BulkResponseItem(TypedDict):
    field_type: NotRequired[str]
    field_id: NotRequired[str]
    field_index: str
    status: int
    error: NotRequired[FieldCommonErrorCause]
    field_primary_term: NotRequired[int]
    result: NotRequired[str]
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_shards: NotRequired[FieldCommonShardInfo]
    field_version: NotRequired[FieldCommonVersionNumber]
    forced_refresh: NotRequired[bool]
    get: NotRequired[FieldCommonInlineGetDictUserDefined]


class GetScriptContextContextMethod(TypedDict):
    name: FieldCommonName
    return_type: str
    params: list[GetScriptContextContextMethodParam]


class GetGetResult(GetGetResultBase):
    field_source: NotRequired[FieldCommonTDocument]


class MgetMultiGetError(TypedDict):
    error: FieldCommonErrorCause
    field_id: FieldCommonId
    field_index: FieldCommonIndexName


MgetResponseItem: TypeAlias = GetGetResult | MgetMultiGetError

MsearchTemplateRequestItem: TypeAlias = (
    MsearchMultisearchHeader | MsearchTemplateTemplateConfig
)


class MtermvectorsOperation(TypedDict):
    field_id: FieldCommonId
    field_index: NotRequired[FieldCommonIndexName]
    doc: NotRequired[Any]
    fields: NotRequired[FieldCommonFields]
    field_statistics: NotRequired[bool]
    filter: NotRequired[TermvectorsFilter]
    offsets: NotRequired[bool]
    payloads: NotRequired[bool]
    positions: NotRequired[bool]
    routing: NotRequired[FieldCommonRouting]
    term_statistics: NotRequired[bool]
    version: NotRequired[FieldCommonVersionNumber]
    version_type: NotRequired[FieldCommonVersionType]


class RankEvalRankEvalMetricDetail(TypedDict):
    metric_score: float
    unrated_docs: list[RankEvalUnratedDocument]
    hits: list[RankEvalRankEvalHitItem]
    metric_details: dict[str, dict[str, Any]]


class RankEvalRankEvalMetricMeanReciprocalRank(RankEvalRankEvalMetricRatingThreshold):
    pass


class RankEvalRankEvalMetricPrecision(RankEvalRankEvalMetricRatingThreshold):
    ignore_unlabeled: NotRequired[bool]


class ReindexRethrottleReindexStatus(TypedDict):
    batches: int
    created: int
    deleted: int
    noops: int
    requests_per_second: float
    retries: FieldCommonRetries
    throttled: NotRequired[FieldCommonDuration]
    throttled_millis: FieldCommonDurationValueUnitMillis
    throttled_until: NotRequired[FieldCommonDuration]
    throttled_until_millis: FieldCommonDurationValueUnitMillis
    total: int
    updated: int
    version_conflicts: int


class ReindexRethrottleReindexTask(TypedDict):
    action: str
    cancellable: bool
    cancelled: NotRequired[bool]
    description: str
    id: int
    node: FieldCommonName
    resource_stats: NotRequired[FieldCommonResourceStats]
    running_time_in_nanos: FieldCommonDurationValueUnitNanos
    start_time_in_millis: FieldCommonEpochTimeUnitMillis
    status: ReindexRethrottleReindexStatus
    type: str
    headers: FieldCommonHttpHeaders


class SearchAggregationProfileDelegateDebug(TypedDict):
    segments_with_doc_count_field: NotRequired[int]
    segments_with_deleted_docs: NotRequired[int]
    filters: NotRequired[list[SearchAggregationProfileDelegateDebugFilter]]
    segments_counted: NotRequired[int]
    segments_collected: NotRequired[int]


class SearchCollector(TypedDict):
    name: str
    reason: str
    time_in_nanos: FieldCommonDurationValueUnitNanos
    children: NotRequired[list[SearchCollector]]


SearchContext: TypeAlias = str | FieldCommonGeoLocation


class SearchFetchProfile(TypedDict):
    type: str
    description: str
    time_in_nanos: FieldCommonDurationValueUnitNanos
    breakdown: SearchFetchProfileBreakdown
    debug: NotRequired[SearchFetchProfileDebug]
    children: NotRequired[list[SearchFetchProfile]]


class SearchPhraseSuggest(SearchSuggestBase):
    options: SearchPhraseSuggestOption | list[SearchPhraseSuggestOption]


class SearchPhraseSuggestCollate(TypedDict):
    params: NotRequired[dict[str, Any]]
    prune: NotRequired[bool]
    query: SearchPhraseSuggestCollateQuery


class SearchQueryProfile(TypedDict):
    breakdown: SearchQueryBreakdown
    description: str
    time_in_nanos: FieldCommonDurationValueUnitNanos
    type: str
    children: NotRequired[list[SearchQueryProfile]]


class SearchSearchProfile(TypedDict):
    collector: list[SearchCollector]
    query: list[SearchQueryProfile]
    rewrite_time: int


class SearchSmoothingModel(TypedDict):
    laplace: NotRequired[SearchLaplaceSmoothingModel]
    linear_interpolation: NotRequired[SearchLinearInterpolationSmoothingModel]
    stupid_backoff: NotRequired[SearchStupidBackoffSmoothingModel]


class SearchTermSuggest(SearchSuggestBase):
    options: SearchTermSuggestOption | list[SearchTermSuggestOption]


class SearchTotalHits(TypedDict):
    relation: SearchTotalHitsRelation
    value: int


class TermvectorsTerm(TypedDict):
    doc_freq: NotRequired[int]
    score: NotRequired[float]
    term_freq: int
    tokens: NotRequired[list[TermvectorsToken]]
    ttf: NotRequired[int]


class TermvectorsTermVector(TypedDict):
    field_statistics: NotRequired[TermvectorsFieldStatistics]
    terms: dict[str, TermvectorsTerm]


class UpdateUpdateWriteResponseBase(FieldCommonWriteResponseBase):
    get: NotRequired[FieldCommonInlineGet]


class BulkItem(TypedDict):
    index: NotRequired[BulkResponseItem]
    create: NotRequired[BulkResponseItem]
    update: NotRequired[BulkResponseItem]
    delete: NotRequired[BulkResponseItem]


class BulkUpdateAction(TypedDict):
    detect_noop: NotRequired[bool]
    doc: NotRequired[dict[str, Any]]
    doc_as_upsert: NotRequired[bool]
    if_seq_no: NotRequired[FieldCommonSequenceNumber]
    if_primary_term: NotRequired[int]
    script: NotRequired[FieldCommonScript]
    scripted_upsert: NotRequired[bool]
    field_source: NotRequired[SearchSourceConfig]
    upsert: NotRequired[dict[str, Any]]


class GetScriptContextContext(TypedDict):
    methods: list[GetScriptContextContextMethod]
    name: FieldCommonName


class MgetOperation(TypedDict):
    field_id: FieldCommonId
    field_index: NotRequired[FieldCommonIndexName]
    routing: NotRequired[FieldCommonRouting]
    field_source: NotRequired[SearchSourceConfig]
    stored_fields: NotRequired[FieldCommonFields]
    version: NotRequired[FieldCommonVersionNumber]
    version_type: NotRequired[FieldCommonVersionType]


class MtermvectorsTermVectorsResult(TypedDict):
    field_id: FieldCommonId
    field_index: FieldCommonIndexName
    field_version: NotRequired[FieldCommonVersionNumber]
    took: NotRequired[int]
    found: NotRequired[bool]
    term_vectors: NotRequired[dict[str, TermvectorsTermVector]]
    error: NotRequired[FieldCommonErrorCause]
    field_type: NotRequired[FieldCommonType]


class RankEvalRankEvalMetric(TypedDict):
    precision: NotRequired[RankEvalRankEvalMetricPrecision]
    recall: NotRequired[RankEvalRankEvalMetricRecall]
    mean_reciprocal_rank: NotRequired[RankEvalRankEvalMetricMeanReciprocalRank]
    dcg: NotRequired[RankEvalRankEvalMetricDiscountedCumulativeGain]
    expected_reciprocal_rank: NotRequired[RankEvalRankEvalMetricExpectedReciprocalRank]


class ReindexRethrottleReindexNode(FieldCommonBaseNode):
    tasks: dict[str, ReindexRethrottleReindexTask]


class SearchAggregationProfileDebug(TypedDict):
    segments_with_multi_valued_ords: NotRequired[int]
    collection_strategy: NotRequired[str]
    segments_with_single_valued_ords: NotRequired[int]
    total_buckets: NotRequired[int]
    built_buckets: NotRequired[int]
    result_strategy: NotRequired[str]
    has_filter: NotRequired[bool]
    delegate: NotRequired[str]
    delegate_debug: NotRequired[SearchAggregationProfileDelegateDebug]
    chars_fetched: NotRequired[int]
    extract_count: NotRequired[int]
    extract_ns: NotRequired[int]
    values_fetched: NotRequired[int]
    collect_analyzed_ns: NotRequired[int]
    collect_analyzed_count: NotRequired[int]
    surviving_buckets: NotRequired[int]
    ordinals_collectors_used: NotRequired[int]
    ordinals_collectors_overhead_too_high: NotRequired[int]
    string_hashing_collectors_used: NotRequired[int]
    numeric_collectors_used: NotRequired[int]
    empty_collectors_used: NotRequired[int]
    deferred_aggregators: NotRequired[list[str]]
    map_reducer: NotRequired[str]


class SearchCompletionContext(TypedDict):
    boost: NotRequired[float]
    context: SearchContext
    neighbours: NotRequired[list[FieldCommonGeoHashPrecision]]
    precision: NotRequired[FieldCommonGeoHashPrecision]
    prefix: NotRequired[bool]


SearchCompletionContextModel: TypeAlias = SearchContext | SearchCompletionContext


class SearchCompletionSuggester(SearchSuggesterBase):
    contexts: NotRequired[dict[str, list[SearchCompletionContextModel]]]
    fuzzy: NotRequired[SearchSuggestFuzziness]
    regex: NotRequired[str]
    skip_duplicates: NotRequired[bool]


class SearchCompletionSuggestOption(TypedDict):
    collate_match: NotRequired[bool]
    contexts: NotRequired[dict[str, list[SearchContext]]]
    fields: NotRequired[dict[str, Any]]
    field_id: NotRequired[str]
    field_index: NotRequired[FieldCommonIndexName]
    field_routing: NotRequired[FieldCommonRouting]
    field_score: NotRequired[float]
    field_source: NotRequired[SearchTDocument]
    text: str
    score: NotRequired[float]


class SearchPhraseSuggester(SearchSuggesterBase):
    collate: NotRequired[SearchPhraseSuggestCollate]
    confidence: NotRequired[float]
    direct_generator: NotRequired[list[SearchDirectGenerator]]
    force_unigrams: NotRequired[bool]
    gram_size: NotRequired[int]
    highlight: NotRequired[SearchPhraseSuggestHighlight]
    max_errors: NotRequired[float]
    real_word_error_likelihood: NotRequired[float]
    separator: NotRequired[str]
    shard_size: NotRequired[int]
    smoothing: NotRequired[SearchSmoothingModel]
    text: NotRequired[str]
    token_limit: NotRequired[int]


class OptionsModel(SearchCompletionSuggestOption):
    field_source: NotRequired[SearchTDocument]


class OptionModel(SearchCompletionSuggestOption):
    field_source: NotRequired[SearchTDocument]


class BulkBulkResponse(TypedDict):
    errors: bool
    items: list[BulkItem]
    took: int
    ingest_took: NotRequired[int]


class SearchAggregationProfile(TypedDict):
    breakdown: SearchAggregationBreakdown
    description: str
    time_in_nanos: FieldCommonDurationValueUnitNanos
    type: str
    debug: NotRequired[SearchAggregationProfileDebug]
    children: NotRequired[list[SearchAggregationProfile]]


class SearchCompletionSuggest(SearchSuggestBase):
    options: OptionsModel | list[OptionModel]


class SearchFieldSuggester(TypedDict):
    prefix: NotRequired[str]
    regex: NotRequired[str]
    text: NotRequired[str]
    completion: NotRequired[SearchCompletionSuggester]
    phrase: NotRequired[SearchPhraseSuggester]
    term: NotRequired[SearchTermSuggester]


class SuggestModel(SearchCompletionSuggest):
    options: NotRequired[OptionsModel | list[OptionModel]]


class SearchShardProfile(TypedDict):
    aggregations: list[SearchAggregationProfile]
    id: str
    searches: list[SearchSearchProfile]
    fetch: NotRequired[SearchFetchProfile]


class SearchSuggest(SearchCompletionSuggest):
    options: NotRequired[OptionsModel | list[OptionModel]]


SearchSuggestModel: TypeAlias = SearchSuggest | SearchPhraseSuggest | SearchTermSuggest


class SearchProfile(TypedDict):
    shards: list[SearchShardProfile]


MsearchMultisearchBody = TypedDict(
    "MsearchMultisearchBody",
    {
        "aggregations": NotRequired[dict[str, AggregationsAggregationContainerModel43]],
        "collapse": NotRequired[SearchFieldCollapse],
        "query": NotRequired[QueryDslQueryContainer],
        "explain": NotRequired[bool],
        "ext": NotRequired[dict[str, dict[str, Any]]],
        "stored_fields": NotRequired[FieldCommonFields],
        "docvalue_fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "knn": NotRequired[QueryDslKnnQuery | list[QueryDslKnnQuery]],
        "from": NotRequired[float],
        "highlight": NotRequired[SearchHighlight],
        "indices_boost": NotRequired[list[dict[str, float]]],
        "min_score": NotRequired[float],
        "post_filter": NotRequired[QueryDslQueryContainer],
        "profile": NotRequired[bool],
        "rescore": NotRequired[SearchRescore | list[SearchRescore]],
        "script_fields": NotRequired[dict[str, FieldCommonScriptField]],
        "search_after": NotRequired[FieldCommonSortResults],
        "size": NotRequired[float],
        "sort": NotRequired[FieldCommonSort],
        "_source": NotRequired[SearchSourceConfig],
        "fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "terminate_after": NotRequired[float],
        "stats": NotRequired[list[str]],
        "timeout": NotRequired[str],
        "track_scores": NotRequired[bool],
        "track_total_hits": NotRequired[SearchTrackHits],
        "version": NotRequired[bool],
        "seq_no_primary_term": NotRequired[bool],
        "pit": NotRequired[SearchPointInTimeReference],
        "suggest": NotRequired[SearchSuggester],
    },
)


class MsearchMultiSearchResult(TypedDict):
    took: float
    responses: list[MsearchResponseItem]


MsearchRequestItem: TypeAlias = MsearchMultisearchHeader | MsearchMultisearchBody

MsearchResponseItem: TypeAlias = Union[
    "MsearchMultiSearchItem", FieldCommonErrorResponseBase
]


class RankEvalRankEvalQuery(TypedDict):
    query: QueryDslQueryContainer
    size: NotRequired[int]


class RankEvalRankEvalRequestItem(TypedDict):
    id: FieldCommonId
    request: NotRequired[RankEvalRankEvalQuery]
    ratings: list[RankEvalDocumentRating]
    template_id: NotRequired[FieldCommonId]
    params: NotRequired[dict[str, Any]]


class ReindexSource(TypedDict):
    index: FieldCommonIndices
    query: NotRequired[QueryDslQueryContainer]
    remote: NotRequired[ReindexRemoteSource]
    size: NotRequired[int]
    slice: NotRequired[FieldCommonSlicedScroll]
    sort: NotRequired[FieldCommonSort]
    field_source: NotRequired[FieldCommonFields]


class ScriptsPainlessExecutePainlessContextSetup(TypedDict):
    document: Any
    index: FieldCommonIndexName
    query: NotRequired[QueryDslQueryContainer]


class SearchShardsShardStoreIndex(TypedDict):
    aliases: NotRequired[list[FieldCommonName]]
    filter: NotRequired[QueryDslQueryContainer]


SearchHighlightFields: TypeAlias = Union[
    dict[str, "SearchHighlightField"], list[dict[str, "SearchHighlightField"]]
]


class SearchHit(TypedDict):
    field_type: NotRequired[FieldCommonType]
    field_index: NotRequired[FieldCommonIndexName]
    field_id: NotRequired[FieldCommonId]
    field_score: NotRequired[float | None]
    field_explanation: NotRequired[ExplainExplanation]
    fields: NotRequired[dict[str, Any]]
    highlight: NotRequired[dict[str, list[str]]]
    inner_hits: NotRequired[dict[str, SearchInnerHitsResult]]
    matched_queries: NotRequired[list[str] | dict[str, float]]
    field_nested: NotRequired[SearchNestedIdentity]
    field_ignored: NotRequired[list[str]]
    ignored_field_values: NotRequired[dict[str, list[str]]]
    field_shard: NotRequired[str]
    field_node: NotRequired[str]
    field_routing: NotRequired[str]
    field_source: NotRequired[SearchTDocument]
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_primary_term: NotRequired[int]
    field_version: NotRequired[FieldCommonVersionNumber]
    sort: NotRequired[FieldCommonSortResults]


class SearchHitsMetadata(TypedDict):
    total: NotRequired[SearchTotalHits | int]
    hits: list[HitModel]
    max_score: NotRequired[float | None]


SearchInnerHits = TypedDict(
    "SearchInnerHits",
    {
        "name": NotRequired[FieldCommonName],
        "size": NotRequired[int],
        "from": NotRequired[int],
        "collapse": NotRequired[SearchFieldCollapse],
        "docvalue_fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "explain": NotRequired[bool],
        "highlight": NotRequired[SearchHighlight],
        "ignore_unmapped": NotRequired[bool],
        "script_fields": NotRequired[dict[str, FieldCommonScriptField]],
        "seq_no_primary_term": NotRequired[bool],
        "fields": NotRequired[list[QueryDslFieldAndFormatModel]],
        "sort": NotRequired[FieldCommonSort],
        "_source": NotRequired[SearchSourceConfig],
        "stored_fields": NotRequired[FieldCommonFields],
        "track_scores": NotRequired[bool],
        "version": NotRequired[bool],
    },
)


class SearchInnerHitsResult(TypedDict):
    hits: SearchHitsMetadata


class SearchRescoreQuery(TypedDict):
    rescore_query: QueryDslQueryContainer
    query_weight: NotRequired[float]
    rescore_query_weight: NotRequired[float]
    score_mode: NotRequired[SearchScoreMode]


class SearchSearchResult(TypedDict):
    took: int
    timed_out: bool
    field_shards: FieldCommonShardStatistics
    phase_took: NotRequired[FieldCommonPhaseTook]
    hits: Hits
    processor_results: NotRequired[list[SearchProcessorExecutionDetail]]
    aggregations: NotRequired[dict[str, AggregationsAggregate]]
    field_clusters: NotRequired[FieldCommonClusterStatistics]
    num_reduce_phases: NotRequired[int]
    profile: NotRequired[SearchProfile]
    pit_id: NotRequired[FieldCommonId]
    field_scroll_id: NotRequired[FieldCommonScrollId]
    suggest: NotRequired[dict[str, list[SearchSuggestModel]]]
    terminated_early: NotRequired[bool]


class UpdateByQueryRethrottleUpdateByQueryRethrottleNode(FieldCommonBaseNode):
    tasks: dict[str, FieldCommonTaskInfo]


class SearchHighlightField(SearchHighlightBase):
    matched_fields: NotRequired[FieldCommonFields]


class HitModel(SearchHit):
    field_source: NotRequired[SearchTDocument]


class SearchHitsMetadataJsonValue(SearchHitsMetadata):
    hits: NotRequired[list[HitModel]]


class Hits(SearchHitsMetadata):
    hits: NotRequired[list[HitModel]]


class MsearchMultiSearchItem(SearchSearchResult):
    status: NotRequired[float]


class SearchSearchResponse(SearchSearchResult):
    pass


class SearchSearchResultJsonValue(SearchSearchResult):
    hits: NotRequired[Hits]
    suggest: NotRequired[
        dict[
            str, list[SuggestModel | SearchPhraseSuggest | SearchTermSuggest | Suggest]
        ]
    ]


FieldCommonBuiltinStorageType: TypeAlias = Literal["fs", "hybridfs", "mmapfs", "niofs"]


class FieldCommonDataStreamTimestampField(TypedDict):
    name: FieldCommonField


class FieldCommonFielddataFrequencyFilter(TypedDict):
    max: float
    min: float
    min_segment_size: int


FieldCommonIndexCheckOnStartup: TypeAlias = Literal["checksum", "false", "true"]


class FieldCommonIndexingPressureMemory(TypedDict):
    limit: NotRequired[str | int]


class FieldCommonIndexRoutingAllocationDisk(TypedDict):
    threshold_enabled: NotRequired[FieldCommonStringifiedBoolean]


class FieldCommonIndexRoutingAllocationInclude(TypedDict):
    field_tier_preference: NotRequired[str]
    field_id: NotRequired[FieldCommonId]


class FieldCommonIndexRoutingAllocationInitialRecovery(TypedDict):
    field_id: NotRequired[FieldCommonId]


FieldCommonIndexRoutingAllocationOptions: TypeAlias = Literal[
    "all", "new_primaries", "none", "primaries"
]

FieldCommonIndexRoutingRebalanceOptions: TypeAlias = Literal[
    "all", "none", "primaries", "replicas"
]


class FieldCommonIndexSettingBlocks(TypedDict):
    read_only: NotRequired[FieldCommonStringifiedBoolean]
    read_only_allow_delete: NotRequired[FieldCommonStringifiedBoolean]
    read: NotRequired[FieldCommonStringifiedBoolean]
    write: NotRequired[FieldCommonStringifiedBoolean]
    metadata: NotRequired[FieldCommonStringifiedBoolean]
    search_only: NotRequired[FieldCommonStringifiedBoolean]


class FieldCommonIndexSettingsAnalyze(TypedDict):
    max_token_count: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexSettingsHighlight(TypedDict):
    max_analyzed_offset: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexSettingsLifecycleStep(TypedDict):
    wait_time_threshold: NotRequired[FieldCommonDuration]


class FieldCommonIndexSettingsMappingLimitDepth(TypedDict):
    limit: NotRequired[FieldCommonStringifiedLong]


class FieldCommonIndexSettingsMappingLimitDimensionFields(TypedDict):
    limit: NotRequired[FieldCommonStringifiedLong]


class FieldCommonIndexSettingsMappingLimitFieldNameLength(TypedDict):
    limit: NotRequired[FieldCommonStringifiedLong]


class FieldCommonIndexSettingsMappingLimitNestedFields(TypedDict):
    limit: NotRequired[FieldCommonStringifiedLong]


class FieldCommonIndexSettingsMappingLimitNestedObjects(TypedDict):
    limit: NotRequired[FieldCommonStringifiedLong]


class FieldCommonIndexSettingsMappingLimitTotalFields(TypedDict):
    limit: NotRequired[FieldCommonStringifiedLong]


class FieldCommonIndexSettingsMergeLogByteSizePolicy(TypedDict):
    max_merge_segment: NotRequired[FieldCommonHumanReadableByteCount]
    max_merge_segment_forced_merge: NotRequired[FieldCommonHumanReadableByteCount]
    max_merged_docs: NotRequired[FieldCommonStringifiedInteger]
    merge_factor: NotRequired[FieldCommonStringifiedInteger]
    min_merge: NotRequired[FieldCommonHumanReadableByteCount]
    no_cfs_ratio: NotRequired[FieldCommonStringifiedDouble]


FieldCommonIndexSettingsMergePolicyName: TypeAlias = Literal[
    "default", "log_byte_size", "tiered"
]


class FieldCommonIndexSettingsMergeScheduler(TypedDict):
    auto_throttle: NotRequired[FieldCommonStringifiedBoolean]
    max_thread_count: NotRequired[FieldCommonStringifiedInteger]
    max_merge_count: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexSettingsMergeTieredPolicy(TypedDict):
    deletes_pct_allowed: NotRequired[FieldCommonStringifiedDouble]
    expunge_deletes_allowed: NotRequired[FieldCommonStringifiedDouble]
    floor_segment: NotRequired[FieldCommonHumanReadableByteCount]
    max_merge_at_once: NotRequired[FieldCommonStringifiedInteger]
    max_merge_at_once_explicit: NotRequired[FieldCommonStringifiedInteger]
    max_merged_segment: NotRequired[FieldCommonHumanReadableByteCount]
    reclaim_deletes_weight: NotRequired[FieldCommonStringifiedDouble]
    segments_per_tier: NotRequired[FieldCommonStringifiedDouble]


class FieldCommonIndexSettingsQueriesCache(TypedDict):
    enabled: FieldCommonStringifiedBoolean


class FieldCommonIndexSettingsQueryString(TypedDict):
    lenient: NotRequired[FieldCommonStringifiedBoolean]


class FieldCommonIndexSettingsSearchConcurrent(TypedDict):
    max_slice_count: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexSettingsSearchConcurrentSegmentSearch(TypedDict):
    mode: NotRequired[str]
    enabled: NotRequired[FieldCommonStringifiedBoolean]


class FieldCommonIndexSettingsSearchStarTreeIndex(TypedDict):
    enabled: NotRequired[FieldCommonStringifiedBoolean]


class FieldCommonIndexSettingsSimilarityBm25(TypedDict):
    b: float
    discount_overlaps: bool
    k1: float
    type: Literal["BM25"]


class FieldCommonIndexSettingsSimilarityDfi(TypedDict):
    independence_measure: FieldCommonDFIIndependenceMeasure
    type: Literal["DFI"]


class FieldCommonIndexSettingsSimilarityDfr(TypedDict):
    after_effect: FieldCommonDFRAfterEffect
    basic_model: FieldCommonDFRBasicModel
    normalization: FieldCommonTermFrequencyNormalization
    type: Literal["DFR"]


FieldCommonIndexSettingsSimilarityIb = TypedDict(
    "FieldCommonIndexSettingsSimilarityIb",
    {
        "distribution": FieldCommonIBDistribution,
        "lambda": FieldCommonIBLambda,
        "normalization": FieldCommonTermFrequencyNormalization,
        "type": Literal["IB"],
    },
)


class FieldCommonIndexSettingsSimilarityLmd(TypedDict):
    mu: float
    type: Literal["LMDirichlet"]


FieldCommonIndexSettingsSimilarityLmj = TypedDict(
    "FieldCommonIndexSettingsSimilarityLmj",
    {
        "lambda": float,
        "type": Literal["LMJelinekMercer"],
    },
)


class FieldCommonIndexSettingsStarTreeDefault(TypedDict):
    max_leaf_docs: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexSettingsStarTreeFieldDefault(TypedDict):
    date_intervals: NotRequired[list[str]]
    metrics: NotRequired[list[str]]


FieldCommonIndexSettingsStoreFsLock: TypeAlias = Literal["native", "simple"]


class FieldCommonIndexSettingsStoreHybridMmap(TypedDict):
    extensions: NotRequired[list[str]]


class FieldCommonIndexSettingsStoreHybridNio(TypedDict):
    extensions: NotRequired[list[str]]


class FieldCommonIndexTemplateDataStreamConfiguration(TypedDict):
    hidden: NotRequired[bool]
    allow_custom_routing: NotRequired[bool]
    timestamp_field: NotRequired[FieldCommonDataStreamTimestampField]


class FieldCommonIndexVersioning(TypedDict):
    created: NotRequired[FieldCommonVersionString]
    created_string: NotRequired[str]


FieldCommonIngestionSourcePointerInitReset: TypeAlias = Literal[
    "EARLIEST",
    "LATEST",
    "NONE",
    "RESET_BY_OFFSET",
    "RESET_BY_TIMESTAMP",
    "earliest",
    "latest",
    "none",
    "reset_by_offset",
    "reset_by_timestamp",
]


class FieldCommonIngestionSourcePoll(TypedDict):
    max_batch_size: NotRequired[FieldCommonStringifiedLong]
    timeout: NotRequired[FieldCommonStringifiedInteger]


FieldCommonIngestionSourceType: TypeAlias = Literal["file", "kafka", "kinesis", "none"]

FieldCommonManagedBy: TypeAlias = Literal[
    "Data stream lifecycle", "Index Lifecycle Management", "Unmanaged"
]

FieldCommonNumericFielddataFormat: TypeAlias = Literal["array", "disabled"]

FieldCommonReplicationType: TypeAlias = Literal["DOCUMENT", "SEGMENT"]


class FieldCommonRetentionLease(TypedDict):
    period: FieldCommonDuration


class FieldCommonSearchIdle(TypedDict):
    after: NotRequired[FieldCommonDuration]


FieldCommonSegmentSortMissing: TypeAlias = Literal["_first", "_last"]

FieldCommonSegmentSortMode: TypeAlias = Literal["max", "min"]

FieldCommonSegmentSortOrder: TypeAlias = Literal["asc", "desc"]


class FieldCommonSlowlogThresholdLevels(TypedDict):
    warn: NotRequired[FieldCommonDuration]
    info: NotRequired[FieldCommonDuration]
    debug: NotRequired[FieldCommonDuration]
    trace: NotRequired[FieldCommonDuration]


class FieldCommonSoftDeletesRetention(TypedDict):
    operations: NotRequired[FieldCommonStringifiedLong]


FieldCommonStorageType: TypeAlias = FieldCommonBuiltinStorageType | str

FieldCommonTranslogDurability: TypeAlias = Literal[
    "ASYNC", "REQUEST", "async", "request"
]


class FieldCommonTranslogRetention(TypedDict):
    size: NotRequired[FieldCommonHumanReadableByteCount]
    age: NotRequired[FieldCommonDuration]


class FieldCommonUpgradeStatus(TypedDict):
    size_in_bytes: NotRequired[FieldCommonByteCount]
    size_to_upgrade_in_bytes: NotRequired[FieldCommonByteCount]
    size_to_upgrade_ancient_in_bytes: NotRequired[FieldCommonByteCount]


class FieldCommonUpgradeVersionStatus(TypedDict):
    upgrade_version: NotRequired[FieldCommonVersionString]
    oldest_lucene_segment_version: NotRequired[FieldCommonVersionString]


AddBlockIndicesBlockOptions: TypeAlias = Literal[
    "metadata", "read", "read_only", "write"
]


class AddBlockIndicesBlockStatus(TypedDict):
    name: FieldCommonIndexName
    blocked: bool


class AnalyzeAnalyzeToken(TypedDict):
    end_offset: int
    position: int
    positionLength: NotRequired[int]
    start_offset: int
    token: str
    type: str


class AnalyzeCharFilterDetail(TypedDict):
    filtered_text: list[str]
    name: str


class AnalyzeExplainAnalyzeToken(TypedDict):
    bytes: str
    end_offset: int
    keyword: NotRequired[bool]
    position: int
    positionLength: int
    start_offset: int
    termFrequency: int
    token: str
    type: str


AnalyzeTextToAnalyze: TypeAlias = FieldCommonStringOrStringArray


class AnalyzeTokenDetail(TypedDict):
    name: str
    tokens: list[AnalyzeExplainAnalyzeToken]


class RecoveryFileDetails(TypedDict):
    length: int
    name: str
    recovered: int


class RecoveryRecoveryBytes(TypedDict):
    percent: FieldCommonPercentageString
    recovered: NotRequired[FieldCommonHumanReadableByteCount]
    recovered_in_bytes: FieldCommonByteCount
    recovered_from_snapshot: NotRequired[FieldCommonHumanReadableByteCount]
    recovered_from_snapshot_in_bytes: NotRequired[FieldCommonByteCount]
    reused: NotRequired[FieldCommonHumanReadableByteCount]
    reused_in_bytes: FieldCommonByteCount
    total: NotRequired[FieldCommonHumanReadableByteCount]
    total_in_bytes: FieldCommonByteCount


class RecoveryRecoveryFiles(TypedDict):
    details: NotRequired[list[RecoveryFileDetails]]
    percent: FieldCommonPercentageString
    recovered: int
    reused: int
    total: int


class RecoveryRecoveryOrigin(TypedDict):
    hostname: NotRequired[str]
    host: NotRequired[FieldCommonHost]
    transport_address: NotRequired[FieldCommonTransportAddress]
    id: NotRequired[FieldCommonId]
    ip: NotRequired[FieldCommonIp]
    name: NotRequired[FieldCommonName]
    bootstrap_new_history_uuid: NotRequired[bool]
    repository: NotRequired[FieldCommonName]
    snapshot: NotRequired[FieldCommonName]
    version: NotRequired[FieldCommonVersionString]
    restoreUUID: NotRequired[FieldCommonUuid]
    index: NotRequired[FieldCommonIndexName]
    isSearchableSnapshot: NotRequired[bool]
    remoteStoreIndexShallowCopy: NotRequired[bool]
    sourceRemoteStoreRepository: NotRequired[str | None]
    sourceRemoteTranslogRepository: NotRequired[str | None]


class ResolveIndexResolveIndexAliasItem(TypedDict):
    name: FieldCommonName
    indices: FieldCommonIndices


class ResolveIndexResolveIndexDataStreamsItem(TypedDict):
    name: FieldCommonDataStreamName
    timestamp_field: FieldCommonField
    backing_indices: FieldCommonIndices


class ResolveIndexResolveIndexItem(TypedDict):
    name: FieldCommonName
    aliases: NotRequired[list[str]]
    attributes: list[str]
    data_stream: NotRequired[FieldCommonDataStreamName]


class SegmentsSegment(TypedDict):
    generation: int
    num_docs: int
    deleted_docs: int
    size: NotRequired[FieldCommonHumanReadableByteCount]
    size_in_bytes: FieldCommonByteCount
    memory: NotRequired[FieldCommonHumanReadableByteCount]
    memory_in_bytes: NotRequired[FieldCommonByteCount]
    committed: bool
    search: bool
    version: FieldCommonVersionString
    compound: bool
    attributes: dict[str, str]


class SegmentsShardSegmentRouting(TypedDict):
    node: str
    primary: bool
    state: str


class SegmentsShardsSegment(TypedDict):
    num_committed_segments: int
    routing: SegmentsShardSegmentRouting
    num_search_segments: int
    segments: dict[str, SegmentsSegment]


ShardStoresShardStoreAllocation: TypeAlias = Literal["primary", "replica", "unused"]


class ShardStoresShardStoreException(TypedDict):
    reason: str
    type: str


ShardStoresShardStoreStatus: TypeAlias = Literal["all", "green", "red", "yellow"]


class SimulateTemplateOverlapping(TypedDict):
    name: FieldCommonName
    index_patterns: list[str]


StatsMetric_1: TypeAlias = Literal[
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


class StatsShardCommit(TypedDict):
    generation: int
    id: FieldCommonId
    num_docs: int
    user_data: dict[str, str]


class StatsShardFileSizeInfo(TypedDict):
    description: str
    size: NotRequired[FieldCommonHumanReadableByteCount]
    size_in_bytes: FieldCommonByteCount
    min_size_in_bytes: NotRequired[FieldCommonByteCount]
    max_size_in_bytes: NotRequired[FieldCommonByteCount]
    average_size_in_bytes: NotRequired[FieldCommonByteCount]
    count: NotRequired[int]


class StatsShardLease(TypedDict):
    id: FieldCommonId
    retaining_seq_no: FieldCommonSequenceNumber
    timestamp: int
    source: str


class StatsShardPath(TypedDict):
    data_path: str
    is_custom_data_path: bool
    state_path: str


class StatsShardRetentionLeases(TypedDict):
    primary_term: int
    version: FieldCommonVersionNumber
    leases: list[StatsShardLease]


StatsShardRoutingState: TypeAlias = Literal[
    "INITIALIZING", "RELOCATING", "STARTED", "UNASSIGNED"
]


class StatsShardSequenceNumber(TypedDict):
    global_checkpoint: int
    local_checkpoint: int
    max_seq_no: FieldCommonSequenceNumber


class UpdateAliasesRemoveAction(TypedDict):
    alias: NotRequired[FieldCommonIndexAlias]
    aliases: NotRequired[FieldCommonIndexAlias | list[FieldCommonIndexAlias]]
    index: NotRequired[FieldCommonIndexName]
    indices: NotRequired[FieldCommonIndices]
    must_exist: NotRequired[bool]


class UpdateAliasesRemoveIndexAction(TypedDict):
    index: NotRequired[FieldCommonIndexName]
    indices: NotRequired[FieldCommonIndices]
    must_exist: NotRequired[bool]


class ValidateQueryIndicesValidationExplanation(TypedDict):
    error: NotRequired[str]
    explanation: NotRequired[str]
    index: FieldCommonIndexName
    valid: bool


class FieldCommonDataStreamIndex(TypedDict):
    index_name: FieldCommonIndexName
    index_uuid: FieldCommonUuid
    ilm_policy: NotRequired[FieldCommonName]
    managed_by: NotRequired[FieldCommonManagedBy]
    prefer_ilm: NotRequired[bool]


class FieldCommonDataStreamStats(TypedDict):
    backing_indices: int
    data_stream: FieldCommonName
    maximum_timestamp: FieldCommonEpochTimeUnitMillis
    store_size: NotRequired[FieldCommonHumanReadableByteCount]
    store_size_bytes: FieldCommonByteCount


class FieldCommonIndexGetUpgradeStatus(TypedDict):
    size_in_bytes: NotRequired[FieldCommonByteCount]
    size_to_upgrade_in_bytes: NotRequired[FieldCommonByteCount]
    size_to_upgrade_ancient_in_bytes: NotRequired[FieldCommonByteCount]
    indices: NotRequired[dict[str, FieldCommonUpgradeStatus]]


class FieldCommonIndexingPressure(TypedDict):
    memory: FieldCommonIndexingPressureMemory


class FieldCommonIndexingSlowlogThresholds(TypedDict):
    index: NotRequired[FieldCommonSlowlogThresholdLevels]


class FieldCommonIndexRoutingAllocation(TypedDict):
    enable: NotRequired[FieldCommonIndexRoutingAllocationOptions]
    include: NotRequired[FieldCommonIndexRoutingAllocationInclude]
    initial_recovery: NotRequired[FieldCommonIndexRoutingAllocationInitialRecovery]
    disk: NotRequired[FieldCommonIndexRoutingAllocationDisk]
    total_shards_per_node: NotRequired[FieldCommonStringifiedInteger]
    total_primary_shards_per_node: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexRoutingRebalance(TypedDict):
    enable: FieldCommonIndexRoutingRebalanceOptions


class FieldCommonIndexSegmentSort(TypedDict):
    field: NotRequired[FieldCommonFields]
    order: NotRequired[FieldCommonSegmentSortOrder | list[FieldCommonSegmentSortOrder]]
    mode: NotRequired[FieldCommonSegmentSortMode | list[FieldCommonSegmentSortMode]]
    missing: NotRequired[
        FieldCommonSegmentSortMissing | list[FieldCommonSegmentSortMissing]
    ]


class FieldCommonIndexSettingsLifecycle(TypedDict):
    name: FieldCommonName
    indexing_complete: NotRequired[FieldCommonStringifiedBoolean]
    origination_date: NotRequired[FieldCommonStringifiedEpochTimeUnitMillis]
    parse_origination_date: NotRequired[bool]
    step: NotRequired[FieldCommonIndexSettingsLifecycleStep]
    rollover_alias: NotRequired[str]


class FieldCommonIndexSettingsMapping(TypedDict):
    coerce: NotRequired[FieldCommonStringifiedBoolean]
    total_fields: NotRequired[FieldCommonIndexSettingsMappingLimitTotalFields]
    depth: NotRequired[FieldCommonIndexSettingsMappingLimitDepth]
    nested_fields: NotRequired[FieldCommonIndexSettingsMappingLimitNestedFields]
    nested_objects: NotRequired[FieldCommonIndexSettingsMappingLimitNestedObjects]
    field_name_length: NotRequired[FieldCommonIndexSettingsMappingLimitFieldNameLength]
    dimension_fields: NotRequired[FieldCommonIndexSettingsMappingLimitDimensionFields]
    ignore_malformed: NotRequired[FieldCommonStringifiedBoolean]


FieldCommonIndexSettingsMergePolicy: TypeAlias = (
    FieldCommonIndexSettingsMergePolicyName | FieldCommonIndexSettingsMergeTieredPolicy
)


class FieldCommonIndexSettingsQueries(TypedDict):
    cache: NotRequired[FieldCommonIndexSettingsQueriesCache]


class FieldCommonIndexSettingsSimilarityScriptedTfidf(TypedDict):
    script: FieldCommonScript
    type: Literal["scripted"]


class FieldCommonIndexSettingsStarTreeField(TypedDict):
    default: NotRequired[FieldCommonIndexSettingsStarTreeFieldDefault]
    max_base_metrics: NotRequired[FieldCommonStringifiedInteger]
    max_date_intervals: NotRequired[FieldCommonStringifiedInteger]
    max_dimensions: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexSettingsStoreFs(TypedDict):
    fs_lock: NotRequired[FieldCommonIndexSettingsStoreFsLock]


class FieldCommonIndexSettingsStoreHybrid(TypedDict):
    mmap: NotRequired[FieldCommonIndexSettingsStoreHybridMmap]
    nio: NotRequired[FieldCommonIndexSettingsStoreHybridNio]


FieldCommonIngestionSourcePointerInit = TypedDict(
    "FieldCommonIngestionSourcePointerInit",
    {
        "reset": NotRequired[FieldCommonIngestionSourcePointerInitReset],
        "reset.value": NotRequired[str],
    },
)


class FieldCommonNumericFielddata(TypedDict):
    format: FieldCommonNumericFielddataFormat


class FieldCommonSearchSlowlogThresholds(TypedDict):
    query: NotRequired[FieldCommonSlowlogThresholdLevels]
    fetch: NotRequired[FieldCommonSlowlogThresholdLevels]


class FieldCommonSoftDeletes(TypedDict):
    enabled: NotRequired[FieldCommonStringifiedBoolean]
    retention: NotRequired[FieldCommonSoftDeletesRetention]
    retention_lease: NotRequired[FieldCommonRetentionLease]


class FieldCommonTranslog(TypedDict):
    sync_interval: NotRequired[FieldCommonDuration]
    durability: NotRequired[FieldCommonTranslogDurability]
    flush_threshold_size: NotRequired[FieldCommonHumanReadableByteCount]
    generation_threshold_size: NotRequired[FieldCommonHumanReadableByteCount]
    retention: NotRequired[FieldCommonTranslogRetention]


class AnalyzeAnalyzerDetail(TypedDict):
    name: str
    tokens: list[AnalyzeExplainAnalyzeToken]


class CloseCloseShardResult(TypedDict):
    failures: list[FieldCommonShardFailure]


class RecoveryRecoveryIndexStatus(TypedDict):
    bytes: NotRequired[RecoveryRecoveryBytes]
    files: RecoveryRecoveryFiles
    size: RecoveryRecoveryBytes
    source_throttle_time: NotRequired[FieldCommonDuration]
    source_throttle_time_in_millis: FieldCommonDurationValueUnitMillis
    target_throttle_time: NotRequired[FieldCommonDuration]
    target_throttle_time_in_millis: FieldCommonDurationValueUnitMillis
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis


class RecoveryRecoveryStartStatus(TypedDict):
    check_index_time: NotRequired[FieldCommonDuration]
    check_index_time_in_millis: FieldCommonDurationValueUnitMillis
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis


class RecoveryTranslogStatus(TypedDict):
    percent: FieldCommonPercentageString
    recovered: int
    total: int
    total_on_start: int
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis


class RecoveryVerifyIndex(TypedDict):
    check_index_time: NotRequired[FieldCommonDuration]
    check_index_time_in_millis: FieldCommonDurationValueUnitMillis
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis


class RolloverRolloverConditions(TypedDict):
    min_age: NotRequired[FieldCommonDuration]
    max_age: NotRequired[FieldCommonDuration]
    max_age_millis: NotRequired[FieldCommonDurationValueUnitMillis]
    min_docs: NotRequired[int]
    max_docs: NotRequired[int]
    max_size: NotRequired[FieldCommonHumanReadableByteCount]
    max_size_bytes: NotRequired[FieldCommonByteCount]
    min_size: NotRequired[FieldCommonHumanReadableByteCount]
    min_size_bytes: NotRequired[FieldCommonByteCount]
    max_primary_shard_size: NotRequired[FieldCommonHumanReadableByteCount]
    max_primary_shard_size_bytes: NotRequired[FieldCommonByteCount]
    min_primary_shard_size: NotRequired[FieldCommonHumanReadableByteCount]
    min_primary_shard_size_bytes: NotRequired[FieldCommonByteCount]
    max_primary_shard_docs: NotRequired[int]
    min_primary_shard_docs: NotRequired[int]


class SegmentsIndexSegment(TypedDict):
    shards: dict[str, list[SegmentsShardsSegment] | SegmentsShardsSegment]


class ShardStoresShardStore(TypedDict):
    allocation: ShardStoresShardStoreAllocation
    allocation_id: NotRequired[FieldCommonId]
    store_exception: NotRequired[ShardStoresShardStoreException]


class ShardStoresShardStoreWrapper(TypedDict):
    stores: list[ShardStoresShardStore]


class StatsShardRouting(TypedDict):
    node: str
    primary: bool
    relocating_node: NotRequired[str | None]
    state: StatsShardRoutingState


class FieldCommonDataStream(TypedDict):
    field_meta: NotRequired[FieldCommonMetadata]
    allow_custom_routing: NotRequired[bool]
    generation: int
    hidden: NotRequired[bool]
    ilm_policy: NotRequired[FieldCommonName]
    next_generation_managed_by: NotRequired[FieldCommonManagedBy]
    prefer_ilm: NotRequired[bool]
    indices: list[FieldCommonDataStreamIndex]
    name: FieldCommonDataStreamName
    replicated: NotRequired[bool]
    status: FieldCommonHealthStatus
    system: NotRequired[bool]
    template: FieldCommonName
    timestamp_field: FieldCommonDataStreamTimestampField


class FieldCommonIndexingSlowlog(TypedDict):
    level: NotRequired[str]
    source: NotRequired[FieldCommonStringifiedInteger]
    reformat: NotRequired[FieldCommonStringifiedBoolean]
    threshold: NotRequired[FieldCommonIndexingSlowlogThresholds]


class FieldCommonIndexRouting(TypedDict):
    allocation: NotRequired[FieldCommonIndexRoutingAllocation]
    rebalance: NotRequired[FieldCommonIndexRoutingRebalance]


class FieldCommonIndexSettingsIndexing(TypedDict):
    slowlog: NotRequired[FieldCommonIndexingSlowlog]


FieldCommonIndexSettingsMerge = TypedDict(
    "FieldCommonIndexSettingsMerge",
    {
        "log_byte_size_policy": NotRequired[
            FieldCommonIndexSettingsMergeLogByteSizePolicy
        ],
        "policy": NotRequired[FieldCommonIndexSettingsMergePolicy],
        "policy.deletes_pct_allowed": NotRequired[FieldCommonStringifiedDouble],
        "policy.expunge_deletes_allowed": NotRequired[FieldCommonStringifiedDouble],
        "policy.floor_segment": NotRequired[FieldCommonHumanReadableByteCount],
        "policy.max_merge_at_once": NotRequired[FieldCommonStringifiedInteger],
        "policy.max_merged_segment": NotRequired[FieldCommonHumanReadableByteCount],
        "policy.reclaim_deletes_weight": NotRequired[FieldCommonStringifiedDouble],
        "policy.segments_per_tier": NotRequired[FieldCommonStringifiedDouble],
        "scheduler": NotRequired[FieldCommonIndexSettingsMergeScheduler],
    },
)


class FieldCommonIndexSettingsSimilarity(TypedDict):
    bm25: NotRequired[FieldCommonIndexSettingsSimilarityBm25]
    dfi: NotRequired[FieldCommonIndexSettingsSimilarityDfi]
    dfr: NotRequired[FieldCommonIndexSettingsSimilarityDfr]
    ib: NotRequired[FieldCommonIndexSettingsSimilarityIb]
    lmd: NotRequired[FieldCommonIndexSettingsSimilarityLmd]
    lmj: NotRequired[FieldCommonIndexSettingsSimilarityLmj]
    scripted_tfidf: NotRequired[FieldCommonIndexSettingsSimilarityScriptedTfidf]


class FieldCommonIndexSettingsStarTree(TypedDict):
    default: NotRequired[FieldCommonIndexSettingsStarTreeDefault]
    field: NotRequired[FieldCommonIndexSettingsStarTreeField]
    max_fields: NotRequired[FieldCommonStringifiedInteger]


class FieldCommonIndexSettingsStore(TypedDict):
    type: FieldCommonStorageType
    allow_mmap: NotRequired[FieldCommonStringifiedBoolean]
    fs: NotRequired[FieldCommonIndexSettingsStoreFs]
    hybrid: NotRequired[FieldCommonIndexSettingsStoreHybrid]
    preload: NotRequired[list[str]]
    stats_refresh_interval: NotRequired[FieldCommonDuration]


class FieldCommonIngestionSourcePointer(TypedDict):
    init: NotRequired[FieldCommonIngestionSourcePointerInit]


class FieldCommonSearchSlowlog(TypedDict):
    level: NotRequired[str]
    reformat: NotRequired[bool]
    threshold: NotRequired[FieldCommonSearchSlowlogThresholds]


class AnalyzeAnalyzeDetail(TypedDict):
    analyzer: NotRequired[AnalyzeAnalyzerDetail]
    charfilters: NotRequired[list[AnalyzeCharFilterDetail]]
    custom_analyzer: bool
    tokenfilters: NotRequired[list[AnalyzeTokenDetail]]
    tokenizer: NotRequired[AnalyzeTokenDetail]


class CloseCloseIndexResult(TypedDict):
    closed: bool
    shards: NotRequired[dict[str, CloseCloseShardResult]]


class RecoveryShardRecovery(TypedDict):
    id: int
    index: RecoveryRecoveryIndexStatus
    primary: bool
    source: RecoveryRecoveryOrigin
    stage: str
    start: NotRequired[RecoveryRecoveryStartStatus]
    start_time: NotRequired[FieldCommonDateTime]
    start_time_in_millis: FieldCommonEpochTimeUnitMillis
    stop_time: NotRequired[FieldCommonDateTime]
    stop_time_in_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    target: RecoveryRecoveryOrigin
    total_time: NotRequired[FieldCommonDuration]
    total_time_in_millis: FieldCommonDurationValueUnitMillis
    translog: RecoveryTranslogStatus
    type: str
    verify_index: RecoveryVerifyIndex


class ShardStoresIndicesShardStores(TypedDict):
    shards: dict[str, ShardStoresShardStoreWrapper]


class StatsIndexStatsBase(TypedDict):
    docs: NotRequired[FieldCommonDocStats]
    store: NotRequired[FieldCommonStoreStats]
    indexing: NotRequired[FieldCommonIndexingStats]
    get: NotRequired[FieldCommonGetStats]
    search: NotRequired[FieldCommonSearchStats]
    merges: NotRequired[FieldCommonMergesStats]
    refresh: NotRequired[FieldCommonRefreshStats]
    flush: NotRequired[FieldCommonFlushStats]
    warmer: NotRequired[FieldCommonWarmerStats]
    query_cache: NotRequired[FieldCommonQueryCacheStats]
    fielddata: NotRequired[FieldCommonFielddataStats]
    completion: NotRequired[FieldCommonCompletionStats]
    segments: NotRequired[FieldCommonSegmentsStats]
    translog: NotRequired[FieldCommonTranslogStats]
    request_cache: NotRequired[FieldCommonRequestCacheStats]
    recovery: NotRequired[FieldCommonRecoveryStats]


class FieldCommonIndexSettingsAnalysis(TypedDict):
    analyzer: NotRequired[dict[str, AnalysisAnalyzer]]
    char_filter: NotRequired[dict[str, AnalysisCharFilter]]
    filter: NotRequired[dict[str, AnalysisTokenFilter]]
    normalizer: NotRequired[dict[str, AnalysisNormalizer]]
    tokenizer: NotRequired[dict[str, AnalysisTokenizer]]


class FieldCommonIndexSettingsSearch(TypedDict):
    concurrent: NotRequired[FieldCommonIndexSettingsSearchConcurrent]
    concurrent_segment_search: NotRequired[
        FieldCommonIndexSettingsSearchConcurrentSegmentSearch
    ]
    default_pipeline: NotRequired[str]
    idle: NotRequired[FieldCommonSearchIdle]
    slowlog: NotRequired[FieldCommonSearchSlowlog]
    throttled: NotRequired[FieldCommonStringifiedBoolean]
    star_tree_index: NotRequired[FieldCommonIndexSettingsSearchStarTreeIndex]


FieldCommonErrorPolicy: TypeAlias = Literal["BLOCK", "DROP"]

FieldCommonIngestionSource = TypedDict(
    "FieldCommonIngestionSource",
    {
        "type": NotRequired[FieldCommonIngestionSourceType],
        "pointer": NotRequired[FieldCommonIngestionSourcePointer],
        "pointer.init.reset": NotRequired[FieldCommonIngestionSourcePointerInitReset],
        "pointer.init.reset.value": NotRequired[str],
        "error_strategy": NotRequired[FieldCommonErrorPolicy],
        "poll": NotRequired[FieldCommonIngestionSourcePoll],
        "poll.max_batch_size": NotRequired[FieldCommonStringifiedLong],
        "poll.timeout": NotRequired[FieldCommonStringifiedInteger],
        "num_processor_threads": NotRequired[FieldCommonStringifiedInteger],
        "internal_queue_size": NotRequired[FieldCommonStringifiedInteger],
        "param": NotRequired[dict[str, Any]],
        "all_active": NotRequired[FieldCommonStringifiedBoolean],
    },
)


class RecoveryRecoveryStatus(TypedDict):
    shards: list[RecoveryShardRecovery]


class StatsIndexShardStatsBase(StatsIndexStatsBase):
    routing: NotRequired[StatsShardRouting]
    commit: NotRequired[StatsShardCommit]
    seq_no: NotRequired[StatsShardSequenceNumber]
    retention_leases: NotRequired[StatsShardRetentionLeases]
    shard_path: NotRequired[StatsShardPath]


class StatsIndexStats(StatsIndexStatsBase):
    pass


FieldCommonIndexSettings = TypedDict(
    "FieldCommonIndexSettings",
    {
        "index": NotRequired["FieldCommonIndexSettings"],
        "mode": NotRequired[str],
        "routing_path": NotRequired[FieldCommonStringOrStringArray],
        "soft_deletes": NotRequired[FieldCommonSoftDeletes],
        "soft_deletes.retention_lease.period": NotRequired[FieldCommonDuration],
        "sort": NotRequired[FieldCommonIndexSegmentSort],
        "number_of_shards": NotRequired[FieldCommonStringifiedInteger],
        "number_of_replicas": NotRequired[FieldCommonStringifiedInteger],
        "number_of_routing_shards": NotRequired[FieldCommonStringifiedInteger],
        "check_on_startup": NotRequired[FieldCommonIndexCheckOnStartup],
        "codec": NotRequired[str],
        "routing_partition_size": NotRequired[FieldCommonStringifiedInteger],
        "load_fixed_bitset_filters_eagerly": NotRequired[FieldCommonStringifiedBoolean],
        "hidden": NotRequired[FieldCommonStringifiedBoolean],
        "auto_expand_replicas": NotRequired[str],
        "merge": NotRequired[FieldCommonIndexSettingsMerge],
        "merge.scheduler.max_thread_count": NotRequired[FieldCommonStringifiedInteger],
        "search": NotRequired[FieldCommonIndexSettingsSearch],
        "search.idle.after": NotRequired[FieldCommonDuration],
        "refresh_interval": NotRequired[FieldCommonDuration],
        "max_result_window": NotRequired[FieldCommonStringifiedInteger],
        "max_inner_result_window": NotRequired[FieldCommonStringifiedInteger],
        "max_rescore_window": NotRequired[FieldCommonStringifiedInteger],
        "max_docvalue_fields_search": NotRequired[FieldCommonStringifiedInteger],
        "max_script_fields": NotRequired[FieldCommonStringifiedInteger],
        "max_ngram_diff": NotRequired[FieldCommonStringifiedInteger],
        "max_shingle_diff": NotRequired[FieldCommonStringifiedInteger],
        "blocks": NotRequired[FieldCommonIndexSettingBlocks],
        "blocks.read_only": NotRequired[FieldCommonStringifiedBoolean],
        "blocks.read_only_allow_delete": NotRequired[FieldCommonStringifiedBoolean],
        "blocks.read": NotRequired[FieldCommonStringifiedBoolean],
        "blocks.write": NotRequired[FieldCommonStringifiedBoolean],
        "blocks.metadata": NotRequired[FieldCommonStringifiedBoolean],
        "max_refresh_listeners": NotRequired[FieldCommonStringifiedInteger],
        "analyze": NotRequired[FieldCommonIndexSettingsAnalyze],
        "analyze.max_token_count": NotRequired[FieldCommonStringifiedInteger],
        "highlight": NotRequired[FieldCommonIndexSettingsHighlight],
        "highlight.max_analyzed_offset": NotRequired[FieldCommonStringifiedInteger],
        "max_terms_count": NotRequired[FieldCommonStringifiedInteger],
        "max_regex_length": NotRequired[FieldCommonStringifiedInteger],
        "routing": NotRequired[FieldCommonIndexRouting],
        "gc_deletes": NotRequired[FieldCommonDuration],
        "default_pipeline": NotRequired[FieldCommonPipelineName],
        "final_pipeline": NotRequired[FieldCommonPipelineName],
        "lifecycle": NotRequired[FieldCommonIndexSettingsLifecycle],
        "lifecycle.name": NotRequired[FieldCommonName],
        "provided_name": NotRequired[FieldCommonName],
        "creation_date": NotRequired[FieldCommonStringifiedEpochTimeUnitMillis],
        "creation_date_string": NotRequired[FieldCommonDateTime],
        "uuid": NotRequired[FieldCommonUuid],
        "version": NotRequired[FieldCommonIndexVersioning],
        "verified_before_close": NotRequired[FieldCommonStringifiedBoolean],
        "format": NotRequired[FieldCommonStringifiedInteger],
        "max_slices_per_scroll": NotRequired[FieldCommonStringifiedInteger],
        "translog": NotRequired[FieldCommonTranslog],
        "translog.durability": NotRequired[FieldCommonTranslogDurability],
        "translog.flush_threshold_size": NotRequired[FieldCommonHumanReadableByteCount],
        "query_string": NotRequired[FieldCommonIndexSettingsQueryString],
        "query_string.lenient": NotRequired[FieldCommonStringifiedBoolean],
        "priority": NotRequired[FieldCommonStringifiedInteger],
        "top_metrics_max_size": NotRequired[FieldCommonStringifiedInteger],
        "analysis": NotRequired[FieldCommonIndexSettingsAnalysis],
        "settings": NotRequired["FieldCommonIndexSettings"],
        "queries": NotRequired[FieldCommonIndexSettingsQueries],
        "similarity": NotRequired[FieldCommonIndexSettingsSimilarity],
        "mapping": NotRequired[FieldCommonIndexSettingsMapping],
        "indexing": NotRequired[FieldCommonIndexSettingsIndexing],
        "indexing_pressure": NotRequired[FieldCommonIndexingPressure],
        "store": NotRequired[FieldCommonIndexSettingsStore],
        "knn": NotRequired[FieldCommonStringifiedBoolean],
        "knn.algo_param.ef_search": NotRequired[FieldCommonStringifiedInteger],
        "composite_index.star_tree": NotRequired[FieldCommonIndexSettingsStarTree],
        "ingestion_source": NotRequired[FieldCommonIngestionSource],
        "replication.type": NotRequired[FieldCommonReplicationType],
    },
)


class StatsAllIndicesStats(TypedDict):
    primaries: StatsIndexStats
    total: StatsIndexStats


class StatsIndexShardStats(StatsIndexShardStatsBase):
    pass


class StatsIndicesStats(TypedDict):
    uuid: FieldCommonUuid
    primaries: StatsIndexStats
    total: StatsIndexStats
    shards: NotRequired[dict[str, list[StatsIndexShardStats]]]


class FieldCommonAlias(TypedDict):
    filter: NotRequired[QueryDslQueryContainer]
    index_routing: NotRequired[FieldCommonRouting]
    is_hidden: NotRequired[bool]
    is_write_index: NotRequired[bool]
    routing: NotRequired[FieldCommonRouting]
    search_routing: NotRequired[FieldCommonRouting]


class FieldCommonAliasDefinition(TypedDict):
    filter: NotRequired[QueryDslQueryContainer]
    index_routing: NotRequired[str]
    is_write_index: NotRequired[bool]
    routing: NotRequired[str]
    search_routing: NotRequired[str]
    is_hidden: NotRequired[bool]


class FieldCommonIndexState(TypedDict):
    aliases: NotRequired[dict[str, FieldCommonAlias]]
    mappings: NotRequired[MappingTypeMapping]
    settings: NotRequired[FieldCommonIndexSettings]
    defaults: NotRequired[FieldCommonIndexSettings]
    data_stream: NotRequired[FieldCommonDataStreamName]


class FieldCommonIndexTemplate(TypedDict):
    index_patterns: FieldCommonNames
    composed_of: NotRequired[list[FieldCommonName]]
    template: NotRequired[FieldCommonIndexTemplateSummary]
    version: NotRequired[FieldCommonVersionNumber]
    priority: NotRequired[int]
    field_meta: NotRequired[FieldCommonMetadata]
    allow_auto_create: NotRequired[bool]
    data_stream: NotRequired[FieldCommonIndexTemplateDataStreamConfiguration]


class FieldCommonIndexTemplateSummary(TypedDict):
    aliases: NotRequired[dict[str, FieldCommonAlias]]
    mappings: NotRequired[MappingTypeMapping]
    settings: NotRequired[FieldCommonIndexSettings]


class FieldCommonTemplateMapping(TypedDict):
    aliases: dict[str, FieldCommonAlias]
    index_patterns: list[FieldCommonName]
    mappings: MappingTypeMapping
    order: int
    settings: dict[str, Any]
    version: NotRequired[FieldCommonVersionNumber]


class GetAliasIndexAliases(TypedDict):
    aliases: dict[str, FieldCommonAliasDefinition]


class GetFieldMappingTypeFieldMappings(TypedDict):
    mappings: dict[str, MappingFieldMapping]


class GetIndexTemplateIndexTemplateItem(TypedDict):
    name: FieldCommonName
    index_template: FieldCommonIndexTemplate


class GetMappingIndexMappingRecord(TypedDict):
    item: NotRequired[MappingTypeMapping]
    mappings: MappingTypeMapping


class PutIndexTemplateIndexTemplateMapping(TypedDict):
    aliases: NotRequired[dict[str, FieldCommonAlias]]
    mappings: NotRequired[MappingTypeMapping]
    settings: NotRequired[FieldCommonIndexSettings]


class SimulateTemplateTemplate(TypedDict):
    aliases: dict[str, FieldCommonAlias]
    mappings: NotRequired[MappingTypeMapping]
    settings: FieldCommonIndexSettings


class UpdateAliasesAction(TypedDict):
    add: NotRequired[UpdateAliasesAddAction]
    remove: NotRequired[UpdateAliasesRemoveAction]
    remove_index: NotRequired[UpdateAliasesRemoveIndexAction]


class UpdateAliasesAddAction(TypedDict):
    alias: NotRequired[FieldCommonIndexAlias]
    aliases: NotRequired[FieldCommonIndexAlias | list[FieldCommonIndexAlias]]
    filter: NotRequired[QueryDslQueryContainer]
    index: NotRequired[FieldCommonIndexName]
    indices: NotRequired[FieldCommonIndices]
    index_routing: NotRequired[FieldCommonRouting]
    is_hidden: NotRequired[bool]
    is_write_index: NotRequired[bool]
    routing: NotRequired[FieldCommonRouting]
    search_routing: NotRequired[FieldCommonRouting]
    must_exist: NotRequired[bool]


class FieldCommonIngestionStateShardFailure(TypedDict):
    shard: int
    error: str


class FieldCommonPauseIngestionResponse(TypedDict):
    acknowledged: bool
    shards_acknowledged: bool
    failures: NotRequired[list[FieldCommonIngestionStateShardFailure]]
    error: NotRequired[str]


FieldCommonPollerState: TypeAlias = Literal[
    "CLOSED", "NONE", "PAUSED", "POLLING", "PROCESSING"
]

FieldCommonResetMode: TypeAlias = Literal["OFFSET", "TIMESTAMP"]


class FieldCommonResetSettings(TypedDict):
    shard: int
    mode: FieldCommonResetMode
    value: str


class FieldCommonResumeIngestionRequest(TypedDict):
    reset_settings: NotRequired[list[FieldCommonResetSettings]]


class FieldCommonResumeIngestionResponse(TypedDict):
    acknowledged: bool
    shards_acknowledged: bool
    failures: NotRequired[list[FieldCommonIngestionStateShardFailure]]
    error: NotRequired[str]


class FieldCommonShardIngestionState(TypedDict):
    shard: NotRequired[int]
    poller_state: NotRequired[FieldCommonPollerState]
    error_policy: NotRequired[FieldCommonErrorPolicy]
    poller_paused: NotRequired[bool]
    write_block_enabled: NotRequired[bool]
    batch_start_pointer: NotRequired[str]


class FieldCommonGetIngestionStateResponse(TypedDict):
    ingestion_state: NotRequired[dict[str, list[FieldCommonShardIngestionState]]]
    next_page_token: NotRequired[str]
    field_shards: NotRequired[FieldCommonShardStatistics]


FieldCommonActionType: TypeAlias = Literal["ADD", "DELETE", "UPDATE"]


class FieldCommonAdditionalConfig(TypedDict):
    space_type: NotRequired[str]


class FieldCommonAdditionalInfo(TypedDict):
    pass


FieldCommonAgentType: TypeAlias = Literal[
    "conversational", "conversational_flow", "flow"
]


class FieldCommonAggregation(TypedDict):
    sum: NotRequired[FieldCommonAggregation]
    max: NotRequired[FieldCommonAggregation]
    field: NotRequired[str]


FieldCommonByteOrder: TypeAlias = Literal["BIG_ENDIAN", "LITTLE_ENDIAN"]


class FieldCommonClientConfig(TypedDict):
    max_connection: NotRequired[int]
    connection_timeout: NotRequired[int]
    read_timeout: NotRequired[int]
    retry_backoff_policy: NotRequired[str]
    max_retry_times: NotRequired[int]
    retry_backoff_millis: NotRequired[int]
    retry_timeout_seconds: NotRequired[int]


FieldCommonColumnType: TypeAlias = Literal["BOOLEAN", "DOUBLE", "INTEGER", "STRING"]

FieldCommonConnectorProtocol: TypeAlias = Literal["aws_sigv4", "http"]


class FieldCommonContent(TypedDict):
    text: NotRequired[str]
    type: NotRequired[str]


class FieldCommonCredential(TypedDict):
    access_key: NotRequired[str]
    secret_key: NotRequired[str]
    session_token: NotRequired[str]


class FieldCommonDataAsMap(TypedDict):
    content: NotRequired[str]
    is_last: NotRequired[bool]


class FieldCommonEntity(TypedDict):
    key: NotRequired[list[str]]
    contribution_value: NotRequired[float]
    base_value: NotRequired[float]
    new_value: NotRequired[float]


class FieldCommonExecuteLocalSampleCalculatorResponse(TypedDict):
    result: NotRequired[float]


FieldCommonFunctionName: TypeAlias = Literal[
    "AD_LIBSVM",
    "ad_libsvm",
    "AGENT",
    "agent",
    "ANOMALY_LOCALIZATION",
    "anomaly_localization",
    "BATCH_RCF",
    "batch_rcf",
    "CONNECTOR",
    "connector",
    "FIT_RCF",
    "fit_rcf",
    "KMEANS",
    "kmeans",
    "LINEAR_REGRESSION",
    "linear_regression",
    "LOCAL_SAMPLE_CALCULATOR",
    "local_sample_calculator",
    "LOGISTIC_REGRESSION",
    "logistic_regression",
    "METRICS_CORRELATION",
    "metrics_correlation",
    "QUESTION_ANSWERING",
    "question_answering",
    "RCF_SUMMARIZE",
    "rcf_summarize",
    "REMOTE",
    "remote",
    "SAMPLE_ALGO",
    "sample_algo",
    "SPARSE_ENCODING",
    "sparse_encoding",
    "SPARSE_TOKENIZE",
    "sparse_tokenize",
    "TEXT_EMBEDDING",
    "text_embedding",
    "TEXT_SIMILARITY",
    "text_similarity",
]


class FieldCommonGuardrailsInputOutput(TypedDict):
    model_id: NotRequired[str]
    response_validation_regex: NotRequired[str]


FieldCommonGuardrailsType: TypeAlias = Literal["local_regex", "model"]


class FieldCommonHeaders(TypedDict):
    content_type: NotRequired[str]


class FieldCommonHitsTotal(TypedDict):
    value: int
    relation: str


class FieldCommonIndex(TypedDict):
    number_of_shards: NotRequired[str]
    number_of_replicas: NotRequired[str]


FieldCommonKMeansDistanceType: TypeAlias = Literal["COSINE", "EUCLIDEAN", "L1"]

FieldCommonLocalSampleCalculatorOperation: TypeAlias = Literal["max", "min", "sum"]


class FieldCommonMemory(TypedDict):
    type: NotRequired[str]
    memory_id: NotRequired[FieldCommonName]
    create_time: NotRequired[str]
    updated_time: NotRequired[str]
    name: NotRequired[FieldCommonName]
    user: NotRequired[str]
    additional_info: NotRequired[FieldCommonAdditionalInfo]


class FieldCommonMemoryIndexSettings(TypedDict):
    index: NotRequired[FieldCommonIndex]


FieldCommonMemoryType: TypeAlias = Literal[
    "history", "long-term", "sessions", "working"
]


class FieldCommonMessage(TypedDict):
    memory_id: NotRequired[FieldCommonName]
    message_id: NotRequired[FieldCommonName]
    create_time: NotRequired[str]
    input: NotRequired[str | None]
    prompt_template: NotRequired[str | None]
    response: NotRequired[str | None]
    origin: NotRequired[str | None]
    additional_info: NotRequired[FieldCommonAdditionalInfo]
    parent_message_id: NotRequired[str | None]
    trace_number: NotRequired[int]
    role: NotRequired[str]
    content: NotRequired[list[FieldCommonContent]]


class FieldCommonMessages(TypedDict):
    role: NotRequired[str]
    content: NotRequired[str]


class FieldCommonMetadata_1(TypedDict):
    pass


FieldCommonMlIndexStatus: TypeAlias = Literal["green", "non-existent", "red", "yellow"]

FieldCommonMlInputDataType: TypeAlias = Literal[
    "DATA_FRAME",
    "QUESTION_ANSWERING",
    "REMOTE",
    "SEARCH_QUERY",
    "TEXT_DOCS",
    "TEXT_SIMILARITY",
]

FieldCommonMlResultDataType: TypeAlias = Literal[
    "BOOLEAN",
    "FLOAT16",
    "FLOAT32",
    "FLOAT64",
    "INT32",
    "INT64",
    "INT8",
    "STRING",
    "UINT8",
    "UNKNOWN",
]

FieldCommonMlStatName: TypeAlias = Literal[
    "ml_config_index_status",
    "ml_connector_count",
    "ml_connector_index_status",
    "ml_controller_index_status",
    "ml_model_count",
    "ml_model_index_status",
    "ml_task_index_status",
]

FieldCommonMlTaskType: TypeAlias = Literal[
    "BATCH_INGEST",
    "BATCH_PREDICTION",
    "DEPLOY_MODEL",
    "EXECUTION",
    "PREDICTION",
    "REGISTER_MODEL",
    "TRAINING",
    "TRAINING_AND_PREDICTION",
]


class FieldCommonModelConfig(TypedDict):
    additional_config: NotRequired[FieldCommonAdditionalConfig]
    all_config: NotRequired[str]
    model_type: NotRequired[str]
    embedding_dimension: NotRequired[int]
    framework_type: NotRequired[str]


FieldCommonModelFormat: TypeAlias = Literal["ONNX", "TORCH_SCRIPT"]

FieldCommonModelGroupAccessMode: TypeAlias = Literal["private", "public", "restricted"]


class FieldCommonModelGroupRegistration(TypedDict):
    model_group_id: str
    status: str


FieldCommonModelState: TypeAlias = Literal[
    "DEPLOYED",
    "DEPLOYING",
    "DEPLOY_FAILED",
    "PARTIALLY_DEPLOYED",
    "REGISTERED",
    "REGISTERING",
    "UNDEPLOYED",
]


class FieldCommonModelStats(TypedDict):
    ml_action_request_count: NotRequired[int]
    ml_action_failure_count: NotRequired[int]
    ml_executing_task_count: NotRequired[int]


class FieldCommonNamespace(TypedDict):
    pass


class FieldCommonOwner(TypedDict):
    name: FieldCommonName
    backend_roles: NotRequired[list[str]]
    roles: NotRequired[list[str]]
    custom_attribute_names: NotRequired[list[str]]
    user_requested_tenant: NotRequired[str | None]
    user_requested_tenant_access: NotRequired[str]


class FieldCommonParameters(TypedDict):
    messages: NotRequired[list[FieldCommonMessages]]
    inputs: NotRequired[str]
    field_llm_interface: NotRequired[str]
    question: NotRequired[str]


FieldCommonPayloadType: TypeAlias = Literal["conversational", "data"]


class FieldCommonPredictRequestStats(TypedDict):
    count: NotRequired[int]
    max: NotRequired[float]
    min: NotRequired[float]
    average: NotRequired[float]
    p50: NotRequired[float]
    p90: NotRequired[float]
    p99: NotRequired[float]


class FieldCommonProfileRequest(TypedDict):
    node_ids: NotRequired[list[FieldCommonId]]
    model_ids: NotRequired[list[FieldCommonId]]
    task_ids: NotRequired[list[FieldCommonId]]
    return_all_tasks: NotRequired[bool]
    return_all_models: NotRequired[bool]


FieldCommonRateLimiterUnit: TypeAlias = Literal[
    "DAYS", "HOURS", "MICROSECONDS", "MILLISECONDS", "MINUTES", "NANOSECONDS", "SECONDS"
]

FieldCommonStatus: TypeAlias = Literal[
    "CANCELLED", "COMPLETED", "COMPLETED_WITH_ERROR", "CREATED", "FAILED", "RUNNING"
]


class FieldCommonStrategyConfiguration(TypedDict):
    llm_result_path: NotRequired[str]
    system_prompt: NotRequired[str]
    llm_id: NotRequired[str]


FieldCommonStrategyType: TypeAlias = Literal["SEMANTIC", "SUMMARY", "USER_PREFERENCE"]

FieldCommonTaskState: TypeAlias = Literal[
    "CANCELLED",
    "CANCELLING",
    "COMPLETED",
    "COMPLETED_WITH_ERROR",
    "CREATED",
    "EXPIRED",
    "FAILED",
    "RUNNING",
]


class FieldCommonToolAttributes(TypedDict):
    input_schema: NotRequired[str]
    strict: NotRequired[bool]


class FieldCommonToolItems(TypedDict):
    name: NotRequired[str]
    type: NotRequired[str]
    description: NotRequired[str]
    parameters: NotRequired[FieldCommonParameters]
    include_output_in_agent_response: NotRequired[bool]
    attributes: NotRequired[FieldCommonToolAttributes]


FieldCommonToolName: TypeAlias = Literal[
    "AgentTool",
    "CatIndexTool",
    "ConnectorTool",
    "CreateAnomalyDetectorTool",
    "IndexMappingTool",
    "ListIndexTool",
    "LogPatternTool",
    "MLModelTool",
    "NeuralSparseSearchTool",
    "PPLTool",
    "QueryPlanningTool",
    "RAGTool",
    "ReadFromScratchPadTool",
    "SearchAlertsTool",
    "SearchAnomalyDetectorsTool",
    "SearchAnomalyResultsTool",
    "SearchIndexTool",
    "SearchMonitorsTool",
    "VectorDBTool",
    "VisualizationTool",
    "WriteToScratchPadTool",
]


class FieldCommonTrainParameters(TypedDict):
    centroids: NotRequired[int]
    iterations: NotRequired[int]
    distance_type: NotRequired[FieldCommonKMeansDistanceType]


class FieldCommonTrainResponse(TypedDict):
    model_id: NotRequired[FieldCommonName]
    status: FieldCommonStatus


class FieldCommonUndeployModelNodeStats(TypedDict):
    pass


class FieldCommonUnloadModelNodeStats(TypedDict):
    pass


class FieldCommonUpdateModelGroupResponse(TypedDict):
    status: NotRequired[str]


class FieldCommonValues(TypedDict):
    column_type: NotRequired[FieldCommonColumnType]
    value: NotRequired[float]


class FieldCommonAction(TypedDict):
    action_type: NotRequired[str]
    method: NotRequired[str]
    headers: NotRequired[FieldCommonHeaders]
    url: NotRequired[str]
    request_body: NotRequired[str]
    pre_process_function: NotRequired[str]
    post_process_function: NotRequired[str]


class FieldCommonAlgorithmOperations(TypedDict):
    deploy: NotRequired[FieldCommonModelStats]
    register: NotRequired[FieldCommonModelStats]
    undeploy: NotRequired[FieldCommonModelStats]
    predict: NotRequired[FieldCommonModelStats]
    train: NotRequired[FieldCommonModelStats]
    train_predict: NotRequired[FieldCommonModelStats]
    execute: NotRequired[FieldCommonModelStats]


FieldCommonAlgorithms: TypeAlias = dict[str, FieldCommonAlgorithmOperations]


class FieldCommonBuckets(TypedDict):
    start_time: NotRequired[int]
    end_time: NotRequired[int]
    overall_aggregate_value: NotRequired[float]
    entities: NotRequired[list[FieldCommonEntity]]


class FieldCommonByteBuffer(TypedDict):
    array: NotRequired[str]
    order: NotRequired[FieldCommonByteOrder]


class FieldCommonColumnMeta(TypedDict):
    name: NotRequired[FieldCommonName]
    column_type: NotRequired[FieldCommonColumnType]


class FieldCommonGetAgenticMemoryResponse(TypedDict):
    action: NotRequired[FieldCommonActionType]
    after: NotRequired[dict[str, Any]]
    before: NotRequired[dict[str, Any]]
    created_time: NotRequired[int]
    infer: NotRequired[bool]
    last_updated_time: NotRequired[int]
    memory: NotRequired[str]
    memory_embedding: NotRequired[list[float]]
    memory_id: NotRequired[str]
    memory_container_id: NotRequired[str]
    messages: NotRequired[list[FieldCommonMessage]]
    metadata: NotRequired[FieldCommonMetadata_1]
    namespace: NotRequired[FieldCommonNamespace]
    namespace_size: NotRequired[int]
    owner_id: NotRequired[str]
    payload_type: NotRequired[FieldCommonPayloadType]
    strategy_id: NotRequired[str]
    strategy_type: NotRequired[FieldCommonStrategyType]
    tags: NotRequired[dict[str, Any]]


class FieldCommonGetAgentResponse(TypedDict):
    name: NotRequired[FieldCommonName]
    type: NotRequired[FieldCommonAgentType]
    description: NotRequired[str]
    tools: NotRequired[list[FieldCommonToolItems]]
    created_time: NotRequired[int]
    last_updated_time: NotRequired[int]
    is_hidden: NotRequired[bool]


class FieldCommonGetConnectorResponse(TypedDict):
    name: NotRequired[FieldCommonName]
    version: NotRequired[FieldCommonVersionString]
    description: NotRequired[str]
    protocol: NotRequired[FieldCommonConnectorProtocol]
    parameters: NotRequired[FieldCommonParameters]
    actions: NotRequired[list[FieldCommonAction]]
    created_time: NotRequired[int]
    last_updated_time: NotRequired[int]


class FieldCommonGuardrails(TypedDict):
    type: NotRequired[FieldCommonGuardrailsType]
    input_guardrail: NotRequired[FieldCommonGuardrailsInputOutput]
    output_guardrail: NotRequired[FieldCommonGuardrailsInputOutput]
    stop_words: NotRequired[AnalysisStopWords]
    index_name: NotRequired[FieldCommonIndexName]
    source_fields: NotRequired[FieldCommonFields]
    regex: NotRequired[dict[str, Any]]
    model_id: NotRequired[str]
    response_filter: NotRequired[str]
    response_validation_regex: NotRequired[str]


class FieldCommonIndexSettings_1(TypedDict):
    session_index: NotRequired[FieldCommonMemoryIndexSettings]
    short_term_memory_index: NotRequired[FieldCommonMemoryIndexSettings]
    long_term_memory_index: NotRequired[FieldCommonMemoryIndexSettings]
    long_term_memory_history_index: NotRequired[FieldCommonMemoryIndexSettings]


class FieldCommonLLM(TypedDict):
    model_id: NotRequired[str]
    parameters: NotRequired[FieldCommonParameters]


class FieldCommonModel(TypedDict):
    name: NotRequired[str]
    model_group_id: NotRequired[str]
    algorithm: NotRequired[str]
    model_version: NotRequired[str]
    model_format: NotRequired[FieldCommonModelFormat]
    model_state: FieldCommonModelState
    model_content_size_in_bytes: NotRequired[int]
    model_content_hash_value: NotRequired[str]
    model_config: NotRequired[FieldCommonModelConfig]
    created_time: NotRequired[int]
    last_updated_time: NotRequired[int]
    last_registered_time: NotRequired[int]
    total_chunks: NotRequired[int]
    is_hidden: NotRequired[bool]


class FieldCommonModelGroup(TypedDict):
    name: str
    latest_version: int
    description: str
    owner: NotRequired[FieldCommonOwner]
    access: FieldCommonModelGroupAccessMode
    created_time: NotRequired[int]
    last_updated_time: NotRequired[int]


class FieldCommonModelProfile(TypedDict):
    model_state: NotRequired[FieldCommonModelState]
    predictor: NotRequired[str]
    worker_nodes: NotRequired[list[FieldCommonNodeIds]]
    predict_request_stats: NotRequired[FieldCommonPredictRequestStats]
    target_worker_nodes: NotRequired[list[FieldCommonNodeIds]]
    memory_size_estimation_cpu: NotRequired[int]
    memory_size_estimation_gpu: NotRequired[int]
    deploy: NotRequired[FieldCommonModelStats]
    register: NotRequired[FieldCommonModelStats]
    undeploy: NotRequired[FieldCommonModelStats]
    predict: NotRequired[FieldCommonModelStats]
    train: NotRequired[FieldCommonModelStats]
    train_predict: NotRequired[FieldCommonModelStats]
    execute: NotRequired[FieldCommonModelStats]


FieldCommonModels: TypeAlias = dict[str, FieldCommonModelProfile]


class FieldCommonNodeStatsDetails(TypedDict):
    ml_deployed_model_count: NotRequired[int]
    ml_jvm_heap_usage: NotRequired[int]
    ml_failure_count: NotRequired[int]
    ml_executing_task_count: NotRequired[int]
    ml_circuit_breaker_trigger_count: NotRequired[int]
    ml_request_count: NotRequired[int]
    algorithms: NotRequired[FieldCommonAlgorithms]
    models: NotRequired[FieldCommonModels]


class FieldCommonOutput(TypedDict):
    name: NotRequired[str]
    data_type: NotRequired[FieldCommonMlResultDataType]
    shape: NotRequired[list[int]]
    data: NotRequired[list[float]]
    byte_buffer: NotRequired[FieldCommonByteBuffer]
    result: NotRequired[str]
    dataAsMap: NotRequired[FieldCommonDataAsMap]


class FieldCommonPredictModelOutput(TypedDict):
    name: NotRequired[str]
    data_type: NotRequired[FieldCommonMlResultDataType]
    shape: NotRequired[list[int]]
    data: list[float]
    byte_buffer: NotRequired[FieldCommonByteBuffer]


class FieldCommonPredictModelResult(TypedDict):
    output: NotRequired[list[FieldCommonPredictModelOutput]]


class FieldCommonRateLimiter(TypedDict):
    limit: FieldCommonStringifiedDouble
    unit: FieldCommonRateLimiterUnit


class FieldCommonResult_1(TypedDict):
    buckets: NotRequired[list[FieldCommonBuckets]]


class FieldCommonRows(TypedDict):
    values: NotRequired[list[FieldCommonValues]]


class FieldCommonStrategy(TypedDict):
    type: NotRequired[FieldCommonStrategyType]
    namespace: NotRequired[list[str]]
    configuration: NotRequired[FieldCommonStrategyConfiguration]
    enabled: NotRequired[bool]
    id: NotRequired[str]


class FieldCommonTask(TypedDict):
    model_id: NotRequired[str]
    task_id: NotRequired[str]
    state: FieldCommonTaskState
    task_type: NotRequired[FieldCommonMlTaskType]
    function_name: NotRequired[FieldCommonFunctionName]
    worker_node: NotRequired[list[FieldCommonNodeIds]]
    create_time: NotRequired[int]
    last_update_time: NotRequired[int]
    is_async: NotRequired[bool]
    error: NotRequired[str]


FieldCommonTasks: TypeAlias = dict[str, FieldCommonTask]


class FieldCommonTool(TypedDict):
    name: NotRequired[FieldCommonName]
    description: NotRequired[str]
    type: NotRequired[str]
    version: NotRequired[FieldCommonVersionString]
    attributes: NotRequired[FieldCommonToolAttributes]


class FieldCommonUndeployModelNode(TypedDict):
    stats: NotRequired[FieldCommonUndeployModelNodeStats]


FieldCommonUndeployModelResponse: TypeAlias = dict[str, FieldCommonUndeployModelNode]


class FieldCommonUnloadModelNode(TypedDict):
    stats: NotRequired[FieldCommonUnloadModelNodeStats]


FieldCommonUnloadModelResponse: TypeAlias = dict[str, FieldCommonUnloadModelNode]


class FieldCommonExecuteAnomalyLocalizationResponse(TypedDict):
    name: NotRequired[str]
    result: NotRequired[FieldCommonResult_1]


class FieldCommonInferenceResults(TypedDict):
    output: NotRequired[list[FieldCommonOutput]]


class FieldCommonMemoryContainerConfiguration(TypedDict):
    embedding_model_type: NotRequired[str]
    embedding_model_id: NotRequired[str]
    embedding_dimension: NotRequired[int]
    llm_id: NotRequired[str]
    index_prefix: NotRequired[str]
    use_system_index: NotRequired[bool]
    disable_history: NotRequired[bool]
    disable_session: NotRequired[bool]
    max_infer_size: NotRequired[int]
    index_settings: NotRequired[FieldCommonIndexSettings_1]
    strategies: NotRequired[list[FieldCommonStrategy]]
    parameters: NotRequired[FieldCommonParameters]


class FieldCommonNode(TypedDict):
    tasks: NotRequired[FieldCommonTasks]
    models: NotRequired[FieldCommonModels]


FieldCommonNodes: TypeAlias = dict[str, FieldCommonNode]

FieldCommonNodeStats: TypeAlias = dict[str, FieldCommonNodeStatsDetails]


class FieldCommonPredictionResult(TypedDict):
    column_metas: NotRequired[list[FieldCommonColumnMeta]]
    rows: NotRequired[list[FieldCommonRows]]


class FieldCommonPredictModelResponse(TypedDict):
    inference_results: NotRequired[list[FieldCommonPredictModelResult]]


class FieldCommonPredictResponse(TypedDict):
    inference_results: NotRequired[list[FieldCommonInferenceResults]]
    status: NotRequired[FieldCommonStatus]
    prediction_result: NotRequired[FieldCommonPredictionResult]


class FieldCommonSource(TypedDict):
    last_deployed_time: NotRequired[int]
    model_version: NotRequired[str]
    version: NotRequired[FieldCommonVersionString]
    created_time: NotRequired[int]
    chunk_number: NotRequired[int]
    deploy_to_all_nodes: NotRequired[bool]
    is_hidden: NotRequired[bool]
    model_id: NotRequired[FieldCommonName]
    description: NotRequired[str]
    model_state: NotRequired[FieldCommonModelState]
    model_content_size_in_bytes: NotRequired[int]
    model_content_hash_value: NotRequired[str]
    planning_worker_node_count: NotRequired[float]
    model_config: NotRequired[FieldCommonModelConfig]
    model_format: NotRequired[FieldCommonModelFormat]
    model_task_type: NotRequired[str]
    last_updated_time: NotRequired[int]
    last_update_time: NotRequired[int]
    last_registered_time: NotRequired[int]
    auto_redeploy_retry_times: NotRequired[int]
    name: NotRequired[FieldCommonName]
    connector_id: NotRequired[str]
    current_worker_node_count: NotRequired[float]
    model_group_id: NotRequired[str]
    planning_worker_nodes: NotRequired[list[FieldCommonNodeIds]]
    total_chunks: NotRequired[int]
    algorithm: NotRequired[str]
    url: NotRequired[str]
    backend_roles: NotRequired[list[str]]
    owner: NotRequired[FieldCommonOwner]
    access: NotRequired[FieldCommonModelGroupAccessMode]
    latest_version: NotRequired[int]
    protocol: NotRequired[FieldCommonConnectorProtocol]
    parameters: NotRequired[FieldCommonParameters]
    actions: NotRequired[list[FieldCommonAction]]
    updated_time: NotRequired[str]
    create_time: NotRequired[str | int]
    application_type: NotRequired[str | None]
    additional_info: NotRequired[FieldCommonAdditionalInfo]
    user: NotRequired[str]
    input: NotRequired[str | None]
    memory_id: NotRequired[FieldCommonName]
    trace_number: NotRequired[str | None]
    response: NotRequired[str | None]
    origin: NotRequired[str | None]
    parent_message_id: NotRequired[str | None]
    prompt_template: NotRequired[str | None]
    type: NotRequired[FieldCommonAgentType]
    tools: NotRequired[list[FieldCommonToolItems]]
    memory: NotRequired[FieldCommonMemory]
    app_type: NotRequired[str]
    is_async: NotRequired[bool]
    function_name: NotRequired[FieldCommonFunctionName]
    input_type: NotRequired[FieldCommonMlInputDataType]
    worker_node: NotRequired[list[FieldCommonNodeIds]]
    task_type: NotRequired[FieldCommonMlTaskType]
    state: NotRequired[FieldCommonStatus]
    error: NotRequired[str]
    configuration: NotRequired[FieldCommonMemoryContainerConfiguration]
    payload_type: NotRequired[FieldCommonPayloadType]
    metadata: NotRequired[FieldCommonMetadata_1]
    namespace: NotRequired[FieldCommonNamespace]
    namespace_size: NotRequired[int]
    owner_id: NotRequired[str]


class FieldCommonTrainPredictResponse(TypedDict):
    status: FieldCommonStatus
    prediction_result: NotRequired[FieldCommonPredictionResult]


class FieldCommonDeleteAgenticMemoryResponse(TypedDict):
    took: NotRequired[int]
    timed_out: NotRequired[bool]
    total: NotRequired[int]
    updated: NotRequired[int]
    created: NotRequired[int]
    deleted: NotRequired[int]
    batches: NotRequired[int]
    version_conflicts: NotRequired[int]
    noops: NotRequired[int]
    result: NotRequired[str]
    retries: NotRequired[FieldCommonRetries]
    throttled_millis: NotRequired[int]
    requests_per_second: NotRequired[float]
    throttled_until_millis: NotRequired[int]
    failures: NotRequired[list[FieldCommonBulkByScrollFailure]]


class FieldCommonExecuteAlgorithmResponse(TypedDict):
    results: NotRequired[list[FieldCommonExecuteAnomalyLocalizationResponse]]


FieldCommonExecuteAlgorithmResponseModel: TypeAlias = (
    FieldCommonExecuteLocalSampleCalculatorResponse
    | FieldCommonExecuteAlgorithmResponse
)


class FieldCommonExecuteToolResponse(TypedDict):
    inference_results: NotRequired[list[FieldCommonInferenceResults]]


class FieldCommonGetMemoryContainerResponse(TypedDict):
    name: NotRequired[FieldCommonName]
    description: NotRequired[str]
    owner: NotRequired[FieldCommonOwner]
    created_time: NotRequired[int]
    last_updated_time: NotRequired[int]
    configuration: NotRequired[FieldCommonMemoryContainerConfiguration]


class FieldCommonGetProfileResponse(TypedDict):
    nodes: NotRequired[FieldCommonNodes]


class FieldCommonGetStatsResponse(TypedDict):
    ml_model_count: NotRequired[int]
    ml_connector_index_status: NotRequired[
        Literal["green", "non-existent", "red", "yellow"]
    ]
    ml_config_index_status: NotRequired[
        Literal["green", "non-existent", "red", "yellow"]
    ]
    ml_task_index_status: NotRequired[Literal["green", "non-existent", "red", "yellow"]]
    ml_connector_count: NotRequired[int]
    ml_model_index_status: NotRequired[
        Literal["green", "non-existent", "red", "yellow"]
    ]
    ml_controller_index_status: NotRequired[
        Literal["green", "non-existent", "red", "yellow"]
    ]
    nodes: NotRequired[FieldCommonNodeStats]


class FieldCommonSearchHitsHit(TypedDict):
    field_version: NotRequired[FieldCommonVersionNumber]
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_primary_term: NotRequired[int]
    field_index: NotRequired[FieldCommonIndexName]
    field_id: NotRequired[FieldCommonId]
    field_score: float | None
    field_source: NotRequired[FieldCommonSource]
    model_id: NotRequired[FieldCommonName]
    sort: NotRequired[list[float]]


class FieldCommonSearchHits(TypedDict):
    total: FieldCommonHitsTotal
    hits: list[FieldCommonSearchHitsHit]
    max_score: NotRequired[float | None]


class FieldCommonSearchResponse(TypedDict):
    took: NotRequired[int]
    timed_out: NotRequired[bool]
    field_shards: NotRequired[FieldCommonShardStatistics]
    hits: FieldCommonSearchHits


FieldCommonSearchTasksResponse: TypeAlias = FieldCommonSearchResponse

FieldCommonSearchAgentsResponse: TypeAlias = FieldCommonSearchResponse

FieldCommonSearchConnectorsResponse: TypeAlias = FieldCommonSearchResponse

FieldCommonSearchMemoryResponse: TypeAlias = FieldCommonSearchResponse

FieldCommonSearchMessageResponse: TypeAlias = FieldCommonSearchResponse

FieldCommonSearchModelGroupsResponse: TypeAlias = FieldCommonSearchResponse

FieldCommonSearchModelsResponse: TypeAlias = FieldCommonSearchResponse


class FieldCommonInputQuery(TypedDict):
    field_source: NotRequired[list[str]]
    size: NotRequired[int]
    query: NotRequired[QueryDslQueryContainer]


FieldCommonGroupBy: TypeAlias = Literal["nodes", "none", "parents"]


class FieldCommonPersistentTaskStatus(TypedDict):
    state: str


FieldCommonRawTaskStatus: TypeAlias = dict[str, Any]


class FieldCommonReplicationTaskStatus(TypedDict):
    phase: str


FieldCommonStatus_1: TypeAlias = (
    FieldCommonReplicationTaskStatus
    | FieldCommonBulkByScrollTaskStatus
    | FieldCommonPersistentTaskStatus
    | FieldCommonRawTaskStatus
)


class FieldCommonTaskExecutingNode(FieldCommonBaseNode):
    tasks: dict[str, FieldCommonTaskInfo]


class FieldCommonTaskInfoBase(TypedDict):
    action: str
    cancelled: NotRequired[bool]
    cancellable: bool
    cancellation_time_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    description: NotRequired[str]
    headers: dict[str, str]
    id: int
    node: FieldCommonNodeId
    running_time: NotRequired[FieldCommonDuration]
    running_time_in_nanos: FieldCommonDurationValueUnitNanos
    start_time_in_millis: FieldCommonEpochTimeUnitMillis
    status: NotRequired[FieldCommonStatus_1]
    type: str
    parent_task_id: NotRequired[FieldCommonTaskId]
    resource_stats: NotRequired[FieldCommonResourceStats]


FieldCommonTaskInfos: TypeAlias = Union[
    list["FieldCommonTaskInfo"], dict[str, "FieldCommonTaskGroup"]
]


class FieldCommonTaskListResponseBase(TypedDict):
    node_failures: NotRequired[list[FieldCommonErrorCause]]
    task_failures: NotRequired[list[FieldCommonTaskFailure]]
    nodes: NotRequired[dict[str, FieldCommonTaskExecutingNode]]
    tasks: NotRequired[FieldCommonTaskInfos]


FieldCommonTaskResponse: TypeAlias = FieldCommonBulkByScrollResponseBase


class FieldCommonTaskGroup(FieldCommonTaskInfoBase):
    children: NotRequired[list[FieldCommonTaskGroup]]


class FieldCommonTaskInfo(FieldCommonTaskInfoBase):
    pass
