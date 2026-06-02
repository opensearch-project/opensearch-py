# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""Type-check OpenSearch search API request/response TypedDicts."""

from __future__ import annotations

from typing import Any

from opensearchpy import OpenSearch
from opensearchpy._types._internal import SearchRequestBody, SearchSearchResponse

client = OpenSearch([{"host": "localhost", "port": 9200}])

request: SearchRequestBody = {
    "query": {"match_all": {}},
    "size": 10,
}

response: SearchSearchResponse = client.search(body=request)

took: int = response["took"]
hit_count: int = len(response["hits"]["hits"])
first_source: dict[str, Any] = response["hits"]["hits"][0].get("field_source", {})
