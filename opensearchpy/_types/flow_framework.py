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

from ._internal import FieldCommonDateTime, FieldCommonDuration, QueryDslQueryContainer

CommonAll: TypeAlias = bool


CommonAllowDelete: TypeAlias = str


CommonProvision: TypeAlias = bool


CommonReprovision: TypeAlias = bool


class CommonResourcesCreated(TypedDict):
    workflow_step_name: NotRequired[str]
    workflow_step_id: NotRequired[str]
    resource_type: NotRequired[str]
    resource_id: NotRequired[str]


class CommonShards(TypedDict):
    total: NotRequired[int]
    successful: NotRequired[int]
    failed: NotRequired[int]
    skipped: NotRequired[int]


class CommonTotal(TypedDict):
    value: NotRequired[int]
    relation: NotRequired[str]


CommonUpdateFields: TypeAlias = bool


CommonUseCase: TypeAlias = str


class CommonUser(TypedDict):
    name: NotRequired[str]
    backend_roles: NotRequired[list[str]]
    roles: NotRequired[list[str]]
    custom_attribute_names: NotRequired[list[str]]
    user_requested_tenant: NotRequired[str]


CommonUserProvidedSubstitutionExpressions: TypeAlias = dict[str, str]


CommonValidation: TypeAlias = str


class CommonVersion(TypedDict):
    template: NotRequired[str]
    compatibility: NotRequired[list[str]]


CommonWorkflowID: TypeAlias = str


class CommonWorkflowIDResponse(TypedDict):
    workflow_id: NotRequired[str]


CommonWorkFlowState: TypeAlias = Literal[
    "COMPLETED", "FAILED", "NOT_STARTED", "PROVISIONING"
]


class CommonWorkFlowStatusDefaultResponse(TypedDict):
    workflow_id: NotRequired[str]
    error: NotRequired[str]
    state: NotRequired[str]
    resources_created: NotRequired[list[str]]


class CommonWorkFlowStatusFullResponse(TypedDict):
    workflow_id: NotRequired[str]
    error: NotRequired[str]
    state: NotRequired[CommonWorkFlowState]
    resources_created: NotRequired[list[str]]
    provisioning_progress: NotRequired[str]
    provision_start_time: NotRequired[str]
    provision_end_time: NotRequired[str]
    user: NotRequired[CommonUser]
    user_outputs: NotRequired[list[str]]


class CommonWorkflowStep(TypedDict):
    inputs: NotRequired[list[str]]
    outputs: NotRequired[list[str]]
    required_plugins: NotRequired[list[str]]
    timeout: NotRequired[FieldCommonDuration]


CommonWorkflowStepName: TypeAlias = str


CommonWorkflowSteps: TypeAlias = dict[str, CommonWorkflowStep]


class ErrorsBadRequestError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsConflictError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsDeprovisioningError(TypedDict):
    error: str


class ErrorsDeprovisioningForbiddenError(TypedDict):
    error: str


class ErrorsDuplicateKeyError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsFlowFrameworkAPIDisabledError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsInvalidParameterError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsInvalidRequestBodyFieldError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsInvalidTemplateVersionError(TypedDict):
    error: NotRequired[str]


class ErrorsMaxWorkflowsLimitError(TypedDict):
    error: NotRequired[str]
    code: NotRequired[int]


class ErrorsMissingParameterError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsParameterConflictError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsRequestBodyParsingFailedError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsRequestTimeoutError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsTemplateNameRequiredError(TypedDict):
    error: NotRequired[str]


class ErrorsTemplateNotFoundError(TypedDict):
    error: NotRequired[str]
    code: NotRequired[int]


class ErrorsUnsupportedFieldUpdateError(TypedDict):
    error: NotRequired[str]


class ErrorsWorkFlowIdNullError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsWorkflowParsingError(TypedDict):
    error: NotRequired[str]


class ErrorsWorkflowSaveError(TypedDict):
    error: NotRequired[str]
    status: NotRequired[int]


class ErrorsWorkflowStepsRetrieveError(TypedDict):
    error: NotRequired[str]
    code: NotRequired[int]


class CommonFlowFrameworkCreate(TypedDict):
    name: str
    description: NotRequired[str]
    use_case: NotRequired[str]
    version: NotRequired[CommonVersion]
    workflows: NotRequired[dict[str, Any]]


class CommonFlowFrameworkGetResponse(TypedDict):
    name: NotRequired[str]
    version: NotRequired[CommonVersion]
    description: NotRequired[str]
    use_case: NotRequired[str]
    workflows: NotRequired[dict[str, Any]]
    user: NotRequired[CommonUser]
    created_time: NotRequired[int]
    last_updated_time: NotRequired[int]
    last_provisioned_time: NotRequired[float]


class CommonFlowFrameworkUpdate(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    use_case: NotRequired[str]
    workflows: NotRequired[dict[str, Any]]
    version: NotRequired[CommonVersion]


class CommonItemsObject(TypedDict):
    field_index: NotRequired[str]
    field_id: NotRequired[str]
    field_version: NotRequired[int]
    field_seq_no: NotRequired[int]
    field_primary_term: NotRequired[int]
    field_score: NotRequired[float]
    field_source: NotRequired[CommonFlowFrameworkGetResponse]


class CommonHits(TypedDict):
    total: NotRequired[CommonTotal]
    max_score: NotRequired[float | None]
    hits: NotRequired[list[CommonItemsObject]]


class CommonSearchStateResponse(TypedDict):
    workflow_id: NotRequired[str]
    provisioning_progress: NotRequired[str]
    state: NotRequired[str]
    user: NotRequired[CommonUser]
    provision_start_time: NotRequired[FieldCommonDateTime]
    provision_end_time: NotRequired[FieldCommonDateTime]
    resources_created: NotRequired[
        CommonResourcesCreated | list[CommonResourcesCreated]
    ]


class CommonStateItems(TypedDict):
    field_index: NotRequired[str]
    field_id: NotRequired[str]
    field_version: NotRequired[int]
    field_seq_no: NotRequired[int]
    field_primary_term: NotRequired[int]
    field_score: NotRequired[float]
    field_source: NotRequired[CommonSearchStateResponse]


class CommonWorkflowSearchResponse(TypedDict):
    took: NotRequired[int]
    timed_out: NotRequired[bool]
    field_shards: NotRequired[CommonShards]
    hits: NotRequired[CommonHits]


class CommonStateHits(TypedDict):
    total: NotRequired[CommonTotal]
    max_score: NotRequired[float | None]
    hits: NotRequired[list[CommonStateItems]]


class CommonWorkflowSearchStateResponse(TypedDict):
    took: NotRequired[int]
    timed_out: NotRequired[bool]
    field_shards: NotRequired[CommonShards]
    hits: NotRequired[CommonStateHits]


class CommonSearchWorkflowRequest(TypedDict):
    query: NotRequired[QueryDslQueryContainer]
