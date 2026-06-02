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

from ._internal import (
    FieldCommonDateTime,
    FieldCommonEpochTimeUnitMillis,
    FieldCommonIds,
)


class ListDanglingIndicesDanglingIndex(TypedDict):
    index_name: str
    index_uuid: str
    creation_date: NotRequired[FieldCommonDateTime]
    creation_date_millis: FieldCommonEpochTimeUnitMillis
    node_ids: FieldCommonIds
