# Snapshot Actions
In this guide, we will look at some snapshot actions that allow you to manage and work with snapshots of your indices.


## Setup
Let's create a client instance, and an index named `movies`:
```python
from opensearchpy import OpenSearch

client = OpenSearch(
  hosts=['https://admin:admin@localhost:9200'],
  use_ssl=True,
  verify_certs=False
)

print(client.info())  # Check server info and make sure the client is connected
client.indices.create(index='movies')
```
## API Actions
### Create Snapshot Repository
Before taking a snapshot, you need to create a snapshot repository to store the snapshots. You can use the `create_repository` API action for this purpose. The following example creates a snapshot repository named `my_repository`:

```python
repo_body = {
    "type": "fs",  # Replace 'fs' with the appropriate repository type
    "settings": {
        "location": "/path/to/repo", 
    }
}
client.snapshot.create_repository(repository='my_repository', body=repo_body)
```

### Create Snapshot
To create a snapshot of an index, you can use the `create` method from the `snapshot` API. The following example creates a snapshot named `my_snapshot` for the movies index:

```python
client.snapshot.create(repository='my_repository', snapshot='my_snapshot', body={"indices": "movies"})
```

### Verify Snapshot Repository
The `verify_repository` API action allows you to verify a snapshot repository. Verifying a repository ensures that it is accessible and operational, but it does not validate the integrity of the snapshots stored within the repository. The following example verifies `my_repository`:

```python
response = client.snapshot.verify_repository(repository='my_repository')
```

### Delete Snapshot
To delete a specific snapshot, use the `delete` API action:

```python
client.snapshot.delete(repository='my_repository', snapshot='my_snapshot')
```
### Restore Snapshot
To restore a snapshot and recreate the indices, mappings, and data, you can use the `restore` method. The following example restores the `my_snapshot` snapshot:

```python
response = client.snapshot.restore(repository='my_repository', snapshot='my_snapshot')
```

### Get Snapshot Status
To check the status of a snapshot, you can use the `status` method.

```python
response = client.snapshot.status(repository='my_repository', snapshot='my_snapshot')
```

### Clone Snapshot
You can clone an existing snapshot to create a new snapshot with the same contents. The `clone` operation allows you to create multiple copies of a snapshot, which can be useful for backup retention or creating snapshots for different purposes. The following example clones a snapshot named `my_snapshot` to create a new snapshot named `my_snapshot_clone`:

```python
client.snapshot.clone(
    repository='my_repository',
    snapshot='my_snapshot',
    target_snapshot='my_snapshot_clone'
)
```
## Get Snapshot
To retrieve information about a specific snapshot, you can use the `get` API action. It provides metadata such as the snapshot's status, indices included in the snapshot, and the timestamp when the snapshot was taken. The following example retrieves information about the `my_snapshot`:

```python
response = client.snapshot.get(
    repository='my_repository',
    snapshot='my_snapshot'
)
```

## Get Repository
To retrieve information about a snapshot repository, you can use the `get_repository` API action. It provides details about the configured repository, including its type and settings. The following example retrieves information about the `my_repository`:

```python
response = client.snapshot.get_repository(repository='my_repository')
```

## Repository Analyze
The `repository_analyze` API action allows you to analyze a snapshot repository for correctness and performance. It checks for any inconsistencies or corruption in the repository. The following example performs a repository analysis on `my_repository`:

```python
response = client.snapshot.repository_analyze(repository='my_repository')
```

## Cleanup

Finally, let's delete the `movies` index and clean up all the snapshots and the repository:
```python
client.indices.delete(index='movies')
client.snapshot.delete(repository='my_repository', snapshot='my_snapshot')
client.snapshot.delete_repository(repository='my_repository')
```