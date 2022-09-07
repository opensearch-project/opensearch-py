# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import ssl
from typing import Any, Mapping, Optional, Union

import urllib3

from .base import Connection

def create_ssl_context(
    cafile: Any = ...,
    capath: Any = ...,
    cadata: Any = ...,
) -> ssl.SSLContext: ...

class Urllib3HttpConnection(Connection):
    pool: urllib3.HTTPConnectionPool
    def __init__(
        self,
        host: str = ...,
        port: Optional[int] = ...,
        url_prefix: str = ...,
        timeout: Optional[Union[float, int]] = ...,
        http_auth: Any = ...,
        use_ssl: bool = ...,
        verify_certs: bool = ...,
        ssl_show_warn: bool = ...,
        ca_certs: Optional[Any] = ...,
        client_cert: Optional[Any] = ...,
        client_key: Optional[Any] = ...,
        ssl_version: Optional[Any] = ...,
        ssl_assert_hostname: Optional[Any] = ...,
        ssl_assert_fingerprint: Optional[Any] = ...,
        maxsize: int = ...,
        headers: Optional[Mapping[str, str]] = ...,
        ssl_context: Optional[Any] = ...,
        http_compress: Optional[bool] = ...,
        opaque_id: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
