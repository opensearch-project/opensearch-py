#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import asyncio
import uuid
from typing import Any

from opensearchpy import AsyncHttpConnection, AsyncOpenSearch


async def index_records(client: Any, index_name: str, item_count: int) -> None:
    """asynchronously bulk index item_count records into the index (index_name)"""
    await asyncio.gather(
        *[
            client.index(
                index=index_name,
                body={
                    "title": "Moneyball",
                    "director": "Bennett Miller",
                    "year": "2011",
                },
                id=uuid.uuid4(),
            )
            for j in range(item_count)
        ]
    )


async def test_async(client_count: int = 1, item_count: int = 1) -> None:
    """
    asynchronously index with item_count records and run client_count
    clients. This function can be used to test balancing the number of
    items indexed with the number of documents.
    """
    host = "localhost"
    port = 9200
    auth = ("admin", "admin")
    index_name = "test-index-async"

    clients = []
    for i in range(client_count):
        clients.append(
            AsyncOpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=False,
                ssl_show_warn=False,
                connection_class=AsyncHttpConnection,
                pool_maxsize=client_count,
            )
        )

    if await clients[0].indices.exists(index_name):
        await clients[0].indices.delete(index_name)

    await clients[0].indices.create(index_name)

    await asyncio.gather(
        *[
            index_records(clients[i], index_name, item_count)
            for i in range(client_count)
        ]
    )

    await clients[0].indices.refresh(index=index_name)
    print(await clients[0].count(index=index_name))

    await clients[0].indices.delete(index_name)

    await asyncio.gather(*[client.close() for client in clients])


def test(item_count: int = 1, client_count: int = 1) -> None:
    """sets up and executes the asynchronous tests"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_async(item_count, client_count))
    loop.close()


ITEM_COUNT = 100


def test_1() -> None:
    """run a test for one item and 32*ITEM_COUNT clients"""
    test(1, 32 * ITEM_COUNT)


def test_2() -> None:
    """run a test for two items and 16*ITEM_COUNT clients"""
    test(2, 16 * ITEM_COUNT)


def test_4() -> None:
    """run a test for two items and 8*ITEM_COUNT clients"""
    test(4, 8 * ITEM_COUNT)


def test_8() -> None:
    """run a test for four items and 4*ITEM_COUNT clients"""
    test(8, 4 * ITEM_COUNT)


def test_16() -> None:
    """run a test for 16 items and 2*ITEM_COUNT clients"""
    test(16, 2 * ITEM_COUNT)


def test_32() -> None:
    """run a test for 32 items and ITEM_COUNT clients"""
    test(32, ITEM_COUNT)


__benchmarks__ = [(test_1, test_8, "1 client vs. more clients (async)")]
