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

from .nodes import FieldCommonNodesResponseBase

FieldCommonNeuralStatName: TypeAlias = Literal[
    "cluster_version",
    "comb_arithmetic_executions",
    "comb_arithmetic_processors",
    "comb_geometric_executions",
    "comb_geometric_processors",
    "comb_harmonic_executions",
    "comb_harmonic_processors",
    "comb_rrf_executions",
    "comb_rrf_processors",
    "hybrid_query_requests",
    "hybrid_query_with_filter_requests",
    "hybrid_query_with_inner_hits_requests",
    "hybrid_query_with_pagination_requests",
    "neural_query_against_knn_requests",
    "neural_query_against_semantic_dense_requests",
    "neural_query_against_semantic_sparse_requests",
    "neural_query_enricher_executions",
    "neural_query_enricher_processors",
    "neural_query_requests",
    "neural_sparse_query_requests",
    "neural_sparse_two_phase_executions",
    "neural_sparse_two_phase_processors",
    "norm_l2_executions",
    "norm_l2_processors",
    "norm_minmax_executions",
    "norm_minmax_processors",
    "norm_zscore_executions",
    "norm_zscore_processors",
    "normalization_processor_executions",
    "normalization_processors",
    "rank_based_normalization_processor_executions",
    "rank_based_normalization_processors",
    "rerank_by_field_executions",
    "rerank_by_field_processors",
    "rerank_ml_executions",
    "rerank_ml_processors",
    "semantic_field_chunking_executions",
    "semantic_field_executions",
    "semantic_highlighting_request_count",
    "skip_existing_executions",
    "skip_existing_processors",
    "sparse_encoding_executions",
    "sparse_encoding_processors",
    "text_chunking_delimiter_executions",
    "text_chunking_delimiter_processors",
    "text_chunking_executions",
    "text_chunking_fixed_char_length_executions",
    "text_chunking_fixed_char_length_processors",
    "text_chunking_fixed_token_length_executions",
    "text_chunking_fixed_token_length_processors",
    "text_chunking_processors",
    "text_embedding_executions",
    "text_embedding_processors_in_pipelines",
    "text_image_embedding_executions",
    "text_image_embedding_processors",
]


class FieldCommonStatMetadata(TypedDict):
    value: int | str
    stat_type: str


class FieldCommonTimestampedEventCounterStat(FieldCommonStatMetadata):
    stat_type: NotRequired[Literal["timestamped_event_counter"]]
    trailing_interval_value: NotRequired[int]
    minutes_since_last_event: NotRequired[int]


FieldCommonTimestampedEventCounterStatModel: TypeAlias = (
    int | FieldCommonTimestampedEventCounterStat
)


FieldCommonFlatNeuralNodeStats = TypedDict(
    "FieldCommonFlatNeuralNodeStats",
    {
        "processors.ingest.text_embedding_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.text_chunking_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.text_chunking_delimiter_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.text_chunking_fixed_token_length_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.text_chunking_fixed_char_length_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.semantic_field_chunking_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.sparse_encoding_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.text_image_embedding_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.skip_existing_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.ingest.semantic_field_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.normalization_processor_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.norm_l2_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.norm_minmax_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.norm_zscore_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.rank_based_normalization_processor_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.comb_geometric_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.comb_rrf_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.comb_harmonic_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.hybrid.comb_arithmetic_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.rerank_ml_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.rerank_by_field_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.neural_sparse_two_phase_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "processors.search.neural_query_enricher_executions": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.hybrid.hybrid_query_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.hybrid.hybrid_query_with_pagination_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.hybrid.hybrid_query_with_filter_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.hybrid.hybrid_query_with_inner_hits_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.neural.neural_query_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.neural.neural_query_against_semantic_sparse_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.neural.neural_query_against_semantic_dense_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.neural.neural_query_against_knn_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "query.neural_sparse.neural_sparse_query_requests": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
        "semantic_highlighting.semantic_highlighting_request_count": NotRequired[
            FieldCommonTimestampedEventCounterStatModel
        ],
    },
)


class FieldCommonInfoCounterStat(FieldCommonStatMetadata):
    stat_type: NotRequired[Literal["info_counter"]]


FieldCommonInfoCounterStatModel: TypeAlias = int | FieldCommonInfoCounterStat


class FieldCommonInfoStringStat(FieldCommonStatMetadata):
    stat_type: NotRequired[Literal["info_string"]]


FieldCommonInfoStringStatModel: TypeAlias = str | FieldCommonInfoStringStat


class FieldCommonNestedNeuralInfoStatsProcessorsIngest(TypedDict):
    text_embedding_processors_in_pipelines: NotRequired[FieldCommonInfoCounterStatModel]
    text_chunking_processors: NotRequired[FieldCommonInfoCounterStatModel]
    text_chunking_delimiter_processors: NotRequired[FieldCommonInfoCounterStatModel]
    text_chunking_fixed_token_length_processors: NotRequired[
        FieldCommonInfoCounterStatModel
    ]
    text_chunking_fixed_char_length_processors: NotRequired[
        FieldCommonInfoCounterStatModel
    ]
    sparse_encoding_processors: NotRequired[FieldCommonInfoCounterStatModel]
    text_image_embedding_processors: NotRequired[FieldCommonInfoCounterStatModel]
    skip_existing_processors: NotRequired[FieldCommonInfoCounterStatModel]


class FieldCommonNestedNeuralInfoStatsProcessorsSearchHybrid(TypedDict):
    normalization_processors: NotRequired[FieldCommonInfoCounterStatModel]
    norm_l2_processors: NotRequired[FieldCommonInfoCounterStatModel]
    norm_minmax_processors: NotRequired[FieldCommonInfoCounterStatModel]
    norm_zscore_processors: NotRequired[FieldCommonInfoCounterStatModel]
    rank_based_normalization_processors: NotRequired[FieldCommonInfoCounterStatModel]
    comb_geometric_processors: NotRequired[FieldCommonInfoCounterStatModel]
    comb_rrf_processors: NotRequired[FieldCommonInfoCounterStatModel]
    comb_harmonic_processors: NotRequired[FieldCommonInfoCounterStatModel]
    comb_arithmetic_processors: NotRequired[FieldCommonInfoCounterStatModel]


class FieldCommonNestedNeuralNodeStatsProcessorsIngest(TypedDict):
    text_embedding_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    text_chunking_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    text_chunking_delimiter_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    text_chunking_fixed_token_length_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    text_chunking_fixed_char_length_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    semantic_field_chunking_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    sparse_encoding_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    text_image_embedding_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    skip_existing_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    semantic_field_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]


class FieldCommonNestedNeuralNodeStatsProcessorsSearchHybrid(TypedDict):
    normalization_processor_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    norm_l2_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    norm_minmax_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    norm_zscore_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    rank_based_normalization_processor_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    comb_geometric_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    comb_rrf_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    comb_harmonic_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    comb_arithmetic_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]


class FieldCommonNestedNeuralNodeStatsQueryHybrid(TypedDict):
    hybrid_query_requests: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    hybrid_query_with_pagination_requests: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    hybrid_query_with_filter_requests: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    hybrid_query_with_inner_hits_requests: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]


class FieldCommonNestedNeuralNodeStatsQueryNeural(TypedDict):
    neural_query_requests: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    neural_query_against_semantic_sparse_requests: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    neural_query_against_semantic_dense_requests: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    neural_query_against_knn_requests: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]


class FieldCommonNestedNeuralNodeStatsQueryNeuralSparse(TypedDict):
    neural_sparse_query_requests: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]


class FieldCommonNestedNeuralNodeStatsSemanticHighlighting(TypedDict):
    semantic_highlighting_request_count: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]


FieldCommonFlatNeuralInfoStats = TypedDict(
    "FieldCommonFlatNeuralInfoStats",
    {
        "cluster_version": NotRequired[FieldCommonInfoStringStatModel],
        "processors.ingest.text_embedding_processors_in_pipelines": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.ingest.text_chunking_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.ingest.text_chunking_delimiter_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.ingest.text_chunking_fixed_token_length_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.ingest.text_chunking_fixed_char_length_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.ingest.sparse_encoding_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.ingest.text_image_embedding_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.ingest.skip_existing_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.normalization_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.norm_l2_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.norm_minmax_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.norm_zscore_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.rank_based_normalization_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.comb_geometric_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.comb_rrf_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.comb_harmonic_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.hybrid.comb_arithmetic_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.rerank_ml_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.rerank_by_field_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.neural_sparse_two_phase_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
        "processors.search.neural_query_enricher_processors": NotRequired[
            FieldCommonInfoCounterStatModel
        ],
    },
)


class FieldCommonFlatNeuralStats(FieldCommonNodesResponseBase):
    cluster_name: NotRequired[str]
    info: NotRequired[FieldCommonFlatNeuralInfoStats]
    all_nodes: NotRequired[FieldCommonFlatNeuralNodeStats]
    nodes: NotRequired[dict[str, FieldCommonFlatNeuralNodeStats]]


class FieldCommonNestedNeuralInfoStatsProcessorsSearch(TypedDict):
    hybrid: NotRequired[FieldCommonNestedNeuralInfoStatsProcessorsSearchHybrid]
    rerank_ml_processors: NotRequired[FieldCommonInfoCounterStatModel]
    rerank_by_field_processors: NotRequired[FieldCommonInfoCounterStatModel]
    neural_sparse_two_phase_processors: NotRequired[FieldCommonInfoCounterStatModel]
    neural_query_enricher_processors: NotRequired[FieldCommonInfoCounterStatModel]


class FieldCommonNestedNeuralNodeStatsProcessorsSearch(TypedDict):
    hybrid: NotRequired[FieldCommonNestedNeuralNodeStatsProcessorsSearchHybrid]
    neural_sparse_two_phase_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    neural_query_enricher_executions: NotRequired[
        FieldCommonTimestampedEventCounterStatModel
    ]
    rerank_by_field_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]
    rerank_ml_executions: NotRequired[FieldCommonTimestampedEventCounterStatModel]


class FieldCommonNestedNeuralNodeStatsQuery(TypedDict):
    hybrid: NotRequired[FieldCommonNestedNeuralNodeStatsQueryHybrid]
    neural: NotRequired[FieldCommonNestedNeuralNodeStatsQueryNeural]
    neural_sparse: NotRequired[FieldCommonNestedNeuralNodeStatsQueryNeuralSparse]


class FieldCommonNestedNeuralInfoStatsProcessors(TypedDict):
    ingest: NotRequired[FieldCommonNestedNeuralInfoStatsProcessorsIngest]
    search: NotRequired[FieldCommonNestedNeuralInfoStatsProcessorsSearch]


class FieldCommonNestedNeuralNodeStatsProcessors(TypedDict):
    ingest: NotRequired[FieldCommonNestedNeuralNodeStatsProcessorsIngest]
    search: NotRequired[FieldCommonNestedNeuralNodeStatsProcessorsSearch]


class FieldCommonNestedNeuralInfoStats(TypedDict):
    cluster_version: NotRequired[FieldCommonInfoStringStatModel]
    processors: NotRequired[FieldCommonNestedNeuralInfoStatsProcessors]


class FieldCommonNestedNeuralNodeStats(TypedDict):
    query: NotRequired[FieldCommonNestedNeuralNodeStatsQuery]
    semantic_highlighting: NotRequired[
        FieldCommonNestedNeuralNodeStatsSemanticHighlighting
    ]
    processors: NotRequired[FieldCommonNestedNeuralNodeStatsProcessors]


class FieldCommonNestedNeuralStats(FieldCommonNodesResponseBase):
    cluster_name: NotRequired[str]
    info: NotRequired[FieldCommonNestedNeuralInfoStats]
    all_nodes: NotRequired[FieldCommonNestedNeuralNodeStats]
    nodes: NotRequired[dict[str, FieldCommonNestedNeuralNodeStats]]


FieldCommonNeuralStats: TypeAlias = (
    FieldCommonNestedNeuralStats | FieldCommonFlatNeuralStats
)
