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


from typing import Any

from mock import Mock
from pytest import fixture

from opensearchpy.connection.connections import add_connection, connections


@fixture  # type: ignore
def mock_client(dummy_response: Any) -> Any:
    # pylint: disable=missing-function-docstring
    client = Mock()
    client.search.return_value = dummy_response
    add_connection("mock", client)
    yield client
    connections._conns = {}
    connections._kwargs = {}


@fixture  # type: ignore
def dummy_response() -> Any:
    # pylint: disable=missing-function-docstring
    return {
        "_shards": {"failed": 0, "successful": 10, "total": 10},
        "hits": {
            "hits": [
                {
                    "_index": "test-index",
                    "_id": "opensearch",
                    "_score": 12.0,
                    "_source": {"city": "Amsterdam", "name": "OpenSearch"},
                },
                {
                    "_index": "test-index",
                    "_id": "42",
                    "_score": 11.123,
                    "_routing": "opensearch",
                    "_source": {
                        "name": {"first": "Shay", "last": "Bannon"},
                        "lang": "java",
                        "twitter": "kimchy",
                    },
                },
                {
                    "_index": "test-index",
                    "_id": "47",
                    "_score": 1,
                    "_routing": "opensearch",
                    "_source": {
                        "name": {"first": "Honza", "last": "Král"},
                        "lang": "python",
                        "twitter": "honzakral",
                    },
                },
                {
                    "_index": "test-index",
                    "_id": "53",
                    "_score": 16.0,
                    "_routing": "opensearch",
                },
            ],
            "max_score": 12.0,
            "total": 123,
        },
        "timed_out": False,
        "took": 123,
    }


@fixture  # type: ignore
def aggs_search() -> Any:
    # pylint: disable=missing-function-docstring
    from opensearchpy import Search

    s = Search(index="flat-git")
    s.aggs.bucket("popular_files", "terms", field="files", size=2).metric(
        "line_stats", "stats", field="stats.lines"
    ).metric("top_commits", "top_hits", size=2, _source=["stats.*", "committed_date"])
    s.aggs.bucket(
        "per_month", "date_histogram", interval="month", field="info.committed_date"
    )
    s.aggs.metric("sum_lines", "sum", field="stats.lines")
    return s


@fixture  # type: ignore
def aggs_data() -> Any:
    # pylint: disable=missing-function-docstring
    return {
        "took": 4,
        "timed_out": False,
        "_shards": {"total": 1, "successful": 1, "failed": 0},
        "hits": {"total": 52, "hits": [], "max_score": 0.0},
        "aggregations": {
            "sum_lines": {"value": 25052.0},
            "per_month": {
                "buckets": [
                    {
                        "doc_count": 38,
                        "key": 1393632000000,
                        "key_as_string": "2014-03-01T00:00:00.000Z",
                    },
                    {
                        "doc_count": 11,
                        "key": 1396310400000,
                        "key_as_string": "2014-04-01T00:00:00.000Z",
                    },
                    {
                        "doc_count": 3,
                        "key": 1398902400000,
                        "key_as_string": "2014-05-01T00:00:00.000Z",
                    },
                ]
            },
            "popular_files": {
                "buckets": [
                    {
                        "key": "opensearchpy",
                        "line_stats": {
                            "count": 40,
                            "max": 228.0,
                            "min": 2.0,
                            "sum": 2151.0,
                            "avg": 53.775,
                        },
                        "doc_count": 40,
                        "top_commits": {
                            "hits": {
                                "total": 40,
                                "hits": [
                                    {
                                        "_id": "3ca6e1e73a071a705b4babd2f581c91a2a3e5037",
                                        "_type": "doc",
                                        "_source": {
                                            "stats": {
                                                "files": 4,
                                                "deletions": 7,
                                                "lines": 30,
                                                "insertions": 23,
                                            },
                                            "committed_date": "2014-05-02T13:47:19",
                                        },
                                        "_score": 1.0,
                                        "_index": "flat-git",
                                    },
                                    {
                                        "_id": "eb3e543323f189fd7b698e66295427204fff5755",
                                        "_type": "doc",
                                        "_source": {
                                            "stats": {
                                                "files": 1,
                                                "deletions": 0,
                                                "lines": 18,
                                                "insertions": 18,
                                            },
                                            "committed_date": "2014-05-01T13:32:14",
                                        },
                                        "_score": 1.0,
                                        "_index": "flat-git",
                                    },
                                ],
                                "max_score": 1.0,
                            }
                        },
                    },
                    {
                        "key": "test_opensearchpy/test_dsl",
                        "line_stats": {
                            "count": 35,
                            "max": 228.0,
                            "min": 2.0,
                            "sum": 1939.0,
                            "avg": 55.4,
                        },
                        "doc_count": 35,
                        "top_commits": {
                            "hits": {
                                "total": 35,
                                "hits": [
                                    {
                                        "_id": "3ca6e1e73a071a705b4babd2f581c91a2a3e5037",
                                        "_type": "doc",
                                        "_source": {
                                            "stats": {
                                                "files": 4,
                                                "deletions": 7,
                                                "lines": 30,
                                                "insertions": 23,
                                            },
                                            "committed_date": "2014-05-02T13:47:19",
                                        },
                                        "_score": 1.0,
                                        "_index": "flat-git",
                                    },
                                    {
                                        "_id": "dd15b6ba17dd9ba16363a51f85b31f66f1fb1157",
                                        "_type": "doc",
                                        "_source": {
                                            "stats": {
                                                "files": 3,
                                                "deletions": 18,
                                                "lines": 62,
                                                "insertions": 44,
                                            },
                                            "committed_date": "2014-05-01T13:30:44",
                                        },
                                        "_score": 1.0,
                                        "_index": "flat-git",
                                    },
                                ],
                                "max_score": 1.0,
                            }
                        },
                    },
                ],
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 120,
            },
        },
    }
