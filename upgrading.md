Upgrading from opensearch-dsl-py to opensearch-py
==================================================

The following PR [#287](https://github.com/opensearch-project/opensearch-py/pull/287) merged opensearch-dsl-py into opensearch-py.

### Overview of architechtural changes:

The following files from dsl are added to "helpers" module - aggs, analysis, document, errors, faceted_search, field, function, index, mapping, query, search, update_by_query, utils, wrappers.

The file "connections" from dsl is added to "connection" module.

The files "serializer" and "exceptions" from dsl are merged into corresponding "searializer" and "exceptions" files in opensearchpy.

Opensearch-dsl-py is now using openseachpy workflows for test execution. 
### Usage differences

opensearch-dsl-py is merged into opensearch-py in a way to produce minimum differences for current opensearch-dsl-py users. Therefore, it creates easy transition from opensearch-dsl-py to opensearch-py.

One primary difference is in importing modules

Before:
```python
from opensearchpy import OpenSearch
    from opensearch_dsl import Search
```

Now:
```python
from opensearchpy import OpenSearch, Search
```








Errors changed:
