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


import asyncio
from typing import Any

import pytest
from _pytest.mark.structures import MarkDecorator

import opensearchpy
from opensearchpy.helpers.test import OPENSEARCH_URL

from ...utils import wipe_cluster

pytestmark: MarkDecorator = pytest.mark.asyncio


@pytest.fixture(scope="function")  # type: ignore
async def async_client() -> Any:
    client = None
    try:
        if not hasattr(opensearchpy, "AsyncOpenSearch"):
            pytest.skip("test requires 'AsyncOpenSearch'")

        kw = {"timeout": 3}
        client = opensearchpy.AsyncOpenSearch(OPENSEARCH_URL, **kw)  # type: ignore

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
