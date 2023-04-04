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
# Create an OpenSearch client with appropriate hosts and connection details
client = OpenSearch(hosts=['localhost'])
# Define the search query with sorting and pagination options
search_body = {
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
# Perform the search operation on the 'movies' index with the defined query and pagination options
response = client.search(
    index='movies',
    size=2,
    from_=5,
    body=search_body
)
# Extract the hits from the response
hits = response['hits']['hits']

# Print the hits
for hit in hits:
    print(hit)
```

With sorting, you can also use the `search_after` parameter to paginate through the search results. Let's say you have already displayed the first page of results, and you want to display the next page. You can use the `search_after` parameter to paginate through the search results. The following example will demonstrate how to get the first 3 pages of results using the search query of the previous example:

```python
# Import the required libraries
from opensearchpy import OpenSearch
# Create an OpenSearch client with appropriate hosts and connection details
client = OpenSearch(hosts=['localhost'])
# Define the search query with sorting and pagination options
search_body = {
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
    ],
    "size": 2
}
# Perform the search operation on the 'movies' index with the defined query and pagination options
response = client.search(
    index='movies',
    body=search_body
)
# Extract the hits from the response
hits = response['hits']['hits']
# Get the last sort value from the first page
search_after = hits[-1]['sort']
# Fetch page 2
search_body["search_after"] = search_after
response = client.search(
    index='movies',
    body=search_body
)
hits_page_2 = response['hits']['hits']
# Get the last sort value from page 2
search_after = hits_page_2[-1]['sort']
# Fetch page 3
search_body["search_after"] = search_after
response = client.search(
    index='movies',
    body=search_body
)
hits_page_3 = response['hits']['hits']
# Print the hits from each page
print("Page 1:")
for hit in hits:
    print(hit)
print("\nPage 2:")
for hit in hits_page_2:
    print(hit)
print("\nPage 3:")
for hit in hits_page_3:
    print(hit)
```


### Pagination with scroll

When retrieving large amounts of non-real-time data, you can use the `scroll` parameter to paginate through the search results. 

```python
from opensearchpy import OpenSearch
# Create an OpenSearch client with appropriate hosts and connection details
client = OpenSearch(hosts=['localhost'])
# Define the search query with scroll and pagination options
search_body = {
    "query": {
        "match": {
            "title": "dark knight"
        }
    },
    "scroll": "1m",  # Set the scroll duration to 1 minute
    "size": 2
}
# Perform the initial search operation on the 'movies' index with the defined query and scroll options
page_1 = client.search(
    index='movies',
    body=search_body
)
# Extract the scroll_id from the response
scroll_id = page_1['_scroll_id']
# Perform the scroll operation to get the next page of results
page_2 = client.scroll(
    scroll_id=scroll_id,
    scroll='1m'
)
# Extract the scroll_id from the response
scroll_id = page_2['_scroll_id']
# Perform another scroll operation to get the third page of results
page_3 = client.scroll(
    scroll_id=scroll_id,
    scroll='1m'
)
# Extract the hits from each page of results
hits_page_1 = page_1['hits']['hits']
hits_page_2 = page_2['hits']['hits']
hits_page_3 = page_3['hits']['hits']
```



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
