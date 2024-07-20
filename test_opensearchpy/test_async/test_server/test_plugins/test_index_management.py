# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy.exceptions import NotFoundError

from .. import AsyncOpenSearchTestCase

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestIndexManagementPlugin(AsyncOpenSearchTestCase):
    POLICY_NAME = "example-policy"
    POLICY_CONTENT = {
        "policy": {
            "description": "hot warm delete workflow",
            "default_state": "hot",
            "schema_version": 1,
            "states": [
                {
                    "name": "hot",
                    "actions": [
                        {
                            "rollover": {
                                "min_index_age": "1d",
                            }
                        }
                    ],
                    "transitions": [{"state_name": "warm"}],
                },
                {
                    "name": "warm",
                    "actions": [{"replica_count": {"number_of_replicas": 5}}],
                    "transitions": [
                        {
                            "state_name": "delete",
                            "conditions": {"min_index_age": "30d"},
                        }
                    ],
                },
                {
                    "name": "delete",
                    "actions": [
                        {
                            "notification": {
                                "destination": {"chime": {"url": "<URL>"}},
                                "message_template": {
                                    "source": "The index {{ctx.index}} is being deleted"
                                },
                            }
                        },
                        {"delete": {}},
                    ],
                },
            ],
            "ism_template": {"index_patterns": ["log*"], "priority": 100},
        }
    }

    async def test_create_policy(self) -> None:
        # Test to create policy
        response = await self.client.index_management.put_policy(
            policy=self.POLICY_NAME, body=self.POLICY_CONTENT
        )

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

    async def test_get_policy(self) -> None:
        # Create a policy
        await self.test_create_policy()

        # Test to fetch the policy
        response = await self.client.index_management.get_policy(self.POLICY_NAME)

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)
        self.assertEqual(response["_id"], self.POLICY_NAME)

    async def test_update_policy(self) -> None:
        # Create a policy
        await self.test_create_policy()

        # Fetch the policy
        response = await self.client.index_management.get_policy(self.POLICY_NAME)
        params = {
            "if_seq_no": response["_seq_no"],
            "if_primary_term": response["_primary_term"],
        }

        policy_content = self.POLICY_CONTENT.copy()
        policy_content["policy"]["description"] = "example workflow"

        # Test to update policy
        response = await self.client.index_management.put_policy(
            policy=self.POLICY_NAME, body=policy_content, params=params
        )

        self.assertNotIn("errors", response)
        self.assertIn("_id", response)

    async def test_delete_policy(self) -> None:
        # Create a policy
        await self.test_create_policy()

        # Test to delete the policy
        response = await self.client.index_management.delete_policy(self.POLICY_NAME)

        self.assertNotIn("errors", response)

        # Try fetching the policy
        with self.assertRaises(NotFoundError):
            response = await self.client.index_management.get_policy(self.POLICY_NAME)
