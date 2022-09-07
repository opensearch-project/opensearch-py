# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


# type: ignore

import os
import time
from unittest import SkipTest, TestCase

from opensearchpy import OpenSearch
from opensearchpy.exceptions import ConnectionError

if "OPENSEARCH_URL" in os.environ:
    OPENSEARCH_URL = os.environ["OPENSEARCH_URL"]
else:
    OPENSEARCH_URL = "https://elastic:changeme@localhost:9200"


def get_test_client(nowait=False, **kwargs):
    # construct kwargs from the environment
    kw = {"timeout": 30}

    if "PYTHON_CONNECTION_CLASS" in os.environ:
        from opensearchpy import connection

        kw["connection_class"] = getattr(
            connection, os.environ["PYTHON_CONNECTION_CLASS"]
        )

    kw.update(kwargs)
    client = OpenSearch(OPENSEARCH_URL, **kw)

    # wait for yellow status
    for _ in range(1 if nowait else 100):
        try:
            client.cluster.health(wait_for_status="yellow")
            return client
        except ConnectionError:
            time.sleep(0.1)
    else:
        # timeout
        raise SkipTest("OpenSearch failed to start.")


class OpenSearchTestCase(TestCase):
    @staticmethod
    def _get_client():
        return get_test_client()

    @classmethod
    def setup_class(cls):
        cls.client = cls._get_client()

    def teardown_method(self, _):
        # Hidden indices expanded in wildcards in OpenSearch 7.7
        expand_wildcards = ["open", "closed"]
        if self.opensearch_version() >= (1, 0):
            expand_wildcards.append("hidden")

        self.client.indices.delete(
            index="*", ignore=404, expand_wildcards=expand_wildcards
        )
        self.client.indices.delete_template(name="*", ignore=404)

    def opensearch_version(self):
        if not hasattr(self, "_opensearch_version"):
            self._opensearch_version = opensearch_version(self.client)
        return self._opensearch_version


def _get_version(version_string):
    if "." not in version_string:
        return ()
    version = version_string.strip().split(".")
    return tuple(int(v) if v.isdigit() else 999 for v in version)


def opensearch_version(client):
    return _get_version(client.info()["version"]["number"])


if "OPENSEARCH_VERSION" in os.environ:
    OPENSEARCH_VERSION = _get_version(os.environ["OPENSEARCH_VERSION"])
else:
    client = OpenSearch(
        OPENSEARCH_URL,
    )
    OPENSEARCH_VERSION = opensearch_version(client)
