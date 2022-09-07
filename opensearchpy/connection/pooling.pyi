# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from .base import Connection

class PoolingConnection(Connection):
    def _make_connection(self) -> Connection: ...
    def _get_connection(self) -> Connection: ...
    def _release_connection(self, con: Connection) -> None: ...
    def close(self) -> None: ...
