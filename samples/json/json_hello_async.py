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
        info = await client.http.get("/")
        print(
            f"Welcome to {info['version']['distribution']} {info['version']['number']}!"
        )

        # create an index

        index_name = "movies"

        index_body = {"settings": {"index": {"number_of_shards": 4}}}

        print(await client.http.put(f"/{index_name}", body=index_body))

        # add a document to the index

        document = {"title": "Moneyball", "director": "Bennett Miller", "year": "2011"}

        id = "1"

        print(
            await client.http.put(
                f"/{index_name}/_doc/{id}?refresh=true", body=document
            )
        )

        # search for a document

        q = "miller"

        query = {
            "size": 5,
            "query": {"multi_match": {"query": q, "fields": ["title^2", "director"]}},
        }

        print(await client.http.post(f"/{index_name}/_search", body=query))

        # delete the document

        print(await client.http.delete(f"/{index_name}/_doc/{id}"))

        # delete the index

        print(await client.http.delete(f"/{index_name}"))

    finally:
        await client.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
