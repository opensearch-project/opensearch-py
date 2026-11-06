# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from unittest.mock import AsyncMock, MagicMock

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy._async.helpers.actions import async_scan
from opensearchpy.helpers import ScanError

pytestmark: MarkDecorator = pytest.mark.asyncio


async def test_async_scan_with_missing_shards_key() -> None:
    """
    A response with hits but no '_shards' key must not raise (regression for
    UnboundLocalError referencing shards_successful before assignment).
    """
    client = MagicMock()
    client.search = AsyncMock(
        return_value={"_scroll_id": "dummy_scroll_id", "hits": {"hits": [{"_id": "1"}]}}
    )
    client.scroll = AsyncMock(
        return_value={"_scroll_id": "dummy_scroll_id", "hits": {"hits": []}}
    )
    client.clear_scroll = AsyncMock(return_value={})

    result = [hit async for hit in async_scan(client, query={})]
    assert result == [{"_id": "1"}]


async def test_async_scan_shard_failure_raises_scan_error() -> None:
    """
    A page whose '_shards' report fewer successful than total triggers the
    shard-failure check (which now runs inside the ``if _shards:`` guard).
    """
    client = MagicMock()
    client.search = AsyncMock(
        return_value={
            "_scroll_id": "dummy_scroll_id",
            "_shards": {"successful": 1, "skipped": 0, "total": 5, "failed": 4},
            "hits": {"hits": [{"_id": "1"}]},
        }
    )
    client.clear_scroll = AsyncMock(return_value={})

    with pytest.raises(ScanError):
        [hit async for hit in async_scan(client, query={})]
