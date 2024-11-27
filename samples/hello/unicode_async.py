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
    An example showing how to create an asynchronous connection
    to OpenSearch, create an index, index a document and
    search to return the document.
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

    try:
        info = await client.info()
        print(
            f"Welcome to {info['version']['distribution']} {info['version']['number']}!"
        )

        index_name = "кино"
        index_create_result = await client.indices.create(index=index_name)
        print(index_create_result)

        document = {"название": "Солярис", "автор": "Андрей Тарковский", "год": "2011"}
        id = "соларис@2011"
        doc_insert_result = await client.index(
            index=index_name, body=document, id=id, refresh=True
        )
        print(doc_insert_result)

        doc_delete_result = await client.delete(index=index_name, id=id)
        print(doc_delete_result)

        index_delete_result = await client.indices.delete(index=index_name)
        print(index_delete_result)

    finally:
        await client.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
