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
    FieldCommonIndexSettings,
    FieldCommonSequenceNumber,
    FieldCommonVersionNumber,
)


class FieldCommonCron(TypedDict):
    expression: NotRequired[str]
    timezone: NotRequired[str]


class FieldCommonDateHistogramDimension(TypedDict):
    fixed_interval: NotRequired[str]
    calendar_interval: NotRequired[str]
    timezone: NotRequired[str]
    source_field: NotRequired[str]
    target_field: NotRequired[str]
    format: NotRequired[str | None]


class FieldCommonExplain(TypedDict):
    metadata_id: NotRequired[str | None]
    rollup_metadata: NotRequired[dict[str, Any] | None]


FieldCommonExplainEntities: TypeAlias = dict[str, FieldCommonExplain]


class FieldCommonHistogramDimension(TypedDict):
    source_field: NotRequired[str]
    target_field: NotRequired[str]
    interval: NotRequired[str]


class FieldCommonInterval(TypedDict):
    start_time: NotRequired[float]
    period: NotRequired[float]
    unit: NotRequired[str]
    cron: NotRequired[list[FieldCommonCron] | FieldCommonCron]
    schedule_delay: NotRequired[float]


class FieldCommonMetricsConfigMetrics(TypedDict):
    avg: NotRequired[dict[str, Any]]
    sum: NotRequired[dict[str, Any]]
    max: NotRequired[dict[str, Any]]
    min: NotRequired[dict[str, Any]]
    value_count: NotRequired[dict[str, Any]]


class FieldCommonSchedule(TypedDict):
    interval: NotRequired[FieldCommonInterval]


class FieldCommonTermsDimension(TypedDict):
    source_field: NotRequired[str]
    target_field: NotRequired[str]


class FieldCommonDimensionsConfigItem(TypedDict):
    histogram: NotRequired[FieldCommonHistogramDimension]
    date_histogram: NotRequired[FieldCommonDateHistogramDimension]
    terms: NotRequired[FieldCommonTermsDimension]


class FieldCommonMetricsConfigItem(TypedDict):
    source_field: NotRequired[str]
    target_field: NotRequired[str]
    metrics: NotRequired[list[FieldCommonMetricsConfigMetrics]]


class FieldCommonRollup(TypedDict):
    rollup_id: NotRequired[str]
    enabled: NotRequired[bool]
    schedule: NotRequired[FieldCommonSchedule]
    last_updated_time: NotRequired[float]
    enabled_time: NotRequired[float]
    description: NotRequired[str]
    schema_version: NotRequired[float]
    source_index: NotRequired[str]
    target_index: NotRequired[str]
    target_index_settings: NotRequired[FieldCommonIndexSettings]
    metadata_id: NotRequired[str | None]
    page_size: NotRequired[float]
    delay: NotRequired[float]
    continuous: NotRequired[bool]
    dimensions: NotRequired[list[FieldCommonDimensionsConfigItem]]
    metrics: NotRequired[list[FieldCommonMetricsConfigItem]]
    error_notification: NotRequired[str]


class FieldCommonRollupEntity(TypedDict):
    field_id: NotRequired[FieldCommonId]
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_primary_term: NotRequired[int]
    field_version: NotRequired[FieldCommonVersionNumber]
    rollup: NotRequired[FieldCommonRollup]
