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


from typing import Any, AsyncGenerator, Dict, Generator

from opensearchpy1 import (
    AIOHttpConnection,
    AsyncOpenSearch,
    AsyncTransport,
    ConnectionPool,
    OpenSearch,
    RequestsHttpConnection,
    Transport,
)
from opensearchpy1.helpers import (
    async_bulk,
    async_reindex,
    async_scan,
    async_streaming_bulk,
    bulk,
    reindex,
    scan,
    streaming_bulk,
)

client = OpenSearch(
    [{"host": "localhost", "port": 9443}],
    transport_class=Transport,
)
t = Transport(
    [{}],
    connection_class=RequestsHttpConnection,
    connection_pool_class=ConnectionPool,
    sniff_on_start=True,
    sniffer_timeout=0.1,
    sniff_timeout=1,
    sniff_on_connection_fail=False,
    max_retries=1,
    retry_on_status={100, 400, 503},
    retry_on_timeout=True,
    send_get_body_as="source",
)


def sync_gen() -> Generator[Dict[Any, Any], None, None]:
    yield {}


def scan_types() -> None:
    for _ in scan(
        client,
        query={"query": {"match_all": {}}},
        request_timeout=10,
        clear_scroll=True,
        scroll_kwargs={"request_timeout": 10},
    ):
        pass
    for _ in scan(
        client,
        raise_on_error=False,
        preserve_order=False,
        scroll="10m",
        size=10,
        request_timeout=10.0,
    ):
        pass


def streaming_bulk_types() -> None:
    for _ in streaming_bulk(client, sync_gen()):
        pass
    for _ in streaming_bulk(client, sync_gen().__iter__()):
        pass
    for _ in streaming_bulk(client, [{}]):
        pass
    for _ in streaming_bulk(client, ({},)):
        pass


def bulk_types() -> None:
    _, _ = bulk(client, sync_gen())
    _, _ = bulk(client, sync_gen().__iter__())
    _, _ = bulk(client, [{}])
    _, _ = bulk(client, ({},))


def reindex_types() -> None:
    _, _ = reindex(
        client, "src-index", "target-index", query={"query": {"match": {"key": "val"}}}
    )
    _, _ = reindex(
        client,
        source_index="src-index",
        target_index="target-index",
        target_client=client,
    )
    _, _ = reindex(
        client,
        "src-index",
        "target-index",
        chunk_size=1,
        scroll="10m",
        scan_kwargs={"request_timeout": 10},
        bulk_kwargs={"request_timeout": 10},
    )


client2 = AsyncOpenSearch(
    [{"host": "localhost", "port": 9443}],
    transport_class=AsyncTransport,
)
t2 = AsyncTransport(
    [{}],
    connection_class=AIOHttpConnection,
    connection_pool_class=ConnectionPool,
    sniff_on_start=True,
    sniffer_timeout=0.1,
    sniff_timeout=1,
    sniff_on_connection_fail=False,
    max_retries=1,
    retry_on_status={100, 400, 503},
    retry_on_timeout=True,
    send_get_body_as="source",
)


async def async_gen() -> AsyncGenerator[Dict[Any, Any], None]:
    yield {}


async def async_scan_types() -> None:
    async for _ in async_scan(
        client2,
        query={"query": {"match_all": {}}},
        request_timeout=10,
        clear_scroll=True,
        scroll_kwargs={"request_timeout": 10},
    ):
        pass
    async for _ in async_scan(
        client2,
        raise_on_error=False,
        preserve_order=False,
        scroll="10m",
        size=10,
        request_timeout=10.0,
    ):
        pass


async def async_streaming_bulk_types() -> None:
    async for _ in async_streaming_bulk(client2, async_gen()):
        pass
    async for _ in async_streaming_bulk(client2, async_gen().__aiter__()):
        pass
    async for _ in async_streaming_bulk(client2, [{}]):
        pass
    async for _ in async_streaming_bulk(client2, ({},)):
        pass


async def async_bulk_types() -> None:
    _, _ = await async_bulk(client2, async_gen())
    _, _ = await async_bulk(client2, async_gen().__aiter__())
    _, _ = await async_bulk(client2, [{}])
    _, _ = await async_bulk(client2, ({},))


async def async_reindex_types() -> None:
    _, _ = await async_reindex(
        client2, "src-index", "target-index", query={"query": {"match": {"key": "val"}}}
    )
    _, _ = await async_reindex(
        client2,
        source_index="src-index",
        target_index="target-index",
        target_client=client2,
    )
    _, _ = await async_reindex(
        client2,
        "src-index",
        "target-index",
        chunk_size=1,
        scroll="10m",
        scan_kwargs={"request_timeout": 10},
        bulk_kwargs={"request_timeout": 10},
    )
