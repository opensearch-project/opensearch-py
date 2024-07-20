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


import warnings

from opensearchpy.client import OpenSearch
from opensearchpy.client.utils import _normalize_hosts

from ..test_cases import OpenSearchTestCase, TestCase


class TestNormalizeHosts(TestCase):
    def test_none_uses_defaults(self) -> None:
        self.assertEqual([{}], _normalize_hosts(None))

    def test_strings_are_used_as_hostnames(self) -> None:
        self.assertEqual([{"host": "elastic.co"}], _normalize_hosts(["elastic.co"]))

    def test_strings_are_parsed_for_port_and_user(self) -> None:
        self.assertEqual(
            [
                {"host": "elastic.co", "port": 42},
                {"host": "elastic.co", "http_auth": "user:secre]"},
            ],
            _normalize_hosts(["elastic.co:42", "user:secre%5D@elastic.co"]),
        )

    def test_strings_are_parsed_for_scheme(self) -> None:
        self.assertEqual(
            [
                {"host": "elastic.co", "port": 42, "use_ssl": True},
                {
                    "host": "elastic.co",
                    "http_auth": "user:secret",
                    "use_ssl": True,
                    "port": 443,
                    "url_prefix": "/prefix",
                },
            ],
            _normalize_hosts(
                ["https://elastic.co:42", "https://user:secret@elastic.co/prefix"]
            ),
        )

    def test_dicts_are_left_unchanged(self) -> None:
        self.assertEqual(
            [{"host": "local", "extra": 123}],
            _normalize_hosts([{"host": "local", "extra": 123}]),
        )

    def test_single_string_is_wrapped_in_list(self) -> None:
        self.assertEqual([{"host": "elastic.co"}], _normalize_hosts("elastic.co"))


class TestClient(OpenSearchTestCase):
    def test_request_timeout_is_passed_through_unescaped(self) -> None:
        self.client.ping(request_timeout=0.1)
        calls = self.assert_url_called("HEAD", "/")
        self.assertEqual([({"request_timeout": 0.1}, {}, None)], calls)

    def test_params_is_copied_when(self) -> None:
        rt = object()
        params = dict(request_timeout=rt)
        self.client.ping(params=params)
        self.client.ping(params=params)
        calls = self.assert_url_called("HEAD", "/", 2)
        self.assertEqual(
            [({"request_timeout": rt}, {}, None), ({"request_timeout": rt}, {}, None)],
            calls,
        )
        self.assertFalse(calls[0][0] is calls[1][0])

    def test_headers_is_copied_when(self) -> None:
        hv = "value"
        headers = dict(Authentication=hv)
        self.client.ping(headers=headers)
        self.client.ping(headers=headers)
        calls = self.assert_url_called("HEAD", "/", 2)
        self.assertEqual(
            [({}, {"authentication": hv}, None), ({}, {"authentication": hv}, None)],
            calls,
        )
        self.assertFalse(calls[0][0] is calls[1][0])

    def test_from_in_search(self) -> None:
        self.client.search(index="i", from_=10)
        calls = self.assert_url_called("POST", "/i/_search")
        self.assertEqual([({"from": "10"}, {}, None)], calls)

    def test_repr_contains_hosts(self) -> None:
        self.assertEqual("<OpenSearch([{}])>", repr(self.client))

    def test_repr_subclass(self) -> None:
        class OtherOpenSearch(OpenSearch):
            pass

        self.assertEqual("<OtherOpenSearch([{}])>", repr(OtherOpenSearch()))

    def test_repr_contains_hosts_passed_in(self) -> None:
        self.assertIn("opensearchpy.org", repr(OpenSearch(["opensearch.org:123"])))

    def test_repr_truncates_host_to_5(self) -> None:
        hosts = [{"host": "opensearch" + str(i)} for i in range(10)]
        client = OpenSearch(hosts)
        self.assertNotIn("opensearch5", repr(client))
        self.assertIn("...", repr(client))

    def test_index_uses_post_if_id_is_empty(self) -> None:
        self.client.index(index="my-index", id="", body={})

        self.assert_url_called("POST", "/my-index/_doc")

    def test_index_uses_put_if_id_is_not_empty(self) -> None:
        self.client.index(index="my-index", id=0, body={})

        self.assert_url_called("PUT", "/my-index/_doc/0")

    def test_tasks_get_without_task_id_deprecated(self) -> None:
        warnings.simplefilter("always", DeprecationWarning)
        with warnings.catch_warnings(record=True) as w:
            self.client.tasks.get()

        self.assert_url_called("GET", "/_tasks")
        self.assertEqual(len(w), 1)
        self.assertIs(w[0].category, DeprecationWarning)
        self.assertEqual(
            str(w[0].message),
            "Calling client.tasks.get() without a task_id is deprecated "
            "and will be removed in v8.0. Use client.tasks.list() instead.",
        )

    def test_tasks_get_with_task_id_not_deprecated(self) -> None:
        warnings.simplefilter("always", DeprecationWarning)
        with warnings.catch_warnings(record=True) as w:
            self.client.tasks.get("task-1")
            self.client.tasks.get(task_id="task-2")

        self.assert_url_called("GET", "/_tasks/task-1")
        self.assert_url_called("GET", "/_tasks/task-2")
        self.assertEqual(len(w), 0)
