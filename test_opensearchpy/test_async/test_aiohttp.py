# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
import os
from typing import Type

import pytest
from pytest import MarkDecorator

from opensearchpy import (
    AIOHttpConnection,
    AsyncConnection,
    AsyncHttpConnection,
    AsyncOpenSearch,
)
from opensearchpy._async.helpers.test import get_test_client

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestAIOHttp:

    def test_default(self) -> None:
        client = AsyncOpenSearch()
        assert client.transport.connection_class == AIOHttpConnection
        assert client.transport.pool_maxsize is None

    def test_connection_class(self) -> None:
        client = AsyncOpenSearch(connection_class=AsyncHttpConnection)
        assert client.transport.connection_class == AsyncHttpConnection
        assert client.transport.pool_maxsize is None

    def test_pool_maxsize(self) -> None:
        client = AsyncOpenSearch(connection_class=AsyncHttpConnection, pool_maxsize=42)
        assert client.transport.connection_class == AsyncHttpConnection
        assert client.transport.pool_maxsize == 42

    @pytest.mark.parametrize(  # type: ignore[misc]
        "connection_class", [AIOHttpConnection, AsyncHttpConnection]
    )
    async def test_default_limit(self, connection_class: Type[AsyncConnection]) -> None:
        client = await get_test_client(
            connection_class=connection_class,
            verify_certs=False,
            http_auth=("admin", os.getenv("OPENSEARCH_PASSWORD", "admin")),
        )
        assert isinstance(
            client.transport.connection_pool.connections[0], connection_class
        )
        assert (
            client.transport.connection_pool.connections[0].session.connector.limit  # type: ignore[attr-defined]
            == 10
        )

    @pytest.mark.parametrize(  # type: ignore[misc]
        "connection_class", [AIOHttpConnection, AsyncHttpConnection]
    )
    async def test_custom_limit(self, connection_class: Type[AsyncConnection]) -> None:
        client = await get_test_client(
            connection_class=connection_class,
            verify_certs=False,
            pool_maxsize=42,
            http_auth=("admin", os.getenv("OPENSEARCH_PASSWORD", "admin")),
        )
        assert isinstance(
            client.transport.connection_pool.connections[0], connection_class
        )
        assert (
            client.transport.connection_pool.connections[0].session.connector.limit  # type: ignore[attr-defined]
            == 42
        )
