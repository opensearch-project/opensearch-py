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


class AlertsActionExecutionResult(TypedDict):
    action_id: NotRequired[str]
    last_execution_time: NotRequired[str]
    throttled_count: NotRequired[int]


class AlertsAlertError(TypedDict):
    timestamp: NotRequired[str]
    message: NotRequired[str]


AlertsAlertSeverityLevel: TypeAlias = Literal["1", "2", "3", "4", "5", "ALL"]


AlertsAlertState: TypeAlias = Literal[
    "ACKNOWLEDGED", "ACTIVE", "COMPLETED", "DELETED", "ERROR"
]


FindingsDetectionType: TypeAlias = Literal["rule", "threat"]


class FindingsDocument(TypedDict):
    index: NotRequired[str]
    id: NotRequired[str]
    found: NotRequired[bool]
    document: NotRequired[str]


class FindingsFindingWithScore(TypedDict):
    finding: NotRequired[str]
    detector_type: NotRequired[str]
    score: NotRequired[float]
    rules: NotRequired[list[str]]


class FindingsQuery(TypedDict):
    id: NotRequired[str]
    name: NotRequired[str]
    fields: NotRequired[list[str]]
    query: NotRequired[str]
    tags: NotRequired[list[str]]
    query_field_names: NotRequired[list[str]]


FindingsRuleSeverity: TypeAlias = Literal["critical", "high", "low", "medium"]


class FindingsSearchFindingCorrelationsResponse(TypedDict):
    findings: list[FindingsFindingWithScore]


class AlertsAlert(TypedDict):
    detector_id: NotRequired[str]
    id: NotRequired[str]
    version: NotRequired[int]
    schema_version: NotRequired[int]
    trigger_id: NotRequired[str]
    trigger_name: NotRequired[str]
    finding_ids: NotRequired[list[str]]
    related_doc_ids: NotRequired[list[str]]
    state: NotRequired[AlertsAlertState]
    error_message: NotRequired[str | None]
    alert_history: NotRequired[list[AlertsAlertError]]
    severity: NotRequired[str]
    action_execution_results: NotRequired[list[AlertsActionExecutionResult]]
    start_time: NotRequired[str]
    last_notification_time: NotRequired[str]
    end_time: NotRequired[str | None]
    acknowledged_time: NotRequired[str | None]


AlertsAlerts: TypeAlias = list[AlertsAlert]


class AlertsGetAlertsResponse(TypedDict):
    alerts: AlertsAlerts
    total_alerts: int


class FindingsFinding(TypedDict):
    detectorId: NotRequired[str]
    id: NotRequired[str]
    related_doc_ids: NotRequired[list[str]]
    index: NotRequired[str]
    queries: NotRequired[list[FindingsQuery]]
    timestamp: NotRequired[int]
    document_list: NotRequired[list[FindingsDocument]]


FindingsFindings: TypeAlias = list[FindingsFinding]


class FindingsGetFindingsResponse(TypedDict):
    total_findings: int
    findings: FindingsFindings
