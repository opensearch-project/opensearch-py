# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from __future__ import unicode_literals

from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from ..client import OpenSearch
from ..serializer import Serializer
from ..transport import Transport

T = TypeVar("T")
SKIP_IN_PATH: Collection[Any]

def _normalize_hosts(
    hosts: Optional[Union[str, Collection[Union[str, Dict[str, Any]]]]]
) -> List[Dict[str, Any]]: ...
def _escape(value: Any) -> str: ...
def _make_path(*parts: Any) -> str: ...

GLOBAL_PARAMS: Tuple[str, ...]

def query_params(
    *es_query_params: str,
) -> Callable[[Callable[..., T]], Callable[..., T]]: ...
def _bulk_body(
    serializer: Serializer, body: Union[str, bytes, Collection[Any]]
) -> str: ...

class NamespacedClient:
    client: OpenSearch
    def __init__(self, client: OpenSearch) -> None: ...
    @property
    def transport(self) -> Transport: ...
