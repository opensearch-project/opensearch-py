#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import time
import uuid
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from thread_with_return_value import ThreadWithReturnValue

host = 'localhost'
port = 9200
auth = ('admin', 'admin')
index_name = 'test-index-sync'
item_count = 1000

import logging
import sys

root = logging.getLogger()
# root.setLevel(logging.DEBUG)
# logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def index_records(client, item_count):
    tt = 0
    for n in range(10):
        data = []
        for i in range(item_count):
            data.append(json.dumps({ "index": { "_index": index_name, "_id": str(uuid.uuid4()) }}))
            data.append(json.dumps({ "value": i }))
        data = "\n".join(data)

        start = time.time() * 1000
        rc = client.bulk(data)
        if rc["errors"]:
            raise Exception(rc["errors"])

        server_time = rc['took']
        total_time = time.time() * 1000 - start

        if total_time < server_time:
            raise Exception(f"total={total_time} < server={server_time}")

        tt += total_time - server_time
    return tt

def test(thread_count = 1, item_count = 1, client_count = 1):
    clients = []
    for i in range(client_count):
        clients.append(OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            ssl_show_warn = False,
            pool_maxsize = thread_count,
            connection_class = RequestsHttpConnection
        ))

    if clients[0].indices.exists(index_name):
        clients[0].indices.delete(index_name)

    clients[0].indices.create(index=index_name, body={
        "mappings":{
            "properties": {
                "value": {
                    "type": "float"
                },
            }
        }
    })

    threads = []
    for thread_id in range(thread_count):
        thread = ThreadWithReturnValue(target=index_records, args=[
            clients[thread_id % len(clients)],
            item_count
        ])
        threads.append(thread)
        thread.start()

    latency = 0
    for t in threads:
        latency += t.join()

    clients[0].indices.refresh(index=index_name)
    count = clients[0].count(index=index_name)

    clients[0].indices.delete(index_name)

    print(f"{count}, latency={latency}")

def test_1():
    test(1, 32 * item_count, 1)

def test_2():
    test(2, 16 * item_count, 2)

def test_4():
    test(4, 8 * item_count, 3)

def test_8():
    test(8, 4 * item_count, 8)

def test_32():
    test(32, item_count, 32)

__benchmarks__ = [
    (test_1, test_32, "1 thread vs. 32 threads (sync)")
]