# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
OpenSearchGrpcTestCase — Base class for gRPC integration tests.

Follows the same pattern as test_server/__init__.py but creates a client
with grpc=True so bulk operations are routed over gRPC.

Skips the entire module if gRPC is not available (OpenSearch < 3.0).
"""

import os
from typing import Any
from unittest import SkipTest
from urllib.parse import urlparse

import grpc

from opensearchpy import OpenSearchGrpc
from opensearchpy.helpers.test import OPENSEARCH_URL
from opensearchpy.helpers.test import OpenSearchTestCase as BaseTestCase

# pylint: disable=invalid-name
CLIENT: Any = None
GRPC_PORT = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
# Derive gRPC host from OPENSEARCH_URL so it works inside Docker containers
_parsed = urlparse(OPENSEARCH_URL)
GRPC_HOST = os.environ.get("OPENSEARCH_GRPC_HOST", _parsed.hostname or "localhost")


def _grpc_available() -> bool:
    """Check if gRPC port is reachable."""
    try:
        channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
        grpc.channel_ready_future(channel).result(timeout=2)
        channel.close()
        return True
    except Exception:
        return False


def get_client(**kwargs: Any) -> Any:
    global CLIENT
    if CLIENT is False:
        raise SkipTest("No gRPC client is available")
    if CLIENT is not None and not kwargs:
        return CLIENT

    if not _grpc_available():
        CLIENT = False
        raise SkipTest(f"gRPC server not available on {GRPC_HOST}:{GRPC_PORT}")

    try:
        # Get OPENSEARCH_URL for REST host
        from opensearchpy.helpers.test import OPENSEARCH_URL

        kw = {"timeout": 30}
        kw.update(kwargs)
        new_client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            **kw,
        )
        # Verify REST is healthy
        new_client.cluster.health(wait_for_status="yellow")
    except SkipTest:
        CLIENT = False
        raise

    if not kwargs:
        CLIENT = new_client

    return new_client


def setup_module() -> None:
    get_client()


class OpenSearchGrpcTestCase(BaseTestCase):
    """
    Integration test case for gRPC transport.

    Inherits teardown from BaseTestCase (deletes all indices after each test).
    Client uses grpc=True so bulk operations go over gRPC automatically.
    All other operations fall back to REST.
    """

    @staticmethod
    def _get_client(**kwargs: Any) -> Any:
        return get_client(**kwargs)
