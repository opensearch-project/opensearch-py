# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_types = (basestring,)  # noqa: F821
    from itertools import imap as map
    from urllib import quote, quote_plus, unquote, urlencode

    from Queue import Queue
    from urlparse import urlparse

    def to_str(x, encoding="ascii"):
        if not isinstance(x, str):
            return x.encode(encoding)
        return x

    to_bytes = to_str

else:
    string_types = str, bytes
    from urllib.parse import quote, quote_plus, unquote, urlencode, urlparse

    map = map
    from queue import Queue

    def to_str(x, encoding="ascii"):
        if not isinstance(x, str):
            return x.decode(encoding)
        return x

    def to_bytes(x, encoding="ascii"):
        if not isinstance(x, bytes):
            return x.encode(encoding)
        return x


try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


try:
    reraise_exceptions = (RecursionError,)
except NameError:
    reraise_exceptions = ()

try:
    import asyncio

    reraise_exceptions += (asyncio.CancelledError,)
except (ImportError, AttributeError):
    pass


__all__ = [
    "string_types",
    "reraise_exceptions",
    "quote_plus",
    "quote",
    "urlencode",
    "unquote",
    "urlparse",
    "map",
    "Queue",
    "Mapping",
]
