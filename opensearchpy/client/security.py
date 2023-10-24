# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


# ----------------------------------------------------
# THIS CODE IS GENERATED AND MANUAL EDITS WILL BE LOST.
#
# To contribute, kindly make essential modifications through either the "opensearch-py client generator":
# https://github.com/opensearch-project/opensearch-py/blob/main/utils/generate-api.py
# or the "OpenSearch API specification" available at:
# https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json
# -----------------------------------------------------


from .utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class SecurityClient(NamespacedClient):
    from ._patch import health_check, update_audit_config

    @query_params()
    def get_account_details(self, params=None, headers=None):
        """
        Returns account details for the current user.

        """
        return self.transport.perform_request(
            "GET", "/_plugins/_security/api/account", params=params, headers=headers
        )

    @query_params()
    def change_password(self, body, params=None, headers=None):
        """
        Changes the password for the current user.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/account",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_action_group(self, action_group, params=None, headers=None):
        """
        Retrieves one action group.


        :arg action_group: Action group to retrieve.
        """
        if action_group in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'action_group'."
            )

        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_action_groups(self, params=None, headers=None):
        """
        Retrieves all action groups.

        """
        return self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/actiongroups/",
            params=params,
            headers=headers,
        )

    @query_params()
    def delete_action_group(self, action_group, params=None, headers=None):
        """
        Delete a specified action group.


        :arg action_group: Action group to delete.
        """
        if action_group in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'action_group'."
            )

        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
        )

    @query_params()
    def create_action_group(self, action_group, body, params=None, headers=None):
        """
        Creates or replaces the specified action group.


        :arg action_group: The name of the action group to create or
            replace
        :arg body:
        """
        for param in (action_group, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_action_group(self, action_group, body, params=None, headers=None):
        """
        Updates individual attributes of an action group.


        :arg action_group:
        :arg body:
        """
        for param in (action_group, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_action_groups(self, body, params=None, headers=None):
        """
        Creates, updates, or deletes multiple action groups in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/actiongroups",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_user(self, username, params=None, headers=None):
        """
        Retrieve one internal user.


        :arg username:
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_users(self, params=None, headers=None):
        """
        Retrieve all internal users.

        """
        return self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/internalusers",
            params=params,
            headers=headers,
        )

    @query_params()
    def delete_user(self, username, params=None, headers=None):
        """
        Delete the specified user.


        :arg username:
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
        )

    @query_params()
    def create_user(self, username, body, params=None, headers=None):
        """
        Creates or replaces the specified user.


        :arg username:
        :arg body:
        """
        for param in (username, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_user(self, username, body, params=None, headers=None):
        """
        Updates individual attributes of an internal user.


        :arg username:
        :arg body:
        """
        for param in (username, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_users(self, body, params=None, headers=None):
        """
        Creates, updates, or deletes multiple internal users in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/internalusers",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_role(self, role, params=None, headers=None):
        """
        Retrieves one role.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_roles(self, params=None, headers=None):
        """
        Retrieves all roles.

        """
        return self.transport.perform_request(
            "GET", "/_plugins/_security/api/roles/", params=params, headers=headers
        )

    @query_params()
    def delete_role(self, role, params=None, headers=None):
        """
        Delete the specified role.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
        )

    @query_params()
    def create_role(self, role, body, params=None, headers=None):
        """
        Creates or replaces the specified role.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_role(self, role, body, params=None, headers=None):
        """
        Updates individual attributes of a role.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_roles(self, body, params=None, headers=None):
        """
        Creates, updates, or deletes multiple roles in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/roles",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_role_mapping(self, role, params=None, headers=None):
        """
        Retrieves one role mapping.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_role_mappings(self, params=None, headers=None):
        """
        Retrieves all role mappings.

        """
        return self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/rolesmapping",
            params=params,
            headers=headers,
        )

    @query_params()
    def delete_role_mapping(self, role, params=None, headers=None):
        """
        Deletes the specified role mapping.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
        )

    @query_params()
    def create_role_mapping(self, role, body, params=None, headers=None):
        """
        Creates or replaces the specified role mapping.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_role_mapping(self, role, body, params=None, headers=None):
        """
        Updates individual attributes of a role mapping.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_role_mappings(self, body, params=None, headers=None):
        """
        Creates or updates multiple role mappings in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/rolesmapping",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_tenant(self, tenant, params=None, headers=None):
        """
        Retrieves one tenant.


        :arg tenant:
        """
        if tenant in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'tenant'.")

        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_tenants(self, params=None, headers=None):
        """
        Retrieves all tenants.

        """
        return self.transport.perform_request(
            "GET", "/_plugins/_security/api/tenants/", params=params, headers=headers
        )

    @query_params()
    def delete_tenant(self, tenant, params=None, headers=None):
        """
        Delete the specified tenant.


        :arg tenant:
        """
        if tenant in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'tenant'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
        )

    @query_params()
    def create_tenant(self, tenant, body, params=None, headers=None):
        """
        Creates or replaces the specified tenant.


        :arg tenant:
        :arg body:
        """
        for param in (tenant, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_tenant(self, tenant, body, params=None, headers=None):
        """
        Add, delete, or modify a single tenant.


        :arg tenant:
        :arg body:
        """
        for param in (tenant, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_tenants(self, body, params=None, headers=None):
        """
        Add, delete, or modify multiple tenants in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/tenants/",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_configuration(self, params=None, headers=None):
        """
        Returns the current Security plugin configuration in JSON format.

        """
        return self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/securityconfig",
            params=params,
            headers=headers,
        )

    @query_params()
    def update_configuration(self, body, params=None, headers=None):
        """
        Adds or updates the existing configuration using the REST API.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/securityconfig/config",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_configuration(self, body, params=None, headers=None):
        """
        A PATCH call is used to update the existing configuration using the REST API.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/securityconfig",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_distinguished_names(self, cluster_name=None, params=None, headers=None):
        """
        Retrieves all distinguished names in the allow list.


        :arg cluster_name:
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "nodesdn", cluster_name),
            params=params,
            headers=headers,
        )

    @query_params()
    def update_distinguished_names(
        self, cluster_name, body=None, params=None, headers=None
    ):
        """
        Adds or updates the specified distinguished names in the cluster’s or node’s
        allow list.


        :arg cluster_name:
        :arg body:
        """
        if cluster_name in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'cluster_name'."
            )

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "nodesdn", cluster_name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def delete_distinguished_names(self, cluster_name, params=None, headers=None):
        """
        Deletes all distinguished names in the specified cluster’s or node’s allow
        list.


        :arg cluster_name:
        """
        if cluster_name in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'cluster_name'."
            )

        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "nodesdn", cluster_name),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_certificates(self, params=None, headers=None):
        """
        Retrieves the cluster’s security certificates.

        """
        return self.transport.perform_request(
            "GET", "/_plugins/_security/api/ssl/certs", params=params, headers=headers
        )

    @query_params()
    def reload_transport_certificates(self, params=None, headers=None):
        """
        Reload transport layer communication certificates.

        """
        return self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/ssl/transport/reloadcerts",
            params=params,
            headers=headers,
        )

    @query_params()
    def reload_http_certificates(self, params=None, headers=None):
        """
        Reload HTTP layer communication certificates.

        """
        return self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/ssl/http/reloadcerts",
            params=params,
            headers=headers,
        )

    @query_params()
    def flush_cache(self, params=None, headers=None):
        """
        Flushes the Security plugin user, authentication, and authorization cache.

        """
        return self.transport.perform_request(
            "DELETE", "/_plugins/_security/api/cache", params=params, headers=headers
        )

    @query_params()
    def health(self, params=None, headers=None):
        """
        Checks to see if the Security plugin is up and running.

        """
        return self.transport.perform_request(
            "GET", "/_plugins/_security/health", params=params, headers=headers
        )

    @query_params()
    def get_audit_configuration(self, params=None, headers=None):
        """
        Retrieves the audit configuration.

        """
        return self.transport.perform_request(
            "GET", "/_plugins/_security/api/audit", params=params, headers=headers
        )

    @query_params()
    def update_audit_configuration(self, body, params=None, headers=None):
        """
        Updates the audit configuration.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/audit/config",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_audit_configuration(self, body, params=None, headers=None):
        """
        A PATCH call is used to update specified fields in the audit configuration.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/audit",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def patch_distinguished_names(self, body, params=None, headers=None):
        """
        Bulk update of distinguished names.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/nodesdn",
            params=params,
            headers=headers,
            body=body,
        )
