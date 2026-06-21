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

from typing import Any, TypedDict

from typing_extensions import NotRequired


class FieldCommonCursor(TypedDict):
    keep_alive: NotRequired[str]


class FieldCommonExplain(TypedDict):
    query: NotRequired[str]
    filter: NotRequired[dict[str, Any]]
    fetch_size: NotRequired[int]


class FieldCommonExplainBody(TypedDict):
    name: NotRequired[str]
    description: NotRequired[dict[str, Any]]
    children: NotRequired[list[FieldCommonExplainBody]]


class FieldCommonExplainResponse(TypedDict):
    root: NotRequired[FieldCommonExplainBody]


class FieldCommonPluginsQuery(TypedDict):
    memory_limit: NotRequired[str]
    size_limit: NotRequired[str | int]


class FieldCommonPpl(TypedDict):
    enabled: NotRequired[bool | str]


class FieldCommonQuery(TypedDict):
    query: NotRequired[str]
    filter: NotRequired[dict[str, Any]]
    fetch_size: NotRequired[int]


class FieldCommonQueryResponse(TypedDict):
    schema: NotRequired[list[dict[str, Any]]]
    datarows: NotRequired[list[list[Any]]]
    cursor: NotRequired[str]
    total: NotRequired[int]
    size: NotRequired[int]
    status: NotRequired[int]


class FieldCommonSql(TypedDict):
    enabled: NotRequired[bool | str]
    slowlog: NotRequired[int | str]
    cursor: NotRequired[FieldCommonCursor]


class FieldCommonSqlClose(TypedDict):
    cursor: NotRequired[str]


class FieldCommonSqlCloseResponse(TypedDict):
    succeeded: NotRequired[bool]


class FieldCommonStats(TypedDict):
    start_time: NotRequired[str]
    end_time: NotRequired[dict[str, Any]]
    cluster_name: NotRequired[dict[str, Any]]
    index: NotRequired[dict[str, Any]]
    query: NotRequired[dict[str, Any]]
    user: NotRequired[dict[str, Any]]
    execution_time: NotRequired[dict[str, Any]]


FieldCommonTransientPlain = TypedDict(
    "FieldCommonTransientPlain",
    {
        "plugins.sql.enabled": NotRequired[bool],
        "plugins.ppl.enabled": NotRequired[bool],
        "plugins.sql.slowlog": NotRequired[int],
        "plugins.sql.cursor.keep_alive": NotRequired[str],
        "plugins.query.memory_limit": NotRequired[str],
        "plugins.query.size_limit": NotRequired[int],
    },
)


class FieldCommonPlugins(TypedDict):
    ppl: NotRequired[FieldCommonPpl]
    query: NotRequired[FieldCommonPluginsQuery]
    sql: NotRequired[FieldCommonSql]


class FieldCommonSqlSettingsPlain(TypedDict):
    transient: NotRequired[FieldCommonTransientPlain]


class FieldCommonTransient(TypedDict):
    plugins: NotRequired[FieldCommonPlugins]


class FieldCommonSqlSettings(TypedDict):
    transient: NotRequired[FieldCommonTransient]


class FieldCommonSqlSettingsResponse(TypedDict):
    acknowledged: NotRequired[bool]
    persistent: NotRequired[dict[str, Any]]
    transient: NotRequired[FieldCommonTransient]
