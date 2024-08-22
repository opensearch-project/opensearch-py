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


from test_opensearchpy.test_cases import OpenSearchTestCase


class TestIndices(OpenSearchTestCase):
    def test_create_one_index(self) -> None:
        self.client.indices.create("test-index")
        self.assert_url_called("PUT", "/test-index")

    def test_delete_multiple_indices(self) -> None:
        self.client.indices.delete(["test-index", "second.index", "third/index"])
        self.assert_url_called("DELETE", "/test-index,second.index,third%2Findex")

    def test_exists_index(self) -> None:
        self.client.indices.exists("second.index,third/index")
        self.assert_url_called("HEAD", "/second.index,third%2Findex")

    def test_passing_empty_value_for_required_param_raises_exception(self) -> None:
        self.assertRaises(ValueError, self.client.indices.exists, index=None)
        self.assertRaises(ValueError, self.client.indices.exists, index=[])
        self.assertRaises(ValueError, self.client.indices.exists, index="")

    def test_create_alias(self) -> None:
        self.client.indices.create("test-index")
        self.client.indices.put_alias("test-index", "test-alias")
        self.assert_url_called("PUT", "/test-index/_alias/test-alias")
