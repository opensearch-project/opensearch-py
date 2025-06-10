#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import json
import os

from opensearchpy import OpenSearch


def main() -> None:
    """
    bulk index 100 items and then delete the index
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
    data = ""
    for i in range(100):
        data += json.dumps({"index": {"_index": index_name, "_id": i}}) + "\n"
        data += json.dumps({"value": i}) + "\n"

    rc = client.bulk(body=data)  # pylint: disable=invalid-name
    if rc["errors"]:
        print("There were errors:")
        for item in rc["items"]:
            print(f"{item['index']['status']}: {item['index']['error']['type']}")
    else:
        print(f"Bulk-inserted {len(rc['items'])} items.")

    # delete index
    client.indices.delete(index=index_name)


if __name__ == "__main__":
    main()
