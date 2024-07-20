# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import json
import time
from typing import Any
from unittest.mock import patch

from opensearchpy.connection import Connection
from opensearchpy.connection_pool import DummyConnectionPool
from opensearchpy.exceptions import ConnectionError, TransportError
from opensearchpy.transport import Transport, get_host_info

from .test_cases import TestCase


class DummyConnection(Connection):
    def __init__(self, **kwargs: Any) -> None:
        self.exception = kwargs.pop("exception", None)
        self.status, self.data = kwargs.pop("status", 200), kwargs.pop("data", "{}")
        self.headers = kwargs.pop("headers", {})
        self.calls: Any = []
        super().__init__(**kwargs)

    def perform_request(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        if self.exception:
            raise self.exception
        return self.status, self.headers, self.data


CLUSTER_NODES = """{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "opensearch",
  "nodes" : {
    "SRZpKFZdQguhhvifmN6UVA" : {
      "name" : "SRZpKFZ",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1",
      "version" : "5.0.0",
      "build_hash" : "253032b",
      "roles" : [ "cluster_manager", "data", "ingest" ],
      "http" : {
        "bound_address" : [ "[fe80::1]:9200", "[::1]:9200", "127.0.0.1:9200" ],
        "publish_address" : "1.1.1.1:123",
        "max_content_length_in_bytes" : 104857600
      }
    }
  }
}"""

CLUSTER_NODES_7X_PUBLISH_HOST = """{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "opensearch",
  "nodes" : {
    "SRZpKFZdQguhhvifmN6UVA" : {
      "name" : "SRZpKFZ",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1",
      "version" : "5.0.0",
      "build_hash" : "253032b",
      "roles" : [ "cluster_manager", "data", "ingest" ],
      "http" : {
        "bound_address" : [ "[fe80::1]:9200", "[::1]:9200", "127.0.0.1:9200" ],
        "publish_address" : "somehost.tld/1.1.1.1:123",
        "max_content_length_in_bytes" : 104857600
      }
    }
  }
}"""


class TestHostsInfoCallback(TestCase):
    def test_cluster_manager_only_nodes_are_ignored(self) -> None:
        nodes = [
            {"roles": ["cluster_manager"]},
            {"roles": ["cluster_manager", "data", "ingest"]},
            {"roles": ["data", "ingest"]},
            {"roles": []},
            {},
        ]
        chosen = [
            i
            for i, node_info in enumerate(nodes)
            if get_host_info(node_info, i) is not None  # type: ignore
        ]
        self.assertEqual([1, 2, 3, 4], chosen)


class TestTransport(TestCase):
    def test_single_connection_uses_dummy_connection_pool(self) -> None:
        t1: Any = Transport([{}])
        self.assertIsInstance(t1.connection_pool, DummyConnectionPool)
        t2: Any = Transport([{"host": "localhost"}])
        self.assertIsInstance(t2.connection_pool, DummyConnectionPool)

    def test_request_timeout_extracted_from_params_and_passed(self) -> None:
        t: Any = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", params={"request_timeout": 42})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", {}, None), t.get_connection().calls[0][0])
        self.assertEqual(
            {"timeout": 42, "ignore": (), "headers": None},
            t.get_connection().calls[0][1],
        )

    def test_timeout_extracted_from_params_and_passed(self) -> None:
        t: Any = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", params={"timeout": 84})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", {}, None), t.get_connection().calls[0][0])
        self.assertEqual(
            {"timeout": 84, "ignore": (), "headers": None},
            t.get_connection().calls[0][1],
        )

    def test_opaque_id(self) -> None:
        t: Any = Transport([{}], opaque_id="app-1", connection_class=DummyConnection)

        t.perform_request("GET", "/")
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", None, None), t.get_connection().calls[0][0])
        self.assertEqual(
            {"timeout": None, "ignore": (), "headers": None},
            t.get_connection().calls[0][1],
        )

        # Now try with an 'x-opaque-id' set on perform_request().
        t.perform_request("GET", "/", headers={"x-opaque-id": "request-1"})
        self.assertEqual(2, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", None, None), t.get_connection().calls[1][0])
        self.assertEqual(
            {"timeout": None, "ignore": (), "headers": {"x-opaque-id": "request-1"}},
            t.get_connection().calls[1][1],
        )

    def test_request_with_custom_user_agent_header(self) -> None:
        t: Any = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", headers={"user-agent": "my-custom-value/1.2.3"})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            {
                "timeout": None,
                "ignore": (),
                "headers": {"user-agent": "my-custom-value/1.2.3"},
            },
            t.get_connection().calls[0][1],
        )

    def test_send_get_body_as_source(self) -> None:
        t: Any = Transport(
            [{}], send_get_body_as="source", connection_class=DummyConnection
        )

        t.perform_request("GET", "/", body={})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            ("GET", "/", {"source": "{}"}, None), t.get_connection().calls[0][0]
        )

    def test_send_get_body_as_post(self) -> None:
        t: Any = Transport(
            [{}], send_get_body_as="POST", connection_class=DummyConnection
        )

        t.perform_request("GET", "/", body={})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("POST", "/", None, b"{}"), t.get_connection().calls[0][0])

    def test_body_gets_encoded_into_bytes(self) -> None:
        t: Any = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", body="你好")
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            ("GET", "/", None, b"\xe4\xbd\xa0\xe5\xa5\xbd"),
            t.get_connection().calls[0][0],
        )

    def test_body_bytes_get_passed_untouched(self) -> None:
        t: Any = Transport([{}], connection_class=DummyConnection)

        body = b"\xe4\xbd\xa0\xe5\xa5\xbd"
        t.perform_request("GET", "/", body=body)
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", None, body), t.get_connection().calls[0][0])

    def test_body_surrogates_replaced_encoded_into_bytes(self) -> None:
        t: Any = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", body="你好\uda6a")
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            ("GET", "/", None, b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"),
            t.get_connection().calls[0][0],
        )

    def test_kwargs_passed_on_to_connections(self) -> None:
        t: Any = Transport([{"host": "google.com"}], port=123)
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://google.com:123", t.connection_pool.connections[0].host)

    def test_kwargs_passed_on_to_connection_pool(self) -> None:
        dt = object()
        t: Any = Transport([{}, {}], dead_timeout=dt)
        self.assertIs(dt, t.connection_pool.dead_timeout)

    def test_custom_connection_class(self) -> None:
        class MyConnection(Connection):
            def __init__(self, **kwargs: Any) -> None:
                self.kwargs = kwargs

        t: Any = Transport([{}], connection_class=MyConnection)
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertIsInstance(t.connection_pool.connections[0], MyConnection)

    def test_add_connection(self) -> None:
        t: Any = Transport([{}], randomize_hosts=False)
        t.add_connection({"host": "google.com", "port": 1234})

        self.assertEqual(2, len(t.connection_pool.connections))
        self.assertEqual(
            "http://google.com:1234", t.connection_pool.connections[1].host
        )

    def test_request_will_fail_after_x_retries(self) -> None:
        t: Any = Transport(
            [{"exception": ConnectionError(None, "abandon ship", Exception())}],
            connection_class=DummyConnection,
        )

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEqual(4, len(t.get_connection().calls))

    def test_failed_connection_will_be_marked_as_dead(self) -> None:
        t: Any = Transport(
            [{"exception": ConnectionError(None, "abandon ship", Exception())}] * 2,
            connection_class=DummyConnection,
        )

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEqual(0, len(t.connection_pool.connections))

    def test_resurrected_connection_will_be_marked_as_live_on_success(self) -> None:
        for method in ("GET", "HEAD"):
            t: Any = Transport([{}, {}], connection_class=DummyConnection)
            con1 = t.connection_pool.get_connection()
            con2 = t.connection_pool.get_connection()
            t.connection_pool.mark_dead(con1)
            t.connection_pool.mark_dead(con2)

            t.perform_request(method, "/")
            self.assertEqual(1, len(t.connection_pool.connections))
            self.assertEqual(1, len(t.connection_pool.dead_count))

    def test_sniff_will_use_seed_connections(self) -> None:
        t: Any = Transport([{"data": CLUSTER_NODES}], connection_class=DummyConnection)
        t.set_connections([{"data": "invalid"}])

        t.sniff_hosts()
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)

    def test_sniff_on_start_fetches_and_uses_nodes_list(self) -> None:
        t: Any = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
        )
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)

    def test_sniff_on_start_ignores_sniff_timeout(self) -> None:
        t: Any = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
            sniff_timeout=12,
        )
        self.assertEqual(
            (("GET", "/_nodes/_all/http"), {"timeout": None}),
            t.seed_connections[0].calls[0],
        )

    def test_sniff_uses_sniff_timeout(self) -> None:
        t: Any = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        t.sniff_hosts()
        self.assertEqual(
            (("GET", "/_nodes/_all/http"), {"timeout": 42}),
            t.seed_connections[0].calls[0],
        )

    def test_sniff_reuses_connection_instances_if_possible(self) -> None:
        t: Any = Transport(
            [{"data": CLUSTER_NODES}, {"host": "1.1.1.1", "port": 123}],
            connection_class=DummyConnection,
            randomize_hosts=False,
        )
        connection = t.connection_pool.connections[1]

        t.sniff_hosts()
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertIs(connection, t.get_connection())

    def test_sniff_on_fail_triggers_sniffing_on_fail(self) -> None:
        t: Any = Transport(
            [
                {"exception": ConnectionError(None, "abandon ship", Exception())},
                {"data": CLUSTER_NODES},
            ],
            connection_class=DummyConnection,
            sniff_on_connection_fail=True,
            max_retries=0,
            randomize_hosts=False,
        )

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)

    @patch("opensearchpy.transport.Transport.sniff_hosts")
    def test_sniff_on_fail_failing_does_not_prevent_retires(
        self, sniff_hosts: Any
    ) -> None:
        sniff_hosts.side_effect = [TransportError("sniff failed")]
        t: Any = Transport(
            [
                {"exception": ConnectionError(None, "abandon ship", Exception())},
                {"data": CLUSTER_NODES},
            ],
            connection_class=DummyConnection,
            sniff_on_connection_fail=True,
            max_retries=3,
            randomize_hosts=False,
        )

        conn_err, conn_data = t.connection_pool.connections
        response = t.perform_request("GET", "/")
        self.assertEqual(json.loads(CLUSTER_NODES), response)
        self.assertEqual(1, sniff_hosts.call_count)
        self.assertEqual(1, len(conn_err.calls))
        self.assertEqual(1, len(conn_data.calls))

    def test_sniff_after_n_seconds(self) -> None:
        t: Any = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniffer_timeout=5,
        )

        for _ in range(4):
            t.perform_request("GET", "/")
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertIsInstance(t.get_connection(), DummyConnection)
        t.last_sniff = time.time() - 5.1

        t.perform_request("GET", "/")
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)
        self.assertTrue(time.time() - 1 < t.last_sniff < time.time() + 0.01)

    def test_sniff_7x_publish_host(self) -> None:
        # Test the response shaped when a 7.x node has publish_host set
        # and the returend data is shaped in the fqdn/ip:port format.
        t: Any = Transport(
            [{"data": CLUSTER_NODES_7X_PUBLISH_HOST}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        t.sniff_hosts()
        # Ensure we parsed out the fqdn and port from the fqdn/ip:port string.
        self.assertEqual(
            t.connection_pool.connection_opts[0][1],
            {"host": "somehost.tld", "port": 123},
        )
