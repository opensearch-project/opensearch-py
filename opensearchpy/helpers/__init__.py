# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import sys

from .actions import (
    _chunk_actions,
    _process_bulk_chunk,
    bulk,
    expand_action,
    parallel_bulk,
    reindex,
    scan,
    streaming_bulk,
)
from .errors import BulkIndexError, ScanError
from .signer import AWSV4SignerAuth

__all__ = [
    "BulkIndexError",
    "ScanError",
    "expand_action",
    "streaming_bulk",
    "bulk",
    "parallel_bulk",
    "scan",
    "reindex",
    "_chunk_actions",
    "_process_bulk_chunk",
    "AWSV4SignerAuth",
]


try:
    # Asyncio only supported on Python 3.6+
    if sys.version_info < (3, 6):
        raise ImportError

    from .._async.helpers import (
        async_bulk,
        async_reindex,
        async_scan,
        async_streaming_bulk,
    )

    __all__ += ["async_scan", "async_bulk", "async_reindex", "async_streaming_bulk"]
except (ImportError, SyntaxError):
    pass
