
# Search
OpenSearch provides a powerful search API that allows you to search for documents in an index. The search API supports a number of parameters that allow you to customize the search operation. In this guide, we will explore the search API and its parameters.

# Setup
Let's start by creating an index and adding some documents to it:

```python
from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

# Provide a CA bundle if you use intermediate CAs with your root CA.
# If this is not given, the CA bundle is is discovered from the first available
# following options:
# - OpenSSL environment variables SSL_CERT_FILE and SSL_CERT_DIR
# - certifi bundle (https://pypi.org/project/certifi/)
# - default behavior of the connection backend (most likely system certs)
ca_certs_path = '/full/path/to/root-ca.pem'

# Optional client certificates if you don't want to use HTTP basic authentication.
# client_cert_path = '/full/path/to/client.pem'
# client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path
)

client.indices.create('movies')


# Adding documents to index
for i in range(10):
    client.index(
        index = 'movies',
        body = {
            'title': f'The Dark Knight #{i}',
            'director': 'Christopher Nolan',
            'year': 2008 + i
        },
        id = i,
    )
client.index(
        index = 'movies',
        body = {
            'title': 'The Godfather',
            'director': 'Francis Ford Coppola',
            'year': 1972
        },
        
)
client.index(
        index = 'movies',
        body = {
            'title': 'The Shawshank Redemption',
            'director': 'Frank Darabont',
            'year': 1994
        },
        
)
client.indices.refresh(index = 'movies')
```

## Search API

### Basic Search

The search API allows you to search for documents in an index. The following example searches for ALL documents in the `movies` index:

```python
response = client.search(index = 'movies')['hits']['hits']
print(response)
```

You can also search for documents that match a specific query. The following example searches for documents that match the query `dark knight`:

```python
response = client.search(
    body = {
        'query':{
            'match':{
                'title':'dark knight'
            }
        }
    },
    index = 'movies'
)['hits']['hits']
print(response)
```

OpenSearch query DSL allows you to specify complex queries. Check out the [OpenSearch query DSL documentation](https://opensearch.org/docs/latest/query-dsl/) for more information.

### Basic Pagination

The search API allows you to paginate through the search results. The following example searches for documents that match the query `dark knight`, sorted by `year` in ascending order, and returns the first 2 results after skipping the first 5 results:

```python
search_body = {
    'query': {
        'match': {
            'title': 'dark knight'
        }
    },
    'sort':[
        {
            'year':{
                'order':'asc'
            }
        }
    ]
}

response = client.search(
    index = 'movies',
    from_ = 5,
    size  = 2,
    body  = search_body
)['hits']['hits']
print(response)
```

With sorting, you can also use the `search_after` parameter to paginate through the search results. Let's say you have already displayed the first page of results, and you want to display the next page. You can use the `search_after` parameter to paginate through the search results. The following example will demonstrate how to get the first 3 pages of results using the search query of the previous example:

```python
page_1 = client.search(
    index='movies',
    size=2,
    body=search_body
)['hits']['hits']
search_body.update({'search_after': page_1[-1]['sort']})

page_2 = client.search(
    index='movies',
    size=2,
    body=search_body
)['hits']['hits']
search_body.update({'search_after': page_2[-1]['sort']})

page_3 = client.search(
    index='movies',
    size=2,
    body=search_body
)['hits']['hits']
search_body.update({'search_after': page_3[-1]['sort']})
```

### Pagination with scroll

When retrieving large amounts of non-real-time data, you can use the `scroll` parameter to paginate through the search results. 

```python
page_1 = client.search(
    index='movies',
    scroll = '1m',
    size=2,
    body=search_body
)
page_2 = client.scroll(
    scroll_id = page_1['_scroll_id'],
    scroll = '1m'
)
page_3 = client.scroll(
    scroll_id = page_2['_scroll_id'],
    scroll = '1m'
)
```

### Pagination with Point in Time

The scroll example above has one weakness: if the index is updated while you are scrolling through the results, they will be paginated inconsistently. To avoid this, you should use the "Point in Time" feature. The following example demonstrates how to use the `point_in_time` and `pit_id` parameters to paginate through the search results:

```python
# create a point in time
pit = client.create_point_in_time(
  index = 'movies',
  keep_alive = '1m'
)

# Include pit info in the search body
search_body.update(
  {'pit': {
    'id': pit['pit_id'],
    'keep_alive': '1m'
  }
  })
pit_search_body = search_body
# Get the first 3 pages of results
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

# Print out the titles of the first 3 pages of results
print([hit['_source']['title'] for hit in page_1])
print([hit['_source']['title'] for hit in page_2])
print([hit['_source']['title'] for hit in page_3])


# delete the point in time
client.delete_point_in_time(body = { 'pit_id': pit['pit_id'] })
```
Note that a point-in-time is associated with an index or a set of index. So, when performing a search with a point-in-time, you DO NOT specify the index in the search.

## Cleanup

```python
client.indices.delete(index = 'movies')
```