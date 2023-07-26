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

from unittest import TestCase

from opensearchpy.connection.connections import add_connection
from opensearchpy.exceptions import NotFoundError
from opensearchpy.helpers.test import get_test_client


class TestSecurityPlugin(TestCase):
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
    USER_CONTENT = {"password": "opensearchpy@123", "opendistro_security_roles": []}

    def setUp(self):
        self.client = get_test_client(verify_certs=False, http_auth=("admin", "admin"))
        add_connection("default", self.client)

    def tearDown(self):
        if self.client:
            self.client.close()

    def test_create_role(self):
        # Test to create role
        response = self.client.security.create_role(
            self.ROLE_NAME, body=self.ROLE_CONTENT
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    def test_create_role_with_body_param_empty(self):
        try:
            self.client.security.create_role(self.ROLE_NAME, body="")
        except ValueError as error:
            assert str(error) == "Empty value passed for a required argument."
        else:
            assert False

    def test_get_role(self):
        # Create a role
        self.test_create_role()

        # Test to fetch the role
        response = self.client.security.get_role(self.ROLE_NAME)

        self.assertNotIn("errors", response)
        self.assertIn(self.ROLE_NAME, response)

    def test_update_role(self):
        # Create a role
        self.test_create_role()

        role_content = self.ROLE_CONTENT.copy()
        role_content["cluster_permissions"] = ["cluster_all"]

        # Test to update role
        response = self.client.security.create_role(self.ROLE_NAME, body=role_content)

        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))

    def test_delete_role(self):
        # Create a role
        self.test_create_role()

        # Test to delete the role
        response = self.client.security.delete_role(self.ROLE_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the role
        with self.assertRaises(NotFoundError):
            response = self.client.security.get_role(self.ROLE_NAME)

    def test_create_user(self):
        # Test to create user
        response = self.client.security.create_user(
            self.USER_NAME, body=self.USER_CONTENT
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    def test_create_user_with_body_param_empty(self):
        try:
            self.client.security.create_user(self.USER_NAME, body="")
        except ValueError as error:
            assert str(error) == "Empty value passed for a required argument."
        else:
            assert False

    def test_create_user_with_role(self):
        self.test_create_role()

        # Test to create user
        response = self.client.security.create_user(
            self.USER_NAME,
            body={
                "password": "opensearchpy@123",
                "opendistro_security_roles": [self.ROLE_NAME],
            },
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    def test_get_user(self):
        # Create a user
        self.test_create_user()

        # Test to fetch the user
        response = self.client.security.get_user(self.USER_NAME)

        self.assertNotIn("errors", response)
        self.assertIn(self.USER_NAME, response)

    def test_update_user(self):
        # Create a user
        self.test_create_user()

        user_content = self.USER_CONTENT.copy()
        user_content["password"] = "123@opensearchpy"

        # Test to update user
        response = self.client.security.create_user(self.USER_NAME, body=user_content)

        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))

    def test_delete_user(self):
        # Create a user
        self.test_create_user()

        # Test to delete the user
        response = self.client.security.delete_user(self.USER_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the user
        with self.assertRaises(NotFoundError):
            response = self.client.security.get_user(self.USER_NAME)
