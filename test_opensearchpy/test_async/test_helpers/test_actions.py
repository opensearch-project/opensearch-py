# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, AsyncIterator, Dict, List
from unittest.mock import AsyncMock

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy import AsyncOpenSearch
from opensearchpy._async.helpers.actions import aiter, async_bulk, async_streaming_bulk

pytestmark: MarkDecorator = pytest.mark.asyncio


class AsyncIterableOnly:
    """
    An ``AsyncIterable`` that is not an async iterator: it defines
    ``__aiter__`` but not ``__anext__``.
    """

    def __init__(self, items: List[Any]) -> None:
        self.items = items

    def __aiter__(self) -> AsyncIterator[Any]:
        return self._generate()

    async def _generate(self) -> AsyncIterator[Any]:
        for item in self.items:
            yield item


def _bulk_response(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    body: str = kwargs["body"]
    # one action line and one source line per document
    count = len(body.strip().split("\n")) // 2
    return {"items": [{"index": {"status": 201}} for _ in range(count)]}


def _client() -> AsyncOpenSearch:
    client = AsyncOpenSearch()
    client.bulk = AsyncMock(side_effect=_bulk_response)
    return client


async def test_aiter_returns_the_iterator_of_an_async_iterable() -> None:
    result = [item async for item in aiter(AsyncIterableOnly([1, 2, 3]))]

    assert result == [1, 2, 3]


async def test_aiter_still_handles_iterators_and_plain_iterables() -> None:
    async def generate() -> AsyncIterator[int]:
        yield 1
        yield 2

    assert [item async for item in aiter(generate())] == [1, 2]
    assert [item async for item in aiter([3, 4])] == [3, 4]


async def test_async_streaming_bulk_accepts_an_async_iterable() -> None:
    actions = AsyncIterableOnly([{"_index": "i", "_id": i, "x": i} for i in range(3)])

    results = [item async for item in async_streaming_bulk(_client(), actions)]

    assert [ok for ok, _ in results] == [True, True, True]


async def test_async_bulk_accepts_an_async_iterable() -> None:
    actions = AsyncIterableOnly([{"_index": "i", "_id": i, "x": i} for i in range(3)])

    assert await async_bulk(_client(), actions) == (3, [])
