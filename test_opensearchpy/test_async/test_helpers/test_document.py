# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from __future__ import unicode_literals

import codecs
import ipaddress
import pickle
from datetime import datetime
from hashlib import sha256
from typing import Any

import pytest
from _pytest.mark.structures import MarkDecorator
from pytest import raises

from opensearchpy import InnerDoc, MetaField, Range, analyzer
from opensearchpy._async.helpers import document
from opensearchpy._async.helpers.index import AsyncIndex
from opensearchpy._async.helpers.mapping import AsyncMapping
from opensearchpy.exceptions import IllegalOperation, ValidationException
from opensearchpy.helpers import field, utils

pytestmark: MarkDecorator = pytest.mark.asyncio


class MyInner(InnerDoc):
    old_field: Any = field.Text()


class MyDoc(document.AsyncDocument):
    title: Any = field.Keyword()
    name: Any = field.Text()
    created_at: Any = field.Date()
    inner: Any = field.Object(MyInner)


class MySubDoc(MyDoc):
    name: Any = field.Keyword()

    class Index:
        name = "default-index"


class MyDoc2(document.AsyncDocument):
    extra: Any = field.Long()


class MyMultiSubDoc(MyDoc2, MySubDoc):
    pass


class Comment(InnerDoc):
    title: Any = field.Text()
    tags: Any = field.Keyword(multi=True)


class DocWithNested(document.AsyncDocument):
    comments: Any = field.Nested(Comment)

    class Index:
        name = "test-doc-with-nested"


class SimpleCommit(document.AsyncDocument):
    files: Any = field.Text(multi=True)

    class Index:
        name = "test-git"


class Secret(str):
    pass


class SecretField(field.CustomField):
    builtin_type: Any = "text"

    def _serialize(self, data: Any) -> Any:
        return codecs.encode(data, "rot_13")

    def _deserialize(self, data: Any) -> Any:
        if isinstance(data, Secret):
            return data
        return Secret(codecs.decode(data, "rot_13"))


class SecretDoc(document.AsyncDocument):
    title: Any = SecretField(index="no")

    class Index:
        name = "test-secret-doc"


class NestedSecret(document.AsyncDocument):
    secrets: Any = field.Nested(SecretDoc)

    class Index:
        name = "test-nested-secret"

    _index: Any


class OptionalObjectWithRequiredField(document.AsyncDocument):
    comments: Any = field.Nested(properties={"title": field.Keyword(required=True)})

    class Index:
        name = "test-required"

    _index: Any


class Host(document.AsyncDocument):
    ip: Any = field.Ip()

    class Index:
        name = "test-host"

    _index: Any


async def test_range_serializes_properly() -> None:
    class DocumentD(document.AsyncDocument):
        lr: Any = field.LongRange()

    d = DocumentD(lr=Range(lt=42))
    assert 40 in d.lr
    assert 47 not in d.lr
    assert {"lr": {"lt": 42}} == d.to_dict()

    d = DocumentD(lr={"lt": 42})
    assert {"lr": {"lt": 42}} == d.to_dict()


async def test_range_deserializes_properly() -> None:
    class DocumentD(InnerDoc):
        lr = field.LongRange()

    d = DocumentD.from_opensearch({"lr": {"lt": 42}}, True)
    assert isinstance(d.lr, Range)
    assert 40 in d.lr
    assert 47 not in d.lr


async def test_resolve_nested() -> None:
    nested, field = NestedSecret._index.resolve_nested("secrets.title")
    assert nested == ["secrets"]
    assert field is NestedSecret._doc_type.mapping["secrets"]["title"]


async def test_conflicting_mapping_raises_error_in_index_to_dict() -> None:
    class DocumentA(document.AsyncDocument):
        name = field.Text()

    class DocumentB(document.AsyncDocument):
        name = field.Keyword()

    i = AsyncIndex("i")
    i.document(DocumentA)
    i.document(DocumentB)

    with raises(ValueError):
        i.to_dict()


async def test_ip_address_serializes_properly() -> None:
    host = Host(ip=ipaddress.IPv4Address("10.0.0.1"))

    assert {"ip": "10.0.0.1"} == host.to_dict()


async def test_matches_uses_index() -> None:
    assert SimpleCommit._matches({"_index": "test-git"})
    assert not SimpleCommit._matches({"_index": "not-test-git"})


async def test_matches_with_no_name_always_matches() -> None:
    class DocumentD(document.AsyncDocument):
        pass

    assert DocumentD._matches({})
    assert DocumentD._matches({"_index": "whatever"})


async def test_matches_accepts_wildcards() -> None:
    class MyDoc(document.AsyncDocument):
        class Index:
            name = "my-*"

    assert MyDoc._matches({"_index": "my-index"})
    assert not MyDoc._matches({"_index": "not-my-index"})


async def test_assigning_attrlist_to_field() -> None:
    sc = SimpleCommit()
    ls = ["README", "README.rst"]
    sc.files = utils.AttrList(ls)

    assert sc.to_dict()["files"] is ls


async def test_optional_inner_objects_are_not_validated_if_missing() -> None:
    d: Any = OptionalObjectWithRequiredField()

    assert d.full_clean() is None


async def test_custom_field() -> None:
    s = SecretDoc(title=Secret("Hello"))

    assert {"title": "Uryyb"} == s.to_dict()
    assert s.title == "Hello"

    s = SecretDoc.from_opensearch({"_source": {"title": "Uryyb"}})
    assert s.title == "Hello"
    assert isinstance(s.title, Secret)


async def test_custom_field_mapping() -> None:
    assert {
        "properties": {"title": {"index": "no", "type": "text"}}
    } == SecretDoc._doc_type.mapping.to_dict()


async def test_custom_field_in_nested() -> None:
    s = NestedSecret()
    s.secrets.append(SecretDoc(title=Secret("Hello")))

    assert {"secrets": [{"title": "Uryyb"}]} == s.to_dict()
    assert s.secrets[0].title == "Hello"


async def test_multi_works_after_doc_has_been_saved() -> None:
    c = SimpleCommit()
    c.full_clean()
    c.files.append("setup.py")

    assert c.to_dict() == {"files": ["setup.py"]}


async def test_multi_works_in_nested_after_doc_has_been_serialized() -> None:
    # Issue #359
    c = DocWithNested(comments=[Comment(title="First!")])

    assert [] == c.comments[0].tags
    assert {"comments": [{"title": "First!"}]} == c.to_dict()
    assert [] == c.comments[0].tags


async def test_null_value_for_object() -> None:
    d = MyDoc(inner=None)

    assert d.inner is None


async def test_inherited_doc_types_can_override_index() -> None:
    class MyDocDifferentIndex(MySubDoc):
        _index: Any

        class Index:
            name: Any = "not-default-index"
            settings: Any = {"number_of_replicas": 0}
            aliases: Any = {"a": {}}
            analyzers: Any = [analyzer("my_analizer", tokenizer="keyword")]

    assert MyDocDifferentIndex._index._name == "not-default-index"
    assert MyDocDifferentIndex()._get_index() == "not-default-index"
    assert MyDocDifferentIndex._index.to_dict() == {
        "aliases": {"a": {}},
        "mappings": {
            "properties": {
                "created_at": {"type": "date"},
                "inner": {
                    "type": "object",
                    "properties": {"old_field": {"type": "text"}},
                },
                "name": {"type": "keyword"},
                "title": {"type": "keyword"},
            }
        },
        "settings": {
            "analysis": {
                "analyzer": {"my_analizer": {"tokenizer": "keyword", "type": "custom"}}
            },
            "number_of_replicas": 0,
        },
    }


async def test_to_dict_with_meta() -> None:
    d = MySubDoc(title="hello")
    d.meta.routing = "some-parent"

    assert {
        "_index": "default-index",
        "_routing": "some-parent",
        "_source": {"title": "hello"},
    } == d.to_dict(True)


async def test_to_dict_with_meta_includes_custom_index() -> None:
    d = MySubDoc(title="hello")
    d.meta.index = "other-index"

    assert {"_index": "other-index", "_source": {"title": "hello"}} == d.to_dict(True)


async def test_to_dict_without_skip_empty_will_include_empty_fields() -> None:
    d = MySubDoc(tags=[], title=None, inner={})

    assert {} == d.to_dict()
    assert {"tags": [], "title": None, "inner": {}} == d.to_dict(skip_empty=False)


async def test_attribute_can_be_removed() -> None:
    d = MyDoc(title="hello")

    del d.title
    assert "title" not in d._d_


async def test_doc_type_can_be_correctly_pickled() -> None:
    d = DocWithNested(
        title="Hello World!", comments=[Comment(title="hellp")], meta={"id": 42}
    )
    s = pickle.dumps(d)

    d2 = pickle.loads(s)

    assert d2 == d
    assert 42 == d2.meta.id
    assert "Hello World!" == d2.title
    assert [{"title": "hellp"}] == d2.comments
    assert isinstance(d2.comments[0], Comment)


async def test_meta_is_accessible_even_on_empty_doc() -> None:
    d = MyDoc()
    d.meta

    d = MyDoc(title="aaa")
    d.meta


async def test_meta_field_mapping() -> None:
    class User(document.AsyncDocument):
        username = field.Text()

        class Meta:
            all = MetaField(enabled=False)
            _index = MetaField(enabled=True)
            dynamic = MetaField("strict")
            dynamic_templates = MetaField([42])

    assert {
        "properties": {"username": {"type": "text"}},
        "_all": {"enabled": False},
        "_index": {"enabled": True},
        "dynamic": "strict",
        "dynamic_templates": [42],
    } == User._doc_type.mapping.to_dict()


async def test_multi_value_fields() -> None:
    class Blog(document.AsyncDocument):
        tags = field.Keyword(multi=True)

    b = Blog()
    assert [] == b.tags
    b.tags.append("search")
    b.tags.append("python")
    assert ["search", "python"] == b.tags


async def test_docs_with_properties() -> None:
    class User(document.AsyncDocument):
        pwd_hash: Any = field.Text()

        def check_password(self, pwd: Any) -> Any:
            return sha256(pwd).hexdigest() == self.pwd_hash

        @property
        def password(self) -> Any:
            raise AttributeError("readonly")

        @password.setter
        def password(self, pwd: Any) -> None:
            self.pwd_hash = sha256(pwd).hexdigest()

    u = User(pwd_hash=sha256(b"secret").hexdigest())
    assert u.check_password(b"secret")
    assert not u.check_password(b"not-secret")

    u.password = b"not-secret"
    assert "password" not in u._d_
    assert not u.check_password(b"secret")
    assert u.check_password(b"not-secret")

    with raises(AttributeError):
        u.password


async def test_nested_can_be_assigned_to() -> None:
    d1 = DocWithNested(comments=[Comment(title="First!")])
    d2 = DocWithNested()

    d2.comments = d1.comments
    assert isinstance(d1.comments[0], Comment)
    assert d2.comments == [{"title": "First!"}]
    assert {"comments": [{"title": "First!"}]} == d2.to_dict()
    assert isinstance(d2.comments[0], Comment)


async def test_nested_can_be_none() -> None:
    d = DocWithNested(comments=None, title="Hello World!")

    assert {"title": "Hello World!"} == d.to_dict()


async def test_nested_defaults_to_list_and_can_be_updated() -> None:
    md = DocWithNested()

    assert [] == md.comments

    md.comments.append({"title": "hello World!"})
    assert {"comments": [{"title": "hello World!"}]} == md.to_dict()


async def test_to_dict_is_recursive_and_can_cope_with_multi_values() -> None:
    md: Any = MyDoc(name=["a", "b", "c"])
    md.inner = [MyInner(old_field="of1"), MyInner(old_field="of2")]

    assert isinstance(md.inner[0], MyInner)

    assert {
        "name": ["a", "b", "c"],
        "inner": [{"old_field": "of1"}, {"old_field": "of2"}],
    } == md.to_dict()


async def test_to_dict_ignores_empty_collections() -> None:
    md: Any = MySubDoc(name="", address={}, count=0, valid=False, tags=[])

    assert {"name": "", "count": 0, "valid": False} == md.to_dict()


async def test_declarative_mapping_definition() -> None:
    assert issubclass(MyDoc, document.AsyncDocument)
    assert hasattr(MyDoc, "_doc_type")
    assert {
        "properties": {
            "created_at": {"type": "date"},
            "name": {"type": "text"},
            "title": {"type": "keyword"},
            "inner": {"type": "object", "properties": {"old_field": {"type": "text"}}},
        }
    } == MyDoc._doc_type.mapping.to_dict()


async def test_you_can_supply_own_mapping_instance() -> None:
    class MyD(document.AsyncDocument):
        title = field.Text()

        class Meta:
            mapping = AsyncMapping()
            mapping.meta("_all", enabled=False)

    assert {
        "_all": {"enabled": False},
        "properties": {"title": {"type": "text"}},
    } == MyD._doc_type.mapping.to_dict()


async def test_document_can_be_created_dynamically() -> None:
    n = datetime.now()
    md: Any = MyDoc(title="hello")
    md.name = "My Fancy Document!"
    md.created_at = n

    inner = md.inner
    # consistent returns
    assert inner is md.inner
    inner.old_field = "Already defined."

    md.inner.new_field = ["undefined", "field"]

    assert {
        "title": "hello",
        "name": "My Fancy Document!",
        "created_at": n,
        "inner": {"old_field": "Already defined.", "new_field": ["undefined", "field"]},
    } == md.to_dict()


async def test_invalid_date_will_raise_exception() -> None:
    md: Any = MyDoc()
    md.created_at = "not-a-date"
    with raises(ValidationException):
        md.full_clean()


async def test_document_inheritance() -> None:
    assert issubclass(MySubDoc, MyDoc)
    assert issubclass(MySubDoc, document.AsyncDocument)
    assert hasattr(MySubDoc, "_doc_type")
    assert {
        "properties": {
            "created_at": {"type": "date"},
            "name": {"type": "keyword"},
            "title": {"type": "keyword"},
            "inner": {"type": "object", "properties": {"old_field": {"type": "text"}}},
        }
    } == MySubDoc._doc_type.mapping.to_dict()


async def test_child_class_can_override_parent() -> None:
    class DocumentA(document.AsyncDocument):
        o = field.Object(dynamic=False, properties={"a": field.Text()})

    class DocumentB(DocumentA):
        o = field.Object(dynamic="strict", properties={"b": field.Text()})

    assert {
        "properties": {
            "o": {
                "dynamic": "strict",
                "properties": {"a": {"type": "text"}, "b": {"type": "text"}},
                "type": "object",
            }
        }
    } == DocumentB._doc_type.mapping.to_dict()


async def test_meta_fields_are_stored_in_meta_and_ignored_by_to_dict() -> None:
    md: Any = MySubDoc(meta={"id": 42}, name="My First doc!")

    md.meta.index = "my-index"
    assert md.meta.index == "my-index"
    assert md.meta.id == 42
    assert {"name": "My First doc!"} == md.to_dict()
    assert {"id": 42, "index": "my-index"} == md.meta.to_dict()


async def test_index_inheritance() -> None:
    assert issubclass(MyMultiSubDoc, MySubDoc)
    assert issubclass(MyMultiSubDoc, MyDoc2)
    assert issubclass(MyMultiSubDoc, document.AsyncDocument)
    assert hasattr(MyMultiSubDoc, "_doc_type")
    assert hasattr(MyMultiSubDoc, "_index")
    assert {
        "properties": {
            "created_at": {"type": "date"},
            "name": {"type": "keyword"},
            "title": {"type": "keyword"},
            "inner": {"type": "object", "properties": {"old_field": {"type": "text"}}},
            "extra": {"type": "long"},
        }
    } == MyMultiSubDoc._doc_type.mapping.to_dict()


async def test_meta_fields_can_be_set_directly_in_init() -> None:
    p = object()
    md: Any = MyDoc(_id=p, title="Hello World!")

    assert md.meta.id is p


async def test_save_no_index(mock_client: Any) -> None:
    md: Any = MyDoc()
    with raises(ValidationException):
        await md.save(using="mock")


async def test_delete_no_index(mock_client: Any) -> None:
    md: Any = MyDoc()
    with raises(ValidationException):
        await md.delete(using="mock")


async def test_update_no_fields() -> None:
    md: Any = MyDoc()
    with raises(IllegalOperation):
        await md.update()


async def test_search_with_custom_alias_and_index(mock_client: Any) -> None:
    search_object: Any = MyDoc.search(
        using="staging", index=["custom_index1", "custom_index2"]
    )

    assert search_object._using == "staging"
    assert search_object._index == ["custom_index1", "custom_index2"]


async def test_from_opensearch_respects_underscored_non_meta_fields() -> None:
    doc: Any = {
        "_index": "test-index",
        "_id": "opensearch",
        "_score": 12.0,
        "fields": {"hello": "world", "_routing": "opensearch", "_tags": ["search"]},
        "_source": {
            "city": "Amsterdam",
            "name": "OpenSearch",
            "_tagline": "You know, for search",
        },
    }

    class Company(document.AsyncDocument):
        class Index:
            name = "test-company"

    c = Company.from_opensearch(doc)

    assert c.meta.fields._tags == ["search"]
    assert c.meta.fields._routing == "opensearch"
    assert c._tagline == "You know, for search"


async def test_nested_and_object_inner_doc() -> None:
    class MySubDocWithNested(MyDoc):
        nested_inner = field.Nested(MyInner)

    props: Any = MySubDocWithNested._doc_type.mapping.to_dict()["properties"]
    assert props == {
        "created_at": {"type": "date"},
        "inner": {"properties": {"old_field": {"type": "text"}}, "type": "object"},
        "name": {"type": "text"},
        "nested_inner": {
            "properties": {"old_field": {"type": "text"}},
            "type": "nested",
        },
        "title": {"type": "keyword"},
    }
