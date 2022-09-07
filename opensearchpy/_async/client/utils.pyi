# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from ...client.utils import SKIP_IN_PATH as SKIP_IN_PATH
from ...client.utils import _bulk_body as _bulk_body
from ...client.utils import _escape as _escape
from ...client.utils import _make_path as _make_path  # noqa
from ...client.utils import _normalize_hosts as _normalize_hosts
from ...client.utils import query_params as query_params
from ..client import AsyncOpenSearch
from ..transport import AsyncTransport

class NamespacedClient:
    client: AsyncOpenSearch
    def __init__(self, client: AsyncOpenSearch) -> None: ...
    @property
    def transport(self) -> AsyncTransport: ...
