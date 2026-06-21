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


class FieldCommonChime(TypedDict):
    url: str


class FieldCommonDeliveryStatus(TypedDict):
    status_code: NotRequired[str]
    status_text: NotRequired[str]


FieldCommonEmailEncryptionMethod: TypeAlias = Literal["none", "ssl", "start_tls"]


class FieldCommonEmailRecipientStatus(TypedDict):
    recipient: NotRequired[str]
    delivery_status: NotRequired[FieldCommonDeliveryStatus]


FieldCommonHeaderParamsMap: TypeAlias = dict[str, int]


FieldCommonHttpMethodType: TypeAlias = Literal["PATCH", "POST", "PUT"]


class FieldCommonMicrosoftTeamsItem(TypedDict):
    url: str


FieldCommonNotificationConfigType: TypeAlias = Literal[
    "chime",
    "email",
    "email_group",
    "microsoft_teams",
    "ses_account",
    "slack",
    "smtp_account",
    "sns",
    "webhook",
]


FieldCommonNotificationsPluginFeaturesMap: TypeAlias = dict[str, str]


class FieldCommonRecipientListItem(TypedDict):
    recipient: NotRequired[str]


FieldCommonRestStatus: TypeAlias = Literal[
    "ACCEPTED",
    "CREATED",
    "MULTI_STATUS",
    "NON_AUTHORITATIVE_INFORMATION",
    "NO_CONTENT",
    "OK",
    "PARTIAL_CONTENT",
    "RESET_CONTENT",
]


class FieldCommonSesAccount(TypedDict):
    region: str
    role_arn: NotRequired[str]
    from_address: str


FieldCommonSeverityType: TypeAlias = Literal["critical", "high", "info"]


class FieldCommonSlackItem(TypedDict):
    url: str


class FieldCommonSmtpAccount(TypedDict):
    host: str
    port: int
    method: FieldCommonEmailEncryptionMethod
    from_address: str


class FieldCommonSnsItem(TypedDict):
    topic_arn: str
    role_arn: NotRequired[str]


FieldCommonTotalHitRelation: TypeAlias = Literal["eq", "gte"]


class FieldCommonWebhook(TypedDict):
    url: str
    method: NotRequired[FieldCommonHttpMethodType]
    header_params: NotRequired[FieldCommonHeaderParamsMap]


FieldCommonDeleteResponseList: TypeAlias = dict[str, FieldCommonRestStatus]


class FieldCommonEmail(TypedDict):
    email_account_id: str
    recipient_list: NotRequired[list[FieldCommonRecipientListItem]]


class FieldCommonEmailGroup(TypedDict):
    recipient_list: list[FieldCommonRecipientListItem]
    email_group_id_list: NotRequired[list[str]]


class FieldCommonEventSource(TypedDict):
    title: NotRequired[str]
    reference_id: NotRequired[str]
    severity: NotRequired[FieldCommonSeverityType]
    tags: NotRequired[list[str]]


class FieldCommonEventStatus(TypedDict):
    config_id: NotRequired[str]
    config_name: NotRequired[str]
    config_type: NotRequired[FieldCommonNotificationConfigType]
    email_recipient_status: NotRequired[list[FieldCommonEmailRecipientStatus]]
    delivery_status: NotRequired[FieldCommonDeliveryStatus]


class FieldCommonNotificationChannel(TypedDict):
    config_id: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    config_type: NotRequired[FieldCommonNotificationConfigType]
    is_enabled: NotRequired[bool]


class FieldCommonNotificationsConfigItem(TypedDict):
    name: str
    description: NotRequired[str]
    config_type: FieldCommonNotificationConfigType
    is_enabled: NotRequired[bool]
    sns: NotRequired[FieldCommonSnsItem]
    slack: NotRequired[FieldCommonSlackItem]
    chime: NotRequired[FieldCommonChime]
    webhook: NotRequired[FieldCommonWebhook]
    smtp_account: NotRequired[FieldCommonSmtpAccount]
    ses_account: NotRequired[FieldCommonSesAccount]
    email_group: NotRequired[FieldCommonEmailGroup]
    email: NotRequired[FieldCommonEmail]
    microsoft_teams: NotRequired[FieldCommonMicrosoftTeamsItem]


class FieldCommonNotificationsConfigsOutputItem(TypedDict):
    config_id: NotRequired[str]
    last_updated_time_ms: NotRequired[int]
    created_time_ms: NotRequired[int]
    config: NotRequired[FieldCommonNotificationsConfigItem]


class FieldCommonDeleteConfigsResponse(TypedDict):
    delete_response_list: NotRequired[FieldCommonDeleteResponseList]


class FieldCommonGetConfigsResponse(TypedDict):
    start_index: NotRequired[int]
    total_hits: NotRequired[int]
    total_hit_relation: NotRequired[FieldCommonTotalHitRelation]
    config_list: NotRequired[list[FieldCommonNotificationsConfigsOutputItem]]


class FieldCommonNotificationsConfig(TypedDict):
    config_id: NotRequired[str]
    config: FieldCommonNotificationsConfigItem
