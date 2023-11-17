#!/usr/bin/env python

# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import os

from opensearchpy import OpenSearch, helpers

# connect to an instance of OpenSearch

host = os.getenv("HOST", default="localhost")
port = int(os.getenv("PORT", 9200))
auth = (os.getenv("USERNAME", "admin"), os.getenv("PASSWORD", "admin"))

client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
)

# check whether an index exists
index_name = "my-index"

if not client.indices.exists(index_name):
    client.indices.create(
        index_name,
        body={
            "mappings": {
                "properties": {
                    "value": {"type": "float"},
                }
            }
        },
    )

# index data
data = []
for i in range(100):
    data.append({"_index": index_name, "_id": i, "value": i})

# serialized bulk raising an exception on error
rc = helpers.bulk(client, data)
print(f"Bulk-inserted {rc[0]} items.")

# parallel bulk with explicit error checking
succeeded = []
failed = []
for success, item in helpers.parallel_bulk(
    client,
    actions=data,
    chunk_size=10,
    raise_on_error=False,
    raise_on_exception=False,
    max_chunk_bytes=20 * 1024 * 1024,
    request_timeout=60,
):
    if success:
        succeeded.append(item)
    else:
        failed.append(item)

if len(failed) > 0:
    print(f"There were {len(failed)} errors:")
    for item in failed:
        print(item["index"]["error"])

if len(succeeded) > 0:
    print(f"Bulk-inserted {len(succeeded)} items.")

# delete index
client.indices.delete(index=index_name)
