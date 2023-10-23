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


import json
import re
import sys
import uuid
import warnings

import pytest
from mock import Mock, patch
from requests.auth import AuthBase

from opensearchpy.compat import reraise_exceptions
from opensearchpy.connection import Connection, RequestsHttpConnection
from opensearchpy.exceptions import (
    ConflictError,
    NotFoundError,
    RequestError,
    TransportError,
)

from ..test_cases import TestCase

if sys.version_info > (3, 0):
    from test_opensearchpy.TestHttpServer import TestHTTPServer


class TestRequestsHttpConnection(TestCase):
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

    def mock_session(self):
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token
        del dummy_session.get_frozen_credentials

        return dummy_session

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="RequestsAWSV4SignerAuth requires python3.6+"
    )
    def test_aws_signer_as_http_auth(self):
        region = "us-west-2"

        import requests

        from opensearchpy.helpers.signer import RequestsAWSV4SignerAuth

        auth = RequestsAWSV4SignerAuth(self.mock_session(), region)
        con = RequestsHttpConnection(http_auth=auth)
        prepared_request = requests.Request("GET", "http://localhost").prepare()
        auth(prepared_request)
        self.assertEqual(auth, con.session.auth)
        self.assertIn("Authorization", prepared_request.headers)
        self.assertIn("X-Amz-Date", prepared_request.headers)
        self.assertIn("X-Amz-Security-Token", prepared_request.headers)
        self.assertIn("X-Amz-Content-SHA256", prepared_request.headers)

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="RequestsAWSV4SignerAuth requires python3.6+"
    )
    def test_aws_signer_when_service_is_specified(self):
        region = "us-west-1"
        service = "aoss"

        import requests

        from opensearchpy.helpers.signer import RequestsAWSV4SignerAuth

        auth = RequestsAWSV4SignerAuth(self.mock_session(), region, service)
        con = RequestsHttpConnection(http_auth=auth)
        prepared_request = requests.Request("GET", "http://localhost").prepare()
        auth(prepared_request)
        self.assertEqual(auth, con.session.auth)
        self.assertIn("Authorization", prepared_request.headers)
        self.assertIn("X-Amz-Date", prepared_request.headers)
        self.assertIn("X-Amz-Security-Token", prepared_request.headers)

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="RequestsAWSV4SignerAuth requires python3.6+"
    )
    @patch("opensearchpy.helpers.signer.AWSV4Signer.sign")
    def test_aws_signer_signs_with_query_string(self, mock_sign):
        region = "us-west-1"
        service = "aoss"

        import requests

        from opensearchpy.helpers.signer import RequestsAWSV4SignerAuth

        auth = RequestsAWSV4SignerAuth(self.mock_session(), region, service)
        prepared_request = requests.Request(
            "GET", "http://localhost", params={"key1": "value1", "key2": "value2"}
        ).prepare()
        auth(prepared_request)
        self.assertEqual(mock_sign.call_count, 1)
        self.assertEqual(
            mock_sign.call_args[0],
            ("GET", "http://localhost/?key1=value1&key2=value2", None),
        )


@pytest.mark.skipif(
    sys.version_info < (3, 0),
    reason="http_server is only available from python 3.x",
)
class TestRequestsConnectionRedirect:
    @classmethod
    def setup_class(cls):
        # Start servers
        cls.server1 = TestHTTPServer(port=8080)
        cls.server1.start()
        cls.server2 = TestHTTPServer(port=8090)
        cls.server2.start()

    @classmethod
    def teardown_class(cls):
        # Stop servers
        cls.server2.stop()
        cls.server1.stop()

    # allow_redirects = False
    def test_redirect_failure_when_allow_redirect_false(self):
        conn = RequestsHttpConnection("localhost", port=8080, use_ssl=False, timeout=60)
        with pytest.raises(TransportError) as e:
            conn.perform_request("GET", "/redirect", allow_redirects=False)
        assert e.value.status_code == 302

    # allow_redirects = True (Default)
    def test_redirect_success_when_allow_redirect_true(self):
        conn = RequestsHttpConnection("localhost", port=8080, use_ssl=False, timeout=60)
        user_agent = conn._get_default_user_agent()
        status, headers, data = conn.perform_request("GET", "/redirect")
        assert status == 200
        data = json.loads(data)
        assert data["headers"] == {
            "Host": "localhost:8090",
            "Accept-Encoding": "identity",
            "User-Agent": user_agent,
        }


class TestSignerWithFrozenCredentials(TestRequestsHttpConnection):
    def mock_session(self):
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token
        dummy_session.get_frozen_credentials = Mock(return_value=dummy_session)

        return dummy_session

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="RequestsAWSV4SignerAuth requires python3.6+"
    )
    def test_requests_http_connection_aws_signer_frozen_credentials_as_http_auth(self):
        region = "us-west-2"

        import requests

        from opensearchpy.helpers.signer import RequestsAWSV4SignerAuth

        mock_session = self.mock_session()

        auth = RequestsAWSV4SignerAuth(mock_session, region)
        con = RequestsHttpConnection(http_auth=auth)
        prepared_request = requests.Request("GET", "http://localhost").prepare()
        auth(prepared_request)
        self.assertEqual(auth, con.session.auth)
        self.assertIn("Authorization", prepared_request.headers)
        self.assertIn("X-Amz-Date", prepared_request.headers)
        self.assertIn("X-Amz-Security-Token", prepared_request.headers)
        self.assertIn("X-Amz-Content-SHA256", prepared_request.headers)
        mock_session.get_frozen_credentials.assert_called_once()
