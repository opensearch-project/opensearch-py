# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
proto_adapter.py — Protobuf Import Adapter

Imports protobuf types and gRPC stubs from the opensearch-protobufs package.
Install with: pip install opensearch-protobufs
"""

from opensearch.protobufs.schemas.common_pb2 import (
    BulkRequest,
    BulkRequestBody,
    BulkResponse,
    DeleteOperation,
    IndexOperation,
    OperationContainer,
    UpdateAction,
    UpdateOperation,
    WriteOperation,
)
from opensearch.protobufs.schemas.common_pb2 import (
    REFRESH_FALSE,
    REFRESH_TRUE,
    REFRESH_UNSPECIFIED,
    REFRESH_WAIT_FOR,
    VERSION_TYPE_EXTERNAL,
    VERSION_TYPE_EXTERNAL_GTE,
    VERSION_TYPE_INTERNAL,
    VERSION_TYPE_UNSPECIFIED,
)
from opensearch.protobufs.services.document_service_pb2_grpc import DocumentServiceStub
from opensearch.protobufs.services.search_service_pb2_grpc import SearchServiceStub

__all__ = [
    "BulkRequest",
    "BulkRequestBody",
    "BulkResponse",
    "OperationContainer",
    "IndexOperation",
    "WriteOperation",
    "UpdateOperation",
    "DeleteOperation",
    "UpdateAction",
    "DocumentServiceStub",
    "SearchServiceStub",
    "REFRESH_TRUE",
    "REFRESH_FALSE",
    "REFRESH_WAIT_FOR",
    "REFRESH_UNSPECIFIED",
    "VERSION_TYPE_INTERNAL",
    "VERSION_TYPE_EXTERNAL",
    "VERSION_TYPE_EXTERNAL_GTE",
    "VERSION_TYPE_UNSPECIFIED",
]
