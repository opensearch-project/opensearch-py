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


class FieldCommonQueryFilter(TypedDict):
    query: str
    language: str


class FieldCommonSelectedDateRange(TypedDict):
    start: str
    end: str
    text: str


class FieldCommonSelectedTimestamp(TypedDict):
    name: str
    type: str


FieldCommonTimeRange = TypedDict(
    "FieldCommonTimeRange",
    {
        "to": str,
        "from": str,
    },
)


class FieldCommonToken(TypedDict):
    name: str
    type: str


class FieldCommonVisualization(TypedDict):
    id: str
    savedVisualizationId: str
    x: int
    y: int
    w: int
    h: int


class FieldCommonOperationalPanel(TypedDict):
    name: str
    visualizations: list[FieldCommonVisualization]
    timeRange: FieldCommonTimeRange
    queryFilter: FieldCommonQueryFilter
    applicationId: str


class FieldCommonSelectedFields(TypedDict):
    text: str
    tokens: list[FieldCommonToken]


class FieldCommonSavedQuery(TypedDict):
    name: str
    description: str
    query: str
    selected_date_range: FieldCommonSelectedDateRange
    selected_timestamp: FieldCommonSelectedTimestamp
    selected_fields: FieldCommonSelectedFields


class FieldCommonSavedVisualization(TypedDict):
    name: str
    description: str
    query: str
    type: str
    selected_date_range: FieldCommonSelectedDateRange
    selected_timestamp: FieldCommonSelectedTimestamp
    selected_fields: FieldCommonSelectedFields


class FieldCommonObservabilityObject(TypedDict):
    objectId: str
    lastUpdatedTimeMs: NotRequired[int]
    createdTimeMs: NotRequired[int]
    tenant: NotRequired[str]
    operationalPanel: NotRequired[FieldCommonOperationalPanel]
    savedVisualization: NotRequired[FieldCommonSavedVisualization]
    savedQuery: NotRequired[FieldCommonSavedQuery]


class FieldCommonObservabilityObjectList(TypedDict):
    startIndex: int
    totalHits: int
    totalHitRelation: str
    observabilityObjectList: list[FieldCommonObservabilityObject]
