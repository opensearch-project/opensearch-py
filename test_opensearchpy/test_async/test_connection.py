# -*- coding: utf-8 -*-
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


import gzip
import io
import json
import ssl
import warnings
from platform import python_version

import aiohttp
import pytest
from mock import patch
from multidict import CIMultiDict
from pytest import raises

from opensearchpy import AIOHttpConnection, AsyncOpenSearch, __versionstr__, serializer
from opensearchpy.compat import reraise_exceptions
from opensearchpy.connection import Connection, async_connections
from opensearchpy.exceptions import ConnectionError, TransportError
from test_opensearchpy.TestHttpServer import TestHTTPServer

pytestmark = pytest.mark.asyncio


class TestAIOHttpConnection:
    async def _get_mock_connection(
        self,
        connection_params={},
        response_code=200,
        response_body=b"{}",
        response_headers={},
    ):
        con = AIOHttpConnection(**connection_params)
        await con._create_aiohttp_session()

        def _dummy_request(*args, **kwargs):
            class DummyResponse:
                async def __aenter__(self, *_, **__):
                    return self

                async def __aexit__(self, *_, **__):
                    pass

                async def text(self):
                    return response_body.decode("utf-8", "surrogatepass")

            dummy_response = DummyResponse()
            dummy_response.headers = CIMultiDict(**response_headers)
            dummy_response.status = response_code
            _dummy_request.call_args = (args, kwargs)
            return dummy_response

        con.session.request = _dummy_request
        return con

    async def test_ssl_context(self):
        try:
            context = ssl.create_default_context()
        except AttributeError:
            # if create_default_context raises an AttributeError Exception
            # it means SSLContext is not available for that version of python
            # and we should skip this test.
            pytest.skip(
                "Test test_ssl_context is skipped cause SSLContext is not available for this version of Python"
            )

        con = AIOHttpConnection(use_ssl=True, ssl_context=context)
        await con._create_aiohttp_session()
        assert con.use_ssl
        assert con.session.connector._ssl == context

    async def test_opaque_id(self):
        con = AIOHttpConnection(opaque_id="app-1")
        assert con.headers["x-opaque-id"] == "app-1"

    async def test_no_http_compression(self):
        con = await self._get_mock_connection()
        assert not con.http_compress
        assert "accept-encoding" not in con.headers

        await con.perform_request("GET", "/")

        _, kwargs = con.session.request.call_args

        assert not kwargs["data"]
        assert "accept-encoding" not in kwargs["headers"]
        assert "content-encoding" not in kwargs["headers"]

    async def test_http_compression(self):
        con = await self._get_mock_connection({"http_compress": True})
        assert con.http_compress
        assert con.headers["accept-encoding"] == "gzip,deflate"

        # 'content-encoding' shouldn't be set at a connection level.
        # Should be applied only if the request is sent with a body.
        assert "content-encoding" not in con.headers

        await con.perform_request("GET", "/", body=b"{}")

        _, kwargs = con.session.request.call_args

        buf = gzip.GzipFile(fileobj=io.BytesIO(kwargs["data"]), mode="rb")
        assert buf.read() == b"{}"
        assert kwargs["headers"]["accept-encoding"] == "gzip,deflate"
        assert kwargs["headers"]["content-encoding"] == "gzip"

        await con.perform_request("GET", "/")

        _, kwargs = con.session.request.call_args

        assert not kwargs["data"]
        assert kwargs["headers"]["accept-encoding"] == "gzip,deflate"
        assert "content-encoding" not in kwargs["headers"]

    async def test_url_prefix(self):
        con = await self._get_mock_connection(
            connection_params={"url_prefix": "/_search/"}
        )
        assert con.url_prefix == "/_search"

        await con.perform_request("GET", "/")

        # Need to convert the yarl URL to a string to compare.
        method, yarl_url = con.session.request.call_args[0]
        assert method == "GET" and str(yarl_url) == "http://localhost:9200/_search/"

    async def test_default_user_agent(self):
        con = AIOHttpConnection()
        assert con._get_default_user_agent() == "opensearch-py/%s (Python %s)" % (
            __versionstr__,
            python_version(),
        )

    async def test_timeout_set(self):
        con = AIOHttpConnection(timeout=42)
        assert 42 == con.timeout

    async def test_keep_alive_is_on_by_default(self):
        con = AIOHttpConnection()
        assert {
            "connection": "keep-alive",
            "content-type": "application/json",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    async def test_http_auth(self):
        con = AIOHttpConnection(http_auth="username:secret")
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "connection": "keep-alive",
            "content-type": "application/json",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    async def test_http_auth_tuple(self):
        con = AIOHttpConnection(http_auth=("username", "secret"))
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "content-type": "application/json",
            "connection": "keep-alive",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    async def test_http_auth_list(self):
        con = AIOHttpConnection(http_auth=["username", "secret"])
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "content-type": "application/json",
            "connection": "keep-alive",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    async def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = AIOHttpConnection(use_ssl=True, verify_certs=False)
            assert 1 == len(w)
            assert (
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure."
                == str(w[0].message)
            )

        assert con.use_ssl
        assert con.scheme == "https"
        assert con.host == "https://localhost:9200"

    async def test_nowarn_when_test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = AIOHttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            await con._create_aiohttp_session()
            assert w == []

        assert isinstance(con.session, aiohttp.ClientSession)

    async def test_doesnt_use_https_if_not_specified(self):
        con = AIOHttpConnection()
        assert not con.use_ssl

    async def test_no_warning_when_using_ssl_context(self):
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            AIOHttpConnection(ssl_context=ctx)
            assert w == [], str([x.message for x in w])

    async def test_warns_if_using_non_default_ssl_kwargs_with_ssl_context(self):
        for kwargs in (
            {"ssl_show_warn": False},
            {"ssl_show_warn": True},
            {"verify_certs": True},
            {"verify_certs": False},
            {"ca_certs": "/path/to/certs"},
            {"ssl_show_warn": True, "ca_certs": "/path/to/certs"},
        ):
            kwargs["ssl_context"] = ssl.create_default_context()

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                AIOHttpConnection(**kwargs)

                assert 1 == len(w)
                assert (
                    "When using `ssl_context`, all other SSL related kwargs are ignored"
                    == str(w[0].message)
                )

    @patch("ssl.SSLContext.load_verify_locations")
    async def test_uses_given_ca_certs(self, load_verify_locations, tmp_path):
        path = tmp_path / "ca_certs.pem"
        path.touch()
        AIOHttpConnection(use_ssl=True, ca_certs=str(path))
        load_verify_locations.assert_called_once_with(cafile=str(path))

    @patch("ssl.SSLContext.load_verify_locations")
    async def test_uses_default_ca_certs(self, load_verify_locations):
        AIOHttpConnection(use_ssl=True)
        load_verify_locations.assert_called_once_with(
            cafile=Connection.default_ca_certs()
        )

    @patch("ssl.SSLContext.load_verify_locations")
    async def test_uses_no_ca_certs(self, load_verify_locations):
        AIOHttpConnection(use_ssl=True, verify_certs=False)
        load_verify_locations.assert_not_called()

    async def test_trust_env(self):
        con = AIOHttpConnection(trust_env=True)
        await con._create_aiohttp_session()

        assert con._trust_env is True
        assert con.session.trust_env is True

    async def test_trust_env_default_value_is_false(self):
        con = AIOHttpConnection()
        await con._create_aiohttp_session()

        assert con._trust_env is False
        assert con.session.trust_env is False

    @patch("opensearchpy.connection.base.logger")
    async def test_uncompressed_body_logged(self, logger):
        con = await self._get_mock_connection(connection_params={"http_compress": True})
        await con.perform_request("GET", "/", body=b'{"example": "body"}')

        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list

        assert '> {"example": "body"}' == req[0][0] % req[0][1:]
        assert "< {}" == resp[0][0] % resp[0][1:]

    async def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = await self._get_mock_connection(response_body=buf)
        status, headers, data = await con.perform_request("GET", "/")
        assert u"你好\uda6a" == data  # fmt: skip

    @pytest.mark.parametrize("exception_cls", reraise_exceptions)
    async def test_recursion_error_reraised(self, exception_cls):
        conn = AIOHttpConnection()

        def request_raise(*_, **__):
            raise exception_cls("Wasn't modified!")

        await conn._create_aiohttp_session()
        conn.session.request = request_raise

        with pytest.raises(exception_cls) as e:
            await conn.perform_request("GET", "/")
        assert str(e.value) == "Wasn't modified!"

    async def test_json_errors_are_parsed(self):
        con = await self._get_mock_connection(
            response_code=400,
            response_body=b'{"error": {"type": "snapshot_in_progress_exception"}}',
            response_headers={"Content-Type": "application/json;"},
        )
        try:
            with pytest.raises(TransportError) as e:
                await con.perform_request("POST", "/", body=b'{"some": "json"')

            assert e.value.error == "snapshot_in_progress_exception"
        finally:
            await con.close()


class TestConnectionHttpServer:
    """Tests the HTTP connection implementations against a live server E2E"""

    @classmethod
    def setup_class(cls):
        # Start server
        cls.server = TestHTTPServer(port=8081)
        cls.server.start()

    @classmethod
    def teardown_class(cls):
        # Stop server
        cls.server.stop()

    async def httpserver(self, conn, **kwargs):
        status, headers, data = await conn.perform_request("GET", "/", **kwargs)
        data = json.loads(data)
        return (status, data)

    async def test_aiohttp_connection(self):
        # Defaults
        conn = AIOHttpConnection("localhost", port=8081, use_ssl=False)
        user_agent = conn._get_default_user_agent()
        status, data = await self.httpserver(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Content-Type": "application/json",
            "Host": "localhost:8081",
            "User-Agent": user_agent,
        }

        # http_compress=False
        conn = AIOHttpConnection(
            "localhost", port=8081, use_ssl=False, http_compress=False
        )
        status, data = await self.httpserver(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Content-Type": "application/json",
            "Host": "localhost:8081",
            "User-Agent": user_agent,
        }

        # http_compress=True
        conn = AIOHttpConnection(
            "localhost", port=8081, use_ssl=False, http_compress=True
        )
        status, data = await self.httpserver(conn)
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "localhost:8081",
            "User-Agent": user_agent,
        }

        # Headers
        conn = AIOHttpConnection(
            "localhost",
            port=8081,
            use_ssl=False,
            http_compress=True,
            headers={"header1": "value1"},
        )
        status, data = await self.httpserver(
            conn, headers={"header2": "value2", "header1": "override!"}
        )
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "localhost:8081",
            "Header1": "override!",
            "Header2": "value2",
            "User-Agent": user_agent,
        }

    async def test_aiohttp_connection_error(self):
        conn = AIOHttpConnection("not.a.host.name")
        with pytest.raises(ConnectionError):
            await conn.perform_request("GET", "/")


async def test_default_connection_is_returned_by_default():
    c = async_connections.AsyncConnections()

    con, con2 = object(), object()
    await c.add_connection("default", con)

    await c.add_connection("not-default", con2)

    assert await c.get_connection() is con


async def test_get_connection_created_connection_if_needed():
    c = async_connections.AsyncConnections()
    await c.configure(
        default={"hosts": ["opensearch.com"]}, local={"hosts": ["localhost"]}
    )
    default = await c.get_connection()
    local = await c.get_connection("local")
    assert isinstance(default, AsyncOpenSearch)
    assert isinstance(local, AsyncOpenSearch)
    assert [{"host": "opensearch.com"}] == default.transport.hosts
    assert [{"host": "localhost"}] == local.transport.hosts


async def test_configure_preserves_unchanged_connections():
    c = async_connections.AsyncConnections()

    await c.configure(
        default={"hosts": ["opensearch.com"]}, local={"hosts": ["localhost"]}
    )
    default = await c.get_connection()
    local = await c.get_connection("local")

    await c.configure(
        default={"hosts": ["not-opensearch.com"]}, local={"hosts": ["localhost"]}
    )
    new_default = await c.get_connection()
    new_local = await c.get_connection("local")

    assert new_local is local
    assert new_default is not default


async def test_remove_connection_removes_both_conn_and_conf():
    c = async_connections.AsyncConnections()

    await c.configure(
        default={"hosts": ["opensearch.com"]}, local={"hosts": ["localhost"]}
    )
    await c.add_connection("local2", object())

    await c.remove_connection("default")
    await c.get_connection("local2")
    await c.remove_connection("local2")

    with raises(Exception):
        await c.get_connection("local2")
        await c.get_connection("default")


async def test_create_connection_constructs_client():
    c = async_connections.AsyncConnections()
    await c.create_connection("testing", hosts=["opensearch.com"])

    con = await c.get_connection("testing")
    assert [{"host": "opensearch.com"}] == con.transport.hosts


async def test_create_connection_adds_our_serializer():
    c = async_connections.AsyncConnections()
    await c.create_connection("testing", hosts=["opensearch.com"])
    result = await c.get_connection("testing")
    assert result.transport.serializer is serializer.serializer
