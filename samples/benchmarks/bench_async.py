#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import asyncio
import math
import uuid
from threading import Thread
from opensearchpy import OpenSearch, AsyncOpenSearch, AsyncHttpConnection

host = 'localhost'
port = 9200
auth = ('admin', 'admin')
index_name = 'test-index-async'
item_count = 100

async def index_records(client, item_count):
    await asyncio.gather(*[
        client.index(
            index = index_name,
            body = {
                'title': f"Moneyball",
                'director': 'Bennett Miller',
                'year': '2011'
            },
            id = uuid.uuid4()
        ) for j in range(item_count)
    ])

async def test_async(client_count = 1, item_count = 1):
    clients = []
    for i in range(client_count):
        clients.append(
            AsyncOpenSearch(
                hosts = [{'host': host, 'port': port}],
                http_auth = auth,
                use_ssl = True,
                verify_certs = False,
                ssl_show_warn = False,
                connection_class = AsyncHttpConnection,
                pool_maxsize = client_count
            )
        )

    if await clients[0].indices.exists(index_name):
        await clients[0].indices.delete(index_name)

    await clients[0].indices.create(index_name)

    await asyncio.gather(*[
        index_records(clients[i], item_count)
        for i in range(client_count)
    ])
       
    await clients[0].indices.refresh(index=index_name)
    print(await clients[0].count(index=index_name))

    await clients[0].indices.delete(index_name)
    
    await asyncio.gather(*[client.close() for client in clients])

def test(item_count = 1, client_count = 1):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_async(item_count, client_count))
    loop.close()

def test_1():
    test(1, 32 * item_count)

def test_2():
    test(2, 16 * item_count)

def test_4():
    test(4, 8 * item_count)

def test_8():
    test(8, 4 * item_count)

def test_16():
    test(16, 2 * item_count)

def test_32():
    test(32, item_count)

__benchmarks__ = [
    (test_1, test_8, "1 client vs. more clients (async)")
]