# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import os
import re
from datetime import datetime

from pytest import fixture, skip

from opensearchpy import AsyncOpenSearch
from opensearchpy._async.helpers.actions import async_bulk
from opensearchpy.connection.async_connections import add_connection
from opensearchpy.exceptions import ConnectionError
from test_opensearchpy.test_server.test_helpers.test_data import (
    DATA,
    FLAT_DATA,
    TEST_GIT_DATA,
    create_flat_git_index,
    create_git_index,
)
from test_opensearchpy.test_server.test_helpers.test_document import (
    Comment,
    History,
    PullRequest,
    User,
)

# from opensearchpy._async.helpers.test import get_test_client


@fixture(scope="session")
async def client():
    opensearch_url = "http://localhost:9200/"
    kwargs = {}
    # "verify_certs": False will optionally generate a warning message
    # (see :class:`~opensearchpy.Urllib3HttpConnection` for detailed description of the options)::
    if (
        "SECURE_INTEGRATION" in os.environ
        and os.environ["SECURE_INTEGRATION"] == "true"
    ):
        opensearch_url = "https://localhost:9200/"
        kwargs = {
            "http_auth": ("admin", "admin"),
            "verify_certs": False,
        }
    try:
        client = AsyncOpenSearch(opensearch_url, **kwargs)
        client.cluster.health(wait_for_status="yellow")
        await add_connection("default", client)
        return client
    except ConnectionError:
        skip()


# @fixture(scope="session")
# def client():
#   client = get_test_client(verify_certs=False, http_auth=("admin", "admin"))
#   add_connection("default", client)
#  return client


@fixture(scope="session")
def opensearch_version(client):
    info = client.info()
    print(info)
    yield tuple(
        int(x)
        for x in re.match(r"^([0-9.]+)", info["version"]["number"]).group(1).split(".")
    )


@fixture
def write_client(client):
    yield client
    client.indices.delete("test-*", ignore=404)
    client.indices.delete_template("test-template", ignore=404)


@fixture
def data_client(client):
    # create mappings
    create_git_index(client, "git")
    create_flat_git_index(client, "flat-git")
    # load data
    async_bulk(client, DATA, raise_on_error=True, refresh=True)
    async_bulk(client, FLAT_DATA, raise_on_error=True, refresh=True)
    yield client
    client.indices.delete("git", ignore=404)
    client.indices.delete("flat-git", ignore=404)


@fixture
def pull_request(write_client):
    PullRequest.init()
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
    pr.save(refresh=True)
    return pr


@fixture
def setup_ubq_tests(client):
    index = "test-git"
    create_git_index(client, index)
    async_bulk(client, TEST_GIT_DATA, raise_on_error=True, refresh=True)
    return index
