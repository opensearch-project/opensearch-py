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
import os
import re
import ssl
import sys
import unittest
import uuid
import warnings
from platform import python_version

import pytest
import six
import urllib3
from mock import Mock, patch
from requests.auth import AuthBase
from urllib3._collections import HTTPHeaderDict

from opensearchpy import __versionstr__
from opensearchpy.compat import reraise_exceptions
from opensearchpy.connection import (
    Connection,
    RequestsHttpConnection,
    Urllib3HttpConnection,
)
from opensearchpy.exceptions import (
    ConflictError,
    ConnectionError,
    NotFoundError,
    RequestError,
    TransportError,
)

from .test_cases import SkipTest, TestCase

try:
    from pytest import MonkeyPatch
except ImportError:  # Old version of pytest for 2.7 and 3.5
    from _pytest.monkeypatch import MonkeyPatch


def gzip_decompress(data):
    buf = gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb")
    return buf.read()


class TestBaseConnection(TestCase):
    def test_empty_warnings(self):
        con = Connection()
        with warnings.catch_warnings(record=True) as w:
            con._raise_warnings(())
            con._raise_warnings([])

        self.assertEqual(w, [])

    def test_raises_warnings(self):
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

    def test_raises_warnings_when_folded(self):
        con = Connection()
        with warnings.catch_warnings(record=True) as warn:
            con._raise_warnings(
                [
                    '299 OpenSearch-7.6.1-aa751 "warning",'
                    '299 OpenSearch-7.6.1-aa751 "folded"',
                ]
            )

        self.assertEqual([str(w.message) for w in warn], ["warning", "folded"])

    @unittest.skipIf(six.PY2, "not compatible with python2")
    def test_raises_errors(self):
        con = Connection()
        with self.assertLogs("opensearch") as captured, self.assertRaises(
            NotFoundError
        ):
            con._raise_error(404, "Not found", "application/json")
        self.assertEqual(len(captured.output), 1)

        # NB: this should assertNoLogs() but that method is not available until python3.10
        with self.assertRaises(NotFoundError):
            con._raise_error(404, "Not found", "text/plain; charset=UTF-8")

    def test_ipv6_host_and_port(self):
        for kwargs, expected_host in [
            ({"host": "::1"}, "http://[::1]:9200"),
            ({"host": "::1", "port": 443}, "http://[::1]:443"),
            ({"host": "::1", "use_ssl": True}, "https://[::1]:9200"),
            ({"host": "127.0.0.1", "port": 1234}, "http://127.0.0.1:1234"),
            ({"host": "localhost", "use_ssl": True}, "https://localhost:9200"),
        ]:
            conn = Connection(**kwargs)
            assert conn.host == expected_host

    def test_compatibility_accept_header(self):
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

    def test_ca_certs_ssl_cert_file(self):
        cert = "/path/to/clientcert.pem"
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setenv("SSL_CERT_FILE", cert)
            assert Connection.default_ca_certs() == cert

    def test_ca_certs_ssl_cert_dir(self):
        cert = "/path/to/clientcert/dir"
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setenv("SSL_CERT_DIR", cert)
            assert Connection.default_ca_certs() == cert

    def test_ca_certs_certifi(self):
        import certifi

        assert Connection.default_ca_certs() == certifi.where()

    def test_no_ca_certs(self):
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setitem(sys.modules, "certifi", None)
            assert Connection.default_ca_certs() is None


class TestUrllib3Connection(TestCase):
    def _get_mock_connection(self, connection_params={}, response_body=b"{}"):
        con = Urllib3HttpConnection(**connection_params)

        def _dummy_urlopen(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = HTTPHeaderDict({})
            dummy_response.status = 200
            dummy_response.data = response_body
            _dummy_urlopen.call_args = (args, kwargs)
            return dummy_response

        con.pool.urlopen = _dummy_urlopen
        return con

    def test_ssl_context(self):
        try:
            context = ssl.create_default_context()
        except AttributeError:
            # if create_default_context raises an AttributeError Exception
            # it means SSLContext is not available for that version of python
            # and we should skip this test.
            raise SkipTest(
                "Test test_ssl_context is skipped cause SSLContext is not available for this version of ptyhon"
            )

        con = Urllib3HttpConnection(use_ssl=True, ssl_context=context)
        self.assertEqual(len(con.pool.conn_kw.keys()), 1)
        self.assertIsInstance(con.pool.conn_kw["ssl_context"], ssl.SSLContext)
        self.assertTrue(con.use_ssl)

    def test_opaque_id(self):
        con = Urllib3HttpConnection(opaque_id="app-1")
        self.assertEqual(con.headers["x-opaque-id"], "app-1")

    def test_no_http_compression(self):
        con = self._get_mock_connection()
        self.assertFalse(con.http_compress)
        self.assertNotIn("accept-encoding", con.headers)

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertFalse(req_body)
        self.assertNotIn("accept-encoding", kwargs["headers"])
        self.assertNotIn("content-encoding", kwargs["headers"])

    def test_http_compression(self):
        con = self._get_mock_connection({"http_compress": True})
        self.assertTrue(con.http_compress)
        self.assertEqual(con.headers["accept-encoding"], "gzip,deflate")

        # 'content-encoding' shouldn't be set at a connection level.
        # Should be applied only if the request is sent with a body.
        self.assertNotIn("content-encoding", con.headers)

        con.perform_request("GET", "/", body=b"{}")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertEqual(gzip_decompress(req_body), b"{}")
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertEqual(kwargs["headers"]["content-encoding"], "gzip")

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertFalse(req_body)
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertNotIn("content-encoding", kwargs["headers"])

    def test_default_user_agent(self):
        con = Urllib3HttpConnection()
        self.assertEqual(
            con._get_default_user_agent(),
            "opensearch-py/%s (Python %s)" % (__versionstr__, python_version()),
        )

    def test_timeout_set(self):
        con = Urllib3HttpConnection(timeout=42)
        self.assertEqual(42, con.timeout)

    def test_keep_alive_is_on_by_default(self):
        con = Urllib3HttpConnection()
        self.assertEqual(
            {
                "connection": "keep-alive",
                "content-type": "application/json",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth(self):
        con = Urllib3HttpConnection(http_auth="username:secret")
        self.assertEqual(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "connection": "keep-alive",
                "content-type": "application/json",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth_tuple(self):
        con = Urllib3HttpConnection(http_auth=("username", "secret"))
        self.assertEqual(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "content-type": "application/json",
                "connection": "keep-alive",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth_list(self):
        con = Urllib3HttpConnection(http_auth=["username", "secret"])
        self.assertEqual(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "content-type": "application/json",
                "connection": "keep-alive",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="AWSV4SignerAuth requires python3.6+"
    )
    def test_aws_signer_as_http_auth(self):
        region = "us-west-2"

        import requests

        from opensearchpy.helpers.signer import AWSV4SignerAuth

        auth = AWSV4SignerAuth(self.mock_session(), region)
        con = RequestsHttpConnection(http_auth=auth)
        prepared_request = requests.Request("GET", "http://localhost").prepare()
        auth(prepared_request)
        self.assertEqual(auth, con.session.auth)
        self.assertIn("Authorization", prepared_request.headers)
        self.assertIn("X-Amz-Date", prepared_request.headers)
        self.assertIn("X-Amz-Security-Token", prepared_request.headers)

    def test_aws_signer_when_region_is_null(self):
        session = self.mock_session()

        from opensearchpy.helpers.signer import AWSV4SignerAuth

        with pytest.raises(ValueError) as e:
            AWSV4SignerAuth(session, None)
        assert str(e.value) == "Region cannot be empty"

        with pytest.raises(ValueError) as e:
            AWSV4SignerAuth(session, "")
        assert str(e.value) == "Region cannot be empty"

    def test_aws_signer_when_credentials_is_null(self):
        region = "us-west-1"

        from opensearchpy.helpers.signer import AWSV4SignerAuth

        with pytest.raises(ValueError) as e:
            AWSV4SignerAuth(None, region)
        assert str(e.value) == "Credentials cannot be empty"

        with pytest.raises(ValueError) as e:
            AWSV4SignerAuth("", region)
        assert str(e.value) == "Credentials cannot be empty"

    def mock_session(self):
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token
        return dummy_session

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(use_ssl=True, verify_certs=False)
            self.assertEqual(1, len(w))
            self.assertEqual(
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure.",
                str(w[0].message),
            )

        self.assertIsInstance(con.pool, urllib3.HTTPSConnectionPool)

    def test_nowarn_when_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            self.assertEqual(0, len(w))

        self.assertIsInstance(con.pool, urllib3.HTTPSConnectionPool)

    def test_doesnt_use_https_if_not_specified(self):
        con = Urllib3HttpConnection()
        self.assertIsInstance(con.pool, urllib3.HTTPConnectionPool)

    def test_no_warning_when_using_ssl_context(self):
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            Urllib3HttpConnection(ssl_context=ctx)
            self.assertEqual(0, len(w))

    def test_warns_if_using_non_default_ssl_kwargs_with_ssl_context(self):
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

                Urllib3HttpConnection(**kwargs)

                self.assertEqual(1, len(w))
                self.assertEqual(
                    "When using `ssl_context`, all other SSL related kwargs are ignored",
                    str(w[0].message),
                )

    def test_uses_given_ca_certs(self):
        path = "/path/to/my/ca_certs.pem"
        c = Urllib3HttpConnection(use_ssl=True, ca_certs=path)
        self.assertEqual(path, c.pool.ca_certs)

    def test_uses_default_ca_certs(self):
        c = Urllib3HttpConnection(use_ssl=True)
        self.assertEqual(Connection.default_ca_certs(), c.pool.ca_certs)

    def test_uses_no_ca_certs(self):
        c = Urllib3HttpConnection(use_ssl=True, verify_certs=False)
        self.assertIsNone(c.pool.ca_certs)

    @patch("opensearchpy.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        con = self._get_mock_connection(connection_params={"http_compress": True})
        con.perform_request("GET", "/", body=b'{"example": "body"}')

        self.assertEqual(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list

        self.assertEqual('> {"example": "body"}', req[0][0] % req[0][1:])
        self.assertEqual("< {}", resp[0][0] % resp[0][1:])

    def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = self._get_mock_connection(response_body=buf)
        status, headers, data = con.perform_request("GET", "/")
        self.assertEqual(u"你好\uda6a", data)  # fmt: skip

    @pytest.mark.skipif(
        not reraise_exceptions, reason="RecursionError isn't defined in Python <3.5"
    )
    def test_recursion_error_reraised(self):
        conn = Urllib3HttpConnection()

        def urlopen_raise(*_, **__):
            raise RecursionError("Wasn't modified!")

        conn.pool.urlopen = urlopen_raise

        with pytest.raises(RecursionError) as e:
            conn.perform_request("GET", "/")
        assert str(e.value) == "Wasn't modified!"


class TestRequestsConnection(TestCase):
    def _get_mock_connection(
        self, connection_params={}, status_code=200, response_body=b"{}"
    ):
        con = RequestsHttpConnection(**connection_params)

        def _dummy_send(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = {}
            dummy_response.status_code = status_code
            dummy_response.content = response_body
            dummy_response.request = args[0]
            dummy_response.cookies = {}
            _dummy_send.call_args = (args, kwargs)
            return dummy_response

        con.session.send = _dummy_send
        return con

    def _get_request(self, connection, *args, **kwargs):
        if "body" in kwargs:
            kwargs["body"] = kwargs["body"].encode("utf-8")

        status, headers, data = connection.perform_request(*args, **kwargs)
        self.assertEqual(200, status)
        self.assertEqual("{}", data)

        timeout = kwargs.pop("timeout", connection.timeout)
        args, kwargs = connection.session.send.call_args
        self.assertEqual(timeout, kwargs["timeout"])
        self.assertEqual(1, len(args))
        return args[0]

    def test_custom_http_auth_is_allowed(self):
        auth = AuthBase()
        c = RequestsHttpConnection(http_auth=auth)

        self.assertEqual(auth, c.session.auth)

    def test_timeout_set(self):
        con = RequestsHttpConnection(timeout=42)
        self.assertEqual(42, con.timeout)

    def test_opaque_id(self):
        con = RequestsHttpConnection(opaque_id="app-1")
        self.assertEqual(con.headers["x-opaque-id"], "app-1")

    def test_no_http_compression(self):
        con = self._get_mock_connection()

        self.assertFalse(con.http_compress)
        self.assertNotIn("content-encoding", con.session.headers)

        con.perform_request("GET", "/")

        req = con.session.send.call_args[0][0]
        self.assertNotIn("content-encoding", req.headers)
        self.assertNotIn("accept-encoding", req.headers)

    def test_http_compression(self):
        con = self._get_mock_connection(
            {"http_compress": True},
        )

        self.assertTrue(con.http_compress)

        # 'content-encoding' shouldn't be set at a session level.
        # Should be applied only if the request is sent with a body.
        self.assertNotIn("content-encoding", con.session.headers)

        con.perform_request("GET", "/", body=b"{}")

        req = con.session.send.call_args[0][0]
        self.assertEqual(req.headers["content-encoding"], "gzip")
        self.assertEqual(req.headers["accept-encoding"], "gzip,deflate")

        con.perform_request("GET", "/")

        req = con.session.send.call_args[0][0]
        self.assertNotIn("content-encoding", req.headers)
        self.assertEqual(req.headers["accept-encoding"], "gzip,deflate")

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = self._get_mock_connection(
                {"use_ssl": True, "url_prefix": "url", "verify_certs": False}
            )
            self.assertEqual(1, len(w))
            self.assertEqual(
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure.",
                str(w[0].message),
            )

        request = self._get_request(con, "GET", "/")

        self.assertEqual("https://localhost:9200/url/", request.url)
        self.assertEqual("GET", request.method)
        self.assertEqual(None, request.body)

    def test_uses_given_ca_certs(self):
        path = "/path/to/my/ca_certs.pem"
        c = RequestsHttpConnection(ca_certs=path)
        self.assertEqual(path, c.session.verify)

    def test_uses_default_ca_certs(self):
        c = RequestsHttpConnection()
        self.assertEqual(Connection.default_ca_certs(), c.session.verify)

    def test_uses_no_ca_certs(self):
        c = RequestsHttpConnection(verify_certs=False)
        self.assertFalse(c.session.verify)

    def test_nowarn_when_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = self._get_mock_connection(
                {
                    "use_ssl": True,
                    "url_prefix": "url",
                    "verify_certs": False,
                    "ssl_show_warn": False,
                }
            )
            self.assertEqual(0, len(w))

        request = self._get_request(con, "GET", "/")

        self.assertEqual("https://localhost:9200/url/", request.url)
        self.assertEqual("GET", request.method)
        self.assertEqual(None, request.body)

    def test_merge_headers(self):
        con = self._get_mock_connection(
            connection_params={"headers": {"h1": "v1", "h2": "v2"}}
        )
        req = self._get_request(con, "GET", "/", headers={"h2": "v2p", "h3": "v3"})
        self.assertEqual(req.headers["h1"], "v1")
        self.assertEqual(req.headers["h2"], "v2p")
        self.assertEqual(req.headers["h3"], "v3")

    def test_default_headers(self):
        con = self._get_mock_connection()
        req = self._get_request(con, "GET", "/")
        self.assertEqual(req.headers["content-type"], "application/json")
        self.assertEqual(req.headers["user-agent"], con._get_default_user_agent())

    def test_custom_headers(self):
        con = self._get_mock_connection()
        req = self._get_request(
            con,
            "GET",
            "/",
            headers={
                "content-type": "application/x-ndjson",
                "user-agent": "custom-agent/1.2.3",
            },
        )
        self.assertEqual(req.headers["content-type"], "application/x-ndjson")
        self.assertEqual(req.headers["user-agent"], "custom-agent/1.2.3")

    def test_http_auth(self):
        con = RequestsHttpConnection(http_auth="username:secret")
        self.assertEqual(("username", "secret"), con.session.auth)

    def test_http_auth_tuple(self):
        con = RequestsHttpConnection(http_auth=("username", "secret"))
        self.assertEqual(("username", "secret"), con.session.auth)

    def test_http_auth_list(self):
        con = RequestsHttpConnection(http_auth=["username", "secret"])
        self.assertEqual(("username", "secret"), con.session.auth)

    def test_repr(self):
        con = self._get_mock_connection({"host": "opensearchpy.com", "port": 443})
        self.assertEqual(
            "<RequestsHttpConnection: http://opensearchpy.com:443>", repr(con)
        )

    def test_conflict_error_is_returned_on_409(self):
        con = self._get_mock_connection(status_code=409)
        self.assertRaises(ConflictError, con.perform_request, "GET", "/", {}, "")

    def test_not_found_error_is_returned_on_404(self):
        con = self._get_mock_connection(status_code=404)
        self.assertRaises(NotFoundError, con.perform_request, "GET", "/", {}, "")

    def test_request_error_is_returned_on_400(self):
        con = self._get_mock_connection(status_code=400)
        self.assertRaises(RequestError, con.perform_request, "GET", "/", {}, "")

    @patch("opensearchpy.connection.base.logger")
    def test_head_with_404_doesnt_get_logged(self, logger):
        con = self._get_mock_connection(status_code=404)
        self.assertRaises(NotFoundError, con.perform_request, "HEAD", "/", {}, "")
        self.assertEqual(0, logger.warning.call_count)

    @patch("opensearchpy.connection.base.tracer")
    @patch("opensearchpy.connection.base.logger")
    def test_failed_request_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(
            response_body=b'{"answer": 42}', status_code=500
        )
        self.assertRaises(
            TransportError,
            con.perform_request,
            "GET",
            "/",
            {"param": 42},
            "{}".encode("utf-8"),
        )

        # trace request
        self.assertEqual(1, tracer.info.call_count)
        # trace response
        self.assertEqual(1, tracer.debug.call_count)
        # log url and duration
        self.assertEqual(1, logger.warning.call_count)
        self.assertTrue(
            re.match(
                r"^GET http://localhost:9200/\?param=42 \[status:500 request:0.[0-9]{3}s\]",
                logger.warning.call_args[0][0] % logger.warning.call_args[0][1:],
            )
        )

    @patch("opensearchpy.connection.base.tracer")
    @patch("opensearchpy.connection.base.logger")
    def test_success_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(response_body=b"""{"answer": "that's it!"}""")
        status, headers, data = con.perform_request(
            "GET",
            "/",
            {"param": 42},
            """{"question": "what's that?"}""".encode("utf-8"),
        )

        # trace request
        self.assertEqual(1, tracer.info.call_count)
        self.assertEqual(
            """curl -H 'Content-Type: application/json' -XGET 'http://localhost:9200/?pretty&param=42' -d '{\n  "question": "what\\u0027s that?"\n}'""",
            tracer.info.call_args[0][0] % tracer.info.call_args[0][1:],
        )
        # trace response
        self.assertEqual(1, tracer.debug.call_count)
        self.assertTrue(
            re.match(
                r'#\[200\] \(0.[0-9]{3}s\)\n#{\n#  "answer": "that\\u0027s it!"\n#}',
                tracer.debug.call_args[0][0] % tracer.debug.call_args[0][1:],
            )
        )

        # log url and duration
        self.assertEqual(1, logger.info.call_count)
        self.assertTrue(
            re.match(
                r"GET http://localhost:9200/\?param=42 \[status:200 request:0.[0-9]{3}s\]",
                logger.info.call_args[0][0] % logger.info.call_args[0][1:],
            )
        )
        # log request body and response
        self.assertEqual(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list
        self.assertEqual('> {"question": "what\'s that?"}', req[0][0] % req[0][1:])
        self.assertEqual('< {"answer": "that\'s it!"}', resp[0][0] % resp[0][1:])

    @patch("opensearchpy.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        con = self._get_mock_connection(connection_params={"http_compress": True})
        con.perform_request("GET", "/", body=b'{"example": "body"}')

        self.assertEqual(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list
        self.assertEqual('> {"example": "body"}', req[0][0] % req[0][1:])
        self.assertEqual("< {}", resp[0][0] % resp[0][1:])

        con = self._get_mock_connection(
            connection_params={"http_compress": True},
            status_code=500,
            response_body=b'{"hello":"world"}',
        )
        with pytest.raises(TransportError):
            con.perform_request("GET", "/", body=b'{"example": "body2"}')

        self.assertEqual(4, logger.debug.call_count)
        _, _, req, resp = logger.debug.call_args_list
        self.assertEqual('> {"example": "body2"}', req[0][0] % req[0][1:])
        self.assertEqual('< {"hello":"world"}', resp[0][0] % resp[0][1:])

    def test_defaults(self):
        con = self._get_mock_connection()
        request = self._get_request(con, "GET", "/")

        self.assertEqual("http://localhost:9200/", request.url)
        self.assertEqual("GET", request.method)
        self.assertEqual(None, request.body)

    def test_params_properly_encoded(self):
        con = self._get_mock_connection()
        request = self._get_request(
            con, "GET", "/", params={"param": "value with spaces"}
        )

        self.assertEqual("http://localhost:9200/?param=value+with+spaces", request.url)
        self.assertEqual("GET", request.method)
        self.assertEqual(None, request.body)

    def test_body_attached(self):
        con = self._get_mock_connection()
        request = self._get_request(con, "GET", "/", body='{"answer": 42}')

        self.assertEqual("http://localhost:9200/", request.url)
        self.assertEqual("GET", request.method)
        self.assertEqual('{"answer": 42}'.encode("utf-8"), request.body)

    def test_http_auth_attached(self):
        con = self._get_mock_connection({"http_auth": "username:secret"})
        request = self._get_request(con, "GET", "/")

        self.assertEqual(request.headers["authorization"], "Basic dXNlcm5hbWU6c2VjcmV0")

    @patch("opensearchpy.connection.base.tracer")
    def test_url_prefix(self, tracer):
        con = self._get_mock_connection({"url_prefix": "/some-prefix/"})
        request = self._get_request(
            con, "GET", "/_search", body='{"answer": 42}', timeout=0.1
        )

        self.assertEqual("http://localhost:9200/some-prefix/_search", request.url)
        self.assertEqual("GET", request.method)
        self.assertEqual('{"answer": 42}'.encode("utf-8"), request.body)

        # trace request
        self.assertEqual(1, tracer.info.call_count)
        self.assertEqual(
            "curl -H 'Content-Type: application/json' -XGET 'http://localhost:9200/_search?pretty' -d '{\n  \"answer\": 42\n}'",
            tracer.info.call_args[0][0] % tracer.info.call_args[0][1:],
        )

    def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = self._get_mock_connection(response_body=buf)
        status, headers, data = con.perform_request("GET", "/")
        self.assertEqual(u"你好\uda6a", data)  # fmt: skip

    @pytest.mark.skipif(
        not reraise_exceptions, reason="RecursionError isn't defined in Python <3.5"
    )
    def test_recursion_error_reraised(self):
        conn = RequestsHttpConnection()

        def send_raise(*_, **__):
            raise RecursionError("Wasn't modified!")

        conn.session.send = send_raise

        with pytest.raises(RecursionError) as e:
            conn.perform_request("GET", "/")
        assert str(e.value) == "Wasn't modified!"


class TestConnectionHttpbin:
    """Tests the HTTP connection implementations against a live server E2E"""

    def httpbin_anything(self, conn, **kwargs):
        status, headers, data = conn.perform_request("GET", "/anything", **kwargs)
        data = json.loads(data)
        data["headers"].pop(
            "X-Amzn-Trace-Id", None
        )  # Remove this header as it's put there by AWS.
        return (status, data)

    def test_urllib3_connection(self):
        # Defaults
        # httpbin.org can be slow sometimes. Hence the timeout
        conn = Urllib3HttpConnection("httpbin.org", port=443, use_ssl=True, timeout=60)
        user_agent = conn._get_default_user_agent()
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=False
        conn = Urllib3HttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=False, timeout=60
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=True
        conn = Urllib3HttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=True, timeout=60
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # Headers
        conn = Urllib3HttpConnection(
            "httpbin.org",
            port=443,
            use_ssl=True,
            http_compress=True,
            headers={"header1": "value1"},
            timeout=60,
        )
        status, data = self.httpbin_anything(
            conn, headers={"header2": "value2", "header1": "override!"}
        )
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "Header1": "override!",
            "Header2": "value2",
            "User-Agent": user_agent,
        }

    def test_urllib3_connection_error(self):
        conn = Urllib3HttpConnection("not.a.host.name")
        with pytest.raises(ConnectionError):
            conn.perform_request("GET", "/")

    def test_requests_connection(self):
        # Defaults
        conn = RequestsHttpConnection("httpbin.org", port=443, use_ssl=True, timeout=60)
        user_agent = conn._get_default_user_agent()
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=False
        conn = RequestsHttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=False, timeout=60
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=True
        conn = RequestsHttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=True, timeout=60
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # Headers
        conn = RequestsHttpConnection(
            "httpbin.org",
            port=443,
            use_ssl=True,
            http_compress=True,
            headers={"header1": "value1"},
            timeout=60,
        )
        status, data = self.httpbin_anything(
            conn, headers={"header2": "value2", "header1": "override!"}
        )
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "Header1": "override!",
            "Header2": "value2",
            "User-Agent": user_agent,
        }

    def test_requests_connection_error(self):
        conn = RequestsHttpConnection("not.a.host.name")
        with pytest.raises(ConnectionError):
            conn.perform_request("GET", "/")
