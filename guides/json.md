- [Making Raw JSON REST Requests](#making-raw-json-rest-requests)
  - [GET](#get)
  - [PUT](#put)
  - [POST](#post)
  - [DELETE](#delete)

# Making Raw JSON REST Requests

The OpenSearch client implements many high-level REST DSLs that invoke OpenSearch APIs. However you may find yourself in a situation that requires you to invoke an API that is not supported by the client. Use `client.transport.perform_request` to do so. See [samples/json](../samples/json) for a complete working sample.

## GET

The following example returns the server version information via `GET /`.

```python
info = client.transport.perform_request('GET', '/')
print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")
```

Note that the client will parse the response as JSON when appropriate.

## PUT

The following example creates an index.

```python
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

client.transport.perform_request("PUT", "/movies", body=index_body)
```

Note that the client will raise errors automatically. For example, if the index already exists, an `opensearchpy.exceptions.RequestError: RequestError(400, 'resource_already_exists_exception',` will be thrown.

## POST

The following example searches for a document.

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

client.transport.perform_request("POST", "/movies/_search", body = query)
```

## DELETE

The following example deletes an index.

```python
client.transport.perform_request("DELETE", "/movies")
```
