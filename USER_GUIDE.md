- [OpenSearch Python Client User Guide](#opensearch-python-client-user-guide)
  - [Setup](#setup)
  - [Basic Features](#basic-features)
    - [Creating a Client](#creating-a-client)
    - [Creating an Index](#creating-an-index)
    - [Adding a Document to an Index](#adding-a-document-to-an-index)
    - [Searching for a Document](#searching-for-a-document)
    - [Deleting a Document](#deleting-a-document)
    - [Deleting an Index](#deleting-an-index)
  - [Advanced Features](#advanced-features)
  - [Plugins](#plugins)

# OpenSearch Python Client User Guide

## Setup

To add the client to your project, install it using [pip](https://pip.pypa.io/):

```bash
pip install opensearch-py
```

Then import it like any other module:

```python
from opensearchpy import OpenSearch
```

For better performance we recommend the async client. See [Asynchronous I/O](guides/async.md) for more information.

In general, we recommend using a package manager, such as [poetry](https://python-poetry.org/docs/), for your projects. This is the package manager used for [samples](samples).

## Basic Features

In the example below, we create a client, create an index with non-default settings, insert a 
document into the index, search for the document, delete the document, and finally delete the index.

You can find working versions of the code below that can be run with a local instance of OpenSearch in [samples](samples).

### Creating a Client

```python
from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False
)

info = client.info()
print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")
```

See [hello.py](samples/hello/hello.py) for a working synchronous sample, and [guides/ssl](guides/ssl.md) for how to setup SSL certificates.

### Creating an Index

```python
index_name = 'test-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(
  index_name, 
  body=index_body
)

print(response)
```

### Adding a Document to an Index

```python
document = {
  'title': 'Moneyball',
  'director': 'Bennett Miller',
  'year': '2011'
}

id = '1'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print(response)
```

### Searching for a Document

```python
q = 'miller'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

response = client.search(
    body = query,
    index = index_name
)

print(response)
```

### Deleting a Document

```python
response = client.delete(
    index = index_name,
    id = id
)
print(response)
```

### Deleting an Index

```python
response = client.indices.delete(
    index = index_name
)

print(response)
```

## Advanced Features

- [Asynchronous I/O](guides/async.md)
- [Authentication (IAM, SigV4)](guides/auth.md)
- [Configuring SSL](guides/ssl.md)
- [Bulk Indexing](guides/bulk.md)
- [High Level DSL](guides/dsl.md)
- [Index Lifecycle](guides/index_lifecycle.md)
- [Search](guides/search.md)
- [Point in Time](guides/point_in_time.md)
- [Using a Proxy](guides/proxy.md)
- [Index Templates](guides/index_template.md)
- [Connection Classes](guides/connection_classes.md)

## Plugins

- [Security](guides/plugins/security.md) 
- [Alerting](guides/plugins/alerting.md) 
- [Index Management](guides/plugins/index_management.md)
- [k-NN](guides/plugins/knn.md)