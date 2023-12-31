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


import ssl
import uuid
import warnings
from gzip import GzipFile
from io import BytesIO
from platform import python_version
from typing import Any

import pytest
import urllib3
from mock import MagicMock, Mock, patch
from urllib3._collections import HTTPHeaderDict

from opensearchpy import __versionstr__
from opensearchpy.connection import Connection, Urllib3HttpConnection
from opensearchpy.exceptions import NotFoundError

from ..test_cases import SkipTest, TestCase


class TestUrllib3HttpConnection(TestCase):
    def _get_mock_connection(
        self,
        connection_params: Any = {},
        response_body: bytes = b"{}",
        response_code: int = 200,
    ) -> Any:
        con = Urllib3HttpConnection(**connection_params)

        def _dummy_urlopen(*args: Any, **kwargs: Any) -> Any:
            dummy_response = Mock()
            dummy_response.headers = HTTPHeaderDict({})
            dummy_response.status = response_code
            dummy_response.data = response_body
            _dummy_urlopen.call_args = (args, kwargs)  # type: ignore
            return dummy_response

        con.pool.urlopen = _dummy_urlopen
        return con

    def test_ssl_context(self) -> None:
        # pylint: disable=missing-function-docstring
        try:
            context = ssl.create_default_context()
        except AttributeError:
            # if create_default_context raises an AttributeError Exception
            # it means SSLContext is not available for that version of python
            # and we should skip this test.
            raise SkipTest(
                "Test test_ssl_context is skipped cause SSLContext is not available for this version of python"
            )

        con = Urllib3HttpConnection(use_ssl=True, ssl_context=context)
        self.assertEqual(len(con.pool.conn_kw.keys()), 1)
        self.assertIsInstance(con.pool.conn_kw["ssl_context"], ssl.SSLContext)
        self.assertTrue(con.use_ssl)

    def test_opaque_id(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Urllib3HttpConnection(opaque_id="app-1")
        self.assertEqual(con.headers["x-opaque-id"], "app-1")

    def test_no_http_compression(self) -> None:
        # pylint: disable=missing-function-docstring
        con = self._get_mock_connection()
        self.assertFalse(con.http_compress)
        self.assertNotIn("accept-encoding", con.headers)

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertFalse(req_body)
        self.assertNotIn("accept-encoding", kwargs["headers"])
        self.assertNotIn("content-encoding", kwargs["headers"])

    def test_http_compression(self) -> None:
        # pylint: disable=missing-function-docstring
        con = self._get_mock_connection({"http_compress": True})
        self.assertTrue(con.http_compress)
        self.assertEqual(con.headers["accept-encoding"], "gzip,deflate")

        # 'content-encoding' shouldn't be set at a connection level.
        # Should be applied only if the request is sent with a body.
        self.assertNotIn("content-encoding", con.headers)

        con.perform_request("GET", "/", body=b"{}")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        buf = GzipFile(fileobj=BytesIO(req_body), mode="rb")

        self.assertEqual(buf.read(), b"{}")
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertEqual(kwargs["headers"]["content-encoding"], "gzip")

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertFalse(req_body)
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertNotIn("content-encoding", kwargs["headers"])

    def test_default_user_agent(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Urllib3HttpConnection()
        self.assertEqual(
            con._get_default_user_agent(),
            "opensearch-py/%s (Python %s)" % (__versionstr__, python_version()),
        )

    def test_timeout_set(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Urllib3HttpConnection(timeout=42)
        self.assertEqual(42, con.timeout)

    def test_keep_alive_is_on_by_default(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Urllib3HttpConnection()
        self.assertEqual(
            {
                "connection": "keep-alive",
                "content-type": "application/json",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth(self) -> None:
        # pylint: disable=missing-function-docstring
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

    def test_http_auth_tuple(self) -> None:
        # pylint: disable=missing-function-docstring
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

    def test_http_auth_list(self) -> None:
        # pylint: disable=missing-function-docstring
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

    @patch(
        "urllib3.HTTPConnectionPool.urlopen",
        return_value=Mock(status=200, headers=HTTPHeaderDict({}), data=b"{}"),
    )
    def test_aws_signer_as_http_auth_adds_headers(self, mock_open: Any) -> None:
        # pylint: disable=missing-function-docstring
        from opensearchpy.helpers.signer import Urllib3AWSV4SignerAuth

        auth = Urllib3AWSV4SignerAuth(self.mock_session(), "us-west-2")
        self.assertEqual(auth.service, "es")
        con = Urllib3HttpConnection(http_auth=auth, headers={"x": "y"})
        con.perform_request("GET", "/")
        self.assertEqual(mock_open.call_count, 1)
        headers = mock_open.call_args[1]["headers"]
        self.assertEqual(headers["x"], "y")
        self.assertTrue(
            headers["Authorization"].startswith("AWS4-HMAC-SHA256 Credential=")
        )
        self.assertIn("X-Amz-Date", headers)
        self.assertIn("X-Amz-Security-Token", headers)
        self.assertIn("X-Amz-Content-SHA256", headers)

    def test_aws_signer_as_http_auth(self) -> None:
        # pylint: disable=missing-function-docstring
        region = "us-west-2"

        from opensearchpy.helpers.signer import Urllib3AWSV4SignerAuth

        auth = Urllib3AWSV4SignerAuth(self.mock_session(), region)
        headers = auth("GET", "http://localhost", None)
        self.assertIn("Authorization", headers)
        self.assertIn("X-Amz-Date", headers)
        self.assertIn("X-Amz-Security-Token", headers)
        self.assertIn("X-Amz-Content-SHA256", headers)

    def test_aws_signer_when_region_is_null(self) -> None:
        # pylint: disable=missing-function-docstring
        session = self.mock_session()

        from opensearchpy.helpers.signer import Urllib3AWSV4SignerAuth

        with pytest.raises(ValueError) as e:
            Urllib3AWSV4SignerAuth(session, None)
        self.assertEqual(str(e.value), "Region cannot be empty")

        with pytest.raises(ValueError) as e:
            Urllib3AWSV4SignerAuth(session, "")
        self.assertEqual(str(e.value), "Region cannot be empty")

    def test_aws_signer_when_credentials_is_null(self) -> None:
        # pylint: disable=missing-function-docstring
        region = "us-west-1"

        from opensearchpy.helpers.signer import Urllib3AWSV4SignerAuth

        with pytest.raises(ValueError) as e:
            Urllib3AWSV4SignerAuth(None, region)
        self.assertEqual(str(e.value), "Credentials cannot be empty")

        with pytest.raises(ValueError) as e:
            Urllib3AWSV4SignerAuth("", region)
        self.assertEqual(str(e.value), "Credentials cannot be empty")

    def test_aws_signer_when_service_is_specified(self) -> None:
        # pylint: disable=missing-function-docstring
        region = "us-west-1"
        service = "aoss"

        from opensearchpy.helpers.signer import Urllib3AWSV4SignerAuth

        auth = Urllib3AWSV4SignerAuth(self.mock_session(), region, service)
        self.assertEqual(auth.service, service)
        headers = auth("GET", "http://localhost", None)
        self.assertIn("Authorization", headers)
        self.assertIn("X-Amz-Date", headers)
        self.assertIn("X-Amz-Security-Token", headers)

    def mock_session(self) -> Any:
        # pylint: disable=missing-function-docstring
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token
        del dummy_session.get_frozen_credentials

        return dummy_session

    def test_uses_https_if_verify_certs_is_off(self) -> None:
        # pylint: disable=missing-function-docstring
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(use_ssl=True, verify_certs=False)
            self.assertEqual(1, len(w))
            self.assertEqual(
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure.",
                str(w[0].message),
            )

        self.assertIsInstance(con.pool, urllib3.HTTPSConnectionPool)

    def test_nowarn_when_uses_https_if_verify_certs_is_off(self) -> None:
        # pylint: disable=missing-function-docstring
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            self.assertEqual(0, len(w))

        self.assertIsInstance(con.pool, urllib3.HTTPSConnectionPool)

    def test_doesnt_use_https_if_not_specified(self) -> None:
        # pylint: disable=missing-function-docstring
        con = Urllib3HttpConnection()
        self.assertIsInstance(con.pool, urllib3.HTTPConnectionPool)

    def test_no_warning_when_using_ssl_context(self) -> None:
        # pylint: disable=missing-function-docstring
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            Urllib3HttpConnection(ssl_context=ctx)
            self.assertEqual(0, len(w))

    def test_warns_if_using_non_default_ssl_kwargs_with_ssl_context(self) -> None:
        # pylint: disable=missing-function-docstring
        kwargs: Any
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

    def test_uses_given_ca_certs(self) -> None:
        # pylint: disable=missing-function-docstring
        path = "/path/to/my/ca_certs.pem"
        c = Urllib3HttpConnection(use_ssl=True, ca_certs=path)
        self.assertEqual(path, c.pool.ca_certs)

    def test_uses_default_ca_certs(self) -> None:
        # pylint: disable=missing-function-docstring
        c = Urllib3HttpConnection(use_ssl=True)
        self.assertEqual(Connection.default_ca_certs(), c.pool.ca_certs)

    def test_uses_no_ca_certs(self) -> None:
        # pylint: disable=missing-function-docstring
        c = Urllib3HttpConnection(use_ssl=True, verify_certs=False)
        self.assertIsNone(c.pool.ca_certs)

    @patch("opensearchpy.connection.base.logger")
    def test_uncompressed_body_logged(self, logger: Any) -> None:
        # pylint: disable=missing-function-docstring
        con = self._get_mock_connection(connection_params={"http_compress": True})
        con.perform_request("GET", "/", body=b'{"example": "body"}')

        self.assertEqual(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list

        self.assertEqual('> {"example": "body"}', req[0][0] % req[0][1:])
        self.assertEqual("< {}", resp[0][0] % resp[0][1:])

    @patch("opensearchpy.connection.base.logger", return_value=MagicMock())
    def test_body_not_logged(self, logger: Any) -> None:
        # pylint: disable=missing-function-docstring
        logger.isEnabledFor.return_value = False

        con = self._get_mock_connection()
        con.perform_request("GET", "/", body=b'{"example": "body"}')

        self.assertEqual(logger.isEnabledFor.call_count, 1)
        self.assertEqual(logger.debug.call_count, 0)

    @patch("opensearchpy.connection.base.logger")
    def test_failure_body_logged(self, logger: Any) -> None:
        # pylint: disable=missing-function-docstring
        con = self._get_mock_connection(response_code=404)
        with pytest.raises(NotFoundError) as e:
            con.perform_request("GET", "/invalid", body=b'{"example": "body"}')
        self.assertEqual(str(e.value), "NotFoundError(404, '{}')")

        self.assertEqual(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list

        self.assertEqual('> {"example": "body"}', req[0][0] % req[0][1:])
        self.assertEqual("< {}", resp[0][0] % resp[0][1:])

    @patch("opensearchpy.connection.base.logger", return_value=MagicMock())
    def test_failure_body_not_logged(self, logger: Any) -> None:
        # pylint: disable=missing-function-docstring
        logger.isEnabledFor.return_value = False

        con = self._get_mock_connection(response_code=404)
        with pytest.raises(NotFoundError) as e:
            con.perform_request("GET", "/invalid")
        self.assertEqual(str(e.value), "NotFoundError(404, '{}')")

        self.assertEqual(logger.isEnabledFor.call_count, 1)
        self.assertEqual(logger.debug.call_count, 0)

    def test_surrogatepass_into_bytes(self) -> None:
        # pylint: disable=missing-function-docstring
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = self._get_mock_connection(response_body=buf)
        status, headers, data = con.perform_request("GET", "/")
        self.assertEqual(u"你好\uda6a", data)  # fmt: skip

    def test_recursion_error_reraised(self) -> None:
        # pylint: disable=missing-function-docstring
        conn = Urllib3HttpConnection()

        def urlopen_raise(*_: Any, **__: Any) -> Any:
            raise RecursionError("Wasn't modified!")

        conn.pool.urlopen = urlopen_raise

        with pytest.raises(RecursionError) as e:
            conn.perform_request("GET", "/")
        self.assertEqual(str(e.value), "Wasn't modified!")


class TestSignerWithFrozenCredentials(TestUrllib3HttpConnection):
    def mock_session(self) -> Any:
        # pylint: disable=missing-function-docstring
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token
        dummy_session.get_frozen_credentials = Mock(return_value=dummy_session)

        return dummy_session

    def test_urllib3_http_connection_aws_signer_frozen_credentials_as_http_auth(
        self,
    ) -> None:
        # pylint: disable=missing-function-docstring
        region = "us-west-2"

        from opensearchpy.helpers.signer import Urllib3AWSV4SignerAuth

        mock_session = self.mock_session()

        auth = Urllib3AWSV4SignerAuth(mock_session, region)
        headers = auth("GET", "http://localhost", None)
        self.assertIn("Authorization", headers)
        self.assertIn("X-Amz-Date", headers)
        self.assertIn("X-Amz-Security-Token", headers)
        self.assertIn("X-Amz-Content-SHA256", headers)
        mock_session.get_frozen_credentials.assert_called_once()
