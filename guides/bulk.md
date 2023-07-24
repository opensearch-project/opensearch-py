- [Bulk Indexing](#bulk-indexing)
  - [Use a Helper](#use-a-helper)

# Bulk Indexing

The [Bulk API](https://opensearch.org/docs/latest/api-reference/document-apis/bulk/) lets you add, update, or delete multiple documents in a single request.

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

response = client.bulk(docs)
print(response)
```

## Use a Helper

```python
from opensearchpy import OpenSearch, helpers

client = OpenSearch(...)

docs = []
def generate_data():
    mywords = ['foo', 'bar', 'baz']
    for index, word in enumerate(mywords):
        docs.append({
            "_index": "mywords",
            "word": word,
            "_id": index
        })
    return docs

response = helpers.bulk(client, generate_data(), max_retries=3)
print(response)
```
