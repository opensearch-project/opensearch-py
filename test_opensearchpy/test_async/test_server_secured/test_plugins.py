# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from __future__ import unicode_literals

from unittest import IsolatedAsyncioTestCase

import pytest

from opensearchpy._async.helpers.test import get_test_client
from opensearchpy.connection.async_connections import add_connection
from opensearchpy.exceptions import NotFoundError

pytestmark = pytest.mark.asyncio


class TestSecurityPlugin(IsolatedAsyncioTestCase):
    ROLE_NAME = "test-role"
    ROLE_CONTENT = {
        "cluster_permissions": ["cluster_monitor"],
        "index_permissions": [
            {
                "index_patterns": ["index", "test-*"],
                "allowed_actions": [
                    "data_access",
                    "indices_monitor",
                ],
            }
        ],
    }

    USER_NAME = "test-user"
    USER_CONTENT = {"password": "test_password", "opendistro_security_roles": []}

    async def asyncSetUp(self):
        self.client = await get_test_client(
            verify_certs=False, http_auth=("admin", "admin")
        )
        await add_connection("default", self.client)

    async def asyncTearDown(self):
        if self.client:
            await self.client.close()

    async def test_create_role(self):
        # Test to create role
        response = await self.client.security.put_role(
            self.ROLE_NAME, body=self.ROLE_CONTENT
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    async def test_get_role(self):
        # Create a role
        await self.test_create_role()

        # Test to fetch the role
        response = await self.client.security.get_role(self.ROLE_NAME)

        self.assertNotIn("errors", response)
        self.assertIn(self.ROLE_NAME, response)

    async def test_update_role(self):
        # Create a role
        await self.test_create_role()

        role_content = self.ROLE_CONTENT.copy()
        role_content["cluster_permissions"] = ["cluster_all"]

        # Test to update role
        response = await self.client.security.put_role(
            self.ROLE_NAME, body=role_content
        )

        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))

    async def test_delete_role(self):
        # Create a role
        await self.test_create_role()

        # Test to delete the role
        response = await self.client.security.delete_role(self.ROLE_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the role
        with self.assertRaises(NotFoundError):
            response = await self.client.security.get_role(self.ROLE_NAME)

    async def test_create_user(self):
        # Test to create user
        response = await self.client.security.put_user(
            self.USER_NAME, body=self.USER_CONTENT
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    async def test_create_user_with_role(self):
        await self.test_create_role()

        # Test to create user
        response = await self.client.security.put_user(
            self.USER_NAME,
            body={
                "password": "test_password",
                "opendistro_security_roles": [self.ROLE_NAME],
            },
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    async def test_get_user(self):
        # Create a user
        await self.test_create_user()

        # Test to fetch the user
        response = await self.client.security.get_user(self.USER_NAME)

        self.assertNotIn("errors", response)
        self.assertIn(self.USER_NAME, response)

    async def test_update_user(self):
        # Create a user
        await self.test_create_user()

        user_content = self.USER_CONTENT.copy()
        user_content["password"] = "password_test"

        # Test to update user
        response = await self.client.security.put_user(
            self.USER_NAME, body=user_content
        )

        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))

    async def test_delete_user(self):
        # Create a user
        await self.test_create_user()

        # Test to delete the user
        response = await self.client.security.delete_user(self.USER_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the user
        with self.assertRaises(NotFoundError):
            response = await self.client.security.get_user(self.USER_NAME)
