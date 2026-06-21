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

from typing import Any, Literal, TypeAlias, TypedDict, Union

from typing_extensions import NotRequired

from ._internal import (
    FieldCommonDurationValueUnitMillis,
    FieldCommonEpochTimeUnitMillis,
    FieldCommonId,
    FieldCommonIndexName,
    FieldCommonName,
    FieldCommonNodeId,
)

FieldCommonDataSourceState: TypeAlias = Literal[
    "AVAILABLE", "CREATE_FAILED", "CREATING", "DELETING"
]


FieldCommonGeoJSONDataType: TypeAlias = Literal["Feature", "FeatureCollection"]


FieldCommonGeospatialFieldType: TypeAlias = Literal["geo_point", "geo_shape"]


FieldCommonPointCoordinate: TypeAlias = float


FieldCommonPointCoordinates: TypeAlias = list[FieldCommonPointCoordinate]


FieldCommonPolygonCoordinates: TypeAlias = list[list[FieldCommonPointCoordinates]]


class FieldCommonPutIP2GeoDataSourceRequest(TypedDict):
    endpoint: NotRequired[str]
    update_interval_in_days: NotRequired[int]


class FieldCommonDatabase(TypedDict):
    provider: NotRequired[str]
    sha256_hash: NotRequired[str]
    updated_at_in_epoch_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    valid_for_in_days: NotRequired[int]
    fields: NotRequired[list[str]]


class Database(TypedDict):
    provider: NotRequired[str]
    sha256_hash: NotRequired[str]
    updated_at_in_epoch_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    valid_for_in_days: NotRequired[int]
    fields: NotRequired[list[str]]


class UpdateStats(TypedDict):
    last_succeeded_at_in_epoch_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    last_processing_time_in_millis: NotRequired[FieldCommonEpochTimeUnitMillis]


class FieldCommonDataSource(TypedDict):
    name: FieldCommonName
    state: FieldCommonDataSourceState
    endpoint: str
    update_interval_in_days: int
    next_update_at_in_epoch_millis: FieldCommonEpochTimeUnitMillis
    database: Database
    update_stats: UpdateStats


FieldCommonEnvelope: TypeAlias = list[FieldCommonPointCoordinates]


class FieldCommonGeoSpatialGeojsonUploadResponse(TypedDict):
    took: FieldCommonDurationValueUnitMillis
    errors: bool
    total: int
    success: int
    failure: int


class FieldCommonGetDataSourceResponse(TypedDict):
    datasources: list[FieldCommonDataSource]


FieldCommonLineStringCoordinates: TypeAlias = list[FieldCommonPointCoordinates]


FieldCommonMultiLineStringCoordinates: TypeAlias = list[
    FieldCommonLineStringCoordinates
]


FieldCommonMultiPointCoordinates: TypeAlias = list[FieldCommonPointCoordinates]


FieldCommonMultiPolygonCoordinates: TypeAlias = list[FieldCommonPolygonCoordinates]


class FieldCommonPoint(TypedDict):
    type: Literal["Point"]
    coordinates: FieldCommonPointCoordinates


class FieldCommonPolygon(TypedDict):
    type: Literal["Polygon"]
    coordinates: FieldCommonPolygonCoordinates


class FieldCommonUpdateStats(TypedDict):
    last_succeeded_at_in_epoch_millis: NotRequired[FieldCommonEpochTimeUnitMillis]
    last_processing_time_in_millis: NotRequired[FieldCommonEpochTimeUnitMillis]


class FieldCommonUploadStatsMetric(TypedDict):
    node_id: FieldCommonNodeId
    id: FieldCommonId
    type: str
    upload: int
    success: int
    failed: int
    duration: FieldCommonDurationValueUnitMillis


class FieldCommonUploadStatsTotal(TypedDict):
    request_count: int
    upload: int
    success: int
    failed: int
    duration: FieldCommonDurationValueUnitMillis


class FieldCommonGeoSpatialUploadStats(TypedDict):
    total: FieldCommonUploadStatsTotal
    metrics: list[FieldCommonUploadStatsMetric]


class FieldCommonLineString(TypedDict):
    type: Literal["LineString"]
    coordinates: FieldCommonLineStringCoordinates


class FieldCommonMultiLineString(TypedDict):
    type: Literal["MultiLineString"]
    coordinates: FieldCommonMultiLineStringCoordinates


class FieldCommonMultiPoint(TypedDict):
    type: Literal["MultiPoint"]
    coordinates: FieldCommonMultiPointCoordinates


class FieldCommonMultiPolygon(TypedDict):
    type: Literal["MultiPolygon"]
    coordinates: FieldCommonMultiPolygonCoordinates


FieldCommonGeoShapes: TypeAlias = (
    FieldCommonPoint
    | FieldCommonMultiPoint
    | FieldCommonLineString
    | FieldCommonMultiLineString
    | FieldCommonPolygon
    | FieldCommonMultiPolygon
    | FieldCommonEnvelope
)


class FieldCommonGeoJSONData(TypedDict):
    type: FieldCommonGeoJSONDataType
    geometry: FieldCommonGeometry
    properties: NotRequired[dict[str, Any]]


class FieldCommonGeoJSONRequest(TypedDict):
    index: FieldCommonIndexName
    field: NotRequired[str]
    type: FieldCommonGeospatialFieldType
    data: list[FieldCommonGeoJSONData]


FieldCommonGeometry: TypeAlias = Union[
    FieldCommonGeoShapes, "FieldCommonGeometryCollection"
]


class FieldCommonGeometryCollection(TypedDict):
    type: Literal["GeometryCollection"]
    geometries: list[FieldCommonGeometry]
