# Search
OpenSearch provides a powerful search API that allows you to search for documents in an index. The search API supports a number of parameters that allow you to customize the search operation. In this guide, we will explore the search API and its parameters.

# Setup
Let's start by creating an index and adding some documents to it:

```python
from opensearchpy import OpenSearch
# Create an OpenSearch client
client = OpenSearch(hosts=['localhost'])
# Create an index
client.indices.create(index='movies')
# Add 10 documents to the index
for i in range(10):
    client.index(
        index='movies',
        id=i,
        doc_type='_doc',
        body={
            'title': f'The Dark Knight {i}',
            'director': 'Christopher Nolan',
            'year': 2008 + i
        }
    )
# Add additional documents to the index
client.index(
    index='movies',
    doc_type='_doc',
    body={
        'title': 'The Godfather',
        'director': 'Francis Ford Coppola',
        'year': 1972
    }
)
client.index(
    index='movies',
    doc_type='_doc',
    body={
        'title': 'The Shawshank Redemption',
        'director': 'Frank Darabont',
        'year': 1994
    }
)
# Refresh the index to make the documents searchable
client.indices.refresh(index='movies')
```

## Search API

### Basic Search

The search API allows you to search for documents in an index. The following example searches for ALL documents in the `movies` index:

```python
from opensearchpy import OpenSearch
# Create an OpenSearch client
client = OpenSearch(hosts=['localhost'])
# Search for all documents in the 'movies' index
response = client.search(index='movies')
# Extract the count of hits from the response
hits_count = response['hits']['total']['value']
# Print the count of hits
print("Total Hits: ", hits_count)
```

You can also search for documents that match a specific query. The following example searches for documents that match the query `dark knight`:

```python
from opensearchpy import OpenSearch
# Create an OpenSearch client
client = OpenSearch(hosts=['localhost'])
# Define the query
query = {
    "query": {
        "match": {
            "title": "dark knight"
        }
    }
}
# Search for documents in the 'movies' index with the given query
response = client.search(index='movies', body=query)
# Extract the hits from the response
hits = response['hits']['hits']
# Print the hits
for hit in hits:
    print(hit)
```

OpenSearch query DSL allows you to specify complex queries. Check out the [OpenSearch query DSL documentation](https://opensearch.org/docs/latest/query-dsl/) for more information.

### Basic Pagination

The search API allows you to paginate through the search results. The following example searches for documents that match the query `dark knight`, sorted by `year` in ascending order, and returns the first 2 results after skipping the first 5 results:

```python
from opensearchpy import OpenSearch
# Create an OpenSearch client
client = OpenSearch(hosts=['localhost'])
# Define the query
query = {
    "query": {
        "match": {
            "title": "dark knight"
        }
    }
}
# Search for documents in the 'movies' index with the given query
response = client.search(index='movies', body=query)
# Extract the hits from the response
hits = response['hits']['hits']
# Print the hits
for hit in hits:
    print(hit)
```

With sorting, you can also use the `search_after` parameter to paginate through the search results. Let's say you have already displayed the first page of results, and you want to display the next page. You can use the `search_after` parameter to paginate through the search results. The following example will demonstrate how to get the first 3 pages of results using the search query of the previous example:

```python
from opensearchpy import OpenSearch
# Create an OpenSearch client
client = OpenSearch(hosts=['localhost'])
# Define the query and sort
query = {
    "query": {
        "match": {
            "title": "dark knight"
        }
    },
    "sort": [
        {
            "year": {
                "order": "asc"
            }
        }
    ]
}
# Perform the initial search to get the first page of results
response = client.search(index='movies', size=2, body=query)
page_1 = response['hits']['hits']
# Extract the sort value of the last hit in page 1
last_sort = page_1[-1]['sort']
# Perform subsequent searches to get next pages of results
response = client.search(index='movies', size=2, body=query, search_after=last_sort)
page_2 = response['hits']['hits']
# Extract the sort value of the last hit in page 2
last_sort = page_2[-1]['sort']
response = client.search(index='movies', size=2, body=query, search_after=last_sort)
page_3 = response['hits']['hits']
# Print the hits in each page
print("Page 1:")
for hit in page_1:
    print(hit)
print("Page 2:")
for hit in page_2:
    print(hit)
print("Page 3:")
for hit in page_3:
    print(hit)
```


### Pagination with scroll

When retrieving large amounts of non-real-time data, you can use the `scroll` parameter to paginate through the search results. 



### Pagination with Point in Time

The scroll example above has one weakness: if the index is updated while you are scrolling through the results, they will be paginated inconsistently. To avoid this, you should use the "Point in Time" feature. The following example demonstrates how to use the `point_in_time` and `pit_id` parameters to paginate through the search results:

```python
from opensearchpy import OpenSearch

# Create a client
client = OpenSearch([{'host': 'localhost'}])

# Create a point in time
pit = client.create_pit(
    index='movies',
    keep_alive='1m'
)

# Include pit info in the search body
pit_search_body = search_body.copy()
pit_search_body.update(
    {'pit': {'id': pit['pit_id'], 'keep_alive': '1m'}}
)

# Get the first 3 pages of results
page_1 = client.search(
    size=2,
    body=pit_search_body
)['hits']['hits']

page_2 = client.search(
    size=2,
    body=pit_search_body.update(
        {'search_after': page_1[-1]['sort']}
    )
)['hits']['hits']

page_3 = client.search(
    size=2,
    body=pit_search_body.update(
        {'search_after': page_2[-1]['sort']}
    )
)['hits']['hits']

# Print out the titles of the first 3 pages of results
print([hit['_source']['title'] for hit in page_1])
print([hit['_source']['title'] for hit in page_2])
print([hit['_source']['title'] for hit in page_3])

# Delete the point in time
client.delete_pit(body={'pit_id': pit['pit_id']})
```

## Cleanup

```python
client.indices.delete(index='movies')
```
