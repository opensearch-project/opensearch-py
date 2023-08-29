# Advanced Index Actions

To perform the advanced index actions using the OpenSearch Python client, you can use the `opensearch-py` library. Here's how you can do it:

## Setup
First, make sure you have the `opensearch-py` library installed. You can install it using pip:

```bash
pip install opensearch-py
```
Let's create an OpenSearch client instance with configuration


Now, you can use the library to perform the advanced index actions:

```python
from opensearchpy import OpenSearch

# Create an OpenSearch client instance
client = OpenSearch(
    hosts=['https://admin:admin@localhost:9200'],  # Replace with your OpenSearch URL and credentials
    use_ssl=False,  # Set to True if using SSL
    verify_certs=False  # Set to True to verify SSL certificates
)
```
## API Actions

### Create an index named 'movies'

Establishing a structure for data storage, such as defining fields and mappings for the 'movies' dataset.

```python
client.indices.create(index='movies')
```

### Clear index cache

Removing stored cache data related to the 'movies' index to improve query performance.

```python
client.indices.clear_cache(index='movies')
```

### Flush index

Forcing the immediate write of pending data to the 'movies' index for data durability.
```python
client.indices.flush(index='movies')
```

### Refresh index

Making recent changes in the 'movies' index immediately available for search.

```python
client.indices.refresh(index='movies')
```

### Close index and Reopen Index

Temporarily suspending read and write operations on the 'movies' index, then resuming access.

```python
client.indices.close(index='movies')
```

```python
client.indices.open(index='movies')
```

### Force merge index

Reducing resource usage and improving performance by merging smaller segments in the 'movies' index.

```python
client.indices.forcemerge(index='movies')
```
### Setting a Write Block
Setting a write block to 'True' for the 'movies' index, preventing write operations on the index, making it read-only.

This action ensures that no new data can be added to the 'movies' index until the write block is set to 'False', providing data protection or a controlled environment for certain use cases.

```python
client.indices.put_settings(
    index='movies',
    body={
        'index': {
            'blocks': {
                'write': True
            }
        }
    }
)
```

### Clone index

Creating a new index ('movies_clone') identical to 'movies,' preserving its structure and data.

```python
client.indices.clone(index='movies', target='movies_clone')
```

### Split index

Let's fist create an index with number of shards 5 and number of routing shards 30  
```python
client.indices.create(
    index='books',
    body={
        'settings': {
            'index.number_of_shards': 5,
            'index.number_of_routing_shards': 30,
            'index.blocks.write': True
        }
    }
)
```

Dividing the 'books' index into a new 'bigger_books' index with more primary shards for scalability.

```python
client.indices.split(
    index='books',
    target='bigger_books',
    body={'settings.index.number_of_shards': 10}
)
```

### Delete indices

Removing multiple indices ('movies,' 'books,' 'movies_clone,' 'bigger_books') to clean up and manage data.

```python
client.indices.delete(index=['movies', 'books', 'movies_clone', 'bigger_books'])
```

## Snapshots
To use a shared file system as a snapshot repository, add it to opensearch.yml:

```bash
path.repo: ["/mnt/snapshots"]
```
On the RPM and Debian installs, you can then mount the file system. If you’re using the Docker install, add the file system to each node in docker-compose.yml before starting the cluster:

```bash
volumes:
  - /Users/jdoe/snapshots:/mnt/snapshots
```


### Create Repository
Define the repository name and snapshot name and create a repository (if it doesn't exist)
```python
repository_name = "my_repository"
snapshot_name = "my_snapshot"


client.snapshot.create_repository(
    repository=repository_name,
    body={
        "type": "fs",  # You can use other repository types like S3
        "settings": {
            "location": "/path/to/your/repository"  # Specify the path to your backup repository
        }
    }
)
```

### Take Snapshot

Take a snapshot of the 'movies' index

```python
client.snapshot.create(
    repository=repository_name,
    snapshot=snapshot_name,
    body={
        "indices": "movies",  # Replace with the name of the index you want to snapshot
        "include_global_state": false   
    }
)
```

### Restore snapshot 

To restore a snapshot of index movies

```python
client.snapshot.restore(
    repository=repository_name,
    snapshot=snapshot_name,
    body={
        "indices": "movies",  # Replace with the index name you want to restore
        "rename_pattern": "movies",  # Optional: Rename the index during restoration
        "rename_replacement": "restored_movies"  # Optional: New index name
    }
)
```