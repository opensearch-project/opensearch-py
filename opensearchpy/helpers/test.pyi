# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Tuple
from unittest import TestCase

from ..client import OpenSearch

OPENSEARCH_URL: str
CA_CERTS: str

def get_test_client(nowait: bool = ..., **kwargs: Any) -> OpenSearch: ...
def _get_version(version_string: str) -> Tuple[int, ...]: ...

class OpenSearchTestCase(TestCase):
    @staticmethod
    def _get_client() -> OpenSearch: ...
    @classmethod
    def setup_class(cls) -> None: ...
    def teardown_method(self, _: Any) -> None: ...
    def opensearch_version(self) -> Tuple[int, ...]: ...
