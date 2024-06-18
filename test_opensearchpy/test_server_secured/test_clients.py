# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import os
from unittest import TestCase

from opensearchpy import OpenSearch
from opensearchpy.helpers.test import OPENSEARCH_URL


class TestSecurity(TestCase):
    def test_security(self) -> None:
        password = os.environ.get("OPENSEARCH_INITIAL_ADMIN_PASSWORD", "admin")
        client = OpenSearch(
            OPENSEARCH_URL,
            http_auth=("admin", password),
            verify_certs=False,
        )

        info = client.info()
        self.assertNotEqual(info["version"]["number"], "")
        self.assertNotEqual(info["tagline"], "")
        self.assertTrue(
            "build_flavor" in info["version"] or "distribution" in info["version"]
        )
