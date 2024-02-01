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

import re
from datetime import datetime
from typing import Any

from pytest import fixture

from opensearchpy.connection.connections import add_connection
from opensearchpy.helpers import bulk
from opensearchpy.helpers.test import get_test_client

from .test_data import (
    DATA,
    FLAT_DATA,
    TEST_GIT_DATA,
    create_flat_git_index,
    create_git_index,
)
from .test_document import Comment, History, PullRequest, User


@fixture(scope="session")  # type: ignore
def client() -> Any:
    client = get_test_client(verify_certs=False, http_auth=("admin", "admin"))
    add_connection("default", client)
    return client


@fixture(scope="session")  # type: ignore
def opensearch_version(client: Any) -> Any:
    """
    yields a major version from the client
    :param client: client to connect to opensearch
    """
    info: Any = client.info()
    print(info)
    yield (int(x) for x in match_version(info))


def match_version(info: Any) -> Any:
    """
    matches the major version from the given client info
    :param info: part of the response from OpenSearch
    """
    match = re.match(r"^([0-9.]+)", info["version"]["number"])
    assert match is not None
    yield match.group(1).split(".")


@fixture  # type: ignore
def write_client(client: Any) -> Any:
    yield client
    client.indices.delete("test-*", ignore=404)
    client.indices.delete_template("test-template", ignore=404)


@fixture(scope="session")  # type: ignore
def data_client(client: Any) -> Any:
    # create mappings
    create_git_index(client, "git")
    create_flat_git_index(client, "flat-git")
    # load data
    bulk(client, DATA, raise_on_error=True, refresh=True)
    bulk(client, FLAT_DATA, raise_on_error=True, refresh=True)
    yield client
    client.indices.delete("git", ignore=404)
    client.indices.delete("flat-git", ignore=404)


@fixture  # type: ignore
def pull_request(write_client: Any) -> Any:
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


@fixture  # type: ignore
def setup_ubq_tests(client: Any) -> str:
    # todo what's a ubq test?
    index = "test-git"
    create_git_index(client, index)
    bulk(client, TEST_GIT_DATA, raise_on_error=True, refresh=True)
    return index
