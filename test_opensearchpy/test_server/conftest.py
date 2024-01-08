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
import time
from typing import Any

import pytest

import opensearchpy
from opensearchpy.helpers.test import OPENSEARCH_URL

from ..utils import wipe_cluster

# Information about the OpenSearch instance running, if any
# Used for
OPENSEARCH_VERSION = ""
OPENSEARCH_BUILD_HASH = ""
OPENSEARCH_REST_API_TESTS: Any = []


@pytest.fixture(scope="session")  # type: ignore
def sync_client_factory() -> Any:
    client = None
    try:
        # Configure the client optionally with an HTTP conn class
        # depending on 'PYTHON_CONNECTION_CLASS' envvar
        kw = {
            "timeout": 3,
            "headers": {"Authorization": "Basic ZWxhc3RpYzpjaGFuZ2VtZQ=="},
        }
        if "PYTHON_CONNECTION_CLASS" in os.environ:
            from opensearchpy import connection

            kw["connection_class"] = getattr(
                connection, os.environ["PYTHON_CONNECTION_CLASS"]
            )

        # We do this little dance with the URL to force
        # Requests to respect 'headers: None' within rest API spec tests.
        client = opensearchpy.OpenSearch(
            OPENSEARCH_URL.replace("elastic:changeme@", ""), **kw  # type: ignore
        )

        # Wait for the cluster to report a status of 'yellow'
        for _ in range(100):
            try:
                client.cluster.health(wait_for_status="yellow")
                break
            except ConnectionError:
                time.sleep(0.1)
        else:
            pytest.skip("OpenSearch wasn't running at %r" % (OPENSEARCH_URL,))

        wipe_cluster(client)
        yield client
    finally:
        if client:
            client.close()


@pytest.fixture(scope="function")  # type: ignore
def sync_client(sync_client_factory: Any) -> Any:
    try:
        yield sync_client_factory
    finally:
        wipe_cluster(sync_client_factory)
