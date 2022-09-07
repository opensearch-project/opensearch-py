# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from unittest import SkipTest

from opensearchpy.helpers import test
from opensearchpy.helpers.test import OpenSearchTestCase as BaseTestCase

client = None


def get_client(**kwargs):
    global client
    if client is False:
        raise SkipTest("No client is available")
    if client is not None and not kwargs:
        return client

    # try and locate manual override in the local environment
    try:
        from test_opensearchpy.local import get_client as local_get_client

        new_client = local_get_client(**kwargs)
    except ImportError:
        # fallback to using vanilla client
        try:
            new_client = test.get_test_client(**kwargs)
        except SkipTest:
            client = False
            raise

    if not kwargs:
        client = new_client

    return new_client


def setup_module():
    get_client()


class OpenSearchTestCase(BaseTestCase):
    @staticmethod
    def _get_client(**kwargs):
        return get_client(**kwargs)
