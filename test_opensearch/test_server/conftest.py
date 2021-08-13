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

import pytest

import opensearch
from opensearch.helpers.test import CA_CERTS, OPENSEARCH_URL

from ..utils import wipe_cluster

# Information about the OpenSearch instance running, if any
# Used for
OPENSEARCH_VERSION = ""
OPENSEARCH_BUILD_HASH = ""
OPENSEARCH_REST_API_TESTS = []


@pytest.fixture(scope="session")
def sync_client_factory():
    client = None
    try:
        # Configure the client with certificates and optionally
        # an HTTP conn class depending on 'PYTHON_CONNECTION_CLASS' envvar
        kw = {
            "timeout": 3,
            "ca_certs": CA_CERTS,
            "headers": {"Authorization": "Basic ZWxhc3RpYzpjaGFuZ2VtZQ=="},
        }
        if "PYTHON_CONNECTION_CLASS" in os.environ:
            from opensearch import connection

            kw["connection_class"] = getattr(
                connection, os.environ["PYTHON_CONNECTION_CLASS"]
            )

        # We do this little dance with the URL to force
        # Requests to respect 'headers: None' within rest API spec tests.
        client = opensearch.OpenSearch(
            OPENSEARCH_URL.replace("elastic:changeme@", ""), **kw
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


@pytest.fixture(scope="function")
def sync_client(sync_client_factory):
    try:
        yield sync_client_factory
    finally:
        wipe_cluster(sync_client_factory)
