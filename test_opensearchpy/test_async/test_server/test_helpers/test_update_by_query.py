# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy._async.helpers.update_by_query import AsyncUpdateByQuery
from opensearchpy.helpers.search import Q

pytestmark: MarkDecorator = pytest.mark.asyncio


async def test_update_by_query_no_script(write_client, setup_ubq_tests) -> None:
    index = setup_ubq_tests

    ubq = (
        AsyncUpdateByQuery(using=write_client)
        .index(index)
        .filter(~Q("exists", field="is_public"))
    )
    response = await ubq.execute()

    assert response.total == 52
    assert response["took"] > 0
    assert not response.timed_out
    assert response.updated == 52
    assert response.deleted == 0
    assert response.took > 0
    assert response.success()


async def test_update_by_query_with_script(write_client, setup_ubq_tests) -> None:
    index = setup_ubq_tests

    ubq = (
        AsyncUpdateByQuery(using=write_client)
        .index(index)
        .filter(~Q("exists", field="parent_shas"))
        .script(source="ctx._source.is_public = false")
    )
    ubq = ubq.params(conflicts="proceed")

    response = await ubq.execute()
    assert response.total == 2
    assert response.updated == 2
    assert response.version_conflicts == 0


async def test_delete_by_query_with_script(write_client, setup_ubq_tests) -> None:
    index = setup_ubq_tests

    ubq = (
        AsyncUpdateByQuery(using=write_client)
        .index(index)
        .filter(Q("match", parent_shas="1dd19210b5be92b960f7db6f66ae526288edccc3"))
        .script(source='ctx.op = "delete"')
    )
    ubq = ubq.params(conflicts="proceed")

    response = await ubq.execute()

    assert response.total == 1
    assert response.deleted == 1
    assert response.success()
