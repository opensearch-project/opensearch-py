# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Collection, Mapping, Optional, Tuple, Union

from ..connection import Connection
from ._extra_imports import aiohttp  # type: ignore

class AsyncConnection(Connection):
    async def perform_request(  # type: ignore
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = ...,
        body: Optional[bytes] = ...,
        timeout: Optional[Union[int, float]] = ...,
        ignore: Collection[int] = ...,
        headers: Optional[Mapping[str, str]] = ...,
    ) -> Tuple[int, Mapping[str, str], str]: ...
    async def close(self) -> None: ...

class AIOHttpConnection(AsyncConnection):
    session: Optional[aiohttp.ClientSession]
    ssl_assert_fingerprint: Optional[str]
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
        ssl_version: Optional[Any] = ...,
        ssl_assert_fingerprint: Optional[Any] = ...,
        maxsize: int = ...,
        headers: Optional[Mapping[str, str]] = ...,
        ssl_context: Optional[Any] = ...,
        http_compress: Optional[bool] = ...,
        opaque_id: Optional[str] = ...,
        loop: Any = ...,
        **kwargs: Any
    ) -> None: ...
