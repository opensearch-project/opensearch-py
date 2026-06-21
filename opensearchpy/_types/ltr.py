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

from ._internal import FieldCommonName, FieldCommonNodeStatistics
from .nodes import FieldCommonNodesResponseBase


class FieldCommonAcknowledgedResponse(TypedDict):
    acknowledged: NotRequired[bool]
    shards_acknowledged: NotRequired[bool]
    index: NotRequired[str]


class FieldCommonCacheItemStats(TypedDict):
    ram: NotRequired[int]
    count: NotRequired[int]


class FieldCommonCacheStat(TypedDict):
    eviction_count: NotRequired[int]
    miss_count: NotRequired[int]
    entry_count: NotRequired[int]
    memory_usage_in_bytes: NotRequired[int]
    hit_count: NotRequired[int]


class FieldCommonCacheStats(TypedDict):
    feature: NotRequired[FieldCommonCacheStat]
    featureset: NotRequired[FieldCommonCacheStat]
    model: NotRequired[FieldCommonCacheStat]


FieldCommonLtrStatName: TypeAlias = Literal[
    "cache", "request_error_count", "request_total_count", "status", "stores"
]


class FieldCommonNodeStats(TypedDict):
    cache: NotRequired[FieldCommonCacheStats]
    request_total_count: NotRequired[int]
    request_error_count: NotRequired[int]


class FieldCommonNodeStatsDetails(TypedDict):
    total: NotRequired[FieldCommonCacheItemStats]
    features: NotRequired[FieldCommonCacheItemStats]
    featuresets: NotRequired[FieldCommonCacheItemStats]
    models: NotRequired[FieldCommonCacheItemStats]


class FieldCommonNotFoundResponse(TypedDict):
    field_index: NotRequired[str]
    field_id: NotRequired[str]
    found: NotRequired[bool]


class FieldCommonStoreDetails(TypedDict):
    store: NotRequired[str]
    index: NotRequired[str]
    version: NotRequired[int]
    counts: NotRequired[dict[str, Any]]


class FieldCommonStoreExistsResponse(TypedDict):
    exists: NotRequired[bool]


class FieldCommonStoreStat(TypedDict):
    model_count: NotRequired[int]
    featureset_count: NotRequired[int]
    feature_count: NotRequired[int]
    status: NotRequired[str]


FieldCommonStoreStats: TypeAlias = dict[str, FieldCommonStoreStat]


class FieldCommonCacheAllStats(TypedDict):
    total: NotRequired[FieldCommonCacheItemStats]
    features: NotRequired[FieldCommonCacheItemStats]
    featuresets: NotRequired[FieldCommonCacheItemStats]
    models: NotRequired[FieldCommonCacheItemStats]


class FieldCommonListStoresResponse(TypedDict):
    stores: dict[str, FieldCommonStoreDetails]


class FieldCommonNodeDetails(TypedDict):
    name: NotRequired[str]
    hostname: NotRequired[str]
    stats: NotRequired[FieldCommonNodeStatsDetails]


class FieldCommonCacheStatsResponse(TypedDict):
    field_nodes: NotRequired[FieldCommonNodeStatistics]
    cluster_name: NotRequired[FieldCommonName]
    all: NotRequired[FieldCommonCacheAllStats]
    stores: NotRequired[dict[str, Any]]
    nodes: NotRequired[dict[str, FieldCommonNodeDetails]]


class FieldCommonStats(FieldCommonNodesResponseBase):
    cluster_name: NotRequired[FieldCommonName]
    stores: NotRequired[FieldCommonStoreStats]
    status: NotRequired[str]
    nodes: NotRequired[dict[str, FieldCommonNodeStats]]
