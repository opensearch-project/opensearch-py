# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#!/usr/bin/env python3
"""Integration test: send bulk data over gRPC bidirectional stream."""

import grpc

from opensearch.protobufs.services.document_service_pb2_grpc import DocumentServiceStub
from opensearch_grpc.translation import toProtoBulkRequest


def generate_bulk_request():
    """Build a BulkRequest with mixed operations."""
    body = [
        {"index": {"_index": "grpc-test", "_id": "1"}},
        {"title": "First doc", "value": 1},
        {"index": {"_index": "grpc-test", "_id": "2"}},
        {"title": "Second doc", "value": 2},
        {"create": {"_index": "grpc-test", "_id": "3"}},
        {"title": "Third doc", "value": 3},
        {"update": {"_index": "grpc-test", "_id": "1"}},
        {"doc": {"value": 100}},
        {"delete": {"_index": "grpc-test", "_id": "2"}},
    ]
    return toProtoBulkRequest(body=body, refresh="true")


def test_bulk_stream():
    """Connect to gRPC server and send a bulk request."""
    target = "localhost:9400"
    print(f"Connecting to gRPC at {target}...")

    channel = grpc.insecure_channel(target)
    stub = DocumentServiceStub(channel)

    request = generate_bulk_request()
    print(f"Sending {len(request.bulk_request_body)} operations...")

    try:
        response = stub.Bulk(request)
        print(f"\n--- Response ---")
        print(f"  errors: {response.errors}")
        print(f"  took: {response.took}ms")
        print(f"  items: {len(response.items)}")
        for item in response.items:
            if item.HasField("index"):
                print(f"  [index] id={item.index.x_id} status={item.index.status}")
            elif item.HasField("create"):
                print(f"  [create] id={item.create.x_id} status={item.create.status}")
            elif item.HasField("update"):
                print(f"  [update] id={item.update.x_id} status={item.update.status}")
            elif item.HasField("delete"):
                print(f"  [delete] id={item.delete.x_id} status={item.delete.status}")
    except grpc.RpcError as e:
        print(f"\ngRPC error: {e.code()} - {e.details()}")

    channel.close()
    print("\nDone.")


if __name__ == "__main__":
    test_bulk_stream()
