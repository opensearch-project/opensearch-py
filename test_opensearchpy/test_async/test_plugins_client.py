# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from unittest import TestCase

from opensearchpy._async.client import AsyncOpenSearch


class TestPluginsClient(TestCase):
    async def test_plugins_client(self) -> None:
        with self.assertWarns(Warning) as w:
            client = AsyncOpenSearch()
            client.plugins.__init__(client)  # double-init
            self.assertEqual(
                str(w.warnings[0].message),
                "Cannot load `alerting` directly to AsyncOpenSearch as it already exists. Use `AsyncOpenSearch.plugin.alerting` instead.",
            )
