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

from ._internal import QueryDslQueryContainer


class FieldCommonAgenticContextResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    agent_steps_summary: NotRequired[bool]
    dsl_query: NotRequired[bool]


class FieldCommonAgenticQueryTranslatorRequestProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    agent_id: str


class FieldCommonCollapseResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    field: str
    context_prefix: NotRequired[str]


class FieldCommonMLOpenSearchReranker(TypedDict):
    model_id: str


FieldCommonNeuralFieldMap: TypeAlias = dict[str, str]


class FieldCommonNeuralQueryEnricherRequestProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    default_model_id: NotRequired[str]
    neural_field_default_id: NotRequired[FieldCommonNeuralFieldMap]


class FieldCommonOversampleRequestProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    sample_factor: float
    content_prefix: NotRequired[str]


class FieldCommonPersonalizeSearchRankingResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    campaign_arn: str
    recipe: str
    weight: float
    item_id_field: NotRequired[str]
    iam_role_arn: NotRequired[str]


class FieldCommonRenameFieldResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    field: str
    target_field: str


class FieldCommonRequestProcessor(TypedDict):
    agentic_query_translator: FieldCommonAgenticQueryTranslatorRequestProcessor


class FieldCommonRequestProcessorModel(TypedDict):
    neural_query_enricher: FieldCommonNeuralQueryEnricherRequestProcessor


class FieldCommonRequestProcessorModel1(TypedDict):
    oversample: FieldCommonOversampleRequestProcessor


class FieldCommonRerankContext(TypedDict):
    document_fields: list[str]


class FieldCommonRerankResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    ml_opensearch: NotRequired[FieldCommonMLOpenSearchReranker]
    context: NotRequired[FieldCommonRerankContext]


class FieldCommonResponseProcessor(TypedDict):
    agentic_context: FieldCommonAgenticContextResponseProcessor


class FieldCommonResponseProcessorModel(TypedDict):
    personalize_search_ranking: FieldCommonPersonalizeSearchRankingResponseProcessor


class FieldCommonResponseProcessorModel1(TypedDict):
    rename_field: FieldCommonRenameFieldResponseProcessor


class FieldCommonResponseProcessorModel2(TypedDict):
    rerank: FieldCommonRerankResponseProcessor


class FieldCommonResponseProcessorModel3(TypedDict):
    collapse: FieldCommonCollapseResponseProcessor


class FieldCommonRetrievalAugmentedGenerationResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    model_id: str
    context_field_list: list[str]
    system_prompt: NotRequired[str]
    user_instructions: NotRequired[str]


class FieldCommonScoreCombinationParameters(TypedDict):
    weights: NotRequired[list[float]]


FieldCommonScoreCombinationTechnique: TypeAlias = Literal[
    "arithmetic_mean", "geometric_mean", "harmonic_mean"
]


FieldCommonScoreNormalizationTechnique: TypeAlias = Literal["l2", "min_max"]


FieldCommonScoreRankerCombinationTechnique: TypeAlias = Literal["rrf"]


class FieldCommonSearchScriptRequestProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    source: str
    lang: NotRequired[str]


class FieldCommonSortResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    field: str
    order: NotRequired[str]
    target_field: NotRequired[str]


class FieldCommonSplitResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    field: str
    separator: str
    preserve_trailing: NotRequired[bool]
    target_field: NotRequired[str]


class FieldCommonTruncateHitsResponseProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    target_size: NotRequired[int]
    context_prefix: NotRequired[str]


class FieldCommonRequestProcessorModel2(TypedDict):
    script: FieldCommonSearchScriptRequestProcessor


class FieldCommonResponseProcessorModel4(TypedDict):
    retrieval_augmented_generation: (
        FieldCommonRetrievalAugmentedGenerationResponseProcessor
    )


class FieldCommonResponseProcessorModel5(TypedDict):
    truncate_hits: FieldCommonTruncateHitsResponseProcessor


class FieldCommonResponseProcessorModel6(TypedDict):
    sort: FieldCommonSortResponseProcessor


class FieldCommonResponseProcessorModel7(TypedDict):
    split: FieldCommonSplitResponseProcessor


FieldCommonResponseProcessorModel8: TypeAlias = (
    FieldCommonResponseProcessor
    | FieldCommonResponseProcessorModel
    | FieldCommonResponseProcessorModel4
    | FieldCommonResponseProcessorModel1
    | FieldCommonResponseProcessorModel2
    | FieldCommonResponseProcessorModel3
    | FieldCommonResponseProcessorModel5
    | FieldCommonResponseProcessorModel6
    | FieldCommonResponseProcessorModel7
)


class FieldCommonScoreCombination(TypedDict):
    technique: NotRequired[FieldCommonScoreCombinationTechnique]
    parameters: NotRequired[FieldCommonScoreCombinationParameters]


class FieldCommonScoreNormalization(TypedDict):
    technique: NotRequired[FieldCommonScoreNormalizationTechnique]


class FieldCommonScoreRankerCombination(TypedDict):
    technique: FieldCommonScoreRankerCombinationTechnique
    rank_constant: NotRequired[int]


class FieldCommonScoreRankerPhaseResultsProcessor(TypedDict):
    combination: FieldCommonScoreRankerCombination


class FieldCommonNormalizationPhaseResultsProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    normalization: NotRequired[FieldCommonScoreNormalization]
    combination: NotRequired[FieldCommonScoreCombination]


FieldCommonPhaseResultsProcessor = TypedDict(
    "FieldCommonPhaseResultsProcessor",
    {
        "normalization-processor": FieldCommonNormalizationPhaseResultsProcessor,
    },
)


FieldCommonPhaseResultsProcessorModel = TypedDict(
    "FieldCommonPhaseResultsProcessorModel",
    {
        "score-ranker-processor": FieldCommonScoreRankerPhaseResultsProcessor,
    },
)


FieldCommonPhaseResultsProcessorModel1: TypeAlias = (
    FieldCommonPhaseResultsProcessor | FieldCommonPhaseResultsProcessorModel
)


class FieldCommonFilterQueryRequestProcessor(TypedDict):
    tag: NotRequired[str]
    description: NotRequired[str]
    ignore_failure: NotRequired[bool]
    query: NotRequired[QueryDslQueryContainer]


class FieldCommonRequestProcessorModel3(TypedDict):
    filter_query: FieldCommonFilterQueryRequestProcessor


FieldCommonRequestProcessorModel4: TypeAlias = (
    FieldCommonRequestProcessor
    | FieldCommonRequestProcessorModel3
    | FieldCommonRequestProcessorModel
    | FieldCommonRequestProcessorModel2
    | FieldCommonRequestProcessorModel1
)


FieldCommonSearchPipelineMap: TypeAlias = dict[
    str, "FieldCommonSearchPipelineStructure"
]


class FieldCommonSearchPipelineStructure(TypedDict):
    description: NotRequired[str]
    version: NotRequired[int]
    request_processors: NotRequired[list[FieldCommonRequestProcessorModel4]]
    response_processors: NotRequired[list[FieldCommonResponseProcessorModel8]]
    phase_results_processors: NotRequired[list[FieldCommonPhaseResultsProcessorModel1]]
