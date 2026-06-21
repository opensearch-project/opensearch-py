# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""Map OpenSearch API schema keys to datamodel-codegen TypedDict class names."""

from __future__ import annotations


def schema_key_to_type_name(schema_key: str) -> str:
    """
    Convert an OpenSearch components/schemas key to the Python TypedDict name
    produced by datamodel-code-generator from the bundled OpenAPI document.

    Examples:
        _core.search___SearchResponse -> SearchSearchResponse
        _common___Id -> FieldCommonId
        _common.query_dsl___QueryContainer -> QueryDslQueryContainer
        SearchRequestBody -> SearchRequestBody
    """
    if "___" not in schema_key:
        return schema_key

    namespace, name = schema_key.split("___", 1)
    if namespace.startswith("_common.query_dsl"):
        return f"QueryDsl{name}"
    if namespace.startswith("_common"):
        return f"FieldCommon{name}"
    if "." in namespace:
        short = namespace.split(".")[-1]
        return f"{short.capitalize()}{name}"
    return name


def schema_ref_to_key(schema_ref: str) -> str | None:
    """Extract the components/schemas key from a JSON pointer ref."""
    prefix = "#/components/schemas/"
    if schema_ref.startswith(prefix):
        return schema_ref[len(prefix) :]
    return None
