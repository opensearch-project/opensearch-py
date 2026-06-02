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


class FieldCommonCronExpression(TypedDict):
    expression: str
    timezone: str


class FieldCommonCronSchedule(TypedDict):
    cron: NotRequired[FieldCommonCronExpression]


class FieldCommonDeletionCondition(TypedDict):
    max_age: NotRequired[str]
    max_count: NotRequired[int]
    min_count: NotRequired[int]


class FieldCommonDeletionConfig(TypedDict):
    schedule: NotRequired[FieldCommonCronSchedule]
    condition: NotRequired[FieldCommonDeletionCondition]
    time_limit: NotRequired[str]


class FieldCommonExecutionInfo(TypedDict):
    message: NotRequired[str]
    cause: NotRequired[str]


class FieldCommonExecutionMetadata(TypedDict):
    info: NotRequired[FieldCommonExecutionInfo]


FieldCommonIntervalUnit: TypeAlias = Literal["Days", "Hours", "Minutes"]


class FieldCommonNotificationChannel(TypedDict):
    id: str


class FieldCommonNotificationConditions(TypedDict):
    creation: NotRequired[bool]
    deletion: NotRequired[bool]
    failure: NotRequired[bool]
    time_limit_exceeded: NotRequired[bool]


class FieldCommonNotificationConfig(TypedDict):
    channel: NotRequired[FieldCommonNotificationChannel]
    conditions: NotRequired[FieldCommonNotificationConditions]


class FieldCommonRetryMetadata(TypedDict):
    count: NotRequired[int]


class FieldCommonSnapshotConfig(TypedDict):
    date_format: NotRequired[str]
    timezone: NotRequired[str]
    indices: NotRequired[str]
    repository: str
    ignore_unavailable: NotRequired[bool]
    include_global_state: NotRequired[bool]
    partial: NotRequired[bool]
    metadata: NotRequired[dict[str, str]]


class FieldCommonTriggerMetadata(TypedDict):
    time: NotRequired[int]


class FieldCommonCreationConfig(TypedDict):
    schedule: FieldCommonCronSchedule
    time_limit: NotRequired[str]


class FieldCommonIntervalConfig(TypedDict):
    start_time: int
    period: int
    unit: FieldCommonIntervalUnit


class FieldCommonIntervalSchedule(TypedDict):
    interval: NotRequired[FieldCommonIntervalConfig]


class FieldCommonSMPolicy(TypedDict):
    name: str
    description: str
    schema_version: NotRequired[int]
    creation: FieldCommonCreationConfig
    deletion: NotRequired[FieldCommonDeletionConfig]
    snapshot_config: FieldCommonSnapshotConfig
    notification: NotRequired[FieldCommonNotificationConfig]
    schedule: NotRequired[FieldCommonIntervalSchedule]
    enabled: NotRequired[bool]
    last_updated_time: NotRequired[int]
    enabled_time: NotRequired[int]


class FieldCommonStateMetadata(TypedDict):
    current_state: NotRequired[str]
    trigger: NotRequired[FieldCommonTriggerMetadata]
    latest_execution: NotRequired[FieldCommonExecutionMetadata]
    retry: NotRequired[FieldCommonRetryMetadata]


class FieldCommonCreateUpdatePolicyRequest(TypedDict):
    description: NotRequired[str]
    creation: FieldCommonCreationConfig
    deletion: NotRequired[FieldCommonDeletionConfig]
    snapshot_config: FieldCommonSnapshotConfig
    notification: NotRequired[FieldCommonNotificationConfig]
    enabled: NotRequired[bool]


class FieldCommonExplainedPolicy(TypedDict):
    name: NotRequired[str]
    creation: NotRequired[FieldCommonStateMetadata]
    deletion: NotRequired[FieldCommonStateMetadata]
    policy_seq_no: NotRequired[int]
    policy_primary_term: NotRequired[int]
    enabled: NotRequired[bool]


class FieldCommonListedPolicy(TypedDict):
    field_id: str
    field_seq_no: NotRequired[int]
    field_primary_term: NotRequired[int]
    sm_policy: FieldCommonSMPolicy


class FieldCommonPolicyExplanation(TypedDict):
    policies: NotRequired[list[FieldCommonExplainedPolicy]]


class FieldCommonPolicyResponse(TypedDict):
    field_id: str
    field_version: int
    field_seq_no: int
    field_primary_term: int
    sm_policy: FieldCommonSMPolicy


class FieldCommonGetPoliciesResponse(TypedDict):
    total_policies: int
    policies: list[FieldCommonListedPolicy]
