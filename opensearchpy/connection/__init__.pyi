# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from .base import Connection as Connection
from .http_requests import RequestsHttpConnection as RequestsHttpConnection
from .http_urllib3 import Urllib3HttpConnection as Urllib3HttpConnection
from .http_urllib3 import create_ssl_context as create_ssl_context
