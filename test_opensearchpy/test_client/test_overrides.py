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


import pytest

from test_opensearchpy.test_cases import OpenSearchTestCase


class TestOverriddenUrlTargets(OpenSearchTestCase):
    def test_create(self) -> None:
        self.client.create(index="test-index", id="test-id", body={})
        self.assert_url_called("PUT", "/test-index/_create/test-id")

    def test_delete(self) -> None:
        self.client.delete(index="test-index", id="test-id")
        self.assert_url_called("DELETE", "/test-index/_doc/test-id")

    def test_exists(self) -> None:
        self.client.exists(index="test-index", id="test-id")
        self.assert_url_called("HEAD", "/test-index/_doc/test-id")

    def test_explain(self) -> None:
        self.client.explain(index="test-index", id="test-id")
        self.assert_url_called("POST", "/test-index/_explain/test-id")

    def test_get(self) -> None:
        self.client.get(index="test-index", id="test-id")
        self.assert_url_called("GET", "/test-index/_doc/test-id")

    def test_get_source(self) -> None:
        self.client.get_source(index="test-index", id="test-id")
        self.assert_url_called("GET", "/test-index/_source/test-id")

    def test_exists_source(self) -> None:
        self.client.exists_source(index="test-index", id="test-id")
        self.assert_url_called("HEAD", "/test-index/_source/test-id")

    def test_index(self) -> None:
        self.client.index(index="test-index", body={})
        self.assert_url_called("POST", "/test-index/_doc")

        self.client.index(index="test-index", id="test-id", body={})
        self.assert_url_called("PUT", "/test-index/_doc/test-id")

    def test_termvectors(self) -> None:
        self.client.termvectors(index="test-index", body={})
        self.assert_url_called("POST", "/test-index/_termvectors")

        self.client.termvectors(index="test-index", id="test-id", body={})
        self.assert_url_called("POST", "/test-index/_termvectors/test-id")

    def test_mtermvectors(self) -> None:
        self.client.mtermvectors(index="test-index", body={})
        self.assert_url_called("POST", "/test-index/_mtermvectors")

    def test_update(self) -> None:
        self.client.update(index="test-index", id="test-id", body={})
        self.assert_url_called("POST", "/test-index/_update/test-id")

    def test_cluster_state(self) -> None:
        self.client.cluster.state()
        self.assert_url_called("GET", "/_cluster/state")

        self.client.cluster.state(index="test-index")
        self.assert_url_called("GET", "/_cluster/state/_all/test-index")

        self.client.cluster.state(index="test-index", metric="test-metric")
        self.assert_url_called("GET", "/_cluster/state/test-metric/test-index")

    def test_cluster_stats(self) -> None:
        self.client.cluster.stats()
        self.assert_url_called("GET", "/_cluster/stats")

        self.client.cluster.stats(node_id="test-node")
        self.assert_url_called("GET", "/_cluster/stats/nodes/test-node")

    def test_indices_put_mapping(self) -> None:
        self.client.indices.put_mapping(body={})
        self.assert_url_called("PUT", "/_all/_mapping")

        self.client.indices.put_mapping(index="test-index", body={})
        self.assert_url_called("PUT", "/test-index/_mapping")

    def test_tasks_get(self) -> None:
        with pytest.warns(DeprecationWarning):
            self.client.tasks.get()
