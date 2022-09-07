# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from __future__ import unicode_literals

from . import OpenSearchTestCase


class TestUnicode(OpenSearchTestCase):
    def test_indices_analyze(self):
        self.client.indices.analyze(body='{"text": "привет"}')


class TestBulk(OpenSearchTestCase):
    def test_bulk_works_with_string_body(self):
        docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))

    def test_bulk_works_with_bytestring_body(self):
        docs = b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))
