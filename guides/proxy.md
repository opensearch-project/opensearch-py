- [Using a Proxy](#using-a-proxy)
  - [Using a Proxy with a Sync Client](#using-a-proxy-with-a-sync-client)
  - [Using a Proxy with an Async Client](#using-a-proxy-with-an-async-client)

# Using a Proxy

## Using a Proxy with a Sync Client

```python
from opensearchpy import OpenSearch, RequestsHttpConnection

OpenSearch(
    hosts=["htps://..."],
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    trust_env=True,
)
```

## Using a Proxy with an Async Client

```python
from opensearchpy import AsyncOpenSearch, AIOHttpConnection

client = AsyncOpenSearch(
    hosts=["htps://..."],
    use_ssl=True,
    verify_certs=True,
    connection_class=AIOHttpConnection,
    trust_env=True,
)
```