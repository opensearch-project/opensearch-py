# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Dict, Union

class ImproperlyConfigured(Exception): ...
class OpenSearchException(Exception): ...
class SerializationError(OpenSearchException): ...

class TransportError(OpenSearchException):
    @property
    def status_code(self) -> Union[str, int]: ...
    @property
    def error(self) -> str: ...
    @property
    def info(self) -> Union[Dict[str, Any], Exception, Any]: ...
    def __str__(self) -> str: ...

class ConnectionError(TransportError):
    def __str__(self) -> str: ...

class SSLError(ConnectionError): ...

class ConnectionTimeout(ConnectionError):
    def __str__(self) -> str: ...

class NotFoundError(TransportError): ...
class ConflictError(TransportError): ...
class RequestError(TransportError): ...
class AuthenticationException(TransportError): ...
class AuthorizationException(TransportError): ...
class OpenSearchWarning(Warning): ...

OpenSearchDeprecationWarning = OpenSearchWarning

HTTP_EXCEPTIONS: Dict[int, OpenSearchException]
