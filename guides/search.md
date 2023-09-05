- [Search](#search)
  - [Setup](#setup)
  - [Search API](#search-api)
    - [Basic Search](#basic-search)
    - [Basic Pagination](#basic-pagination)
    - [Pagination with Scroll](#pagination-with-scroll)
    - [Pagination with Point in Time](#pagination-with-point-in-time)
  - [Cleanup](#cleanup)

# Search

OpenSearch provides a powerful search API that allows you to search for documents in an index. The search API supports a number of parameters that allow you to customize the search operation. In this guide, we will explore the search API and its parameters.

## Setup

Let's start by creating an index and adding some documents to it:

```python
from opensearchpy import OpenSearch
# create an OpenSearch client
client = OpenSearch(hosts=['localhost'])

# create an index
client.indices.create(index='movies')

# add 10 documents to the index
for i in range(10):
    client.index(
        index='movies',
        id=i,
        body={
            'title': f'The Dark Knight {i}',
            'director': 'Christopher Nolan',
            'year': 2008 + i
        }
    )

# add additional documents to the index
client.index(
    index='movies',
    body={
        'title': 'The Godfather',
        'director': 'Francis Ford Coppola',
        'year': 1972
    }
)

client.index(
    index='movies',
    body={
        'title': 'The Shawshank Redemption',
        'director': 'Frank Darabont',
        'year': 1994
    }
)

# refresh the index to make the documents searchable
client.indices.refresh(index='movies')
```

## Search API

### Basic Search

The search API allows you to search for documents in an index. The following example searches for ALL documents in the `movies` index:

```python
# search for all documents in the 'movies' index
response = client.search(index='movies')

# extract the count of hits from the response
hits_count = response['hits']['total']['value']

# print the count of hits
print("Total Hits: ", hits_count)
```

You can also search for documents that match a specific query. The following example searches for documents that match the query `dark knight`:

```python
# define the query
query = {
    "query": {
        "match": {
            "title": "dark knight"
        }
    }
}

# search for documents in the 'movies' index with the given query
response = client.search(index='movies', body=query)

# extract the hits from the response
hits = response['hits']['hits']

# print the hits
for hit in hits:
    print(hit)
```

OpenSearch query DSL allows you to specify more complex queries. Check out the [OpenSearch query DSL documentation](https://opensearch.org/docs/latest/query-dsl/) for more information.

### Basic Pagination

The search API allows you to paginate through the search results. The following example searches for documents that match the query `dark knight`, sorted by `year` in ascending order, and returns the first 2 results after skipping the first 5 results:

```python
# define the search query with sorting and pagination options
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

# perform the search operation on the 'movies' index with the defined query and pagination options
response = client.search(
    index='movies',
    size=2,
    from_=5,
    body=search_body
)

# extract the hits from the response
hits = response['hits']['hits']

# print the hits
for hit in hits:
    print(hit)
```

With sorting, you can also use the `search_after` parameter to paginate through the search results. Let's say you have already displayed the first page of results, and you want to display the next page. You can use the `search_after` parameter to paginate through the search results. The following example will demonstrate how to get the first 3 pages of results using the search query of the previous example:

```python
# define the search query with sorting and pagination options
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

# perform the search operation on the 'movies' index with the defined query and pagination options
response = client.search(
    index='movies',
    body=search_body
)

# extract the hits from the response
hits = response['hits']['hits']

# get the last sort value from the first page
search_after = hits[-1]['sort']

# fetch page 2
search_body["search_after"] = search_after
response = client.search(
    index='movies',
    body=search_body
)
hits_page_2 = response['hits']['hits']

# get the last sort value from page 2
search_after = hits_page_2[-1]['sort']

# fetch page 3
search_body["search_after"] = search_after
response = client.search(
    index='movies',
    body=search_body
)

hits_page_3 = response['hits']['hits']
# print the hits from each page
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

### Pagination with Scroll

When retrieving large amounts of non-real-time data, you can use the `scroll` parameter to paginate through the search results. 

```python
# define the search query with scroll and pagination options
search_body = {
    "query": {
        "match": {
            "title": "dark knight"
        }
    },
    "size": 2
}

# perform the initial search operation on the 'movies' index with the defined query and scroll options
page_1 = client.search(
    index='movies',
    scroll='1m',
    body=search_body
)

# extract the scroll_id from the response
scroll_id = page_1['_scroll_id']

# perform the scroll operation to get the next page of results
page_2 = client.scroll(
    scroll_id=scroll_id,
    scroll='1m'
)

# extract the scroll_id from the response
scroll_id = page_2['_scroll_id']

# perform another scroll operation to get the third page of results
page_3 = client.scroll(
    scroll_id=scroll_id,
    scroll='1m'
)

# extract the hits from each page of results
hits_page_1 = page_1['hits']['hits']
hits_page_2 = page_2['hits']['hits']
hits_page_3 = page_3['hits']['hits']
```

### Pagination with Point in Time

The scroll example above has one weakness: if the index is updated while you are scrolling through the results, they will be paginated inconsistently. To avoid this, you should use the "Point in Time" feature. The following example demonstrates how to use the `point_in_time` and `pit_id` parameters to paginate through the search results:

```python
# define the search query with sorting and pagination options
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

# create a point in time
pit = client.create_point_in_time(
  index = 'movies',
  keep_alive = '1m'
)

# include pit info in the search body
search_body.update(
    {
        'pit': {
            'id': pit['pit_id'],
            'keep_alive': '1m'
        }
    }
)
pit_search_body = search_body
# get the first 3 pages of results
page_1 = client.search(
  size = 2,
  body = pit_search_body
)['hits']['hits']
pit_search_body.update({'search_after':page_1[-1]['sort']})
page_2 = client.search(
  size = 2,
  body = pit_search_body
)['hits']['hits']
pit_search_body.update({'search_after':page_2[-1]['sort']})
page_3 = client.search(
  size = 2,
  body = pit_search_body
)['hits']['hits']

# print out the titles of the first 3 pages of results
print([hit['_source']['title'] for hit in page_1])
print([hit['_source']['title'] for hit in page_2])
print([hit['_source']['title'] for hit in page_3])

# delete the point in time
client.delete_point_in_time(body = { 'pit_id': pit['pit_id'] })
```

## Cleanup

```python
client.indices.delete(index='movies')
```
