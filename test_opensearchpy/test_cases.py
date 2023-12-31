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


from collections import defaultdict
from typing import Any, Mapping, Optional, Sequence
from unittest import SkipTest, TestCase

from opensearchpy import OpenSearch


class DummyTransport(object):
    def __init__(
        self, hosts: Sequence[str], responses: Any = None, **kwargs: Any
    ) -> None:
        # pylint: disable=missing-function-docstring
        self.hosts = hosts
        self.responses = responses
        self.call_count: int = 0
        self.calls: Any = defaultdict(list)

    def perform_request(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        body: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        # pylint: disable=missing-function-docstring
        resp: Any = (200, {})
        if self.responses:
            resp = self.responses[self.call_count]
        self.call_count += 1
        self.calls[(method, url)].append((params, headers, body))
        return resp


class OpenSearchTestCase(TestCase):
    def setUp(self) -> None:
        # pylint: disable=missing-function-docstring
        super(OpenSearchTestCase, self).setUp()
        self.client: Any = OpenSearch(transport_class=DummyTransport)  # type: ignore

    def assert_call_count_equals(self, count: int) -> None:
        # pylint: disable=missing-function-docstring
        self.assertEqual(count, self.client.transport.call_count)

    def assert_url_called(self, method: str, url: str, count: int = 1) -> Any:
        # pylint: disable=missing-function-docstring
        self.assertIn((method, url), self.client.transport.calls)
        calls = self.client.transport.calls[(method, url)]
        self.assertEqual(count, len(calls))
        return calls


class TestOpenSearchTestCase(OpenSearchTestCase):
    def test_our_transport_used(self) -> None:
        # pylint: disable=missing-function-docstring
        self.assertIsInstance(self.client.transport, DummyTransport)

    def test_start_with_0_call(self) -> None:
        # pylint: disable=missing-function-docstring
        self.assert_call_count_equals(0)

    def test_each_call_is_recorded(self) -> None:
        # pylint: disable=missing-function-docstring
        self.client.transport.perform_request("GET", "/")
        self.client.transport.perform_request("DELETE", "/42", params={}, body="body")
        self.assert_call_count_equals(2)
        self.assertEqual(
            [({}, None, "body")], self.assert_url_called("DELETE", "/42", 1)
        )


__all__ = ["SkipTest", "TestCase"]
