# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from ..exceptions import OpenSearchException


class BulkIndexError(OpenSearchException):
    @property
    def errors(self):
        """List of errors from execution of the last chunk."""
        return self.args[1]


class ScanError(OpenSearchException):
    def __init__(self, scroll_id, *args, **kwargs):
        super(ScanError, self).__init__(*args, **kwargs)  # type: ignore
        self.scroll_id = scroll_id
