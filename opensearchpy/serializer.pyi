# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Dict, Optional

class Serializer(object):
    mimetype: str
    def loads(self, s: str) -> Any: ...
    def dumps(self, data: Any) -> str: ...

class TextSerializer(Serializer):
    mimetype: str
    def loads(self, s: str) -> Any: ...
    def dumps(self, data: Any) -> str: ...

class JSONSerializer(Serializer):
    mimetype: str
    def default(self, data: Any) -> Any: ...
    def loads(self, s: str) -> Any: ...
    def dumps(self, data: Any) -> str: ...

DEFAULT_SERIALIZERS: Dict[str, Serializer]

class Deserializer(object):
    def __init__(
        self,
        serializers: Dict[str, Serializer],
        default_mimetype: str = ...,
    ) -> None: ...
    def loads(self, s: str, mimetype: Optional[str] = ...) -> Any: ...
