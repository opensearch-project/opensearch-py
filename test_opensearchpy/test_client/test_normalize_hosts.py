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

from opensearchpy.client.utils import _normalize_hosts

from ..test_cases import TestCase


class TestNormalizeHosts(TestCase):
    def test_none_uses_defaults(self) -> None:
        self.assertEqual([{}], _normalize_hosts(None))

    def test_strings_are_used_as_hostnames(self) -> None:
        self.assertEqual(
            [{"host": "opensearch.org"}], _normalize_hosts(["opensearch.org"])
        )

    def test_strings_are_parsed_for_port_and_user(self) -> None:
        self.assertEqual(
            [
                {"host": "opensearch.org", "port": 42},
                {"host": "opensearch.org", "http_auth": "user:secre]"},
            ],
            _normalize_hosts(["opensearch.org:42", "user:secre%5D@opensearch.org"]),
        )

    def test_strings_are_parsed_for_scheme(self) -> None:
        self.assertEqual(
            [
                {"host": "opensearch.org", "port": 42, "use_ssl": True},
                {
                    "host": "opensearch.org",
                    "http_auth": "user:secret",
                    "use_ssl": True,
                    "port": 443,
                    "url_prefix": "/prefix",
                },
            ],
            _normalize_hosts(
                [
                    "https://opensearch.org:42",
                    "https://user:secret@opensearch.org/prefix",
                ]
            ),
        )

    def test_dicts_are_left_unchanged(self) -> None:
        self.assertEqual(
            [{"host": "local", "extra": 123}],
            _normalize_hosts([{"host": "local", "extra": 123}]),
        )

    def test_single_string_is_wrapped_in_list(self) -> None:
        self.assertEqual(
            [{"host": "opensearch.org"}], _normalize_hosts("opensearch.org")
        )
