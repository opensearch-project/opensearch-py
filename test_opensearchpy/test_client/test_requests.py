# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from unittest import TestCase

from opensearchpy import OpenSearch, RequestsHttpConnection


class TestRequests(TestCase):
    def test_connection_class(self):
        client = OpenSearch(connection_class=RequestsHttpConnection)
        self.assertEqual(client.transport.pool_maxsize, None)
        self.assertEqual(client.transport.connection_class, RequestsHttpConnection)
        self.assertIsInstance(
            client.transport.connection_pool.connections[0], RequestsHttpConnection
        )

    def test_pool_maxsize(self):
        client = OpenSearch(connection_class=RequestsHttpConnection, pool_maxsize=42)
        self.assertEqual(client.transport.pool_maxsize, 42)
        self.assertEqual(
            client.transport.connection_pool.connections[0]
            .session.adapters["https://"]
            ._pool_maxsize,
            42,
        )
