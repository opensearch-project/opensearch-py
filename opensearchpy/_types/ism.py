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
    FieldCommonShardStatistics,
    FieldCommonVersionNumber,
    FieldCommonWriteResponseBase,
)


class FieldCommonActionAlias(TypedDict):
    actions: NotRequired[dict[str, Any]]


class FieldCommonActionAllocation(TypedDict):
    require: NotRequired[dict[str, Any]]
    include: NotRequired[dict[str, Any]]
    exclude: NotRequired[dict[str, Any]]
    wait_for: NotRequired[bool]


class FieldCommonActionClose(TypedDict):
    pass


class FieldCommonActionCustom(TypedDict):
    pass


class FieldCommonActionDelete(TypedDict):
    pass


class FieldCommonActionForceMerge(TypedDict):
    max_num_segments: NotRequired[int]


class FieldCommonActionIndexPriority(TypedDict):
    priority: NotRequired[float]


class FieldCommonActionNotification(TypedDict):
    pass


class FieldCommonActionOpen(TypedDict):
    pass


class FieldCommonActionReadOnly(TypedDict):
    pass


class FieldCommonActionReadWrite(TypedDict):
    pass


class FieldCommonActionReplicaCount(TypedDict):
    number_of_replicas: NotRequired[float]


class FieldCommonActionRetry(TypedDict):
    count: NotRequired[int]
    backoff: NotRequired[str]
    delay: NotRequired[str]


class FieldCommonActionRollover(TypedDict):
    min_size: NotRequired[str]
    min_index_age: NotRequired[str]
    min_doc_count: NotRequired[float]
    min_primary_shard_size: NotRequired[str]
    copy_alias: NotRequired[bool]


class FieldCommonActionRollup(TypedDict):
    pass


class FieldCommonActionShrink(TypedDict):
    pass


class FieldCommonActionSnapshot(TypedDict):
    repository: NotRequired[str]
    snapshot: NotRequired[str]
    include_global_state: NotRequired[bool]


class FieldCommonActionTimeout(TypedDict):
    timeout: NotRequired[dict[str, Any]]


class FieldCommonActionTransform(TypedDict):
    pass


class FieldCommonAddPolicyRequest(TypedDict):
    policy_id: str


class FieldCommonChannel(TypedDict):
    id: NotRequired[str]


class FieldCommonErrorNotificationChime(TypedDict):
    url: NotRequired[str]


class FieldCommonErrorNotificationDestination(TypedDict):
    name: NotRequired[str]
    last_update_time: NotRequired[int]


class FieldCommonExplainIndexResponse(TypedDict):
    total_managed_indices: NotRequired[float]


FieldCommonExplainPolicy = TypedDict(
    "FieldCommonExplainPolicy",
    {
        "index.plugins.index_state_management.policy_id": NotRequired[str | None],
        "index.opendistro.index_state_management.policy_id": NotRequired[str | None],
        "enabled": NotRequired[bool | None],
    },
)


class FieldCommonFailedIndex(TypedDict):
    index_name: NotRequired[str]
    index_uuid: NotRequired[str]
    reason: NotRequired[str]


class FieldCommonIncludeState(TypedDict):
    state: NotRequired[str]


class FieldCommonIsmTemplate(TypedDict):
    index_patterns: NotRequired[list[str]]
    priority: NotRequired[float]
    last_updated_time: NotRequired[int]


class FieldCommonMetadata(TypedDict):
    field_id: NotRequired[FieldCommonId]
    field_primary_term: NotRequired[float]
    field_seq_no: NotRequired[FieldCommonSequenceNumber]
    field_version: NotRequired[FieldCommonVersionNumber]


class FieldCommonRefreshSearchAnalyzersResponseDetails(TypedDict):
    index: NotRequired[str]
    refreshed_analyzers: NotRequired[list[str]]


class FieldCommonRetryIndexRequest(TypedDict):
    state: str


class FieldCommonSlackCustomWebhook(TypedDict):
    url: NotRequired[str]
    scheme: NotRequired[str]
    host: NotRequired[str]
    port: NotRequired[int]
    path: NotRequired[str]
    query_params: NotRequired[dict[str, Any]]
    header_params: NotRequired[dict[str, Any]]
    username: NotRequired[str]
    password: NotRequired[str]


class FieldCommonTransition(TypedDict):
    state_name: NotRequired[str]
    conditions: NotRequired[dict[str, Any]]


class FieldCommonAction(TypedDict):
    timeout: NotRequired[FieldCommonActionTimeout]
    retry: NotRequired[FieldCommonActionRetry]
    alias: NotRequired[FieldCommonActionAlias]
    delete: NotRequired[FieldCommonActionDelete]
    force_merge: NotRequired[FieldCommonActionForceMerge]
    read_only: NotRequired[FieldCommonActionReadOnly]
    read_write: NotRequired[FieldCommonActionReadWrite]
    replica_count: NotRequired[FieldCommonActionReplicaCount]
    index_priority: NotRequired[FieldCommonActionIndexPriority]
    close: NotRequired[FieldCommonActionClose]
    open: NotRequired[FieldCommonActionOpen]
    snapshot: NotRequired[FieldCommonActionSnapshot]
    rollover: NotRequired[FieldCommonActionRollover]
    notification: NotRequired[FieldCommonActionNotification]
    allocation: NotRequired[FieldCommonActionAllocation]
    rollup: NotRequired[FieldCommonActionRollup]
    transform: NotRequired[FieldCommonActionTransform]
    shrink: NotRequired[FieldCommonActionShrink]
    custom: NotRequired[FieldCommonActionCustom]


class FieldCommonChangePolicyRequest(TypedDict):
    policy_id: str
    state: NotRequired[str]
    include: NotRequired[list[FieldCommonIncludeState]]


class FieldCommonChangeResponse(TypedDict):
    updated_indices: NotRequired[float]
    failures: NotRequired[bool]
    failed_indices: NotRequired[list[FieldCommonFailedIndex]]


FieldCommonDeletePolicyResponse: TypeAlias = FieldCommonWriteResponseBase


class FieldCommonErrorNotification(TypedDict):
    destination: NotRequired[FieldCommonErrorNotificationDestination]
    channel: NotRequired[FieldCommonChannel]
    message_template: NotRequired[dict[str, Any]]


class FieldCommonErrorNotificationSlack(TypedDict):
    url: NotRequired[str]
    custom_webhook: NotRequired[FieldCommonSlackCustomWebhook]


class FieldCommonRefreshSearchAnalyzersResponse(TypedDict):
    field_shards: NotRequired[FieldCommonShardStatistics]
    successful_refresh_details: NotRequired[
        list[FieldCommonRefreshSearchAnalyzersResponseDetails]
    ]


FieldCommonRetryIndexResponse: TypeAlias = FieldCommonChangeResponse


class FieldCommonStates(TypedDict):
    name: NotRequired[str]
    actions: NotRequired[list[FieldCommonAction]]
    transitions: NotRequired[list[FieldCommonTransition]]


FieldCommonChangePolicyResponse: TypeAlias = FieldCommonChangeResponse


class FieldCommonPolicy(TypedDict):
    policy_id: NotRequired[str]
    description: NotRequired[str]
    last_updated_time: NotRequired[int]
    schema_version: NotRequired[float]
    error_notification: NotRequired[FieldCommonErrorNotification | None]
    default_state: NotRequired[str]
    states: NotRequired[list[FieldCommonStates]]
    ism_template: NotRequired[
        FieldCommonIsmTemplate | list[FieldCommonIsmTemplate] | None
    ]


class FieldCommonPolicyEnvelope(TypedDict):
    policy: NotRequired[FieldCommonPolicy]


class FieldCommonPolicyWithMetadata(FieldCommonMetadata, FieldCommonPolicyEnvelope):
    pass


FieldCommonPutPolicyRequest: TypeAlias = FieldCommonPolicyEnvelope


class FieldCommonPutPolicyResponse(FieldCommonMetadata):
    policy: NotRequired[FieldCommonPolicyEnvelope]


FieldCommonRemovePolicyResponse: TypeAlias = FieldCommonChangePolicyResponse


FieldCommonAddPolicyResponse: TypeAlias = FieldCommonChangePolicyResponse


class FieldCommonGetPoliciesResponse(TypedDict):
    total_policies: NotRequired[float]
    policies: NotRequired[list[FieldCommonPolicyWithMetadata]]


FieldCommonGetPolicyResponse: TypeAlias = FieldCommonPolicyWithMetadata
