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

import unittest

from opensearchpy.exceptions import NotFoundError
from opensearchpy.helpers.test import OPENSEARCH_VERSION, SECURE_INTEGRATION

from . import OpenSearchTestCase


class TestAlertingPlugin(OpenSearchTestCase):
    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION < (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_create_destination(self):
        # Test to create alert destination
        dummy_destination = {
            "name": "my-destination",
            "type": "slack",
            "slack": {"url": "http://www.example.com"},
        }
        response = self.client.alerting.create_destination(dummy_destination)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION < (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_get_destination(self):
        # Create a dummy destination
        self.test_create_destination()

        # Try fetching the destination
        response = self.client.alerting.get_destination()

        self.assertNotIn("errors", response)
        self.assertGreaterEqual(response["totalDestinations"], 1)
        self.assertEqual(response["totalDestinations"], len(response["destinations"]))

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION < (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_create_monitor(self):
        # Create a dummy destination
        self.test_create_destination()

        # Try fetching the destination
        destination = self.client.alerting.get_destination()
        self.assertGreaterEqual(
            destination["totalDestinations"],
            1,
            "No destination entries found in the database.",
        )

        # Select the first destination available
        destination = destination["destinations"][0]

        # A dummy schedule for 1 minute interval
        schedule = {"period": {"interval": 1, "unit": "MINUTES"}}

        # A dummy query fetching everything
        query = {"query": {"query_string": {"query": "*"}}}

        # A dummy action with the dummy destination
        action = {
            "name": "test-action",
            "destination_id": destination["id"],
            "message_template": {"source": "This is my message body."},
            "throttle_enabled": True,
            "throttle": {"value": 27, "unit": "MINUTES"},
            "subject_template": {"source": "TheSubject"},
        }

        # A dummy trigger with the dummy action
        triggers = {
            "name": "test-trigger",
            "severity": "1",
            "condition": {
                "script": {
                    "source": "ctx.results[0].hits.total.value > 0",
                    "lang": "painless",
                }
            },
            "actions": [action],
        }

        # A dummy monitor with the dummy schedule, dummy query, dummy trigger
        monitor = {
            "type": "monitor",
            "name": "test-monitor",
            "monitor_type": "query_level_monitor",
            "enabled": True,
            "schedule": schedule,
            "inputs": [{"search": {"indices": ["*"], "query": query}}],
            "triggers": [triggers],
        }

        response = self.client.alerting.create_monitor(monitor)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)
        self.assertIn("monitor", response)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION < (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_search_monitor(self):
        # Create a dummy monitor
        self.test_create_monitor()

        # Create a monitor search query by it's name
        query = {"query": {"match": {"monitor.name": "test-monitor"}}}

        # Perform the search with the above query
        response = self.client.alerting.search_monitor(query)

        self.assertNotIn("errors", response)
        self.assertIn("hits", response)
        self.assertEqual(response["hits"]["total"]["value"], 1, "No monitor found.")

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION < (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_get_monitor(self):
        # Create a dummy monitor
        self.test_create_monitor()

        # Create a monitor search query by it's name
        query = {"query": {"match": {"monitor.name": "test-monitor"}}}

        # Perform the search with the above query
        response = self.client.alerting.search_monitor(query)

        # Select the first monitor
        monitor = response["hits"]["hits"][0]

        # Fetch the monitor by id
        response = self.client.alerting.get_monitor(monitor["_id"])

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)
        self.assertIn("monitor", response)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION < (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_run_monitor(self):
        # Create a dummy monitor
        self.test_create_monitor()

        # Create a monitor search query by it's name
        query = {"query": {"match": {"monitor.name": "test-monitor"}}}

        # Perform the search with the above query
        response = self.client.alerting.search_monitor(query)

        # Select the first monitor
        monitor = response["hits"]["hits"][0]

        # Run the monitor by id
        response = self.client.alerting.run_monitor(monitor["_id"])

        self.assertEqual(response["error"], None)
        self.assertIn("monitor_name", response)
        self.assertIn("period_start", response)
        self.assertIn("period_end", response)


@unittest.skipUnless(
    SECURE_INTEGRATION,
    "Security plugin is disbaled",
)
class TestSecurityPlugin(OpenSearchTestCase):
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

    def test_create_role(self):
        # Test to create role
        response = self.client.security.put_role(self.ROLE_NAME, body=self.ROLE_CONTENT)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

    def test_get_role(self):
        # Create a role
        self.test_create_role()

        # Test to fetch the role
        response = self.client.security.get_role(self.ROLE_NAME)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)
        self.assertEqual(response["_id"], self.ROLE_NAME)

    def test_update_role(self):
        # Create a role
        self.test_create_role()

        role_content = self.ROLE_CONTENT.copy()
        role_content["cluster_permissions"] = ["cluster_all"]

        # Test to update role
        response = self.client.security.put_role(self.ROLE_NAME, body=role_content)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

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
        response = self.client.security.put_user(self.USER_NAME, body=self.USER_CONTENT)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

    def test_create_user_with_role(self):
        self.test_create_role()

        # Test to create user
        response = self.client.security.put_user(
            self.USER_NAME,
            body={
                "password": "test_password",
                "opendistro_security_roles": [self.ROLE_NAME],
            },
        )

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

    def test_get_user(self):
        # Create a user
        self.test_create_user()

        # Test to fetch the user
        response = self.client.security.get_user(self.USER_NAME)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)
        self.assertEqual(response["_id"], self.USER_NAME)

    def test_update_user(self):
        # Create a user
        self.test_create_user()

        user_content = self.USER_CONTENT.copy()
        user_content["cluster_permissions"] = ["cluster_all"]

        # Test to update user
        response = self.client.security.put_user(self.USER_NAME, body=user_content)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

    def test_delete_user(self):
        # Create a user
        self.test_create_user()

        # Test to delete the user
        response = self.client.security.delete_user(self.USER_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the user
        with self.assertRaises(NotFoundError):
            response = self.client.security.get_user(self.USER_NAME)
