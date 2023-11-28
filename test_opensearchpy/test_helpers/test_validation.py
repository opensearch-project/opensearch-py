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

from datetime import datetime
from typing import Any

from pytest import raises

from opensearchpy import (
    Boolean,
    Date,
    Document,
    InnerDoc,
    Integer,
    Nested,
    Object,
    Text,
)
from opensearchpy.exceptions import ValidationException


class Author(InnerDoc):
    name: Any = Text(required=True)
    email: Any = Text(required=True)

    def clean(self) -> None:
        print(self, type(self), self.name)
        if self.name.lower() not in self.email:
            raise ValidationException("Invalid email!")


class BlogPost(Document):
    authors = Nested(Author, required=True)
    created = Date()
    inner = Object()


class BlogPostWithStatus(Document):
    published = Boolean(required=True)


class AutoNowDate(Date):
    def clean(self, data: Any) -> Any:
        if data is None:
            data = datetime.now()
        return super(AutoNowDate, self).clean(data)


class Log(Document):
    timestamp = AutoNowDate(required=True)
    data = Text()


def test_required_int_can_be_0() -> None:
    class DT(Document):
        i = Integer(required=True)

    dt: Any = DT(i=0)
    assert dt.full_clean() is None


def test_required_field_cannot_be_empty_list() -> None:
    class DT(Document):
        i = Integer(required=True)

    dt = DT(i=[])
    with raises(ValidationException):
        dt.full_clean()


def test_validation_works_for_lists_of_values() -> None:
    class DT(Document):
        i = Date(required=True)

    dt1: Any = DT(i=[datetime.now(), "not date"])
    with raises(ValidationException):
        dt1.full_clean()

    dt2: Any = DT(i=[datetime.now(), datetime.now()])
    assert None is dt2.full_clean()


def test_field_with_custom_clean() -> None:
    ls = Log()
    ls.full_clean()

    assert isinstance(ls.timestamp, datetime)


def test_empty_object() -> None:
    d: Any = BlogPost(authors=[{"name": "Guian", "email": "guiang@bitquilltech.com"}])
    d.inner = {}

    d.full_clean()


def test_missing_required_field_raises_validation_exception() -> None:
    d1: Any = BlogPost()
    with raises(ValidationException):
        d1.full_clean()

    d2: Any = BlogPost()
    d2.authors.append({"name": "Guian"})
    with raises(ValidationException):
        d2.full_clean()

    d3: Any = BlogPost()
    d3.authors.append({"name": "Guian", "email": "guiang@bitquilltech.com"})
    d3.full_clean()


def test_boolean_doesnt_treat_false_as_empty() -> None:
    d: Any = BlogPostWithStatus()
    with raises(ValidationException):
        d.full_clean()
    d.published = False
    d.full_clean()
    d.published = True
    d.full_clean()


def test_custom_validation_on_nested_gets_run() -> None:
    d: Any = BlogPost(
        authors=[Author(name="Guian", email="king@example.com")], created=None
    )

    assert isinstance(d.authors[0], Author)

    with raises(ValidationException):
        d.full_clean()


def test_accessing_known_fields_returns_empty_value() -> None:
    d: Any = BlogPost()

    assert [] == d.authors

    d.authors.append({})
    assert None is d.authors[0].name
    assert None is d.authors[0].email


def test_empty_values_are_not_serialized() -> None:
    d: Any = BlogPost(
        authors=[{"name": "Guian", "email": "guiang@bitquilltech.com"}], created=None
    )

    d.full_clean()
    assert d.to_dict() == {
        "authors": [{"name": "Guian", "email": "guiang@bitquilltech.com"}]
    }
