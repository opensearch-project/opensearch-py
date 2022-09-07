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
    AsyncIterable,
    Callable,
    Collection,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

from ..client import OpenSearch
from ..serializer import Serializer

logger: logging.Logger

def expand_action(data: Any) -> Tuple[Dict[str, Any], Optional[Any]]: ...
def _chunk_actions(
    actions: Any, chunk_size: int, max_chunk_bytes: int, serializer: Serializer
) -> Generator[Any, None, None]: ...
def _process_bulk_chunk(
    client: OpenSearch,
    bulk_actions: Any,
    bulk_data: Any,
    raise_on_exception: bool = ...,
    raise_on_error: bool = ...,
    *args: Any,
    **kwargs: Any
) -> Generator[Tuple[bool, Any], None, None]: ...
def streaming_bulk(
    client: OpenSearch,
    actions: Union[Iterable[Any], AsyncIterable[Any]],
    chunk_size: int = ...,
    max_chunk_bytes: int = ...,
    raise_on_error: bool = ...,
    expand_action_callback: Callable[[Any], Tuple[Dict[str, Any], Optional[Any]]] = ...,
    raise_on_exception: bool = ...,
    max_retries: int = ...,
    initial_backoff: Union[float, int] = ...,
    max_backoff: Union[float, int] = ...,
    yield_ok: bool = ...,
    ignore_status: Optional[Union[int, Collection[int]]] = ...,
    *args: Any,
    **kwargs: Any
) -> Generator[Tuple[bool, Any], None, None]: ...
def bulk(
    client: OpenSearch,
    actions: Iterable[Any],
    stats_only: bool = ...,
    ignore_status: Optional[Union[int, Collection[int]]] = ...,
    *args: Any,
    **kwargs: Any
) -> Tuple[int, Union[int, List[Any]]]: ...
def parallel_bulk(
    client: OpenSearch,
    actions: Iterable[Any],
    thread_count: int = ...,
    chunk_size: int = ...,
    max_chunk_bytes: int = ...,
    queue_size: int = ...,
    expand_action_callback: Callable[[Any], Tuple[Dict[str, Any], Optional[Any]]] = ...,
    ignore_status: Optional[Union[int, Collection[int]]] = ...,
    *args: Any,
    **kwargs: Any
) -> Generator[Tuple[bool, Any], None, None]: ...
def scan(
    client: OpenSearch,
    query: Optional[Any] = ...,
    scroll: str = ...,
    raise_on_error: bool = ...,
    preserve_order: bool = ...,
    size: int = ...,
    request_timeout: Optional[Union[float, int]] = ...,
    clear_scroll: bool = ...,
    scroll_kwargs: Optional[Mapping[str, Any]] = ...,
    **kwargs: Any
) -> Generator[Any, None, None]: ...
def reindex(
    client: OpenSearch,
    source_index: Union[str, Collection[str]],
    target_index: str,
    query: Any = ...,
    target_client: Optional[OpenSearch] = ...,
    chunk_size: int = ...,
    scroll: str = ...,
    scan_kwargs: Optional[Mapping[str, Any]] = ...,
    bulk_kwargs: Optional[Mapping[str, Any]] = ...,
) -> Tuple[int, Union[int, List[Any]]]: ...
