# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import sys
from typing import Tuple

from .client import OpenSearch as OpenSearch
from .connection import Connection as Connection
from .connection import RequestsHttpConnection as RequestsHttpConnection
from .connection import Urllib3HttpConnection as Urllib3HttpConnection
from .connection_pool import ConnectionPool as ConnectionPool
from .connection_pool import ConnectionSelector as ConnectionSelector
from .connection_pool import RoundRobinSelector as RoundRobinSelector
from .exceptions import AuthenticationException as AuthenticationException
from .exceptions import AuthorizationException as AuthorizationException
from .exceptions import ConflictError as ConflictError
from .exceptions import ConnectionError as ConnectionError
from .exceptions import ConnectionTimeout as ConnectionTimeout
from .exceptions import ImproperlyConfigured as ImproperlyConfigured
from .exceptions import NotFoundError as NotFoundError
from .exceptions import OpenSearchDeprecationWarning as OpenSearchDeprecationWarning
from .exceptions import OpenSearchException as OpenSearchException
from .exceptions import RequestError as RequestError
from .exceptions import SerializationError as SerializationError
from .exceptions import SSLError as SSLError
from .exceptions import TransportError as TransportError
from .serializer import JSONSerializer as JSONSerializer
from .transport import Transport as Transport

try:
    if sys.version_info < (3, 6):
        raise ImportError

    from ._async.client import AsyncOpenSearch as AsyncOpenSearch
    from ._async.http_aiohttp import AIOHttpConnection as AIOHttpConnection
    from ._async.transport import AsyncTransport as AsyncTransport
    from .helpers import AWSV4SignerAuth as AWSV4SignerAuth
except (ImportError, SyntaxError):
    pass

VERSION: Tuple[int, int, int]
__version__: Tuple[int, int, int]
__versionstr__: str
