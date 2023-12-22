#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import logging
import sys
import time
from typing import Any

from thread_with_return_value import ThreadWithReturnValue

from opensearchpy import OpenSearch


def get_info(client: Any, request_count: int) -> float:
    """get info from client"""
    tt: float = 0
    for n in range(request_count):
        start = time.time() * 1000
        client.info()
        total_time = time.time() * 1000 - start
        tt += total_time
    return tt


def test(thread_count: int = 1, request_count: int = 1, client_count: int = 1) -> None:
    """test to index with thread_count threads, item_count records and run client_count clients"""
    host = "localhost"
    port = 9200
    auth = ("admin", "admin")

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
    for i in range(client_count):
        clients.append(
            OpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=False,
                ssl_show_warn=False,
                pool_maxsize=thread_count,
            )
        )

    threads = []
    for thread_id in range(thread_count):
        thread = ThreadWithReturnValue(
            target=get_info, args=[clients[thread_id % len(clients)], request_count]
        )
        threads.append(thread)
        thread.start()

    latency = 0
    for t in threads:
        latency += t.join()

    print(f"latency={latency}")


REQUEST_COUNT = 250


def test_1() -> None:
    """testing 1 threads"""
    test(1, 32 * REQUEST_COUNT, 1)


def test_2() -> None:
    """testing 2 threads"""
    test(2, 16 * REQUEST_COUNT, 2)


def test_4() -> None:
    """testing 4 threads"""
    test(4, 8 * REQUEST_COUNT, 3)


def test_8() -> None:
    """testing 8 threads"""
    test(8, 4 * REQUEST_COUNT, 8)


def test_32() -> None:
    """testing 32 threads"""
    test(32, REQUEST_COUNT, 32)


__benchmarks__ = [(test_1, test_32, "1 thread vs. 32 threads (sync)")]
