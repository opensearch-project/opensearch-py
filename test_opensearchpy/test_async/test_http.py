# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import pytest
from _pytest.mark.structures import MarkDecorator

from .test_client import OpenSearchTestCaseWithDummyTransport

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestHttpClient(OpenSearchTestCaseWithDummyTransport):
    async def test_head(self) -> None:
        # pylint: disable=missing-function-docstring
        await self.client.http.head("/")
        self.assert_call_count_equals(1)
        assert [(None, None, None)] == self.assert_url_called("HEAD", "/", 1)

    async def test_get(self) -> None:
        # pylint: disable=missing-function-docstring
        await self.client.http.get("/")
        self.assert_call_count_equals(1)
        assert [(None, None, None)] == self.assert_url_called("GET", "/", 1)

    async def test_put(self) -> None:
        # pylint: disable=missing-function-docstring
        await self.client.http.put(url="/xyz", params={"X": "Y"}, body="body")
        self.assert_call_count_equals(1)
        assert [({"X": "Y"}, None, "body")] == self.assert_url_called("PUT", "/xyz", 1)

    async def test_post(self) -> None:
        # pylint: disable=missing-function-docstring
        await self.client.http.post(url="/xyz", params={"X": "Y"}, body="body")
        self.assert_call_count_equals(1)
        assert [({"X": "Y"}, None, "body")] == self.assert_url_called("POST", "/xyz", 1)

    async def test_post_with_headers(self) -> None:
        # pylint: disable=missing-function-docstring
        await self.client.http.post(
            url="/xyz", headers={"A": "B"}, params={"X": "Y"}, body="body"
        )
        self.assert_call_count_equals(1)
        assert [({"X": "Y"}, {"A": "B"}, "body")] == self.assert_url_called(
            "POST", "/xyz", 1
        )

    async def test_delete(self) -> None:
        # pylint: disable=missing-function-docstring
        await self.client.http.delete(url="/xyz", params={"X": "Y"}, body="body")
        self.assert_call_count_equals(1)
        assert [({"X": "Y"}, None, "body")] == self.assert_url_called(
            "DELETE", "/xyz", 1
        )
