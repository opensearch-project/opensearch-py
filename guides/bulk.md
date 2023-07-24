- [Bulk Indexing](#bulk-indexing)
  - [Line-Delimited JSON](#line-delimited-json)
  - [Bulk Helper](#bulk-helper)

# Bulk Indexing

The [Bulk API](https://opensearch.org/docs/latest/api-reference/document-apis/bulk/) lets you add, update, or delete multiple documents in a single request.

## Line-Delimited JSON

The `bulk` API accepts line-delimited JSON. This method requires the caller to evaluate the return value and parse errors in the case of a failure or partial success. See [samples/bulk/bulk-ld.py](../samples/bulk/bulk-ld.py) for a working sample.

```python
from opensearchpy import OpenSearch

client = OpenSearch(...)

docs = '''
{"index": {"_index": "index-2022-06-08", "_id": "1"}}
{"name": "foo"} 
{"index": {"_index": "index-2022-06-09", "_id": "2"}}
{"name": "bar"}
{"index": {"_index": "index-2022-06-10", "_id": "3"}}
{"name": "baz"}
'''

response = client.bulk(data)
if response["errors"]:
    print(f"There were errors!")
else:
    print(f"Bulk-inserted {len(rc['items'])} items.")
```

## Bulk Helper

A helper can generate the line-delimited JSON for you from a Python array that contains `_index` and `_id` fields, and parse errors. The `helpers.bulk` implementation will raise `BulkIndexError` if any error occurs. This may indicate a partially successful result. See [samples/bulk/bulk-helpers.py](../samples/bulk/bulk-helpers.py) for a working sample.

```python
from opensearchpy import OpenSearch, helpers

client = OpenSearch(...)

docs = [
    { "_index": "words", "_id": "word1", word: "foo" },
    { "_index": "words", "_id": "word2", word: "bar" },
    { "_index": "words", "_id": "word3", word: "baz" },
]

response = helpers.bulk(client, docs, max_retries=3)
print(response)
```

