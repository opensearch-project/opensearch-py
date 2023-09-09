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
Define the repository name and create a repository (if it doesn't exist)
### Define a repository for storing snapshots in your file system
```python
repository_name = "my_repository"
repository_settings = {
        "type": "fs",  # You can use other repository types like S3
        "settings": {
            "location": "/path/to/your/repository"  # Specify the path to your backup repository
        }
}
```

### Define a repository for storing snapshots in cloud storage
```python
repository_name = "my_s3_repository"
repository_settings = {
    "type": "s3",
    "settings": {
        "bucket": "my-backup-bucket",
        "region": "us-east-1",
        "base_path": "opensearch-backups"
    }
}
```
### Create the repository
```python
client.snapshot.create_repository(repository=repository_name, body=repository_settings)
```

### Take Snapshot

Take a snapshot of the 'movies' index

```python
snapshot_name = "my_snapshot"
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

### List all snapshots in a repository
```python
snapshots = client.snapshot.get(repository=repository_name)
print(snapshots)
```

### Delete a snapshot
```python
snapshot_to_delete = "old_snapshot"
response = client.snapshot.delete(repository=repository_name, snapshot=snapshot_to_delete)
print(response)
```

### Restore a snapshot
```python
snapshot_to_restore = "my_snapshot"
response = client.snapshot.restore(repository=repository_name, snapshot=snapshot_to_restore)
print(response)
```
