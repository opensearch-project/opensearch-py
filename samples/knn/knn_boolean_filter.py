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
import random

from opensearchpy import OpenSearch, helpers


def main() -> None:
    """
    create, query, and delete a kNN index
    """
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
    dimensions = 5

    if not client.indices.exists(index_name):
        client.indices.create(
            index_name,
            body={
                "settings": {"index.knn": True},
                "mappings": {
                    "properties": {
                        "values": {"type": "knn_vector", "dimension": dimensions},
                    }
                },
            },
        )

    # index data
    vectors = []
    genres = ["fiction", "drama", "romance"]
    for i in range(3000):
        vec = []
        for _ in range(dimensions):
            vec.append(round(random.uniform(0, 1), 2))

        vectors.append(
            {
                "_index": index_name,
                "_id": i,
                "values": vec,
                "metadata": {"genre": random.choice(genres)},
            }
        )

    # bulk index
    helpers.bulk(client, vectors)

    client.indices.refresh(index=index_name)

    # search
    genre = random.choice(genres)
    vec = []
    for _ in range(dimensions):
        vec.append(round(random.uniform(0, 1), 2))
    print(f"Searching for {vec} with the '{genre}' genre ...")

    search_query = {
        "query": {
            "bool": {
                "filter": {"bool": {"must": [{"term": {"metadata.genre": genre}}]}},
                "must": {"knn": {"values": {"vector": vec, "k": 5}}},
            }
        }
    }
    results = client.search(index=index_name, body=search_query)
    for hit in results["hits"]["hits"]:
        print(hit)

    # delete index
    client.indices.delete(index=index_name)


if __name__ == "__main__":
    main()
