#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import logging
from os import environ
from time import sleep
from urllib.parse import urlparse

from boto3 import Session

from opensearchpy import OpenSearch, Urllib3AWSV4SignerAuth, Urllib3HttpConnection


def main() -> None:
    """
    1. connects to an OpenSearch cluster on AWS defined by environment variables (i.e. ENDPOINT - cluster endpoint like
    my-test-domain.us-east-1.es.amazonaws.com; AWS_REGION like us-east-1, us-west-2; and SERVICE like es which
    differentiates beteween serverless and the managed service.
    2. creates an index called "movies" and adds a single document
    3. queries for that document
    4. deletes the document
    5. deletes the index
    """
    # verbose logging
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

    url = urlparse(environ["ENDPOINT"])
    region = environ.get("AWS_REGION", "us-east-1")
    service = environ.get("SERVICE", "es")

    credentials = Session().get_credentials()

    auth = Urllib3AWSV4SignerAuth(credentials, region, service)

    client = OpenSearch(
        hosts=[{"host": url.netloc, "port": url.port or 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=Urllib3HttpConnection,
        timeout=30,
    )

    # TODO: remove when OpenSearch Serverless adds support for /
    if service == "es":
        info = client.info()
        print(f"{info['version']['distribution']}: {info['version']['number']}")

    # create an index
    index = "movies"
    client.indices.create(index=index)

    try:
        # index data
        document = {"director": "Bennett Miller", "title": "Moneyball", "year": 2011}
        client.index(index=index, body=document, id="1")

        # wait for the document to index
        sleep(1)

        # search for the document
        results = client.search(body={"query": {"match": {"director": "miller"}}})
        for hit in results["hits"]["hits"]:
            print(hit["_source"])

        # delete the document
        client.delete(index=index, id="1")
    finally:
        # delete the index
        client.indices.delete(index=index)


if __name__ == "__main__":
    main()
