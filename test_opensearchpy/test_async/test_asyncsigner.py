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

import pytest

from ..test_cases import TestCase

pytestmark = pytest.mark.asyncio


class TestAsyncSigner(TestCase):
    @pytest.mark.skipif(
        sys.version_info < (3, 6), reason="AWSV4SignerAsyncAuth requires python3.6+"
    )
    async def test_aws_signer_async_as_http_auth(self):
        region = "us-west-2"

        from opensearchpy.helpers.asyncsigner import AWSV4SignerAsyncAuth

        auth = AWSV4SignerAsyncAuth(self.mock_session(), region)
        headers = auth("GET", "http://localhost")
        self.assertIn("Authorization", headers)
        self.assertIn("X-Amz-Date", headers)
        self.assertIn("X-Amz-Security-Token", headers)

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

        with pytest.raises(ValueError) as e:
            assert str(e.value) == "Credentials cannot be empty"
