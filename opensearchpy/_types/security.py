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

from .nodes import FieldCommonNodesResponseBase


class FieldCommonActionGroup(TypedDict):
    reserved: NotRequired[bool]
    hidden: NotRequired[bool]
    allowed_actions: NotRequired[list[str]]
    type: NotRequired[str]
    description: NotRequired[str]
    static: NotRequired[bool]


FieldCommonActionGroupsMap: TypeAlias = dict[str, FieldCommonActionGroup]


class FieldCommonAllowListConfig(TypedDict):
    enabled: NotRequired[bool]
    requests: NotRequired[dict[str, list[str]]]


class FieldCommonAuditLogsConfig(TypedDict):
    ignore_users: NotRequired[list[str]]
    ignore_requests: NotRequired[list[str]]
    ignore_headers: NotRequired[list[str]]
    ignore_url_params: NotRequired[list[str]]
    disabled_rest_categories: NotRequired[list[str]]
    disabled_transport_categories: NotRequired[list[str]]
    log_request_body: NotRequired[bool]
    resolve_indices: NotRequired[bool]
    resolve_bulk_requests: NotRequired[bool]
    exclude_sensitive_headers: NotRequired[bool]
    enable_transport: NotRequired[bool]
    enable_rest: NotRequired[bool]


class FieldCommonAuthInfo(TypedDict):
    user: NotRequired[str]
    user_name: NotRequired[str]
    user_requested_tenant: NotRequired[str | None]
    remote_address: NotRequired[str | None]
    backend_roles: NotRequired[list[str]]
    custom_attribute_names: NotRequired[list[str]]
    roles: NotRequired[list[str]]
    tenants: NotRequired[dict[str, bool]]
    principal: NotRequired[str | None]
    peer_certificates: NotRequired[float | str]
    sso_logout_url: NotRequired[str | None]
    size_of_user: NotRequired[str]
    size_of_custom_attributes: NotRequired[str]
    size_of_backendroles: NotRequired[str]


class FieldCommonCertificatesDetail(TypedDict):
    issuer_dn: NotRequired[str]
    subject_dn: NotRequired[str]
    san: NotRequired[str]
    not_before: NotRequired[str]
    not_after: NotRequired[str]


class FieldCommonCertificateTypes(TypedDict):
    http: NotRequired[list[dict[str, FieldCommonCertificatesDetail]]]
    transport: NotRequired[list[dict[str, FieldCommonCertificatesDetail]]]


class FieldCommonChangePasswordRequestContent(TypedDict):
    current_password: str
    password: str


class FieldCommonClientError(TypedDict):
    status: NotRequired[int]
    error: NotRequired[str]


class FieldCommonComplianceConfig(TypedDict):
    enabled: NotRequired[bool]
    write_log_diffs: NotRequired[bool]
    read_watched_fields: NotRequired[Any]
    read_ignore_users: NotRequired[list[str]]
    write_watched_indices: NotRequired[list[str]]
    write_ignore_users: NotRequired[list[str]]
    read_metadata_only: NotRequired[bool]
    write_metadata_only: NotRequired[bool]
    external_config: NotRequired[bool]
    internal_config: NotRequired[bool]


class FieldCommonConfigUpgradePayload(TypedDict):
    config: NotRequired[list[str]]


class FieldCommonCreated(TypedDict):
    status: NotRequired[float | str]
    message: NotRequired[str]


class FieldCommonCreateTenantParams(TypedDict):
    description: NotRequired[str]


class FieldCommonDashboardsInfo(TypedDict):
    user_name: NotRequired[str]
    not_fail_on_forbidden_enabled: NotRequired[bool]
    opensearch_dashboards_mt_enabled: NotRequired[bool]
    opensearch_dashboards_index: NotRequired[str]
    opensearch_dashboards_server_user: NotRequired[str]
    multitenancy_enabled: NotRequired[bool]
    private_tenant_enabled: NotRequired[bool]
    default_tenant: NotRequired[str]
    sign_in_options: NotRequired[list[str]]
    password_validation_error_message: NotRequired[str]
    password_validation_regex: NotRequired[str]


class FieldCommonDistinguishedNames(TypedDict):
    nodes_dn: NotRequired[list[str]]


FieldCommonDistinguishedNamesMap: TypeAlias = dict[str, FieldCommonDistinguishedNames]


FieldCommonDynamicOptions = TypedDict(
    "FieldCommonDynamicOptions",
    {
        "filtered_alias_mode": NotRequired[str],
        "disable_rest_auth": NotRequired[bool],
        "disable_intertransport_auth": NotRequired[bool],
        "respect_request_indices_options": NotRequired[bool],
        "opensearch-dashboards": NotRequired[dict[str, Any]],
        "kibana": NotRequired[dict[str, Any]],
        "http": NotRequired[dict[str, Any]],
        "authc": NotRequired[dict[str, Any]],
        "authz": NotRequired[dict[str, Any]],
        "auth_failure_listeners": NotRequired[dict[str, Any]],
        "do_not_fail_on_forbidden": NotRequired[bool],
        "multi_rolespan_enabled": NotRequired[bool],
        "hosts_resolver_mode": NotRequired[str],
        "do_not_fail_on_forbidden_empty": NotRequired[bool],
        "on_behalf_of": NotRequired[dict[str, Any]],
    },
)


FieldCommonErrorStatus: TypeAlias = Literal[
    "BAD_REQUEST",
    "CONFLICT",
    "FORBIDDEN",
    "INTERNAL_SERVER_ERROR",
    "NOT_FOUND",
    "NOT_IMPLEMENTED",
    "UNAUTHORIZED",
]


class FieldCommonGenerateOBOToken(TypedDict):
    user: NotRequired[str]
    authenticationToken: NotRequired[str]
    durationSeconds: NotRequired[str]


class FieldCommonGetCertificates(TypedDict):
    http_certificates_list: NotRequired[list[FieldCommonCertificatesDetail]]
    transport_certificates_list: NotRequired[list[FieldCommonCertificatesDetail]]


class FieldCommonHealthInfo(TypedDict):
    message: NotRequired[str | None]
    mode: NotRequired[str]
    status: NotRequired[str]
    settings: NotRequired[dict[str, Any]]


class FieldCommonIndexPermission(TypedDict):
    index_patterns: NotRequired[list[str]]
    dls: NotRequired[str]
    fls: NotRequired[list[str]]
    masked_fields: NotRequired[list[str]]
    allowed_actions: NotRequired[list[str]]


class FieldCommonInternalServerError(TypedDict):
    error: NotRequired[str]


class FieldCommonMultiTenancyConfig(TypedDict):
    default_tenant: NotRequired[str]
    private_tenant_enabled: NotRequired[bool]
    multitenancy_enabled: NotRequired[bool]
    sign_in_options: NotRequired[list[str]]


class FieldCommonOBOToken(TypedDict):
    description: str
    service: NotRequired[str]
    duration: NotRequired[str]


class FieldCommonOk(TypedDict):
    status: NotRequired[float | str]
    message: NotRequired[str]


class FieldCommonPatchOperation(TypedDict):
    op: str
    path: str
    value: NotRequired[Any]


class FieldCommonPermissionsInfo(TypedDict):
    user: NotRequired[str]
    user_name: NotRequired[str]
    has_api_access: NotRequired[bool]
    disabled_endpoints: NotRequired[dict[str, list[str]]]


class FieldCommonRoleMapping(TypedDict):
    hosts: NotRequired[list[str]]
    users: NotRequired[list[str]]
    reserved: NotRequired[bool]
    hidden: NotRequired[bool]
    backend_roles: NotRequired[list[str]]
    and_backend_roles: NotRequired[list[str]]
    description: NotRequired[str]


FieldCommonRoleMappings: TypeAlias = dict[str, FieldCommonRoleMapping]


class FieldCommonSSLInfo(TypedDict):
    principal: str | None
    peer_certificates: float | str
    peer_certificates_list: NotRequired[list[str]]
    local_certificates_list: NotRequired[list[str]]
    ssl_protocol: str | None
    ssl_cipher: str | None
    ssl_openssl_available: NotRequired[bool]
    ssl_openssl_version: NotRequired[float | str]
    ssl_openssl_version_string: NotRequired[str | None]
    ssl_openssl_non_available_cause: NotRequired[str | None]
    ssl_openssl_supports_key_manager_factory: NotRequired[bool]
    ssl_openssl_supports_hostname_validation: NotRequired[bool]
    ssl_provider_http: str | None
    ssl_provider_transport_server: str
    ssl_provider_transport_client: str


class FieldCommonTenant(TypedDict):
    reserved: NotRequired[bool]
    hidden: NotRequired[bool]
    description: NotRequired[str]
    static: NotRequired[bool]


FieldCommonTenantInfo: TypeAlias = dict[str, str]


class FieldCommonTenantPermission(TypedDict):
    tenant_patterns: NotRequired[list[str]]
    allowed_actions: NotRequired[list[str]]


FieldCommonTenantsMap: TypeAlias = dict[str, FieldCommonTenant]


class FieldCommonUpgradeCheck(TypedDict):
    status: NotRequired[str]
    upgradeAvailable: NotRequired[bool]
    upgradeActions: NotRequired[dict[str, dict[str, list[str]]]]


class FieldCommonUpgradePerform(TypedDict):
    status: NotRequired[str]
    upgrades: NotRequired[dict[str, dict[str, list[str]]]]


FieldCommonUserAttributes: TypeAlias = dict[str, str]


class FieldCommonUserTenants(TypedDict):
    global_tenant: NotRequired[bool]
    admin_tenant: NotRequired[bool]
    admin: NotRequired[bool]


class FieldCommonWhoAmI(TypedDict):
    dn: NotRequired[str | None]
    is_admin: NotRequired[bool]
    is_node_certificate_request: NotRequired[bool]


class FieldCommonAccountDetails(TypedDict):
    user_name: NotRequired[str]
    is_reserved: NotRequired[bool]
    is_hidden: NotRequired[bool]
    is_internal_user: NotRequired[bool]
    user_requested_tenant: NotRequired[str | None]
    backend_roles: NotRequired[list[str]]
    custom_attribute_names: NotRequired[list[str]]
    tenants: NotRequired[FieldCommonUserTenants]
    roles: NotRequired[list[str]]


class FieldCommonAuditConfig(TypedDict):
    compliance: NotRequired[FieldCommonComplianceConfig]
    enabled: NotRequired[bool]
    audit: NotRequired[FieldCommonAuditLogsConfig]


class FieldCommonAuditConfigWithReadOnly(TypedDict):
    field_readonly: NotRequired[list[str]]
    config: NotRequired[FieldCommonAuditConfig]


class FieldCommonCertificatesPerNode(TypedDict):
    name: NotRequired[str]
    certificates: NotRequired[dict[str, FieldCommonCertificateTypes]]


class FieldCommonDynamicConfig(TypedDict):
    dynamic: NotRequired[FieldCommonDynamicOptions]


class FieldCommonError(TypedDict):
    status: NotRequired[FieldCommonErrorStatus]
    message: NotRequired[str]


class FieldCommonGetCertificatesNew(FieldCommonNodesResponseBase):
    cluster_name: NotRequired[str]
    nodes: NotRequired[dict[str, FieldCommonCertificatesPerNode]]


class FieldCommonRole(TypedDict):
    reserved: NotRequired[bool]
    hidden: NotRequired[bool]
    description: NotRequired[str]
    cluster_permissions: NotRequired[list[str]]
    index_permissions: NotRequired[list[FieldCommonIndexPermission]]
    tenant_permissions: NotRequired[list[FieldCommonTenantPermission]]
    static: NotRequired[bool]


FieldCommonRolesMap: TypeAlias = dict[str, FieldCommonRole]


class FieldCommonSecurityConfig(TypedDict):
    config: NotRequired[FieldCommonDynamicConfig]


class FieldCommonUser(TypedDict):
    password: NotRequired[str]
    hash: NotRequired[str]
    reserved: NotRequired[bool]
    hidden: NotRequired[bool]
    backend_roles: NotRequired[list[str]]
    attributes: NotRequired[FieldCommonUserAttributes]
    description: NotRequired[str]
    opendistro_security_roles: NotRequired[list[str]]
    static: NotRequired[bool]


FieldCommonUsersMap: TypeAlias = dict[str, FieldCommonUser]
