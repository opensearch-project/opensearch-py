# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
# ----------------------------------------------------
# THIS CODE IS GENERATED. MANUAL EDITS WILL BE LOST.
# ----------------------------------------------------
# <auto-generated-code>
#  The code was automatically generated using a [Python generator](https://github.com/saimedhi/opensearch-py/blob/Python-Client-Generator/utils/generate-api.py) with the assistance of [ninja templates](https://github.com/saimedhi/opensearch-py/tree/Python-Client-Generator/utils/templates), using [OpenAPI specifications](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) as input.
#  Modifying this file can lead to incorrect behavior and any changes will be overwritten upon code regeneration.
#  To contribute, please make the necessary changes to either the [Python generator](https://github.com/saimedhi/opensearch-py/blob/Python-Client-Generator/utils/generate-api.py) or the [OpenAPI specifications](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) as needed.
# </auto-generated-code>

from typing import Any, Collection, MutableMapping, Optional, Tuple, Union

from .utils import NamespacedClient

class RemoteStoreClient(NamespacedClient):
    async def restore(
        self,
        *,
        body: Any,
        cluster_manager_timeout: Optional[Any] = ...,
        wait_for_completion: Optional[Any] = ...,
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
