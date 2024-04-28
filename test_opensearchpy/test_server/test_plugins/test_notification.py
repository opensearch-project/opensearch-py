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

from opensearchpy.helpers.test import OPENSEARCH_VERSION

from opensearchpy.exceptions import NotFoundError

from .. import OpenSearchTestCase


class TestNotificationPlugin(OpenSearchTestCase):
    CONFIG_ID = "sample-id"
    CONTENT = {
        "config_id": "sample-id",
        "name": "sample-name",
        "config": {
            "name": "Sample Slack Channel",
            "description": "This ialerting.create_destination(dummy_destination)s a Slack channel",
            "config_type": "slack",
            "is_enabled": True,
            "slack": {"url": "https://sample-slack-webhook"},
        },
    }

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION >= (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_create_config(self) -> None:
        response = self.client.plugins.notifications.create_config(self.CONTENT)

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION >= (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_list_channel_config(self) -> None:
        self.test_create_config()

        response = self.client.plugins.notifications.list_features()

        self.assertNotIn("errors", response)
        self.assertIn("allowed_config_type_list", response)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION >= (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_list_all_config(self) -> None:
        self.test_create_config()

        response = self.client.plugins.notifications.get_configs()

        self.assertNotIn("errors", response)
        self.assertIn("config_list", response)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION >= (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_get_config(self) -> None:
        self.test_create_config()

        response = self.client.plugins.notifications.get_config(config_id=self.CONFIG_ID)

        self.assertNotIn("errors", response)
        self.assertIn("config_list", response)
        self.assertEqual(response["config_list"][0]["config_id"], self.CONFIG_ID)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION >= (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_update_config(self) -> None:
        # Create configuration
        self.test_create_config()

        # Fetch the configuration
        response = self.client.plugins.notifications.get_config(self.CONFIG_ID)

        channel_content = self.CONTENT.copy()
        channel_content["config"]["name"] = "Slack Channel"
        channel_content["config"]["description"] = "This is an updated channel configuration"
        channel_content["config"]["config_type"] = "slack"
        channel_content["config"]["is_enabled"] = True
        channel_content["config"]["slack"]["url"] = "https://hooks.slack.com/sample-url"

        # Test to updat configuration
        response = self.client.plugins.notifications.update_config(
            config_id=self.CONFIG_ID, body=channel_content
        )

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)

    @unittest.skipUnless(
        (OPENSEARCH_VERSION) and (OPENSEARCH_VERSION >= (2, 0, 0)),
        "Plugin not supported for opensearch version",
    )
    def test_delete_config(self) -> None:
        self.test_create_config()

        response = self.client.plugins.notifications.delete_config(
            config_id=self.CONFIG_ID
        )

        self.assertNotIn("errors", response)

        # Try fetching the policy
        with self.assertRaises(NotFoundError):
            response = self.client.plugins.notifications.get_config(self.CONFIG_ID)
