#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import asyncio

from opensearchpy import AsyncOpenSearch


async def main() -> None:
    # connect to OpenSearch
    host = "localhost"
    port = 9200
    auth = ("admin", "admin")  # For testing only. Don't store credentials in code.

    client = AsyncOpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    try:
        info = await client.info()
        print(
            f"Welcome to {info['version']['distribution']} {info['version']['number']}!"
        )

        # create an index

        index_name = "test-index"

        index_body = {"settings": {"index": {"number_of_shards": 4}}}

        if not await client.indices.exists(index=index_name):
            await client.indices.create(index_name, body=index_body)

        # add some documents to the index, asynchronously
        await asyncio.gather(
            *[
                client.index(
                    index=index_name,
                    body={
                        "title": f"Moneyball {i}",
                        "director": "Bennett Miller",
                        "year": "2011",
                    },
                    id=i,
                )
                for i in range(10)
            ]
        )

        # refresh the index
        await client.indices.refresh(index=index_name)

        # search for a document
        q = "miller"

        query = {
            "size": 5,
            "query": {"multi_match": {"query": q, "fields": ["title^2", "director"]}},
        }

        results = await client.search(body=query, index=index_name)

        for hit in results["hits"]["hits"]:
            print(hit)

        # delete the documents
        await asyncio.gather(
            *[client.delete(index=index_name, id=i) for i in range(10)]
        )

        # delete the index
        await client.indices.delete(index=index_name)

    finally:
        await client.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
