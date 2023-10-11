from opensearchpy import OpenSearch

# Create a client instance
client = OpenSearch(
  hosts=['https://localhost:9200'],
  use_ssl=True,
  verify_certs=False,
  http_auth=('admin', 'admin')
)

# You can create an index template to define default settings and mappings for indices of certain patterns. The following example creates an index template named `books` with default settings and mappings for indices of the `books-*` pattern:
client.indices.put_index_template(
name='books',
body={
  'index_patterns': ['books-*'],
  'priority': 1,
  'template': {
    'settings': {
      'index': {
        'number_of_shards': 3,
        'number_of_replicas': 0
      }
    },
    'mappings': {
      'properties': {
        'title': { 'type': 'text' },
        'author': { 'type': 'text' },
        'published_on': { 'type': 'date' },
        'pages': { 'type': 'integer' }
      }
    }
  }
}
)

# Now, when you create an index that matches the `books-*` pattern, OpenSearch will automatically apply the template's settings and mappings to the index. Let's create an index named books-nonfiction and verify that its settings and mappings match those of the template:
client.indices.create(index='books-nonfiction')
print(client.indices.get(index='books-nonfiction'))

# If multiple index templates match the index's name, OpenSearch will apply the template with the highest `priority`. The following example creates two index templates named `books-*` and `books-fiction-*` with different settings:
client.indices.put_index_template(
name='books',
body={
  'index_patterns': ['books-*'],
  'priority': 1,
  'template': {
    'settings': {
      'index': {
        'number_of_shards': 3,
        'number_of_replicas': 0
      }
    }
  }
}
)

client.indices.put_index_template(
name='books-fiction',
body={
  'index_patterns': ['books-fiction-*'],
  'priority': 2,
  'template': {
    'settings': {
      'index': {
        'number_of_shards': 1,
        'number_of_replicas': 1
      }
    }
  }
}
)

# # Test multiple index templates
client.indices.create(index='books-fiction-romance')
print(client.indices.get(index='books-fiction-romance'))


# Composable index templates are a new type of index template that allow you to define multiple component templates and compose them into a final template. The following example creates a component template named `books_mappings` with default mappings for indices of the `books-*` and `books-fiction-*` patterns:
client.cluster.put_component_template(
name='books_mappings',
body={
  'template': {
    'mappings': {
      'properties': {
        'title': { 'type': 'text' },
        'author': { 'type': 'text' },
        'published_on': { 'type': 'date' },
        'pages': { 'type': 'integer' }
      }
    }
  }
}
)

client.indices.put_index_template(
name='books',
body={
  'index_patterns': ['books-*'],
  'composed_of': ['books_mappings'],
  'priority': 4,
  'template': {
    'settings': {
      'index': {
        'number_of_shards': 3,
        'number_of_replicas': 0
      }
    }
  }
}
)

client.indices.put_index_template(
name='books-fiction',
body={
  'index_patterns': ['books-fiction-*'],
  'composed_of': ['books_mappings'],
  'priority': 5,
  'template': {
    'settings': {
      'index': {
        'number_of_shards': 1,
        'number_of_replicas': 1
      }
    }
  }
}
)


# Test composable index templates
client.indices.create(index='books-fiction-horror')
print(client.indices.get(index='books-fiction-horror'))

# Get an index template
print(client.indices.get_index_template(name='books'))

# Delete an index template
client.indices.delete_index_template(name='books')

# Cleanup
client.indices.delete(index='books-*')
client.indices.delete_index_template(name='books-fiction')
client.cluster.delete_component_template(name='books_mappings')