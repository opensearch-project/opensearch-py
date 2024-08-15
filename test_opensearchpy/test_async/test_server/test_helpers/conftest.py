# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import os
import re
from datetime import datetime
from typing import Any

import pytest
from pytest import fixture

from opensearchpy._async.helpers.actions import async_bulk
from opensearchpy._async.helpers.test import get_test_client
from opensearchpy.connection.async_connections import add_connection
from test_opensearchpy.test_async.test_server.test_helpers.test_data import (
    DATA,
    FLAT_DATA,
    TEST_GIT_DATA,
    create_flat_git_index,
    create_git_index,
)
from test_opensearchpy.test_async.test_server.test_helpers.test_document import (
    Comment,
    History,
    PullRequest,
    User,
)

pytestmark = pytest.mark.asyncio


@fixture(scope="function")  # type: ignore
async def client() -> Any:
    client = await get_test_client(
        verify_certs=False,
        http_auth=("admin", os.getenv("OPENSEARCH_PASSWORD", "admin")),
    )
    await add_connection("default", client)
    return client


@fixture(scope="function")  # type: ignore
async def opensearch_version(client: Any) -> Any:
    """
    yields the version of the OpenSearch cluster
    :param client: client connection to OpenSearch
    :return: yields major version number
    """
    info = await client.info()
    print(info)
    yield (int(x) async for x in match_version(info))


async def match_version(info: Any) -> Any:
    """
    matches the full semver server version with the given info
    :param info: response from the OpenSearch cluster
    """
    match = re.match(r"^([0-9.]+)", info["version"]["number"])
    assert match is not None
    yield match.group(1).split(".")


@fixture  # type: ignore
async def write_client(client: Any) -> Any:
    yield client
    await client.indices.delete("test-*", ignore=404)
    await client.indices.delete_template("test-template", ignore=404)


@fixture  # type: ignore
async def data_client(client: Any) -> Any:
    """
    create mappings
    """
    await create_git_index(client, "git")
    await create_flat_git_index(client, "flat-git")
    # load data
    await async_bulk(client, DATA, raise_on_error=True, refresh=True)
    await async_bulk(client, FLAT_DATA, raise_on_error=True, refresh=True)
    yield client
    await client.indices.delete("git", ignore=404)
    await client.indices.delete("flat-git", ignore=404)


@fixture  # type: ignore
async def pull_request(write_client: Any) -> Any:
    """
    create dummy pull request instance
    :param write_client: #todo not used
    :return: instance of PullRequest
    """
    await PullRequest.init()
    pr = PullRequest(
        _id=42,
        comments=[
            Comment(
                content="Hello World!",
                author=User(name="honzakral"),
                created_at=datetime(2018, 1, 9, 10, 17, 3, 21184),
                history=[
                    History(
                        timestamp=datetime(2012, 1, 1),
                        diff="-Ahoj Svete!\n+Hello World!",
                    )
                ],
            ),
        ],
        created_at=datetime(2018, 1, 9, 9, 17, 3, 21184),
    )
    await pr.save(refresh=True)
    return pr


@fixture  # type: ignore
async def setup_update_by_query_tests(client: Any) -> str:
    """
    sets up update by query tests
    :param client:
    :return: an index name
    """
    index = "test-git"
    await create_git_index(client, index)
    await async_bulk(client, TEST_GIT_DATA, raise_on_error=True, refresh=True)
    return index
