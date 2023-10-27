# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from typing import Any

from .utils import DslBase

class Query(DslBase): ...
class MatchAll(Query): ...
class MatchNone(Query): ...
class Bool(Query): ...
class FunctionScore(Query): ...
class Boosting(Query): ...
class ConstantScore(Query): ...
class DisMax(Query): ...
class Filtered(Query): ...
class Indices(Query): ...
class Percolate(Query): ...
class Nested(Query): ...
class HasChild(Query): ...
class HasParent(Query): ...
class TopChildren(Query): ...
class SpanFirst(Query): ...
class SpanMulti(Query): ...
class SpanNear(Query): ...
class SpanNot(Query): ...
class SpanOr(Query): ...
class FieldMaskingSpan(Query): ...
class SpanContaining(Query): ...
class SpanWithin(Query): ...
class Common(Query): ...
class Fuzzy(Query): ...
class FuzzyLikeThis(Query): ...
class FuzzyLikeThisField(Query): ...
class RankFeature(Query): ...
class DistanceFeature(Query): ...
class GeoBoundingBox(Query): ...
class GeoDistance(Query): ...
class GeoDistanceRange(Query): ...
class GeoPolygon(Query): ...
class GeoShape(Query): ...
class GeohashCell(Query): ...
class Ids(Query): ...
class Intervals(Query): ...
class Limit(Query): ...
class Match(Query): ...
class MatchPhrase(Query): ...
class MatchPhrasePrefix(Query): ...
class MatchBoolPrefix(Query): ...
class Exists(Query): ...
class MoreLikeThis(Query): ...
class MoreLikeThisField(Query): ...
class MultiMatch(Query): ...
class Prefix(Query): ...
class QueryString(Query): ...
class Range(Query): ...
class Regexp(Query): ...
class Shape(Query): ...
class SimpleQueryString(Query): ...
class SpanTerm(Query): ...
class Template(Query): ...
class Term(Query): ...
class Terms(Query): ...
class TermsSet(Query): ...
class Wildcard(Query): ...
class Script(Query): ...
class ScriptScore(Query): ...
class Type(Query): ...
class ParentId(Query): ...
class Wrapper(Query): ...

def Q(name_or_query: Any, **params: Any) -> Any: ...
