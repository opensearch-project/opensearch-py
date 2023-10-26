# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from opensearchpy.client import OpenSearch

from ...test_cases import TestCase


class TestPluginsClient(TestCase):
    def test_plugins_client(self):
        with self.assertWarns(Warning) as w:
            client = OpenSearch()
            client.plugins.__init__(client)  # double-init
            self.assertEqual(
                str(w.warnings[0].message),
                "Cannot load `alerting` directly to OpenSearch as it already exists. Use `OpenSearch.plugin.alerting` instead.",
            )
