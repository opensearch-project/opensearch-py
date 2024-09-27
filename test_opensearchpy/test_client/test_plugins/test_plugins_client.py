# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import re

from opensearchpy.client import OpenSearch

from ...test_cases import TestCase


class TestPluginsClient(TestCase):
    def test_plugins_client(self) -> None:
        with self.assertWarns(Warning) as w:
            client = OpenSearch()
            # double-init
            client.plugins.__init__(client)  # type: ignore # pylint: disable=unnecessary-dunder-call
            self.assertTrue(
                re.match(
                    r"Cannot load `\w+` directly to OpenSearch as it already exists. Use `OpenSearch.plugin.\w+` instead.",
                    str(w.warnings[0].message),
                )
            )
