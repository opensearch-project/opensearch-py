# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

# ------------------------------------------------------------------------------------------
# THIS CODE IS AUTOMATICALLY GENERATED AND MANUAL EDITS WILL BE LOST
#
# To contribute, kindly make modifications in the opensearch-py client generator
# or in the OpenSearch API specification, and run `nox -rs generate`. See DEVELOPER_GUIDE.md
# and https://github.com/opensearch-project/opensearch-api-specification for details.
# -----------------------------------------------------------------------------------------+

from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired


class FieldCommonRemoteStoreRestoreShardsInfo(TypedDict):
    total: NotRequired[int]
    failed: NotRequired[int]
    successful: NotRequired[int]


class FieldCommonRemoteStoreRestoreInfo(TypedDict):
    snapshot: NotRequired[str]
    indices: NotRequired[list[str]]
    shards: NotRequired[FieldCommonRemoteStoreRestoreShardsInfo]
