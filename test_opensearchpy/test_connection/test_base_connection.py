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


import os
import sys
import warnings

from opensearchpy.connection import Connection

from ..test_cases import TestCase

try:
    from pytest import MonkeyPatch
except ImportError:  # Old version of pytest for 2.7 and 3.5
    from _pytest.monkeypatch import MonkeyPatch

from pytest import raises

from opensearchpy import OpenSearch, serializer
from opensearchpy.connection import connections


class TestBaseConnection(TestCase):
    def test_empty_warnings(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Connection()
        with warnings.catch_warnings(record=True) as w:
            con._raise_warnings(())
            con._raise_warnings([])

        self.assertEqual(w, [])

    def test_raises_warnings(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Connection()

        with warnings.catch_warnings(record=True) as warn:
            con._raise_warnings(['299 OpenSearch-7.6.1-aa751 "this is deprecated"'])

        self.assertEqual([str(w.message) for w in warn], ["this is deprecated"])

        with warnings.catch_warnings(record=True) as warn:
            con._raise_warnings(
                [
                    '299 OpenSearch-7.6.1-aa751 "this is also deprecated"',
                    '299 OpenSearch-7.6.1-aa751 "this is also deprecated"',
                    '299 OpenSearch-7.6.1-aa751 "guess what? deprecated"',
                ]
            )

        self.assertEqual(
            [str(w.message) for w in warn],
            ["this is also deprecated", "guess what? deprecated"],
        )

    def test_raises_warnings_when_folded(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Connection()
        with warnings.catch_warnings(record=True) as warn:
            con._raise_warnings(
                [
                    '299 OpenSearch-7.6.1-aa751 "warning",'
                    '299 OpenSearch-7.6.1-aa751 "folded"',
                ]
            )

        self.assertEqual([str(w.message) for w in warn], ["warning", "folded"])

    def test_ipv6_host_and_port(self) -> None:
        # pylint: disable=missing-function-docstring
        for kwargs, expected_host in [
            ({"host": "::1"}, "http://[::1]:9200"),
            ({"host": "::1", "port": 443}, "http://[::1]:443"),
            ({"host": "::1", "use_ssl": True}, "https://[::1]:9200"),
            ({"host": "127.0.0.1", "port": 1234}, "http://127.0.0.1:1234"),
            ({"host": "localhost", "use_ssl": True}, "https://localhost:9200"),
        ]:
            conn = Connection(**kwargs)  # type: ignore
            assert conn.host == expected_host

    def test_compatibility_accept_header(self) -> None:
        # pylint: disable=missing-function-docstring
        try:
            conn = Connection()
            assert "accept" not in conn.headers

            os.environ["ELASTIC_CLIENT_APIVERSIONING"] = "0"

            conn = Connection()
            assert "accept" not in conn.headers

            os.environ["ELASTIC_CLIENT_APIVERSIONING"] = "1"

            conn = Connection()
            assert (
                conn.headers["accept"]
                == "application/vnd.elasticsearch+json;compatible-with=7"
            )
        finally:
            os.environ.pop("ELASTIC_CLIENT_APIVERSIONING")

    def test_ca_certs_ssl_cert_file(self) -> None:
        # pylint: disable=missing-function-docstring
        cert = "/path/to/clientcert.pem"
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setenv("SSL_CERT_FILE", cert)
            assert Connection.default_ca_certs() == cert

    def test_ca_certs_ssl_cert_dir(self) -> None:
        # pylint: disable=missing-function-docstring
        cert = "/path/to/clientcert/dir"
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setenv("SSL_CERT_DIR", cert)
            assert Connection.default_ca_certs() == cert

    def test_ca_certs_certifi(self) -> None:
        # pylint: disable=missing-function-docstring
        import certifi

        assert Connection.default_ca_certs() == certifi.where()

    def test_no_ca_certs(self) -> None:
        # pylint: disable=missing-function-docstring
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setitem(sys.modules, "certifi", None)
            assert Connection.default_ca_certs() is None

    def test_default_connection_is_returned_by_default(self) -> None:
        # pylint: disable=missing-function-docstring
        c = connections.Connections()

        con, con2 = object(), object()
        c.add_connection("default", con)

        c.add_connection("not-default", con2)

        assert c.get_connection() is con

    def test_get_connection_created_connection_if_needed(self) -> None:
        # pylint: disable=missing-function-docstring
        c = connections.Connections()
        c.configure(
            default={"hosts": ["opensearch.com"]}, local={"hosts": ["localhost"]}
        )

        default = c.get_connection()
        local = c.get_connection("local")

        assert isinstance(default, OpenSearch)
        assert isinstance(local, OpenSearch)

        assert [{"host": "opensearch.com"}] == default.transport.hosts
        assert [{"host": "localhost"}] == local.transport.hosts

    def test_configure_preserves_unchanged_connections(self) -> None:
        # pylint: disable=missing-function-docstring
        c = connections.Connections()

        c.configure(
            default={"hosts": ["opensearch.com"]}, local={"hosts": ["localhost"]}
        )
        default = c.get_connection()
        local = c.get_connection("local")

        c.configure(
            default={"hosts": ["not-opensearch.com"]}, local={"hosts": ["localhost"]}
        )
        new_default = c.get_connection()
        new_local = c.get_connection("local")

        assert new_local is local
        assert new_default is not default

    def test_remove_connection_removes_both_conn_and_conf(self) -> None:
        # pylint: disable=missing-function-docstring
        c = connections.Connections()

        c.configure(
            default={"hosts": ["opensearch.com"]}, local={"hosts": ["localhost"]}
        )
        c.add_connection("local2", object())

        c.remove_connection("default")
        c.get_connection("local2")
        c.remove_connection("local2")

        with raises(Exception):
            c.get_connection("local2")
            c.get_connection("default")

    def test_create_connection_constructs_client(self) -> None:
        # pylint: disable=missing-function-docstring
        c = connections.Connections()
        c.create_connection("testing", hosts=["opensearch.com"])

        con = c.get_connection("testing")
        assert [{"host": "opensearch.com"}] == con.transport.hosts

    def test_create_connection_adds_our_serializer(self) -> None:
        # pylint: disable=missing-function-docstring
        c = connections.Connections()
        c.create_connection("testing", hosts=["opensearch.com"])

        assert c.get_connection("testing").transport.serializer is serializer.serializer
