#!/usr/bin/env python3
"""Bulk request script for OpenSearch."""

from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False,
)

INDEX = "test-bulk"

# Create index
client.indices.create(index=INDEX, body={"settings": {"number_of_shards": 1}}, ignore=400)

# Bulk request
actions = []
for i in range(100):
    actions.append({"index": {"_index": INDEX, "_id": i}})
    actions.append({"title": f"Document {i}", "value": i})

resp = client.bulk(body=actions, refresh=True)
print(f"Bulk indexed {len(actions)//2} docs, errors: {resp['errors']}")

# Verify
count = client.count(index=INDEX)
print(f"Total docs in '{INDEX}': {count['count']}")
