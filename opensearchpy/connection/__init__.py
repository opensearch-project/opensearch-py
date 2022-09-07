# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from .base import Connection
from .http_requests import RequestsHttpConnection
from .http_urllib3 import Urllib3HttpConnection, create_ssl_context

__all__ = [
    "Connection",
    "RequestsHttpConnection",
    "Urllib3HttpConnection",
    "create_ssl_context",
]
