# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
from unittest import TestCase

from opensearchpy.helpers.signer import derive_signature_url


class TestUrllib3Connection(TestCase):
    def test_derive_signature_url(self):
        assert (
            derive_signature_url("http://localhost:10552/", singing_port=443)
            == "http://localhost:443/"
        )
        assert (
            derive_signature_url("http://localhost:10552/foo/bar", singing_port=443)
            == "http://localhost:443/foo/bar"
        )
        assert (
            derive_signature_url("http://localhost/", singing_port=443)
            == "http://localhost:443/"
        )
        assert (
            derive_signature_url("http://localhost/foo/bar", singing_port=443)
            == "http://localhost:443/foo/bar"
        )

    def test_derive_signature_url_no_hostname(self):
        self.assertRaises(RuntimeError, derive_signature_url, "http://", 23)
