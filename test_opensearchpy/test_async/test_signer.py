# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import sys
import uuid

import pytest
from mock import Mock

pytestmark = pytest.mark.asyncio


class TestAsyncSigner:
    def mock_session(self, disable_get_frozen=True):
        access_key = uuid.uuid4().hex
        secret_key = uuid.uuid4().hex
        token = uuid.uuid4().hex
        dummy_session = Mock()
        dummy_session.access_key = access_key
        dummy_session.secret_key = secret_key
        dummy_session.token = token
        dummy_session.get_frozen_credentials = Mock(return_value=dummy_session)

        if disable_get_frozen:
            del dummy_session.get_frozen_credentials

        return dummy_session

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="AWSV4SignerAsyncAuth requires python3.6+"
    )
    async def test_aws_signer_async_frozen_credentials_as_http_auth(self):
        region = "us-west-2"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        mock_session = self.mock_session(disable_get_frozen=False)

        auth = AWSV4SignerAsyncAuth(mock_session, region)
        headers = auth("GET", "http://localhost", {}, {})
        assert "Authorization" in headers
        assert "X-Amz-Date" in headers
        assert "X-Amz-Security-Token" in headers
        assert len(mock_session.get_frozen_credentials.mock_calls) == 1

    async def test_aws_signer_async_as_http_auth(self):
        region = "us-west-2"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        auth = AWSV4SignerAsyncAuth(self.mock_session(), region)
        headers = auth("GET", "http://localhost", {}, {})
        assert "Authorization" in headers
        assert "X-Amz-Date" in headers
        assert "X-Amz-Security-Token" in headers

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="AWSV4SignerAuth requires python3.6+"
    )
    async def test_aws_signer_async_when_region_is_null(self):
        session = self.mock_session()

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        with pytest.raises(ValueError) as e:
            AWSV4SignerAsyncAuth(session, None)
        assert str(e.value) == "Region cannot be empty"

        with pytest.raises(ValueError) as e:
            AWSV4SignerAsyncAuth(session, "")
        assert str(e.value) == "Region cannot be empty"

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="AWSV4SignerAuth requires python3.6+"
    )
    async def test_aws_signer_async_when_credentials_is_null(self):
        region = "us-west-1"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        with pytest.raises(ValueError) as e:
            AWSV4SignerAsyncAuth(None, region)
        assert str(e.value) == "Credentials cannot be empty"

    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="AWSV4SignerAsyncAuth requires python3.6+"
    )
    async def test_aws_signer_async_when_service_is_specified(self):
        region = "us-west-2"
        service = "aoss"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        auth = AWSV4SignerAsyncAuth(self.mock_session(), region, service)
        headers = auth("GET", "http://localhost", {}, {})
        assert "Authorization" in headers
        assert "X-Amz-Date" in headers
        assert "X-Amz-Security-Token" in headers
        assert "X-Amz-Content-SHA256" in headers
