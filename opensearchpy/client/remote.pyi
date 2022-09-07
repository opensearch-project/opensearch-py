# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Collection, MutableMapping, Optional, Tuple, Union

from .utils import NamespacedClient

class RemoteClient(NamespacedClient):
    def info(
        self,
        *,
        timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        human: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        format: Optional[str] = None,
        filter_path: Optional[Union[str, Collection[str]]] = None,
        http_auth: Optional[Union[str, Tuple[str, str]]] = ...,
        api_key: Optional[Union[str, Tuple[str, str]]] = ...,
        params: Optional[MutableMapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
    ) -> Any: ...
