# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
from typing import Any, Union

from .utils import NamespacedClient as NamespacedClient

class SecurityClient(NamespacedClient):
    async def get_account_details(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def change_password(
        self,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def get_action_group(
        self,
        action_group: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def get_action_groups(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def delete_action_group(
        self,
        action_group: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def create_action_group(
        self,
        action_group: Any,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def patch_action_group(
        self,
        action_group: Any,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def patch_action_groups(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_user(
        self,
        username: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def get_users(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def delete_user(
        self,
        username: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def create_user(
        self,
        username: Any,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def patch_user(
        self,
        username: Any,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def patch_users(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_role(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_roles(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def delete_role(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def create_role(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def patch_role(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def patch_roles(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_role_mapping(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_role_mappings(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def delete_role_mapping(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def create_role_mapping(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def patch_role_mapping(
        self, role: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def patch_role_mappings(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_tenant(
        self,
        tenant: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def get_tenants(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def delete_tenant(
        self,
        tenant: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def create_tenant(
        self,
        tenant: Any,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def patch_tenant(
        self,
        tenant: Any,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def patch_tenants(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_configuration(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def update_configuration(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def patch_configuration(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_distinguished_names(
        self,
        cluster_name: Union[Any, None] = ...,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def update_distinguished_names(
        self,
        cluster_name: Any,
        body: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def delete_distinguished_names(
        self,
        cluster_name: Any,
        params: Union[Any, None] = ...,
        headers: Union[Any, None] = ...,
    ) -> Any: ...
    async def get_certificates(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def reload_transport_certificates(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def reload_http_certificates(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def flush_cache(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def health(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def get_audit_configuration(
        self, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def update_audit_configuration(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
    async def patch_audit_configuration(
        self, body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
    ) -> Any: ...
