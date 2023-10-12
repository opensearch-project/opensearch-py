#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import time

from thread_with_return_value import ThreadWithReturnValue

from opensearchpy import OpenSearch

host = "localhost"
port = 9200
auth = ("admin", "admin")
request_count = 250

# import logging
# import sys

# root = logging.getLogger()
# # root.setLevel(logging.DEBUG)
# # logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)

# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)


def get_info(client, request_count):
    tt = 0
    for n in range(request_count):
        start = time.time() * 1000
        rc = client.info()
        total_time = time.time() * 1000 - start
        tt += total_time
    return tt


def test(thread_count=1, request_count=1, client_count=1):
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


def test_1():
    test(1, 32 * request_count, 1)


def test_2():
    test(2, 16 * request_count, 2)


def test_4():
    test(4, 8 * request_count, 3)


def test_8():
    test(8, 4 * request_count, 8)


def test_32():
    test(32, request_count, 32)


__benchmarks__ = [(test_1, test_32, "1 thread vs. 32 threads (sync)")]
