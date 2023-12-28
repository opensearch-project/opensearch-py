#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import tempfile

from opensearchpy import OpenSearch

# connect to OpenSearch

HOST = "localhost"
PORT = 9200
auth = ("admin", "admin")  # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts=[{"host": HOST, "port": PORT}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
)

# Create an index

INDEX_NAME = "test-snapshot"
client.indices.create(index=INDEX_NAME)

# Create a temporary directory for the snapshot repository
temp_repo = tempfile.TemporaryDirectory()
TEMP_REPO_LOCATION = "/usr/share/opensearch/backups"

# Define the repository body with the temporary location
repo_body = {
    "type": "fs",  # Replace 'fs' with the appropriate repository type
    "settings": {
        "location": TEMP_REPO_LOCATION,  # Replace with the desired repository location
    },
}

REPOSITORY_NAME = "my_repository"
response = client.snapshot.create_repository(repository=REPOSITORY_NAME, body=repo_body)

print(response)

# Create a snapshot

SNAPSHOT_NAME = "my_snapshot"
response = client.snapshot.create(
    repository=REPOSITORY_NAME, snapshot=SNAPSHOT_NAME, body={"indices": INDEX_NAME}
)

print(response)

# Get Snapshot Information

snapshot_info = client.snapshot.get(repository=REPOSITORY_NAME, snapshot=SNAPSHOT_NAME)

print(snapshot_info)

# Clean up - Delete Snapshot and Repository

client.snapshot.delete(repository=REPOSITORY_NAME, snapshot=SNAPSHOT_NAME)
client.snapshot.delete_repository(repository=REPOSITORY_NAME)

# Clean up - Delete Index

client.indices.delete(index=INDEX_NAME)
