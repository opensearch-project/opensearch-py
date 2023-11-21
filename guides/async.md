- [Asynchronous I/O](#asynchronous-io)
  - [Setup](#setup)
  - [Async Loop](#async-loop)
  - [Connect to OpenSearch](#connect-to-opensearch)
  - [Create an Index](#create-an-index)
  - [Index Documents](#index-documents)
  - [Refresh the Index](#refresh-the-index)
  - [Search](#search)
  - [Delete Documents](#delete-documents)
  - [Delete the Index](#delete-the-index)

# Asynchronous I/O

This client supports asynchronous I/O that improves performance and increases throughput. See [hello_async.py](../samples/hello/hello_async.py) or [knn_async_basics.py](../samples/knn/knn_async_basics.py) for a working asynchronous sample.

## Setup

To add the async client to your project, install it using [pip](https://pip.pypa.io/):

```bash
pip install opensearch-py[async]
```

In general, we recommend using a package manager, such as [poetry](https://python-poetry.org/docs/), for your projects. This is the package manager used for [samples](../samples). The following example includes `opensearch-py[async]` in `pyproject.toml`.

```toml
[tool.poetry.dependencies]
opensearch-py = { path = "../", extras=["async"] }
```

## Async Loop

```python
import asyncio

async def main():
    client = AsyncOpenSearch(...)
    try:
        # your code here
    finally:
        client.close()
    
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
```

## Connect to OpenSearch

```python
host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

client = AsyncOpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_show_warn = False
)

info = await client.info()
print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")
```

## Create an Index

```python
index_name = 'test-index'

index_body = {
    'settings': {
        'index': {
            'number_of_shards': 4
        }
    }
}

if not await client.indices.exists(index=index_name):
    await client.indices.create(
        index_name, 
        body=index_body
    )
```

## Index Documents

```python
await asyncio.gather(*[
    client.index(
        index = index_name,
        body = {
            'title': f"Moneyball {i}",
            'director': 'Bennett Miller',
            'year': '2011'
        },
        id = i
    ) for i in range(10)
])
```

## Refresh the Index

```python
await client.indices.refresh(index=index_name)
```

## Search

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

    results = await client.search(
        body = query,
        index = index_name
    )

    for hit in results["hits"]["hits"]:
      print(hit)
```

## Delete Documents

```python
await asyncio.gather(*[
    client.delete(
        index = index_name,
        id = i
    ) for i in range(10)
])
```

## Delete the Index

```python
await client.indices.delete(
    index = index_name
)
```
