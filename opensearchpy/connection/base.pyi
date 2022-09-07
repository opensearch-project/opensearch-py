# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import logging
from typing import (
    Any,
    AnyStr,
    Collection,
    Dict,
    List,
    Mapping,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Union,
)

logger: logging.Logger
tracer: logging.Logger

class Connection(object):
    headers: Dict[str, str]
    use_ssl: bool
    http_compress: bool
    scheme: str
    hostname: str
    port: Optional[int]
    host: str
    url_prefix: str
    timeout: Optional[Union[float, int]]
    def __init__(
        self,
        host: str = ...,
        port: Optional[int] = ...,
        use_ssl: bool = ...,
        url_prefix: str = ...,
        timeout: Optional[Union[float, int]] = ...,
        headers: Optional[Mapping[str, str]] = ...,
        http_compress: Optional[bool] = ...,
        opaque_id: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def _gzip_compress(self, body: bytes) -> bytes: ...
    def _raise_warnings(self, warning_headers: Sequence[str]) -> None: ...
    def _pretty_json(self, data: Any) -> str: ...
    def _log_trace(
        self,
        method: Any,
        path: Any,
        body: Any,
        status_code: Any,
        response: Any,
        duration: Any,
    ) -> None: ...
    def perform_request(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = ...,
        body: Optional[bytes] = ...,
        timeout: Optional[Union[int, float]] = ...,
        ignore: Collection[int] = ...,
        headers: Optional[Mapping[str, str]] = ...,
    ) -> Tuple[int, Mapping[str, str], str]: ...
    def log_request_success(
        self,
        method: str,
        full_url: str,
        path: str,
        body: Optional[bytes],
        status_code: int,
        response: str,
        duration: float,
    ) -> None: ...
    def log_request_fail(
        self,
        method: str,
        full_url: str,
        path: str,
        body: Optional[bytes],
        duration: float,
        status_code: Optional[int] = ...,
        response: Optional[str] = ...,
        exception: Optional[Exception] = ...,
    ) -> None: ...
    def _raise_error(
        self, status_code: int, raw_data: str, content_type: Optional[str]
    ) -> NoReturn: ...
    def _get_default_user_agent(self) -> str: ...
