# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from unittest import TestCase

from urllib3.connectionpool import HTTPConnectionPool

from opensearchpy import OpenSearch, Urllib3HttpConnection


class TestUrlLib3(TestCase):
    def test_default(self) -> None:
        client = OpenSearch()
        self.assertEqual(client.transport.connection_class, Urllib3HttpConnection)
        self.assertEqual(client.transport.pool_maxsize, None)

    def test_connection_class(self) -> None:
        client = OpenSearch(connection_class=Urllib3HttpConnection)
        self.assertEqual(client.transport.connection_class, Urllib3HttpConnection)
        self.assertIsInstance(
            client.transport.connection_pool.connections[0], Urllib3HttpConnection
        )
        self.assertIsInstance(
            client.transport.connection_pool.connections[0].pool, HTTPConnectionPool
        )

    def test_pool_maxsize(self) -> None:
        client = OpenSearch(connection_class=Urllib3HttpConnection, pool_maxsize=42)
        self.assertEqual(client.transport.pool_maxsize, 42)
        # https://github.com/python/cpython/blob/3.12/Lib/queue.py#L35
        self.assertEqual(
            client.transport.connection_pool.connections[0].pool.pool.maxsize, 42
        )
