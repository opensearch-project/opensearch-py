# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Callable, Collection, Dict, List, Mapping, Optional, Type, Union

from .connection import Connection
from .connection_pool import ConnectionPool
from .serializer import Deserializer, Serializer

def get_host_info(
    node_info: Dict[str, Any], host: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]: ...

class Transport(object):
    DEFAULT_CONNECTION_CLASS: Type[Connection]
    connection_pool: ConnectionPool
    deserializer: Deserializer

    max_retries: int
    retry_on_timeout: bool
    retry_on_status: Collection[int]
    send_get_body_as: str
    serializer: Serializer
    connection_pool_class: Type[ConnectionPool]
    connection_class: Type[Connection]
    kwargs: Any
    hosts: Optional[List[Dict[str, Any]]]
    seed_connections: List[Connection]
    sniffer_timeout: Optional[float]
    sniff_on_start: bool
    sniff_on_connection_fail: bool
    last_sniff: float
    sniff_timeout: Optional[float]
    host_info_callback: Callable[
        [Dict[str, Any], Optional[Dict[str, Any]]], Optional[Dict[str, Any]]
    ]
    def __init__(
        self,
        hosts: Any,
        connection_class: Optional[Type[Any]] = ...,
        connection_pool_class: Type[ConnectionPool] = ...,
        host_info_callback: Callable[
            [Dict[str, Any], Optional[Dict[str, Any]]], Optional[Dict[str, Any]]
        ] = ...,
        sniff_on_start: bool = ...,
        sniffer_timeout: Optional[float] = ...,
        sniff_timeout: float = ...,
        sniff_on_connection_fail: bool = ...,
        serializer: Serializer = ...,
        serializers: Optional[Mapping[str, Serializer]] = ...,
        default_mimetype: str = ...,
        max_retries: int = ...,
        retry_on_status: Collection[int] = ...,
        retry_on_timeout: bool = ...,
        send_get_body_as: str = ...,
        **kwargs: Any
    ) -> None: ...
    def add_connection(self, host: Any) -> None: ...
    def set_connections(self, hosts: Collection[Any]) -> None: ...
    def get_connection(self) -> Connection: ...
    def sniff_hosts(self, initial: bool = ...) -> None: ...
    def mark_dead(self, connection: Connection) -> None: ...
    def perform_request(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]] = ...,
        params: Optional[Mapping[str, Any]] = ...,
        body: Optional[Any] = ...,
    ) -> Union[bool, Any]: ...
    def close(self) -> None: ...
