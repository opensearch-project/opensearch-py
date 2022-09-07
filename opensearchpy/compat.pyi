# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import sys
from typing import Callable, Tuple, Type, Union

PY2: bool
string_types: Tuple[type, ...]

to_str: Callable[[Union[str, bytes]], str]
to_bytes: Callable[[Union[str, bytes]], bytes]
reraise_exceptions: Tuple[Type[Exception], ...]

if sys.version_info[0] == 2:
    from itertools import imap as map
    from urllib import quote as quote
    from urllib import quote_plus as quote_plus
    from urllib import unquote as unquote
    from urllib import urlencode as urlencode

    from Queue import Queue as Queue
    from urlparse import urlparse as urlparse
else:
    from urllib.parse import quote as quote
    from urllib.parse import quote_plus as quote_plus
    from urllib.parse import unquote as unquote
    from urllib.parse import urlencode as urlencode
    from urllib.parse import urlparse as urlparse

    map = map
    from queue import Queue as Queue
