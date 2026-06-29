# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
test_translation — Integration tests for the gRPC translation layer.

Uses OpenSearchGrpcTestCase for tests that require a running server.
Skips gracefully when gRPC is not available.
"""

import os
from typing import Any
from unittest import SkipTest

import grpc

from opensearchpy import OpenSearchGrpc
from opensearchpy.helpers.test import OpenSearchTestCase as BaseTestCase
from opensearchpy.helpers.test import OPENSEARCH_URL

# pylint: disable=invalid-name
CLIENT: Any = None
GRPC_PORT = int(os.environ.get("OPENSEARCH_GRPC_PORT", "9400"))
GRPC_HOST = os.environ.get("OPENSEARCH_GRPC_HOST", "localhost")


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
        kw = {"timeout": 30}
        kw.update(kwargs)
        new_client = OpenSearchGrpc(
            hosts=[OPENSEARCH_URL],
            grpc_hosts=[{"host": GRPC_HOST, "port": GRPC_PORT}],
            **kw,
        )
        new_client.cluster.health(wait_for_status="yellow")
    except Exception:
        CLIENT = False
        raise SkipTest("OpenSearch server not available")

    if not kwargs:
        CLIENT = new_client

    return new_client


def setup_module() -> None:
    get_client()


class OpenSearchGrpcTestCase(BaseTestCase):
    """
    Integration test case for gRPC translation layer tests.

    Inherits teardown from BaseTestCase (deletes all indices after each test).
    Client uses OpenSearchGrpc so bulk operations go over gRPC.
    """

    @staticmethod
    def _get_client(**kwargs: Any) -> Any:
        return get_client(**kwargs)
