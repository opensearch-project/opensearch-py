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
from typing import Any

from opensearchpy import OpenSearch, helpers


def main() -> None:
    """
    demonstrates how to bulk load data using opensearchpy.helpers
    including examples of serial, parallel, and streaming bulk load
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

    if not client.indices.exists(index=index_name):
        client.indices.create(
            index=index_name,
            body={
                "mappings": {
                    "properties": {
                        "value": {"type": "float"},
                    }
                }
            },
        )

    # index data
    data = []
    for i in range(100):
        data.append({"_index": index_name, "_id": i, "value": i})

    # serialized bulk raising an exception on error
    rc = helpers.bulk(client, data)  # pylint: disable=invalid-name
    print(f"Bulk-inserted {rc[0]} items (bulk).")

    # parallel bulk with explicit error checking
    succeeded = []
    failed = []
    for success, item in helpers.parallel_bulk(
        client,
        actions=data,
        chunk_size=10,
        raise_on_error=False,
        raise_on_exception=False,
        max_chunk_bytes=20 * 1024 * 1024,
        request_timeout=60,
    ):
        if success:
            succeeded.append(item)
        else:
            failed.append(item)

    if len(failed) > 0:
        print(f"There were {len(failed)} errors:")
        for item in failed:
            print(item["index"]["error"])

    if len(succeeded) > 0:
        print(f"Bulk-inserted {len(succeeded)} items (parallel_bulk).")

    # streaming bulk with a data generator
    def _generate_data() -> Any:
        for i in range(100):
            yield {"_index": index_name, "_id": i, "value": i}

    succeeded = []
    failed = []
    for success, item in helpers.streaming_bulk(client, actions=_generate_data()):
        if success:
            succeeded.append(item)
        else:
            failed.append(item)

    if len(failed) > 0:
        print(f"There were {len(failed)} errors:")
        for item in failed:
            print(item["index"]["error"])

    if len(succeeded) > 0:
        print(f"Bulk-inserted {len(succeeded)} items (streaming_bulk).")

    # delete index
    client.indices.delete(index=index_name)


if __name__ == "__main__":
    main()
