# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy import helpers
from opensearchpy._async.helpers.actions import async_bulk, async_streaming_bulk
from opensearchpy.serializer import JSONSerializer

pytestmark: MarkDecorator = pytest.mark.asyncio

DOCS: Any = [{"resource": "ok"}, {"resource": {"resourceId": "i-1"}}]


def bulk_response() -> Any:
    """
    A fresh bulk response for two index actions, the second of which the server
    failed to parse. A new object per call because the helpers consume it with
    ``popitem()``.
    """
    return {
        "errors": True,
        "items": [
            {"index": {"_index": "test-index", "_id": "1", "status": 201}},
            {
                "index": {
                    "_index": "test-index",
                    "_id": "2",
                    "status": 400,
                    "error": {
                        "type": "mapper_parsing_exception",
                        "reason": "failed to parse field [resource]",
                    },
                }
            },
        ],
    }


def mock_client() -> Any:
    """
    An AsyncOpenSearch-like mock whose bulk() returns ``bulk_response()``.
    """
    client = Mock()
    client.transport.serializer = JSONSerializer()
    client.bulk = AsyncMock(side_effect=lambda *args, **kwargs: bulk_response())
    return client


async def test_failed_action_source_is_yielded_when_opted_in() -> None:
    results = [
        result
        async for result in async_streaming_bulk(
            mock_client(),
            list(DOCS),
            raise_on_error=False,
            yield_failed_action_source=True,
        )
    ]

    assert [ok for ok, _ in results] == [True, False]
    assert "data" not in results[0][1]["index"]
    assert results[1][1]["index"]["data"] == {"resource": {"resourceId": "i-1"}}


async def test_failed_action_source_is_not_yielded_by_default() -> None:
    results = [
        result
        async for result in async_streaming_bulk(
            mock_client(), list(DOCS), raise_on_error=False
        )
    ]

    assert [ok for ok, _ in results] == [True, False]
    for _, item in results:
        assert "data" not in item["index"]


async def test_raise_on_error_payload_is_unchanged() -> None:
    with pytest.raises(helpers.BulkIndexError) as excinfo:
        [result async for result in async_streaming_bulk(mock_client(), list(DOCS))]

    errors = excinfo.value.errors
    assert len(errors) == 1
    assert errors[0]["index"]["_id"] == "2"
    assert errors[0]["index"]["data"] == {"resource": {"resourceId": "i-1"}}


async def test_async_bulk_errors_carry_the_source() -> None:
    success, errors = await async_bulk(
        mock_client(),
        list(DOCS),
        raise_on_error=False,
        yield_failed_action_source=True,
    )

    assert success == 1
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert errors[0]["index"]["data"] == {"resource": {"resourceId": "i-1"}}
