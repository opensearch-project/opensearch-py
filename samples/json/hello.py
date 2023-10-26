#!/usr/bin/env python

# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from opensearchpy import OpenSearch

# connect to OpenSearch

host = "localhost"
port = 9200
auth = ("admin", "admin")  # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
)

info = client.transport.perform_request("GET", "/")
print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")

# create an index

index_name = "movies"

index_body = {"settings": {"index": {"number_of_shards": 4}}}

print(client.transport.perform_request("PUT", f"/{index_name}", body=index_body))

# add a document to the index

document = {"title": "Moneyball", "director": "Bennett Miller", "year": "2011"}

id = "1"

print(
    client.transport.perform_request(
        "PUT", f"/{index_name}/_doc/{id}?refresh=true", body=document
    )
)

# search for a document

q = "miller"

query = {
    "size": 5,
    "query": {"multi_match": {"query": q, "fields": ["title^2", "director"]}},
}

print(client.transport.perform_request("POST", f"/{index_name}/_search", body=query))

# delete the document

print(client.transport.perform_request("DELETE", f"/{index_name}/_doc/{id}"))

# delete the index

print(client.transport.perform_request("DELETE", f"/{index_name}"))
