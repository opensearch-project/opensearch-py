# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from __future__ import annotations

from typing import Any, Literal, TypeAlias, TypedDict

from typing_extensions import NotRequired

from ._internal import (
    FieldCommonActionStatusOptions,
    FieldCommonDateTime,
    FieldCommonField,
    FieldCommonFields,
    FieldCommonId,
    FieldCommonIndexName,
    FieldCommonMetadata,
    FieldCommonName,
    FieldCommonScript,
    FieldCommonSortOrder,
    FieldCommonStringifiedVersionNumber,
    FieldCommonVersionNumber,
    FieldCommonVersionType,
)

FieldCommonConvertType: TypeAlias = Literal[
    "auto", "boolean", "double", "float", "integer", "long", "string"
]

FieldCommonJsonProcessorConflictStrategy: TypeAlias = Literal["merge", "replace"]

FieldCommonShapeType: TypeAlias = Literal["geo_shape", "xy_shape"]

FieldCommonUserAgentProperty: TypeAlias = Literal[
    "BUILD",
    "DEVICE",
    "MAJOR",
    "MINOR",
    "NAME",
    "OS",
    "OS_MAJOR",
    "OS_MINOR",
    "OS_NAME",
    "PATCH",
]


class SimulateDocument(TypedDict):
    field_id: NotRequired[FieldCommonId]
    field_index: NotRequired[FieldCommonIndexName]
    field_source: Any


class SimulateIngest(TypedDict):
    timestamp: FieldCommonDateTime
    pipeline: NotRequired[FieldCommonName]


class SimulateDocumentSimulation(TypedDict):
    field_id: FieldCommonId
    field_index: FieldCommonIndexName
    field_ingest: SimulateIngest
    field_routing: NotRequired[str]
    field_source: dict[str, Any]
    field_version: NotRequired[FieldCommonStringifiedVersionNumber]
    field_version_type: NotRequired[FieldCommonVersionType]


class SimulatePipelineSimulation(TypedDict):
    doc: NotRequired[SimulateDocumentSimulation]
    processor_results: NotRequired[list[SimulatePipelineSimulation]]
    tag: NotRequired[str]
    processor_type: NotRequired[str]
    status: NotRequired[FieldCommonActionStatusOptions]


class FieldCommonPipeline(TypedDict):
    description: NotRequired[str]
    on_failure: NotRequired[list[FieldCommonProcessorContainer]]
    processors: NotRequired[list[FieldCommonProcessorContainer]]
    version: NotRequired[FieldCommonVersionNumber]
    field_meta: NotRequired[FieldCommonMetadata]


class FieldCommonProcessorContainer(TypedDict):
    attachment: NotRequired[FieldCommonAttachmentProcessor]
    append: NotRequired[FieldCommonAppendProcessor]
    csv: NotRequired[FieldCommonCsvProcessor]
    convert: NotRequired[FieldCommonConvertProcessor]
    date: NotRequired[FieldCommonDateProcessor]
    date_index_name: NotRequired[FieldCommonDateIndexNameProcessor]
    dot_expander: NotRequired[FieldCommonDotExpanderProcessor]
    fail: NotRequired[FieldCommonFailProcessor]
    foreach: NotRequired[FieldCommonForeachProcessor]
    json: NotRequired[FieldCommonJsonProcessor]
    user_agent: NotRequired[FieldCommonUserAgentProcessor]
    kv: NotRequired[FieldCommonKeyValueProcessor]
    geoip: NotRequired[FieldCommonGeoIpProcessor]
    grok: NotRequired[FieldCommonGrokProcessor]
    gsub: NotRequired[FieldCommonGsubProcessor]
    join: NotRequired[FieldCommonJoinProcessor]
    lowercase: NotRequired[FieldCommonLowercaseProcessor]
    remove: NotRequired[FieldCommonRemoveProcessor]
    rename: NotRequired[FieldCommonRenameProcessor]
    script: NotRequired[FieldCommonScript]
    set: NotRequired[FieldCommonSetProcessor]
    sort: NotRequired[FieldCommonSortProcessor]
    split: NotRequired[FieldCommonSplitProcessor]
    trim: NotRequired[FieldCommonTrimProcessor]
    uppercase: NotRequired[FieldCommonUppercaseProcessor]
    urldecode: NotRequired[FieldCommonUrlDecodeProcessor]
    bytes: NotRequired[FieldCommonBytesProcessor]
    dissect: NotRequired[FieldCommonDissectProcessor]
    set_security_user: NotRequired[FieldCommonSetSecurityUserProcessor]
    pipeline: NotRequired[FieldCommonPipelineProcessor]
    drop: NotRequired[FieldCommonDropProcessor]
    circle: NotRequired[FieldCommonCircleProcessor]
    text_embedding: NotRequired[FieldCommonTextEmbeddingProcessor]


FieldCommonProcessorBase = TypedDict(
    "FieldCommonProcessorBase",
    {
        "description": NotRequired[str],
        "if": NotRequired[str],
        "ignore_failure": NotRequired[bool],
        "on_failure": NotRequired[list[FieldCommonProcessorContainer]],
        "tag": NotRequired[str],
    },
)


class FieldCommonAppendProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    value: list[Any]
    allow_duplicates: NotRequired[bool]


class FieldCommonAttachmentProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    indexed_chars: NotRequired[int]
    indexed_chars_field: NotRequired[FieldCommonField]
    properties: NotRequired[list[str]]
    target_field: NotRequired[FieldCommonField]
    resource_name: NotRequired[str]


class FieldCommonBytesProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    target_field: NotRequired[FieldCommonField]


class FieldCommonCircleProcessor(FieldCommonProcessorBase):
    error_distance: float
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    shape_type: FieldCommonShapeType
    target_field: NotRequired[FieldCommonField]


class FieldCommonConvertProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    target_field: NotRequired[FieldCommonField]
    type: FieldCommonConvertType


class FieldCommonCsvProcessor(FieldCommonProcessorBase):
    empty_value: NotRequired[Any]
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    quote: NotRequired[str]
    separator: NotRequired[str]
    target_fields: FieldCommonFields
    trim: NotRequired[bool]


class FieldCommonDateIndexNameProcessor(FieldCommonProcessorBase):
    date_formats: list[str]
    date_rounding: str
    field: FieldCommonField
    index_name_format: NotRequired[str]
    index_name_prefix: NotRequired[str]
    locale: NotRequired[str]
    timezone: NotRequired[str]


class FieldCommonDateProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    formats: list[str]
    locale: NotRequired[str]
    target_field: NotRequired[FieldCommonField]
    timezone: NotRequired[str]


class FieldCommonDissectProcessor(FieldCommonProcessorBase):
    append_separator: NotRequired[str]
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    pattern: str


class FieldCommonDotExpanderProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    path: NotRequired[str]


class FieldCommonDropProcessor(FieldCommonProcessorBase):
    pass


class FieldCommonFailProcessor(FieldCommonProcessorBase):
    message: str


class FieldCommonForeachProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    processor: FieldCommonProcessorContainer


class FieldCommonGeoIpProcessor(FieldCommonProcessorBase):
    database_file: NotRequired[str]
    field: FieldCommonField
    first_only: NotRequired[bool]
    ignore_missing: NotRequired[bool]
    properties: NotRequired[list[str]]
    target_field: NotRequired[FieldCommonField]


class FieldCommonGrokProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    pattern_definitions: NotRequired[dict[str, str]]
    patterns: list[str]
    trace_match: NotRequired[bool]


class FieldCommonGsubProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    pattern: str
    replacement: str
    target_field: NotRequired[FieldCommonField]


class FieldCommonJoinProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    separator: str
    target_field: NotRequired[FieldCommonField]


class FieldCommonJsonProcessor(FieldCommonProcessorBase):
    add_to_root: NotRequired[bool]
    add_to_root_conflict_strategy: NotRequired[FieldCommonJsonProcessorConflictStrategy]
    allow_duplicate_keys: NotRequired[bool]
    field: FieldCommonField
    target_field: NotRequired[FieldCommonField]


class FieldCommonKeyValueProcessor(FieldCommonProcessorBase):
    exclude_keys: NotRequired[list[str]]
    field: FieldCommonField
    field_split: str
    ignore_missing: NotRequired[bool]
    include_keys: NotRequired[list[str]]
    prefix: NotRequired[str]
    strip_brackets: NotRequired[bool]
    target_field: NotRequired[FieldCommonField]
    trim_key: NotRequired[str]
    trim_value: NotRequired[str]
    value_split: str


class FieldCommonLowercaseProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    target_field: NotRequired[FieldCommonField]


class FieldCommonPipelineProcessor(FieldCommonProcessorBase):
    name: FieldCommonName
    ignore_missing_pipeline: NotRequired[bool]


class FieldCommonRemoveProcessor(FieldCommonProcessorBase):
    field: FieldCommonFields
    ignore_missing: NotRequired[bool]


class FieldCommonRenameProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    target_field: FieldCommonField


class FieldCommonSetProcessor(FieldCommonProcessorBase):
    copy_from: NotRequired[FieldCommonField]
    field: FieldCommonField
    ignore_empty_value: NotRequired[bool]
    media_type: NotRequired[str]
    override: NotRequired[bool]
    value: NotRequired[Any]


class FieldCommonSetSecurityUserProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    properties: NotRequired[list[str]]


class FieldCommonSortProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    order: NotRequired[FieldCommonSortOrder]
    target_field: NotRequired[FieldCommonField]


class FieldCommonSplitProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    preserve_trailing: NotRequired[bool]
    separator: str
    target_field: NotRequired[FieldCommonField]


class FieldCommonTextEmbeddingProcessor(FieldCommonProcessorBase):
    model_id: FieldCommonId
    field_map: dict[str, str]
    batch_size: NotRequired[int]


class FieldCommonTrimProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    target_field: NotRequired[FieldCommonField]


class FieldCommonUppercaseProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    target_field: NotRequired[FieldCommonField]


class FieldCommonUrlDecodeProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    target_field: NotRequired[FieldCommonField]


class FieldCommonUserAgentProcessor(FieldCommonProcessorBase):
    field: FieldCommonField
    ignore_missing: NotRequired[bool]
    options: NotRequired[list[FieldCommonUserAgentProperty]]
    regex_file: NotRequired[str]
    target_field: NotRequired[FieldCommonField]
