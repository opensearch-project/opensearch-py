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

# connect to OpenSearch


def main() -> None:
    """
    an example showing how to create an synchronous connection to
    OpenSearch, create an index, index a document and search to
    return the document
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

    info = client.info()
    print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")

    # create an index

    index_name = "test-index"

    index_body = {"settings": {"index": {"number_of_shards": 4}}}

    response = client.indices.create(index_name, body=index_body)

    print(response)

    # add a document to the index

    document = {"title": "Moneyball", "director": "Bennett Miller", "year": "2011"}

    doc_id = "1"

    response = client.index(index=index_name, body=document, id=doc_id, refresh=True)

    print(response)

    # search for a document

    user_query = "miller"

    query = {
        "size": 5,
        "query": {
            "multi_match": {"query": user_query, "fields": ["title^2", "director"]}
        },
    }

    response = client.search(body=query, index=index_name)

    print(response)

    # delete the document

    response = client.delete(index=index_name, id=doc_id)

    print(response)

    # delete the index

    response = client.indices.delete(index=index_name)

    print(response)


if __name__ == "__main__":
    main()
