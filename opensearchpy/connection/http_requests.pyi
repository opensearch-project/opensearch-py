# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Mapping, Optional

import requests

from .base import Connection

class RequestsHttpConnection(Connection):
    session: requests.Session
    def __init__(
        self,
        host: str = ...,
        port: Optional[int] = ...,
        http_auth: Optional[Any] = ...,
        use_ssl: bool = ...,
        verify_certs: bool = ...,
        ssl_show_warn: bool = ...,
        ca_certs: Optional[Any] = ...,
        client_cert: Optional[Any] = ...,
        client_key: Optional[Any] = ...,
        headers: Optional[Mapping[str, str]] = ...,
        http_compress: Optional[bool] = ...,
        opaque_id: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
