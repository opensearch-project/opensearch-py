# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.



import os
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

    def setUp(self) -> None:
        password = os.environ.get("OPENSEARCH_INITIAL_ADMIN_PASSWORD", "admin")
        self.client = get_test_client(verify_certs=False, http_auth=("admin", password))
        add_connection("default", self.client)

    def tearDown(self) -> None:
        if self.client:
            self.client.close()

    def test_create_role(self) -> None:
        # Test to create role
        response = self.client.security.create_role(
            self.ROLE_NAME, body=self.ROLE_CONTENT
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    def test_create_role_with_body_param_empty(self) -> None:
        try:
            self.client.security.create_role(self.ROLE_NAME, body="")
        except ValueError as error:
            assert str(error) == "Empty value passed for a required argument."
        else:
            assert False

    def test_get_role(self) -> None:
        # Create a role
        self.test_create_role()

        # Test to fetch the role
        response = self.client.security.get_role(self.ROLE_NAME)

        self.assertNotIn("errors", response)
        self.assertIn(self.ROLE_NAME, response)

    def test_update_role(self) -> None:
        # Create a role
        self.test_create_role()

        role_content = self.ROLE_CONTENT.copy()
        role_content["cluster_permissions"] = ["cluster_all"]

        # Test to update role
        response = self.client.security.create_role(self.ROLE_NAME, body=role_content)

        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))

    def test_delete_role(self) -> None:
        # Create a role
        self.test_create_role()

        # Test to delete the role
        response = self.client.security.delete_role(self.ROLE_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the role
        with self.assertRaises(NotFoundError):
            response = self.client.security.get_role(self.ROLE_NAME)

    def test_create_user(self) -> None:
        # Test to create user
        response = self.client.security.create_user(
            self.USER_NAME, body=self.USER_CONTENT
        )

        self.assertNotIn("errors", response)
        self.assertIn(response.get("status"), ["CREATED", "OK"])

    def test_create_user_with_body_param_empty(self) -> None:
        try:
            self.client.security.create_user(self.USER_NAME, body="")
        except ValueError as error:
            assert str(error) == "Empty value passed for a required argument."
        else:
            assert False

    def test_create_user_with_role(self) -> None:
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

    def test_get_user(self) -> None:
        # Create a user
        self.test_create_user()

        # Test to fetch the user
        response = self.client.security.get_user(self.USER_NAME)

        self.assertNotIn("errors", response)
        self.assertIn(self.USER_NAME, response)

    def test_update_user(self) -> None:
        # Create a user
        self.test_create_user()

        user_content = self.USER_CONTENT.copy()
        user_content["password"] = "123@opensearchpy"

        # Test to update user
        response = self.client.security.create_user(self.USER_NAME, body=user_content)

        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))

    def test_delete_user(self) -> None:
        # Create a user
        self.test_create_user()

        # Test to delete the user
        response = self.client.security.delete_user(self.USER_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the user
        with self.assertRaises(NotFoundError):
            response = self.client.security.get_user(self.USER_NAME)

    def test_health_check(self) -> None:
        response = self.client.security.health_check()
        self.assertNotIn("errors", response)
        self.assertEqual("UP", response.get("status"))

    def test_health(self) -> None:
        response = self.client.security.health()
        self.assertNotIn("errors", response)
        self.assertEqual("UP", response.get("status"))

    AUDIT_CONFIG_SETTINGS = {
        "enabled": True,
        "audit": {
            "ignore_users": [],
            "ignore_requests": [],
            "disabled_rest_categories": ["AUTHENTICATED", "GRANTED_PRIVILEGES"],
            "disabled_transport_categories": ["AUTHENTICATED", "GRANTED_PRIVILEGES"],
            "log_request_body": False,
            "resolve_indices": False,
            "resolve_bulk_requests": False,
            "exclude_sensitive_headers": True,
            "enable_transport": False,
            "enable_rest": True,
        },
        "compliance": {
            "enabled": True,
            "write_log_diffs": False,
            "read_watched_fields": {},
            "read_ignore_users": [],
            "write_watched_indices": [],
            "write_ignore_users": [],
            "read_metadata_only": True,
            "write_metadata_only": True,
            "external_config": False,
            "internal_config": True,
        },
    }

    def test_update_audit_config(self) -> None:
        response = self.client.security.update_audit_config(
            body=self.AUDIT_CONFIG_SETTINGS
        )
        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))

    def test_update_audit_configuration(self) -> None:
        response = self.client.security.update_audit_configuration(
            body=self.AUDIT_CONFIG_SETTINGS
        )
        self.assertNotIn("errors", response)
        self.assertEqual("OK", response.get("status"))
