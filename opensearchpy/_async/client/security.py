# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
# ----------------------------------------------------
# THIS CODE IS GENERATED. MANUAL EDITS WILL BE LOST.

# To contribute, please make necessary modifications to either [Python generator](https://github.com/opensearch-project/opensearch-py/blob/main/utils/generate-api.py) or [OpenAPI specs](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) as needed.
# -----------------------------------------------------

from .utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class SecurityClient(NamespacedClient):
    @query_params()
    async def change_password(self, body, params=None, headers=None):
        """
        Changes the password for the current user.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/account",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def create_role(self, role, body, params=None, headers=None):
        """
        Creates or replaces the specified role.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def create_role_mapping(self, role, body, params=None, headers=None):
        """
        Creates or replaces the specified role mapping.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def create_tenant(self, tenant, body=None, params=None, headers=None):
        """
        Creates or replaces the specified tenant.


        :arg tenant:
        :arg body:
        """
        if tenant in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'tenant'.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def create_user(self, username, body, params=None, headers=None):
        """
        Creates or replaces the specified user.


        :arg username:
        :arg body:
        """
        for param in (username, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def delete_role(self, role, params=None, headers=None):
        """
        Delete role.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
        )

    @query_params()
    async def delete_role_mapping(self, role, params=None, headers=None):
        """
        Deletes the specified role mapping.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
        )

    @query_params()
    async def delete_tenant(self, tenant, params=None, headers=None):
        """
        Delete the specified tenant.


        :arg tenant:
        """
        if tenant in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'tenant'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
        )

    @query_params()
    async def delete_user(self, username, params=None, headers=None):
        """
        Delete the specified user.


        :arg username:
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
        )

    @query_params()
    async def flush_cache(self, params=None, headers=None):
        """
        Flushes the Security plugin user, authentication, and authorization cache.

        """
        return await self.transport.perform_request(
            "DELETE", "/_plugins/_security/api/cache", params=params, headers=headers
        )

    @query_params()
    async def get_account_details(self, params=None, headers=None):
        """
        Returns account details for the current user.

        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/account", params=params, headers=headers
        )

    @query_params()
    async def get_audit_config(self, params=None, headers=None):
        """
        A GET call retrieves the audit configuration.

        """
        return await self.transport.perform_request(
            "GET", "/_opendistro/_security/api/audit", params=params, headers=headers
        )

    @query_params()
    async def get_certificates(self, params=None, headers=None):
        """
        Returns the cluster’s security certificates.

        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/ssl/certs", params=params, headers=headers
        )

    @query_params()
    async def get_role(self, role, params=None, headers=None):
        """
        Retrieves one role.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
        )

    @query_params()
    async def get_role_mapping(self, role, params=None, headers=None):
        """
        Retrieves one role mapping.


        :arg role:
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
        )

    @query_params()
    async def get_roles(self, params=None, headers=None):
        """
        Retrieves all roles.

        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/roles/", params=params, headers=headers
        )

    @query_params()
    async def get_roles_mapping(self, params=None, headers=None):
        """
        Retrieves all role mappings.

        """
        return await self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/rolesmapping",
            params=params,
            headers=headers,
        )

    @query_params()
    async def get_tenant(self, tenant, params=None, headers=None):
        """
        Retrieves one tenant.


        :arg tenant:
        """
        if tenant in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'tenant'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
        )

    @query_params()
    async def get_tenants(self, params=None, headers=None):
        """
        Retrieves all tenants.

        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/tenants/", params=params, headers=headers
        )

    @query_params()
    async def get_user(self, username, params=None, headers=None):
        """
        Providing information about given internal user.


        :arg username:
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
        )

    @query_params()
    async def get_users(self, params=None, headers=None):
        """
        Lists of all internal users.

        """
        return await self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/internalusers",
            params=params,
            headers=headers,
        )

    @query_params()
    async def patch_audit_config(self, body, params=None, headers=None):
        """
        A PATCH call is used to update specified fields in the audit configuration.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PATCH",
            "/_opendistro/_security/api/audit",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_role(self, role, body, params=None, headers=None):
        """
        Updates individual attributes of a role.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_role_mapping(self, role, body, params=None, headers=None):
        """
        Updates individual attributes of a role mapping.


        :arg role:
        :arg body:
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_roles(self, body, params=None, headers=None):
        """
        Creates, updates, or deletes multiple roles in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/roles",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_roles_mappings(self, body, params=None, headers=None):
        """
        Creates or updates multiple role mappings in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/rolesmapping",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_tenant(self, tenant, body, params=None, headers=None):
        """
        Add, delete, or modify a single tenant.


        :arg tenant:
        :arg body:
        """
        for param in (tenant, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_tenants(self, body, params=None, headers=None):
        """
        Add, delete, or modify multiple tenants in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/tenants/",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_user(self, username, body, params=None, headers=None):
        """
        Updates individual attributes of an internal user.


        :arg username:
        :arg body:
        """
        for param in (username, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def patch_users(self, body, params=None, headers=None):
        """
        Creates, updates, or deletes multiple internal users in a single call.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/internalusers",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def reload_http_certificates(self, params=None, headers=None):
        """
        Reloads SSL certificates that are about to expire without restarting the
        OpenSearch node.

        """
        return await self.transport.perform_request(
            "PUT",
            "/_opendistro/_security/api/ssl/http/reloadcerts",
            params=params,
            headers=headers,
        )

    @query_params()
    async def reload_transport_certificates(self, params=None, headers=None):
        """
        Reloads SSL certificates that are about to expire without restarting the
        OpenSearch node.

        """
        return await self.transport.perform_request(
            "PUT",
            "/_opendistro/_security/api/ssl/transport/reloadcerts",
            params=params,
            headers=headers,
        )

    @query_params()
    async def update_audit_config(self, body, params=None, headers=None):
        """
        A PUT call updates the audit configuration.


        :arg body:
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PUT",
            "/_opendistro/_security/api/audit/config",
            params=params,
            headers=headers,
            body=body,
        )
