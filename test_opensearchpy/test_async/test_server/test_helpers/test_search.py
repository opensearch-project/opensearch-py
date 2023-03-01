# -*- coding: utf-8 -*-
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

from __future__ import unicode_literals

from pytest import raises
import pytest
from opensearchpy import Date, Document, Keyword, Q, Text, TransportError
from opensearchpy._async.helpers.search import AsyncMultiSearch, AsyncSearch
from opensearchpy.helpers.response import aggs
from test_opensearchpy.test_server.test_helpers.test_data import FLAT_DATA
pytestmark = pytest.mark.asyncio

class Repository(Document):
    created_at = Date()
    description = Text(analyzer="snowball")
    tags = Keyword()

    @classmethod
    def search(cls):
        return super(Repository, cls).search().filter("term", commit_repo="repo")

    class Index:
        name = "git"


class Commit(Document):
    class Index:
        name = "flat-git"


def test_filters_aggregation_buckets_are_accessible(data_client):
    has_tests_query = Q("term", files="test_opensearchpy/test_dsl")
    s = Commit.search()[0:0]
    s.aggs.bucket("top_authors", "terms", field="author.name.raw").bucket(
        "has_tests", "filters", filters={"yes": has_tests_query, "no": ~has_tests_query}
    ).metric("lines", "stats", field="stats.lines")
    response = s.execute()

    assert isinstance(
        response.aggregations.top_authors.buckets[0].has_tests.buckets.yes, aggs.Bucket
    )
    assert (
        35
        == response.aggregations.top_authors.buckets[0].has_tests.buckets.yes.doc_count
    )
    assert (
        228
        == response.aggregations.top_authors.buckets[0].has_tests.buckets.yes.lines.max
    )


def test_top_hits_are_wrapped_in_response(data_client):
    s = Commit.search()[0:0]
    s.aggs.bucket("top_authors", "terms", field="author.name.raw").metric(
        "top_commits", "top_hits", size=5
    )
    response = s.execute()

    top_commits = response.aggregations.top_authors.buckets[0].top_commits
    assert isinstance(top_commits, aggs.TopHitsData)
    assert 5 == len(top_commits)

    hits = [h for h in top_commits]
    assert 5 == len(hits)
    assert isinstance(hits[0], Commit)


async def test_inner_hits_are_wrapped_in_response(data_client):
    s = AsyncSearch(index="git")[0:1].query(
        "has_parent", parent_type="repo", inner_hits={}, query=Q("match_all")
    )
    response = await s.execute()

    commit = response.hits[0]
    assert isinstance(commit.meta.inner_hits.repo, response.__class__)
    assert repr(commit.meta.inner_hits.repo[0]).startswith("<Hit(git/opensearch-py): ")


def test_scan_respects_doc_types(data_client):
    repos = list(Repository.search().scan())

    assert 1 == len(repos)
    assert isinstance(repos[0], Repository)
    assert repos[0].organization == "opensearch"


async def test_scan_iterates_through_all_docs(data_client):
    s = AsyncSearch(index="flat-git")
    result = s.scan()
    print("Remove Later")
    print (result)
    print("Remove Later")
    commits = list(result)

    assert 52 == len(commits)
    assert {d["_id"] for d in FLAT_DATA} == {c.meta.id for c in commits}


def test_response_is_cached(data_client):
    s = Repository.search()
    repos = list(s)

    assert hasattr(s, "_response")
    assert s._response.hits == repos


async def test_multi_search(data_client):
    s1 = Repository.search()
    s2 = AsyncSearch(index="flat-git")

    ms = AsyncMultiSearch()
    ms = ms.add(s1).add(s2)

    r1, r2 = await ms.execute()

    assert 1 == len(r1)
    assert isinstance(r1[0], Repository)
    assert r1._search is s1

    assert 52 == r2.hits.total.value
    assert r2._search is s2


async def test_multi_missing(data_client):
    s1 = Repository.search()
    s2 = AsyncSearch(index="flat-git")
    s3 = AsyncSearch(index="does_not_exist")

    ms = AsyncMultiSearch()
    ms = ms.add(s1).add(s2).add(s3)

    with raises(TransportError):
        await ms.execute()

    r1, r2, r3 = await ms.execute(raise_on_error=False)

    assert 1 == len(r1)
    assert isinstance(r1[0], Repository)
    assert r1._search is s1

    assert 52 == r2.hits.total.value
    assert r2._search is s2

    assert r3 is None


async def test_raw_subfield_can_be_used_in_aggs(data_client):
    s = AsyncSearch(index="git")[0:0]
    s.aggs.bucket("authors", "terms", field="author.name.raw", size=1)
    print("Remove later5")
    r = await s.execute()
    print("Remove later1")
    print(r)
    print("Remove later2")
    authors = r.aggregations.authors
    print("Remove later3")
    print(authors)
    print("Remove later4")
    assert 1 == len(authors)
    assert {"key": "Honza Král", "doc_count": 52} == authors[0]
