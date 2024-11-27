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
    An example showing how to create a synchronous connection to
    OpenSearch, create an index, index a document and search to
    return the document.
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

    index_name = "кино"
    index_create_result = client.indices.create(index=index_name)
    print(index_create_result)

    document = {"название": "Солярис", "автор": "Андрей Тарковский", "год": "2011"}
    id = "соларис@2011"
    doc_insert_result = client.index(
        index=index_name, body=document, id=id, refresh=True
    )
    print(doc_insert_result)

    doc_delete_result = client.delete(index=index_name, id=id)
    print(doc_delete_result)

    index_delete_result = client.indices.delete(index=index_name)
    print(index_delete_result)


if __name__ == "__main__":
    main()
