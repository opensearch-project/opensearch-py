#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import asyncio
import os
import random

from opensearchpy import AsyncOpenSearch, AsyncHttpConnection, helpers

async def main():
    # connect to an instance of OpenSearch
    host = os.getenv('HOST', default='localhost')
    port = int(os.getenv('PORT', 9200))
    auth = (
        os.getenv('USERNAME', 'admin'), 
        os.getenv('PASSWORD', 'admin')
    )

    client = AsyncOpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        connection_class=AsyncHttpConnection,
        ssl_show_warn = False
    )

    # check whether an index exists
    index_name = "my-index"
    dimensions = 5

    if not await client.indices.exists(index_name):
        await client.indices.create(index_name, 
            body={
                "settings":{
                    "index.knn": True
                },
                "mappings":{
                    "properties": {
                        "values": {
                            "type": "knn_vector", 
                            "dimension": dimensions
                        },
                    }
                }
            }
        )

    # index data
    vectors = []
    for i in range(10):
        vec = []
        for j in range(dimensions): 
            vec.append(round(random.uniform(0, 1), 2)) 
    
        vectors.append({
            "_index": index_name,
            "_id": i,
            "values": vec,
        })

    # bulk index
    await helpers.async_bulk(client, vectors)

    await client.indices.refresh(index=index_name)

    # search
    vec = []
    for j in range(dimensions): 
        vec.append(round(random.uniform(0, 1), 2)) 
    print(f"Searching for {vec} ...")

    search_query = {"query": {"knn": {"values": {"vector": vec, "k": 3}}}}
    results = await client.search(index=index_name, body=search_query)
    for hit in results["hits"]["hits"]:
        print(hit)

    # delete index
    await client.indices.delete(index=index_name)

    await client.close()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()

