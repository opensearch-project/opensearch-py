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

import pickle

from pytest import raises

from opensearchpy import Q, serializer
from opensearchpy.helpers import utils


def test_attrdict_pickle() -> None:
    # pylint: disable=missing-function-docstring
    ad = utils.AttrDict({})

    pickled_ad = pickle.dumps(ad)
    assert ad == pickle.loads(pickled_ad)


def test_attrlist_pickle() -> None:
    # pylint: disable=missing-function-docstring
    al = utils.AttrList([])

    pickled_al = pickle.dumps(al)
    assert al == pickle.loads(pickled_al)


def test_attrlist_slice() -> None:
    # pylint: disable=missing-function-docstring
    class MyAttrDict(utils.AttrDict):
        pass

    ls = utils.AttrList([{}, {}], obj_wrapper=MyAttrDict)
    assert isinstance(ls[:][0], MyAttrDict)


def test_merge() -> None:
    # pylint: disable=missing-function-docstring
    a = utils.AttrDict({"a": {"b": 42, "c": 47}})
    b = {"a": {"b": 123, "d": -12}, "e": [1, 2, 3]}

    utils.merge(a, b)

    assert a == {"a": {"b": 123, "c": 47, "d": -12}, "e": [1, 2, 3]}


def test_merge_conflict() -> None:
    # pylint: disable=missing-function-docstring
    for d in (
        {"a": 42},
        {"a": {"b": 47}},
    ):
        utils.merge({"a": {"b": 42}}, d)
        with raises(ValueError):
            utils.merge({"a": {"b": 42}}, d, True)


def test_attrdict_bool() -> None:
    # pylint: disable=missing-function-docstring
    d = utils.AttrDict({})

    assert not d
    d.title = "Title"
    assert d


def test_attrlist_items_get_wrapped_during_iteration() -> None:
    # pylint: disable=missing-function-docstring
    al = utils.AttrList([1, object(), [1], {}])

    ls = list(iter(al))

    assert isinstance(ls[2], utils.AttrList)
    assert isinstance(ls[3], utils.AttrDict)


def test_serializer_deals_with_attr_versions() -> None:
    # pylint: disable=missing-function-docstring
    d = utils.AttrDict({"key": utils.AttrList([1, 2, 3])})

    assert serializer.serializer.dumps(d) == serializer.serializer.dumps(
        {"key": [1, 2, 3]}
    )


def test_serializer_deals_with_objects_with_to_dict() -> None:
    # pylint: disable=missing-function-docstring
    class MyClass(object):
        def to_dict(self) -> int:
            return 42

    assert serializer.serializer.dumps(MyClass()) == "42"


def test_recursive_to_dict() -> None:
    # pylint: disable=missing-function-docstring
    assert utils.recursive_to_dict({"k": [1, (1.0, {"v": Q("match", key="val")})]}) == {
        "k": [1, (1.0, {"v": {"match": {"key": "val"}}})]
    }


def test_attrdict_get() -> None:
    # pylint: disable=missing-function-docstring
    a = utils.AttrDict({"a": {"b": 42, "c": 47}})
    assert a.get("a", {}).get("b", 0) == 42
    assert a.get("a", {}).get("e", 0) == 0
    assert a.get("d", {}) == {}
    with raises(AttributeError):
        assert a.get("d")
