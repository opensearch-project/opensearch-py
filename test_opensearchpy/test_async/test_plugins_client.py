# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import re
import warnings

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy._async.client import AsyncOpenSearch

pytestmark: MarkDecorator = pytest.mark.asyncio


class TestPluginsClient:
    async def test_plugins_client(self) -> None:
        with warnings.catch_warnings(record=True) as w:
            client = AsyncOpenSearch()
            # testing double-init here
            client.plugins.__init__(client)  # type: ignore # pylint: disable=unnecessary-dunder-call
            assert re.match(
                r"Cannot load `\w+` directly to AsyncOpenSearch as it already exists. Use `AsyncOpenSearch.plugin.\w+` instead.",
                str(w[0].message),
            )
