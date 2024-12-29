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

from opensearchpy.exceptions import RequestError

from . import OpenSearchTestCase


class TestSpecialCharacters(OpenSearchTestCase):
    def test_index_with_slash(self) -> None:
        index_name = "movies/shmovies"
        with pytest.raises(RequestError) as e:
            self.client.indices.create(index=index_name)
        self.assertEqual(
            str(e.value),
            "RequestError(400, 'invalid_index_name_exception', 'Invalid index name [movies/shmovies], must not contain the following characters [ , \", *, \\\\, <, |, ,, >, /, ?]')",
        )


class TestUnicode(OpenSearchTestCase):
    def test_indices_lifecycle_english(self) -> None:
        index_name = "movies"

        index_create_result = self.client.indices.create(index=index_name)
        self.assertTrue(index_create_result["acknowledged"])
        self.assertEqual(index_name, index_create_result["index"])

        document = {"name": "Solaris", "director": "Andrei Tartakovsky", "year": "2011"}
        id = "solaris@2011"
        doc_insert_result = self.client.index(
            index=index_name, body=document, id=id, refresh=True
        )
        self.assertEqual("created", doc_insert_result["result"])
        self.assertEqual(index_name, doc_insert_result["_index"])
        self.assertEqual(id, doc_insert_result["_id"])

        doc_delete_result = self.client.delete(index=index_name, id=id)
        self.assertEqual("deleted", doc_delete_result["result"])
        self.assertEqual(index_name, doc_delete_result["_index"])
        self.assertEqual(id, doc_delete_result["_id"])

        index_delete_result = self.client.indices.delete(index=index_name)
        self.assertTrue(index_delete_result["acknowledged"])

    def test_indices_lifecycle_russian(self) -> None:
        index_name = "кино"
        index_create_result = self.client.indices.create(index=index_name)
        self.assertTrue(index_create_result["acknowledged"])
        self.assertEqual(index_name, index_create_result["index"])

        document = {"название": "Солярис", "автор": "Андрей Тарковский", "год": "2011"}
        id = "соларис@2011"
        doc_insert_result = self.client.index(
            index=index_name, body=document, id=id, refresh=True
        )
        self.assertEqual("created", doc_insert_result["result"])
        self.assertEqual(index_name, doc_insert_result["_index"])
        self.assertEqual(id, doc_insert_result["_id"])

        doc_delete_result = self.client.delete(index=index_name, id=id)
        self.assertEqual("deleted", doc_delete_result["result"])
        self.assertEqual(index_name, doc_delete_result["_index"])
        self.assertEqual(id, doc_delete_result["_id"])

        index_delete_result = self.client.indices.delete(index=index_name)
        self.assertTrue(index_delete_result["acknowledged"])

    def test_indices_analyze(self) -> None:
        self.client.indices.analyze(body='{"text": "привет"}')


class TestBulk(OpenSearchTestCase):
    def test_bulk_works_with_string_body(self) -> None:
        docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))

    def test_bulk_works_with_bytestring_body(self) -> None:
        docs = b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))

    def test_bulk_works_with_delete(self) -> None:
        docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}\n{ "delete" : { "_index" : "bulk_test_index", "_id": "1" } }'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(2, len(response["items"]))

        # Check insertion status
        self.assertEqual(201, response["items"][0]["index"]["status"])
        # Check deletion status
        self.assertEqual(200, response["items"][1]["delete"]["status"])


class TestClose(OpenSearchTestCase):
    def test_close_doesnt_break_client(self) -> None:
        self.client.cluster.health()
        self.client.close()
        self.client.cluster.health()

    def test_with_doesnt_break_client(self) -> None:
        for _ in range(2):
            with self.client as client:
                client.cluster.health()
