# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import asyncio

import pytest

import opensearchpy
from opensearchpy.helpers.test import OPENSEARCH_URL

from ...utils import wipe_cluster

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
async def async_client():
    client = None
    try:
        if not hasattr(opensearchpy, "AsyncOpenSearch"):
            pytest.skip("test requires 'AsyncOpenSearch'")

        kw = {"timeout": 3}
        client = opensearchpy.AsyncOpenSearch(OPENSEARCH_URL, **kw)

        # wait for yellow status
        for _ in range(100):
            try:
                await client.cluster.health(wait_for_status="yellow")
                break
            except ConnectionError:
                await asyncio.sleep(0.1)
        else:
            # timeout
            pytest.skip("OpenSearch failed to start.")

        yield client

    finally:
        if client:
            wipe_cluster(client)
            await client.close()
