# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from typing import Any, Optional

from botocore.credentials import Credentials

class AWSV4SignerAsyncAuth:
    @property
    def __init__(self, credentials: Credentials, region: str) -> None: ...
    @property
    def __call__(self, *args: Any, **kwds: Any) -> Any: ...
    @property
    def _sign_request(
        self, method: str, url: str, query_string: Optional[str], body: Optional[str]
    ) -> dict: ...
