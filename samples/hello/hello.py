#!/usr/bin/env python

# A basic OpenSearch "Hello World" sample that prints the version of the server.

from opensearchpy import OpenSearch

# connect to OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_show_warn = False
)

info = client.info()
print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")

# create an index

index_name = 'test-index'

index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(
  index_name, 
  body=index_body
)

print(response)

# add a document to the index

document = {
  'title': 'Moneyball',
  'director': 'Bennett Miller',
  'year': '2011'
}

id = '1'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print(response)

# search for a document

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

response = client.search(
    body = query,
    index = index_name
)

print(response)

# delete the document

response = client.delete(
    index = index_name,
    id = id
)

print(response)

# delete the index

response = client.indices.delete(
    index = index_name
)

print(response)
