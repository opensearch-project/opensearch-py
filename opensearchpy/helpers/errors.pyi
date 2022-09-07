# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, List

from ..exceptions import OpenSearchException

class BulkIndexError(OpenSearchException):
    @property
    def errors(self) -> List[Any]: ...

class ScanError(OpenSearchException):
    scroll_id: str
    def __init__(self, scroll_id: str, *args: Any, **kwargs: Any) -> None: ...
