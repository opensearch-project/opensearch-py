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
import os

from opensearchpy import AsyncOpenSearch


async def main() -> None:
    """
    This sample uses asyncio and AsyncOpenSearch to asynchronously
    connect to local OpenSearch cluster, performs a search query on an index,
    retrieves the first page of results, and fetches the next page of results
    using the search_after parameter.
    """

    # connect to OpenSearch
    host = "localhost"
    port = 9200
    auth = (
        "admin",
        os.getenv("OPENSEARCH_PASSWORD", "admin"),
    )  # For testing only. Don't store credentials in code.

    client = AsyncOpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    # create an index
    await client.indices.create(index="movies")

    try:
        # add a large dataset (100 movies)
        for i in range(15):
            await client.index(
                index="movies",
                id=i,
                body={
                    "title": f"The Dark Knight {i}",
                    "director": "Christopher Nolan",
                    "year": 2008 + i,
                },
            )

        for i in range(95):
            await client.index(
                index="movies",
                id=i + 15,
                body={
                    "title": f"Movie Title {i + 15}",
                    "director": f"Director {i + 15}",
                    "year": 1950 + i + 15,
                },
            )

        # refresh the index to make the documents searchable
        await client.indices.refresh(index="movies")

        # define the search query with sorting and pagination options
        search_body = {
            "query": {"match": {"title": "dark knight"}},
            "sort": [{"year": {"order": "asc"}}],
            "size": 10,
        }

        page = 1
        total_hits = 0
        while True:
            # execute the search
            response = await client.search(index="movies", body=search_body)
            hits = response["hits"]["hits"]

            # break if no more results
            if not hits:
                break

            print(f"\nPage {page}:")

            for hit in hits:
                print(hit)
                total_hits += 1

            # get the sort values of the last document for the next page
            last_sort = hits[-1]["sort"]
            search_body["search_after"] = last_sort
            page += 1

        print("\nPagination Summary:")
        print(f"Total pages: {page - 1}")
        print(f"Total hits: {total_hits}")
        print(f"Results per page: {search_body['size']}")
    finally:
        # delete the index
        await client.indices.delete(index="movies")
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
