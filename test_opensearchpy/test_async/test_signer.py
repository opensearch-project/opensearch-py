# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import uuid
from typing import Any, Collection, Dict, Mapping, Optional, Tuple, Union
from unittest.mock import Mock, patch

import pytest
from _pytest.mark.structures import MarkDecorator

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestAsyncSigner:
    def mock_session(self) -> Mock:
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token

        del dummy_session.get_frozen_credentials

        return dummy_session

    async def test_aws_signer_async_as_http_auth(self) -> None:
        region = "us-west-2"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        auth = AWSV4SignerAsyncAuth(self.mock_session(), region)
        headers = auth("GET", "http://localhost")
        assert "Authorization" in headers
        assert "X-Amz-Date" in headers
        assert "X-Amz-Security-Token" in headers

    async def test_aws_signer_async_when_region_is_null(self) -> None:
        session = self.mock_session()

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        with pytest.raises(ValueError) as e:
            AWSV4SignerAsyncAuth(session, None)  # type: ignore
        assert str(e.value) == "Region cannot be empty"

        with pytest.raises(ValueError) as e:
            AWSV4SignerAsyncAuth(session, "")
        assert str(e.value) == "Region cannot be empty"

    async def test_aws_signer_async_when_credentials_is_null(self) -> None:
        region = "us-west-1"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        with pytest.raises(ValueError) as e:
            AWSV4SignerAsyncAuth(None, region)
        assert str(e.value) == "Credentials cannot be empty"

    async def test_aws_signer_async_when_service_is_specified(self) -> None:
        region = "us-west-2"
        service = "aoss"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        auth = AWSV4SignerAsyncAuth(self.mock_session(), region, service)
        headers = auth("GET", "http://localhost")
        assert "Authorization" in headers
        assert "X-Amz-Date" in headers
        assert "X-Amz-Security-Token" in headers
        assert "X-Amz-Content-SHA256" in headers

    async def test_aws_signer_async_fetch_url_with_querystring(self) -> None:
        region = "us-west-2"
        service = "aoss"

        from botocore.awsrequest import AWSRequest

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        with patch(
            "botocore.awsrequest.AWSRequest", side_effect=AWSRequest
        ) as mock_aws_request:
            auth = AWSV4SignerAsyncAuth(self.mock_session(), region, service)
            auth("GET", "http://localhost/?foo=bar", headers={"host": "otherhost:443"})
            mock_aws_request.assert_called_with(
                method="GET", url="http://otherhost:443/?foo=bar", data=None
            )


class TestAsyncSignerWithFrozenCredentials(TestAsyncSigner):
    def mock_session(self, disable_get_frozen: bool = True) -> Mock:
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token
        dummy_session.get_frozen_credentials = Mock(return_value=dummy_session)

        return dummy_session

    async def test_aws_signer_async_frozen_credentials_as_http_auth(self) -> None:
        region = "us-west-2"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        mock_session = self.mock_session()

        auth = AWSV4SignerAsyncAuth(mock_session, region)
        headers = auth("GET", "http://localhost")
        assert "Authorization" in headers
        assert "X-Amz-Date" in headers
        assert "X-Amz-Security-Token" in headers
        assert len(mock_session.get_frozen_credentials.mock_calls) == 1


class TestAsyncSignerWithSpecialCharacters:
    def mock_session(self) -> Mock:
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token

        del dummy_session.get_frozen_credentials

        return dummy_session

    async def test_aws_signer_async_consitent_url(self) -> None:
        region = "us-west-2"

        from opensearchpy import AsyncOpenSearch
        from opensearchpy.connection.http_async import AsyncHttpConnection
        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        # Store URLs for comparison
        signed_url = None
        sent_url = None

        doc_id = "doc_id:with!special*chars%3A"
        quoted_doc_id = "doc_id%3Awith%21special*chars%253A"
        url = f"https://search-domain.region.es.amazonaws.com:9200/index/_doc/{quoted_doc_id}"

        # Create a mock signer class to capture the signed URL
        class MockSigner(AWSV4SignerAsyncAuth):
            def _sign_request(
                self,
                method: str,
                url: str,
                body: Optional[Union[str, bytes]] = None,
                headers: Optional[Dict[str, str]] = None,
            ) -> Dict[str, str]:
                nonlocal signed_url
                signed_url = url
                return {}

        # Create a mock connection class to capture the sent URL
        class MockConnection(AsyncHttpConnection):
            async def perform_request(
                self: "MockConnection",
                method: str,
                url: str,
                params: Optional[Mapping[str, Any]] = None,
                body: Optional[Any] = None,
                timeout: Optional[Union[int, float]] = None,
                ignore: Collection[int] = (),
                headers: Optional[Mapping[str, str]] = None,
            ) -> Tuple[int, Mapping[str, str], str]:
                nonlocal sent_url
                sent_url = f"{self.host}{url}"
                return 200, {}, "{}"

        auth = MockSigner(self.mock_session(), region)
        auth("GET", url)

        client = AsyncOpenSearch(
            hosts=[{"host": "search-domain.region.es.amazonaws.com"}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=MockConnection,
        )
        await client.index("index", {"test": "data"}, id=doc_id)
        assert signed_url == sent_url, "URLs don't match"
