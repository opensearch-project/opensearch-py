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


from typing import Any

from .utils import SKIP_IN_PATH, NamespacedClient, _bulk_body, _make_path, query_params


class SecurityClient(NamespacedClient):
    from ._patch import health_check, update_audit_config  # type: ignore

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_account_details(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Returns account details for the current user.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/account", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def change_password(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Changes the password for the current user.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
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

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_action_group(
        self,
        action_group: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves one action group.


        :arg action_group: Action group to retrieve.
        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if action_group in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'action_group'."
            )

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_action_groups(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves all action groups.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/actiongroups",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def delete_action_group(
        self,
        action_group: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Delete a specified action group.


        :arg action_group: Action group to delete.
        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if action_group in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'action_group'."
            )

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def create_action_group(
        self,
        action_group: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or replaces the specified action group.


        :arg action_group: The name of the action group to create or
            replace
        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (action_group, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_action_group(
        self,
        action_group: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Updates individual attributes of an action group.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (action_group, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "actiongroups", action_group),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_action_groups(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates, updates, or deletes multiple action groups in a single call.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/actiongroups",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_user(
        self,
        username: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieve one internal user.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_users(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieve all internal users.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/internalusers",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def delete_user(
        self,
        username: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Delete the specified user.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def create_user(
        self,
        username: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or replaces the specified user.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
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

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_user(
        self,
        username: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Updates individual attributes of an internal user.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (username, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "internalusers", username),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_users(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates, updates, or deletes multiple internal users in a single call.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/internalusers",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_role(
        self,
        role: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves one role.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_roles(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves all roles.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/roles/", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def delete_role(
        self,
        role: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Delete the specified role.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def create_role(
        self,
        role: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or replaces the specified role.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
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

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_role(
        self,
        role: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Updates individual attributes of a role.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "roles", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_roles(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates, updates, or deletes multiple roles in a single call.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/roles",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_role_mapping(
        self,
        role: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves one role mapping.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_role_mappings(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves all role mappings.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/rolesmapping",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def delete_role_mapping(
        self,
        role: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Deletes the specified role mapping.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if role in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'role'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def create_role_mapping(
        self,
        role: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or replaces the specified role mapping.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
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

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_role_mapping(
        self,
        role: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Updates individual attributes of a role mapping.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (role, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "rolesmapping", role),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_role_mappings(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or updates multiple role mappings in a single call.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/rolesmapping",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_tenant(
        self,
        tenant: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves one tenant.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if tenant in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'tenant'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_tenants(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves all tenants.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/tenants/", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def delete_tenant(
        self,
        tenant: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Delete the specified tenant.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if tenant in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'tenant'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def create_tenant(
        self,
        tenant: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Creates or replaces the specified tenant.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (tenant, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_tenant(
        self,
        tenant: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Add, delete, or modify a single tenant.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (tenant, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            _make_path("_plugins", "_security", "api", "tenants", tenant),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_tenants(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Add, delete, or modify multiple tenants in a single call.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/tenants/",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_configuration(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Returns the current Security plugin configuration in JSON format.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET",
            "/_plugins/_security/api/securityconfig",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def update_configuration(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Adds or updates the existing configuration using the REST API.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/securityconfig/config",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_configuration(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        A PATCH call is used to update the existing configuration using the REST API.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/securityconfig",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_distinguished_names(
        self,
        cluster_name: Any = None,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves distinguished names.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_security", "api", "nodesdn", cluster_name),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def update_distinguished_names(
        self,
        cluster_name: Any,
        body: Any = None,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Adds or updates the specified distinguished names in the cluster’s or node’s
        allow list.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if cluster_name in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'cluster_name'."
            )

        return await self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_security", "api", "nodesdn", cluster_name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def delete_distinguished_names(
        self,
        cluster_name: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Deletes all distinguished names in the specified cluster’s or node’s allow
        list.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if cluster_name in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'cluster_name'."
            )

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_security", "api", "nodesdn", cluster_name),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_certificates(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves the cluster’s security certificates.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/ssl/certs", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def reload_transport_certificates(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Reload transport layer communication certificates.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/ssl/transport/reloadcerts",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def reload_http_certificates(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Reload HTTP layer communication certificates.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/ssl/http/reloadcerts",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def flush_cache(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Flushes the Security plugin user, authentication, and authorization cache.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "DELETE", "/_plugins/_security/api/cache", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def health(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Checks to see if the Security plugin is up and running.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/health", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def get_audit_configuration(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Retrieves the audit configuration.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return await self.transport.perform_request(
            "GET", "/_plugins/_security/api/audit", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def update_audit_configuration(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Updates the audit configuration.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PUT",
            "/_plugins/_security/api/audit/config",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_audit_configuration(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        A PATCH call is used to update specified fields in the audit configuration.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/audit",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    async def patch_distinguished_names(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Bulk update of distinguished names.


        :arg error_trace: Whether to include the stack trace of returned
            errors.
        :arg filter_path: Comma-separated list of filters used to reduce
            the response.
        :arg human: Whether to return human readable values for
            statistics.
        :arg pretty: Whether to pretty format the returned JSON
            response.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "PATCH",
            "/_plugins/_security/api/nodesdn",
            params=params,
            headers=headers,
            body=body,
        )
