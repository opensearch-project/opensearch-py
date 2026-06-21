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


class FieldCommonPostQuerySetsRequest(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    sampling: NotRequired[str]
    querySetSize: NotRequired[int]


class FieldCommonPostQuerySetsResponse(TypedDict):
    query_set_id: NotRequired[str]
    query_set_result: NotRequired[str]


class FieldCommonPostScheduledExperimentsRequest(TypedDict):
    experimentId: NotRequired[str]
    cronExpression: NotRequired[str]


class FieldCommonPostScheduledExperimentsResponse(TypedDict):
    job_id: NotRequired[str]
    job_result: NotRequired[str]


class FieldCommonPutExperimentResponse(TypedDict):
    experiment_id: NotRequired[str]
    experiment_result: NotRequired[str]


class FieldCommonPutHybridOptimizerExperimentRequest(TypedDict):
    querySetId: NotRequired[str]
    searchConfigurationList: NotRequired[list[str]]
    judgmentList: NotRequired[list[str]]
    size: NotRequired[int]
    type: NotRequired[str]


class FieldCommonPutImportJudgmentsRequest(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    type: NotRequired[str]
    judgmentRatings: NotRequired[list[dict[str, Any]]]


class FieldCommonPutJudgmentsResponse(TypedDict):
    judgment_id: NotRequired[str]


class FieldCommonPutLLMJudgmentsRequest(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    type: NotRequired[str]
    modelId: NotRequired[str]
    querySetId: NotRequired[str]
    searchConfigurationList: NotRequired[list[str]]
    size: NotRequired[int]
    ignoreFailure: NotRequired[bool]
    contextFields: NotRequired[list[str]]


class FieldCommonPutPairwiseExperimentRequest(TypedDict):
    querySetId: NotRequired[str]
    searchConfigurationList: NotRequired[list[str]]
    size: NotRequired[int]
    type: NotRequired[str]


class FieldCommonPutPointwiseExperimentRequest(TypedDict):
    querySetId: NotRequired[str]
    searchConfigurationList: NotRequired[list[str]]
    judgmentList: NotRequired[list[str]]
    size: NotRequired[int]
    type: NotRequired[str]


class FieldCommonPutQuerySetsRequest(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    sampling: NotRequired[str]
    querySetQueries: NotRequired[list[dict[str, Any]]]


class FieldCommonPutQuerySetsResponse(TypedDict):
    query_set_id: NotRequired[str]
    query_set_result: NotRequired[str]


class FieldCommonPutSearchConfigurationRequest(TypedDict):
    name: NotRequired[str]
    index: NotRequired[str]
    query: NotRequired[str]
    searchPipeline: NotRequired[str]


class FieldCommonPutSearchConfigurationResponse(TypedDict):
    search_configuration_id: NotRequired[str]
    search_configuration_result: NotRequired[str]


class FieldCommonPutUBIJudgmentsRequest(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    type: NotRequired[str]
    clickModel: NotRequired[str]
    maxRank: NotRequired[int]
