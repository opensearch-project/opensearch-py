#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from opensearchpy import OpenSearch

import tempfile

# connect to OpenSearch

host = "localhost"
port = 9200
auth = ("admin", "admin")  # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False
)

# Create an index

index_name = "test-snapshot"
client.indices.create(index=index_name)

# Create a temporary directory for the snapshot repository
temp_repo = tempfile.TemporaryDirectory()
temp_repo_location = "/usr/share/opensearch/backups"

# Define the repository body with the temporary location
repo_body = {
    "type": "fs",  # Replace 'fs' with the appropriate repository type
    "settings": {
        "location": temp_repo_location,  # Replace with the desired repository location
    }
}

repository_name = "my_repository"
response = client.snapshot.create_repository(repository=repository_name, body=repo_body)

print(response)

# Create a snapshot

snapshot_name = "my_snapshot"
response = client.snapshot.create(repository=repository_name, snapshot=snapshot_name, body={"indices": index_name})

print(response)

# Get Snapshot Information

snapshot_info = client.snapshot.get(repository=repository_name, snapshot=snapshot_name)

print(snapshot_info)

# Clean up - Delete Snapshot and Repository

client.snapshot.delete(repository=repository_name, snapshot=snapshot_name)
client.snapshot.delete_repository(repository=repository_name)

# Clean up - Delete Index

client.indices.delete(index=index_name)
