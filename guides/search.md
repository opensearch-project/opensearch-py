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
