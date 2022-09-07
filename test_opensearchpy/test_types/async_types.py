# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from typing import Any, AsyncGenerator, Dict

from opensearchpy import (
    AIOHttpConnection,
    AsyncOpenSearch,
    AsyncTransport,
    ConnectionPool,
)
from opensearchpy.helpers import (
    async_bulk,
    async_reindex,
    async_scan,
    async_streaming_bulk,
)

client = AsyncOpenSearch(
    [{"host": "localhost", "port": 9443}],
    transport_class=AsyncTransport,
)
t = AsyncTransport(
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
        client,
        query={"query": {"match_all": {}}},
        request_timeout=10,
        clear_scroll=True,
        scroll_kwargs={"request_timeout": 10},
    ):
        pass
    async for _ in async_scan(
        client,
        raise_on_error=False,
        preserve_order=False,
        scroll="10m",
        size=10,
        request_timeout=10.0,
    ):
        pass


async def async_streaming_bulk_types() -> None:
    async for _ in async_streaming_bulk(client, async_gen()):
        pass
    async for _ in async_streaming_bulk(client, async_gen().__aiter__()):
        pass
    async for _ in async_streaming_bulk(client, [{}]):
        pass
    async for _ in async_streaming_bulk(client, ({},)):
        pass


async def async_bulk_types() -> None:
    _, _ = await async_bulk(client, async_gen())
    _, _ = await async_bulk(client, async_gen().__aiter__())
    _, _ = await async_bulk(client, [{}])
    _, _ = await async_bulk(client, ({},))


async def async_reindex_types() -> None:
    _, _ = await async_reindex(
        client, "src-index", "target-index", query={"query": {"match": {"key": "val"}}}
    )
    _, _ = await async_reindex(
        client,
        source_index="src-index",
        target_index="target-index",
        target_client=client,
    )
    _, _ = await async_reindex(
        client,
        "src-index",
        "target-index",
        chunk_size=1,
        scroll="10m",
        scan_kwargs={"request_timeout": 10},
        bulk_kwargs={"request_timeout": 10},
    )
