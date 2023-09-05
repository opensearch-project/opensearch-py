# Advanced Index Actions Guide
- [Advanced Index Actions](#advanced-index-actions)
  - [Setup](#setup)
  - [Api Actions](#api-actions)
    - [Clear Index Cache](#clear-index-cache)
    - [Flush Index](#flush-index)
    - [Refresh Index](#refresh-index)
    - [Open/Close Index](#open-close-index)
    - [Force merge index](#force-merge-index)
    - [Clone index](#clone-index)
    - [Split index](#split-index)
  - [Cleanup](#cleanup)
# Advanced Index Actions

In this guide, we will look at some advanced index actions that are not covered in the [Index Lifecycle](index_lifecycle.md) guide.

## Setup

Let's create a client instance, and an index named `movies`:

```python
from opensearchpy import OpenSearch
client = OpenSearch(
    hosts=['https://admin:admin@localhost:9200'],
    use_ssl=True,
    verify_certs=False
)
client.indices.create(index='movies')
```

## API Actions

### Clear Index Cache

You can clear the cache of an index or indices by using the `indices.clear_cache` API action. The following example clears the cache of the `movies` index:

```python
client.indices.clear_cache(index='movies')
```

By default, the `indices.clear_cache` API action clears all types of cache. To clear specific types of cache pass the the `query`, `fielddata`, or `request` parameter to the API action:

```python
client.indices.clear_cache(index='movies', query=True)
client.indices.clear_cache(index='movies', fielddata=True, request=True)
```

### Flush Index

Sometimes you might want to flush an index or indices to make sure that all data in the transaction log is persisted to the index. To flush an index or indices use the `indices.flush` API action. The following example flushes the `movies` index:

```python
client.indices.flush(index='movies')
```

### Refresh Index

You can refresh an index or indices to make sure that all changes are available for search. To refresh an index or indices use the `indices.refresh` API action:

```python
client.indices.refresh(index='movies')
```

### Open/Close Index

You can close an index to prevent read and write operations on the index. A closed index does not have to maintain certain data structures that an opened index require, reducing the memory and disk space required by the index. The following example closes and reopens the `movies` index:

```python
client.indices.close(index='movies')
client.indices.open(index='movies')
```

### Force merge index

You can force merge an index or indices to reduce the number of segments in the index. This can be useful if you have a large number of small segments in the index. Merging segments reduces the memory footprint of the index. Do note that this action is resource intensive and it is only recommended for read-only indices. The following example force merges the `movies` index:

```python
client.indices.forcemerge(index='movies')
```

### Clone index

You can clone an index to create a new index with the same mappings, data, and MOST of the settings. The source index must be in read-only state for cloning. The following example blocks write operations from `movies` index, clones the said index to create a new index named `movies_clone`, then re-enables write:

```python
client.indices.put_settings(index='movies', body={'index': {'blocks': {'write': True}}})
client.indices.clone(index='movies', target='movies_clone')
client.indices.put_settings(index='movies', body={'index': {'blocks': {'write': False}}})
```

### Split index

You can split an index into another index with more primary shards. The source index must be in read-only state for splitting. The following example create the read-only `books` index with 30 routing shards and 5 shards (which is divisible by 30), splits index into `bigger_books` with 10 shards (which is also divisible by 30), then re-enables write:

```python
client.indices.create(
  index='books',
  body={ 'settings': {
    'index': { 'number_of_shards': 5,
             'number_of_routing_shards': 30,
             'blocks': { 'write': True } } } })

client.indices.split(
  index='books',
  target='bigger_books',
  body={ 'settings': { 'index': { 'number_of_shards': 10 } } })

client.indices.put_settings(index='books', body={ 'index': { 'blocks': { 'write': False } } })
```

## Cleanup

Let's delete all the indices we created in this guide:

```python
client.indices.delete(index=['movies', 'books', 'movies_clone', 'bigger_books'])
```
