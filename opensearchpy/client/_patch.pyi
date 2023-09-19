# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
from typing import Any, Collection, MutableMapping, Optional, Tuple, Type, Union

def list_all_point_in_time(
    *,
    pretty: Optional[bool] = ...,
    human: Optional[bool] = ...,
    error_trace: Optional[bool] = ...,
    format: Optional[str] = ...,
    filter_path: Optional[Union[str, Collection[str]]] = ...,
    request_timeout: Optional[Union[int, float]] = ...,
    ignore: Optional[Union[int, Collection[int]]] = ...,
    opaque_id: Optional[str] = ...,
    http_auth: Optional[Union[str, Tuple[str, str]]] = ...,
    api_key: Optional[Union[str, Tuple[str, str]]] = ...,
    params: Optional[MutableMapping[str, Any]] = ...,
    headers: Optional[MutableMapping[str, str]] = ...,
) -> Any: ...
def create_point_in_time(
    *,
    index: Optional[Any] = ...,
    expand_wildcards: Optional[Any] = ...,
    ignore_unavailable: Optional[Any] = ...,
    keep_alive: Optional[Any] = ...,
    preference: Optional[Any] = ...,
    routing: Optional[Any] = ...,
    pretty: Optional[bool] = ...,
    human: Optional[bool] = ...,
    error_trace: Optional[bool] = ...,
    format: Optional[str] = ...,
    filter_path: Optional[Union[str, Collection[str]]] = ...,
    request_timeout: Optional[Union[int, float]] = ...,
    ignore: Optional[Union[int, Collection[int]]] = ...,
    opaque_id: Optional[str] = ...,
    http_auth: Optional[Union[str, Tuple[str, str]]] = ...,
    api_key: Optional[Union[str, Tuple[str, str]]] = ...,
    params: Optional[MutableMapping[str, Any]] = ...,
    headers: Optional[MutableMapping[str, str]] = ...,
) -> Any: ...
def delete_point_in_time(
    *,
    body: Optional[Any] = ...,
    all: Optional[bool] = ...,
    pretty: Optional[bool] = ...,
    human: Optional[bool] = ...,
    error_trace: Optional[bool] = ...,
    format: Optional[str] = ...,
    filter_path: Optional[Union[str, Collection[str]]] = ...,
    request_timeout: Optional[Union[int, float]] = ...,
    ignore: Optional[Union[int, Collection[int]]] = ...,
    opaque_id: Optional[str] = ...,
    http_auth: Optional[Union[str, Tuple[str, str]]] = ...,
    api_key: Optional[Union[str, Tuple[str, str]]] = ...,
    params: Optional[MutableMapping[str, Any]] = ...,
    headers: Optional[MutableMapping[str, str]] = ...,
) -> Any: ...
def health_check(
    params: Union[Any, None] = ..., headers: Union[Any, None] = ...
) -> Union[bool, Any]: ...
def update_audit_config(
    body: Any, params: Union[Any, None] = ..., headers: Union[Any, None] = ...
) -> Union[bool, Any]: ...
