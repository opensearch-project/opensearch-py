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

from typing import Any, TypeAlias, TypedDict

from typing_extensions import NotRequired

from ._internal import (
    FieldCommonId,
    FieldCommonSequenceNumber,
    FieldCommonVersionNumber,
    QueryDslQueryContainer,
)


class FieldCommonContinuousStats(TypedDict):
    last_timestamp: NotRequired[float]
    documents_behind: NotRequired[dict[str, float]]


class FieldCommonDateHistogramGroup(TypedDict):
    fixed_interval: NotRequired[str]
    calendar_interval: NotRequired[str]
    timezone: NotRequired[str]
    source_field: NotRequired[str]
    target_field: NotRequired[str]


class FieldCommonExplainStats(TypedDict):
    pages_processed: NotRequired[float]
    documents_processed: NotRequired[float]
    documents_indexed: NotRequired[float]
    index_time_in_millis: NotRequired[float]
    search_time_in_millis: NotRequired[float]


class FieldCommonHistogramGroup(TypedDict):
    source_field: NotRequired[str]
    target_field: NotRequired[str]
    interval: NotRequired[str]


class FieldCommonPreview(TypedDict):
    documents: NotRequired[list[dict[str, Any]]]


class FieldCommonScheduleInterval(TypedDict):
    start_time: NotRequired[float]
    period: NotRequired[float]
    unit: NotRequired[str]


class FieldCommonTermsGroup(TypedDict):
    source_field: NotRequired[str]
    target_field: NotRequired[str]


class FieldCommonTransformMetadata(TypedDict):
    continuous_stats: NotRequired[FieldCommonContinuousStats]
    transform_id: NotRequired[str]
    last_updated_at: NotRequired[float]
    status: NotRequired[str]
    failure_reason: NotRequired[str]
    stats: NotRequired[FieldCommonExplainStats]


class FieldCommonExplain(TypedDict):
    metadata_id: NotRequired[str | None]
    transform_metadata: NotRequired[FieldCommonTransformMetadata | None]


FieldCommonExplainResponse: TypeAlias = dict[str, FieldCommonExplain]


class FieldCommonGroupsConfigItem(TypedDict):
    histogram: NotRequired[FieldCommonHistogramGroup]
    date_histogram: NotRequired[FieldCommonDateHistogramGroup]
    terms: NotRequired[FieldCommonTermsGroup]


class FieldCommonSchedule(TypedDict):
    interval: FieldCommonScheduleInterval


class FieldCommonTransform(TypedDict):
    transform_id: NotRequired[str]
    schema_version: NotRequired[float]
    continuous: NotRequired[bool]
    schedule: NotRequired[FieldCommonSchedule]
    metadata_id: NotRequired[str | None]
    updated_at: NotRequired[float]
    enabled: NotRequired[bool]
    enabled_at: NotRequired[float | None]
    description: NotRequired[str]
    source_index: NotRequired[str]
    data_selection_query: NotRequired[QueryDslQueryContainer]
    target_index: NotRequired[str]
    roles: NotRequired[list[str]]
    page_size: NotRequired[float]
    groups: NotRequired[list[FieldCommonGroupsConfigItem]]
    aggregations: NotRequired[dict[str, FieldCommonGroupsConfigItem]]


class FieldCommonTransformRequest(TypedDict):
    transform: FieldCommonTransform


class FieldCommonTransformResponse(TypedDict):
    field_id: NotRequired[FieldCommonId]
    field_primary_term: NotRequired[int]
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_version: NotRequired[FieldCommonVersionNumber]
    transform: NotRequired[FieldCommonTransform]


class FieldCommonTransformsResponse(TypedDict):
    total_transforms: NotRequired[float]
    transforms: NotRequired[list[FieldCommonTransformResponse]]
