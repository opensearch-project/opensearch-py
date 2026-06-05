"""
proto_adapter.py — Protobuf Import Adapter

This module is the single point of import for all protobuf types and gRPC stubs.
All other modules import from here instead of directly from the proto/ folder.

When the `opensearch-protobufs` PyPI package publishes real stubs, we only
need to change the imports in THIS file — everything else stays the same.

Current state (v0.0.2): Package is a namespace reservation only.
    → We use locally compiled stubs from opensearch_grpc/proto/

Future state (when package has real stubs):
    → Switch imports to: from opensearch_protobufs import common_pb2, ...
"""

# ─── Current: Import from locally compiled proto stubs ────────────────────────
# When opensearch-protobufs publishes real modules, replace these two lines:
#   from opensearch_protobufs.schemas import common_pb2
#   from opensearch_protobufs.services import document_service_pb2_grpc

from opensearch_grpc.proto import common_pb2, document_service_pb2_grpc

# ─── Re-export everything that other modules need ─────────────────────────────

# Protobuf message types (for building requests)
BulkRequest = common_pb2.BulkRequest
BulkRequestBody = common_pb2.BulkRequestBody
BulkResponse = common_pb2.BulkResponse
OperationContainer = common_pb2.OperationContainer
IndexOperation = common_pb2.IndexOperation
WriteOperation = common_pb2.WriteOperation
UpdateOperation = common_pb2.UpdateOperation
DeleteOperation = common_pb2.DeleteOperation
UpdateAction = common_pb2.UpdateAction

# Enum values
REFRESH_TRUE = common_pb2.REFRESH_TRUE
REFRESH_FALSE = common_pb2.REFRESH_FALSE
REFRESH_WAIT_FOR = common_pb2.REFRESH_WAIT_FOR
REFRESH_UNSPECIFIED = common_pb2.REFRESH_UNSPECIFIED
VERSION_TYPE_INTERNAL = common_pb2.VERSION_TYPE_INTERNAL
VERSION_TYPE_EXTERNAL = common_pb2.VERSION_TYPE_EXTERNAL
VERSION_TYPE_EXTERNAL_GTE = common_pb2.VERSION_TYPE_EXTERNAL_GTE
VERSION_TYPE_UNSPECIFIED = common_pb2.VERSION_TYPE_UNSPECIFIED

# gRPC service stub
DocumentServiceStub = document_service_pb2_grpc.DocumentServiceStub
