# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from __future__ import unicode_literals

from .. import OpenSearchTestCase


class TestNotificationPlugin(OpenSearchTestCase):
    async def test_create_channel_notification(self) -> None:
        content = {
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
        response = self.client.plugins.notifications.create_config(content)

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)

    async def test_list_all_channel_configurations(self) -> None:
        response = self.client.plugins.notifications.list_features()

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)

    async def test_list_all_notification_configurations(self) -> None:
        response = self.client.plugins.notifications.get_config()

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)

    async def test_get_channel_configuration(self) -> None:
        response = self.client.plugins.notifications.get_config(config_id="sample-id")

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)

    async def test_update_channel_configuration(self) -> None:
        response = self.client.plugins.notifications.update_config(
            config_id="sample-id"
        )

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)

    async def test_delete_channel_configuration(self) -> None:
        # Try fetching the destination
        response = self.client.plugins.notifications.delete_config(
            config_id="sample-id"
        )

        self.assertNotIn("errors", response)
        self.assertIn("config_id", response)
