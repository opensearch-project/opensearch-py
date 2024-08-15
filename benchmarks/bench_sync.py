#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import json
import logging
import os
import sys
import time
import uuid
from typing import Any

from thread_with_return_value import ThreadWithReturnValue

from opensearchpy import OpenSearch, Urllib3HttpConnection


def index_records(client: Any, index_name: str, item_count: int) -> Any:
    """bulk index item_count records into index_name"""
    total_time = 0
    for _ in range(10):
        data: Any = []
        for item in range(item_count):
            data.append(
                json.dumps({"index": {"_index": index_name, "_id": str(uuid.uuid4())}})
            )
            data.append(json.dumps({"value": item}))
        data = "\n".join(data)

        start = time.time() * 1000
        response = client.bulk(data)
        if response["errors"]:
            raise Exception(response["errors"])

        server_time = response["took"]
        this_time = time.time() * 1000 - start

        if this_time < server_time:
            raise Exception(f"total={this_time} < server={server_time}")

        total_time += this_time - server_time
    return total_time


def test(thread_count: int = 1, item_count: int = 1, client_count: int = 1) -> None:
    """test to index with thread_count threads, item_count records and run client_count clients"""
    host = "localhost"
    port = 9200
    auth = ("admin", os.getenv("OPENSEARCH_PASSWORD", "admin"))
    index_name = "test-index-sync"

    root = logging.getLogger()
    # root.setLevel(logging.DEBUG)
    # logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    clients = []
    for _ in range(client_count):
        clients.append(
            OpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=False,
                ssl_show_warn=False,
                pool_maxsize=thread_count,
                connection_class=Urllib3HttpConnection,
            )
        )

    if clients[0].indices.exists(index_name):
        clients[0].indices.delete(index_name)

    clients[0].indices.create(
        index=index_name,
        body={
            "mappings": {
                "properties": {
                    "value": {"type": "float"},
                }
            }
        },
    )

    threads = []
    for thread_id in range(thread_count):
        thread = ThreadWithReturnValue(
            target=index_records,
            args=[clients[thread_id % len(clients)], index_name, item_count],
        )
        threads.append(thread)
        thread.start()

    latency = 0
    for thread in threads:
        latency += thread.join()

    clients[0].indices.refresh(index=index_name)
    count = clients[0].count(index=index_name)

    clients[0].indices.delete(index_name)

    print(f"{count}, latency={latency}")


ITEM_COUNT = 1000


def test_1() -> None:
    """testing 1 threads"""
    test(1, 32 * ITEM_COUNT, 1)


def test_2() -> None:
    """testing 2 threads"""
    test(2, 16 * ITEM_COUNT, 2)


def test_4() -> None:
    """testing 4 threads"""
    test(4, 8 * ITEM_COUNT, 3)


def test_8() -> None:
    """testing 8 threads"""
    test(8, 4 * ITEM_COUNT, 8)


def test_32() -> None:
    """testing 32 threads"""
    test(32, ITEM_COUNT, 32)


__benchmarks__ = [(test_1, test_32, "1 thread vs. 32 threads (sync)")]
