#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import asyncio
from threading import Thread
from opensearchpy import OpenSearch, AsyncOpenSearch, RequestsHttpConnection

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
count = 1000

def test_thread_loop_index_record(client, index_name, i):
    client.index(
        index = index_name,
            body = {
                'title': f"Moneyball {i}",
                'director': 'Bennett Miller',
                'year': '2011'
            },
            id = i
        )

def test_multithread_loop():
    clients = []
    for i in range(10):
        clients.append(OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            ssl_show_warn = False
        ))

    index_name = 'test-index-sync'
    if clients[0].indices.exists(index_name):
        clients[0].indices.delete(index_name)

    clients[0].indices.create(index_name)

    for i in range(count):
        threads = []
        threads.append(
            Thread(target=test_thread_loop_index_record, args=[
                clients[i % len(clients)],
                index_name,
                i
            ])
        )

        for t in threads:
            t.start()

        for t in threads:
            t.join()
    
    clients[0].indices.delete(index_name)

def test_thread_loop():
    sync_client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_show_warn = False
    )

    index_name = 'test-index-sync'
    if sync_client.indices.exists(index_name):
        sync_client.indices.delete(index_name)

    sync_client.indices.create(index_name)

    for i in range(count):
        threads = []
        threads.append(
            Thread(target=test_thread_loop_index_record, args=[
                sync_client,
                index_name,
                i
            ])
        )

        for t in threads:
            t.start()

        for t in threads:
            t.join()
    
    sync_client.indices.delete(index_name)

def test_sync_loop():
    sync_client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_show_warn = False,
        connection_class = RequestsHttpConnection,
        pool_maxsize = 1
    )

    index_name = 'test-index-sync'
    if sync_client.indices.exists(index_name):
        sync_client.indices.delete(index_name)

    sync_client.indices.create(index_name)

    for i in range(count):
        sync_client.index(
            index = index_name,
                body = {
                    'title': f"Moneyball {i}",
                    'director': 'Bennett Miller',
                    'year': '2011'
                },
            id = i
        )
    
    sync_client.indices.delete(index_name)

async def test_info_async():
    async_client = AsyncOpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_show_warn = False
    )

    index_name = 'test-index-async'
    if await async_client.indices.exists(index_name):
        await async_client.indices.delete(index_name)

    await async_client.indices.create(index_name)

    await asyncio.gather(*[
        async_client.index(
            index = index_name,
            body = {
                'title': f"Moneyball {i}",
                'director': 'Bennett Miller',
                'year': '2011'
            },
            id = i
        ) for i in range(count)
    ])

    await async_client.indices.delete(index_name)
    await async_client.close()

def test_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_info_async())
    loop.close()

__benchmarks__ = [
    #(test_sync_loop, test_thread_loop, "Sync vs. threaded."),
    #(test_sync_loop, test_async_loop, "Sync vs. async."),
    (test_multithread_loop, test_async_loop, "Multithread loop vs. async.")
    
]