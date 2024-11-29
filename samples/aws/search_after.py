#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import os

from opensearchpy import OpenSearch


def main() -> None:
    """
    An example showing how to use search_after to paginate through the search results.
    It performs a search query on an index, retrieves the first page of results,
    and then fetches the next page of results using the search_after parameter.
    """

    host = "localhost"
    port = 9200
    auth = (
        "admin",
        os.getenv("OPENSEARCH_PASSWORD", "admin"),
    )  # For testing only. Don't store credentials in code.

    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    # create an index
    client.indices.create(index="movies")

    try:
        # add 10 documents to the index
        for i in range(10):
            client.index(
                index="movies",
                id=i,
                body={
                    "title": f"The Dark Knight {i}",
                    "director": "Christopher Nolan",
                    "year": 2008 + i,
                },
            )

        # add additional documents to the index
        client.index(
            index="movies",
            body={
                "title": "The Godfather",
                "director": "Francis Ford Coppola",
                "year": 1972,
            },
        )

        client.index(
            index="movies",
            body={
                "title": "The Shawshank Redemption",
                "director": "Frank Darabont",
                "year": 1994,
            },
        )

        # refresh the index to make the documents searchable
        client.indices.refresh(index="movies")

        # define the search query with sorting and pagination options
        search_body = {
            "query": {"match": {"title": "dark knight"}},
            "sort": [{"year": {"order": "asc"}}],
            "size": 2,
        }

        # perform the search operation on the 'movies' index with the defined query and pagination options
        response = client.search(index="movies", body=search_body)

        # extract the hits from the response
        hits = response["hits"]["hits"]

        # get the last sort value from the first page
        search_after = hits[-1]["sort"]

        # fetch page 2
        search_body["search_after"] = search_after
        response = client.search(index="movies", body=search_body)
        hits_page_2 = response["hits"]["hits"]

        # get the last sort value from page 2
        search_after = hits_page_2[-1]["sort"]

        # fetch page 3
        search_body["search_after"] = search_after
        response = client.search(index="movies", body=search_body)

        hits_page_3 = response["hits"]["hits"]
        # print the hits from each page
        print("Page 1:")
        for hit in hits:
            print(hit)
        print("\nPage 2:")
        for hit in hits_page_2:
            print(hit)
        print("\nPage 3:")
        for hit in hits_page_3:
            print(hit)
    finally:
        # delete the index
        client.indices.delete(index="movies")


if __name__ == "__main__":
    main()
