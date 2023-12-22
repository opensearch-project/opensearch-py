#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from opensearchpy import OpenSearch

# For cleaner output, comment in the two lines below to disable warnings and informational messages
# import urllib3
# urllib3.disable_warnings()


def main() -> None:
    """
    provides samples for different ways to handle documents including indexing, searching, updating, and deleting
    """
    # Connect to OpenSearch
    client = OpenSearch(
        hosts=["https://localhost:9200"],
        use_ssl=True,
        verify_certs=False,
        http_auth=("admin", "admin"),
    )

    # Create an index
    index = "movies"
    if not client.indices.exists(index=index):
        client.indices.create(index=index)

    # Create documents
    client.index(
        index=index, id=1, body={"title": "Beauty and the Beast", "year": 1991}
    )
    client.index(
        index=index,
        id=2,
        body={"title": "Beauty and the Beast - Live Action", "year": 2017},
    )

    # Index a document
    client.index(index=index, id=2, body={"title": "The Lion King", "year": 1994})

    # Create a document with auto-generated ID
    result = client.index(index=index, body={"title": "The Lion King 2", "year": 1998})
    print(result)

    # Get a document
    result = client.get(index=index, id=1)["_source"]
    print(result)

    # Get a document with _source includes
    result = client.get(index=index, id=1, _source_includes=["title"])["_source"]
    print(result)

    # Get a document with _source excludes
    result = client.get(index=index, id=1, _source_excludes=["title"])["_source"]
    print(result)

    # Get multiple documents
    result = client.mget(index=index, body={"docs": [{"_id": 1}, {"_id": 2}]})["docs"]
    print(result)

    # Check if a document exists
    result = client.exists(index=index, id=1)
    print(result)

    # Update a document
    client.update(index=index, id=1, body={"doc": {"year": 1995}})

    # Update a document using script
    client.update(
        index=index, id=1, body={"script": {"source": "ctx._source.year += 5"}}
    )

    # Update multiple documents by query
    client.update_by_query(
        index=index,
        body={
            "script": {"source": "ctx._source.year -= 1"},
            "query": {"range": {"year": {"gt": 2023}}},
        },
    )

    # Delete a document
    client.delete(index=index, id=1)

    # Delete a document with ignore 404
    client.delete(index=index, id=1, ignore=404)

    # Delete multiple documents by query
    client.delete_by_query(
        index=index, body={"query": {"range": {"year": {"gt": 2023}}}}
    )

    # Delete the index
    client.indices.delete(index=index)
    print("Deleted index!")


if __name__ == "__main__":
    main()
