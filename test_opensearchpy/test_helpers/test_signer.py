# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import uuid
from unittest.mock import Mock

import requests

from opensearchpy.helpers.signer import RequestsAWSV4SignerAuth


class TestRequestsSignerExcludesTransportHeaders:
    """End-to-end check of the synchronous requests path.

    RequestsAWSV4SignerAuth signs a real requests PreparedRequest, whose headers
    the requests library populates with hop-by-hop / volatile values (Connection,
    Content-Type, Content-Length, ...). If any of those are signed, the transport
    later mutating them breaks the signature -- the exact bug this fix addresses.
    Unlike the async unit test (which uses a hand-built header dict), this drives
    the real requests plumbing with headers requests injects itself.
    """

    def mock_credentials(self) -> Mock:
        credentials = Mock()
        credentials.access_key = uuid.uuid4().hex
        credentials.secret_key = uuid.uuid4().hex
        credentials.token = uuid.uuid4().hex
        del credentials.get_frozen_credentials
        return credentials

    def test_transport_injected_headers_are_not_signed(self) -> None:
        prepared = requests.Session().prepare_request(
            requests.Request(
                "POST", "http://localhost:9200/index/_doc", json={"a": 1}
            )
        )
        # sanity: the requests library really does inject the problematic headers
        assert "Connection" in prepared.headers
        assert "Content-Type" in prepared.headers

        auth = RequestsAWSV4SignerAuth(self.mock_credentials(), "us-west-2")
        signed = auth(prepared)

        signed_headers = (
            signed.headers["Authorization"]
            .split("SignedHeaders=")[1]
            .split(",")[0]
            .split(";")
        )
        assert "host" in signed_headers
        for volatile in (
            "connection",
            "content-type",
            "content-length",
            "accept-encoding",
            "user-agent",
        ):
            assert volatile not in signed_headers
