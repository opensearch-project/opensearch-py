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

from typing import Literal, TypeAlias, TypedDict

from typing_extensions import NotRequired


class ResourceLimits(TypedDict):
    memory: float
    cpu: NotRequired[float]


class ResourceLimitsModel(TypedDict):
    memory: NotRequired[float]
    cpu: float


class ResourceLimitsModel1(TypedDict):
    memory: float
    cpu: NotRequired[float]


class ResourceLimitsModel2(TypedDict):
    memory: NotRequired[float]
    cpu: float


FieldCommonResiliencyMode: TypeAlias = Literal["enforced", "monitor", "soft"]


class FieldCommonResourceLimitsSchema(TypedDict):
    memory: NotRequired[float]
    cpu: NotRequired[float]


class FieldCommonQueryGroupCreate(TypedDict):
    name: str
    resiliency_mode: FieldCommonResiliencyMode
    resource_limits: ResourceLimits | ResourceLimitsModel


class FieldCommonQueryGroupResponse(TypedDict):
    field_id: str
    name: str
    resiliency_mode: FieldCommonResiliencyMode
    updated_at: int
    resource_limits: ResourceLimitsModel1 | ResourceLimitsModel2


class FieldCommonQueryGroupUpdate(TypedDict):
    resiliency_mode: NotRequired[FieldCommonResiliencyMode]
    resource_limits: NotRequired[FieldCommonResourceLimitsSchema]
