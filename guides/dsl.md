- [High Level DSL](#high-level-dsl)

## High Level DSL

The opensearch-py client includes a high level interface called opensearch-py-dsl that supports creating and indexing documents, searching with and without filters, and updating documents using queries. See [opensearch-dsl-py client documentation](https://opensearch.org/docs/latest/clients/python-high-level/) for details and [the API reference](https://github.com/opensearch-project/opensearch-py/tree/main/docs/source/api-ref).

In the below example, [Search API](https://github.com/opensearch-project/opensearch-py/blob/main/opensearchpy/helpers/search.py) from opensearch-dsl-py client is used. 

```python
from opensearchpy import OpenSearch, Search

client = OpenSearch(...)

s = Search(
        using=client, 
        index=index_name
    )
    .filter("term", category="search")
    .query("match", title="python")

response = s.execute()

for hit in response:
    print(hit.meta.score, hit.title)
```