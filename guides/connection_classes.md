- [Connection Classes](#connection-classes)
  - [Selecting a Connection Class](#selecting-a-connection-class)
    - [Urllib3HttpConnection](#urllib3httpconnection)
    - [RequestsHttpConnection](#requestshttpconnection)
    - [AsyncHttpConnection](#asynchttpconnection)
  - [Connection Pooling](#connection-pooling)

# Connection Classes

The OpenSearch Python synchrnous client supports both the `Urllib3HttpConnection` connection class (default) from the [urllib3](https://pypi.org/project/urllib3/) library, and `RequestsHttpConnection` from the [requests](https://pypi.org/project/requests/) library. We recommend you use the default, unless your application is standardized on `requests`. 

The faster, asynchronous client, implements a class called `AsyncHttpConnection`, which uses [aiohttp](https://pypi.org/project/aiohttp/).

## Selecting a Connection Class

### Urllib3HttpConnection

```python
from opensearchpy import OpenSearch, Urllib3HttpConnection

client = OpenSearch(
    hosts = [{'host': 'localhost', 'port': 9200}],
    http_auth = ('admin', 'admin'),
    use_ssl = True,
    verify_certs = False,
    ssl_show_warn = False,
    connection_class = Urllib3HttpConnection
)
```

### RequestsHttpConnection

```python
from opensearchpy import OpenSearch, RequestsHttpConnection

client = OpenSearch(
    hosts = [{'host': 'localhost', 'port': 9200}],
    http_auth = ('admin', 'admin'),
    use_ssl = True,
    verify_certs = False,
    ssl_show_warn = False,
    connection_class = RequestsHttpConnection
)
```

### AsyncHttpConnection

```python
from opensearchpy import AsyncOpenSearch, AsyncHttpConnection

async def main():
    client = AsyncOpenSearch(
        hosts = [{'host': 'localhost', 'port': 9200}],
        http_auth = ('admin', 'admin'),
        use_ssl = True,
        verify_certs = False,
        ssl_show_warn = False,
        connection_class = AsyncHttpConnection
    )
```

## Connection Pooling

The OpenSearch Python client has a connection pool for each `host` value specified during initialization, and a connection pool for HTTP connections to each host implemented in the underlying HTTP libraries. You can adjust the max size of the latter connection pool with `pool_maxsize`. 

If you don't set this value, each connection library implementation will provide its default, which is typically `10`. Changing the pool size may improve performance in some multithreaded scenarios.

The following example sets the number of connections in the connection pool to 12.

```python
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts = [{'host': 'localhost', 'port': 9200}],
    http_auth = ('admin', 'admin'),
    use_ssl = True,
    verify_certs = False,
    ssl_show_warn = False,
    pool_maxsize = 12,
)
```