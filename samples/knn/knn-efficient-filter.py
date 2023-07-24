#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import random

from opensearchpy import OpenSearch, helpers

# connect to an instance of OpenSearch

host = os.getenv('HOST', default='localhost')
port = int(os.getenv('PORT', 9200))
auth = (
    os.getenv('USERNAME', 'admin'), 
    os.getenv('PASSWORD', 'admin')
)

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_show_warn = False
)

# check whether an index exists
index_name = "hotels-index"

if not client.indices.exists(index_name):
    client.indices.create(index_name, 
        body={
            "settings":{
                "index.knn": True,
                "knn.algo_param.ef_search": 100,
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings":{
                "properties": {
                    "location": {
                        "type": "knn_vector", 
                        "dimension": 2,
                        "method": {
                            "name": "hnsw",
                            "space_type": "l2",
                            "engine": "lucene",
                            "parameters": {
                                "ef_construction": 100,
                                "m": 16
                            }
                        }
                    },
                }
            }
        }
    )

# index data
vectors = [
    { "_index": "hotels-index", "_id": "1", "location": [5.2, 4.4], "parking" : "true", "rating" : 5 },
    { "_index": "hotels-index", "_id": "2", "location": [5.2, 3.9], "parking" : "false", "rating" : 4 },
    { "_index": "hotels-index", "_id": "3", "location": [4.9, 3.4], "parking" : "true", "rating" : 9 },
    { "_index": "hotels-index", "_id": "4", "location": [4.2, 4.6], "parking" : "false", "rating" : 6},
    { "_index": "hotels-index", "_id": "5", "location": [3.3, 4.5], "parking" : "true", "rating" : 8 },
    { "_index": "hotels-index", "_id": "6", "location": [6.4, 3.4], "parking" : "true", "rating" : 9 },
    { "_index": "hotels-index", "_id": "7", "location": [4.2, 6.2], "parking" : "true", "rating" : 5 },
    { "_index": "hotels-index", "_id": "8", "location": [2.4, 4.0], "parking" : "true", "rating" : 8 },
    { "_index": "hotels-index", "_id": "9", "location": [1.4, 3.2], "parking" : "false", "rating" : 5 },
    { "_index": "hotels-index", "_id": "10", "location": [7.0, 9.9], "parking" : "true", "rating" : 9 },
    { "_index": "hotels-index", "_id": "11", "location": [3.0, 2.3], "parking" : "false", "rating" : 6 },
    { "_index": "hotels-index", "_id": "12", "location": [5.0, 1.0], "parking" : "true", "rating" : 3 },
]

helpers.bulk(client, vectors)

client.indices.refresh(index=index_name)

# search
search_query = {
    "size": 3,
    "query": {
        "knn": {
            "location": {
            "vector": [5, 4],
            "k": 3,
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "rating": {
                                    "gte": 8,
                                    "lte": 10
                                }
                            }
                        },
                        {
                            "term": {
                                "parking": "true"
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
}

results = client.search(index=index_name, body=search_query)
for hit in results["hits"]["hits"]:
    print(hit)

# delete index
client.indices.delete(index=index_name)
