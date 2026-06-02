"""
simpledoc_gRPC.py — Single Document gRPC Translation Layer

This module handles the full round-trip for single document operations:

    Python Client Dict → Protobuf Request → gRPC Transport → Protobuf Response → Python Client Dict

The opensearch-py low-level client uses Python dicts for requests and responses.
Under the hood, this module:
  1. Converts the client's Python dict into a protobuf BulkRequest message
  2. Sends it over gRPC to the OpenSearch server
  3. Receives the protobuf BulkResponse from the server
  4. Converts the protobuf response back into a Python dict matching opensearch-py format

This is transparent to the user — they interact with normal Python dicts.
"""

import json
import grpc

from opensearch_grpc.proto_adapter import (
    BulkRequest,
    BulkRequestBody,
    OperationContainer,
    IndexOperation,
    WriteOperation,
    UpdateOperation,
    DeleteOperation,
    UpdateAction,
    DocumentServiceStub,
    REFRESH_TRUE,
    REFRESH_FALSE,
    REFRESH_WAIT_FOR,
    REFRESH_UNSPECIFIED,
    VERSION_TYPE_INTERNAL,
    VERSION_TYPE_EXTERNAL,
    VERSION_TYPE_EXTERNAL_GTE,
    VERSION_TYPE_UNSPECIFIED,
)
from opensearch_grpc.translation import ResponseConverter, _build_single_request


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API — These functions mirror the opensearch-py low-level client methods
# ═══════════════════════════════════════════════════════════════════════════════


def index_document(index, body, id=None, routing=None, pipeline=None,
                   refresh=None, timeout=None, require_alias=None,
                   if_primary_term=None, if_seq_no=None,
                   version=None, version_type=None,
                   grpc_target="localhost:9400"):
    """
    Index a single document via gRPC.

    Mirrors: client.index(index=..., body=..., id=..., ...)

    Flow:
        1. Python dict (body) → protobuf BulkRequest
        2. Send over gRPC to OpenSearch
        3. Protobuf BulkResponse → Python dict (returned to caller)

    Args:
        index: Name of the index to store the document in.
        body: The document as a Python dict (e.g. {"title": "Hello", "value": 1}).
        id: Optional document ID. If not provided, OpenSearch auto-generates one.
        routing: Custom routing value for shard placement.
        pipeline: Ingest pipeline to preprocess the document.
        refresh: When to make the change visible ("true", "false", "wait_for").
        timeout: Request timeout (e.g. "30s").
        require_alias: If True, the index must be an alias.
        if_primary_term: Optimistic concurrency control — primary term check.
        if_seq_no: Optimistic concurrency control — sequence number check.
        version: Explicit version for external versioning.
        version_type: Version type ("internal", "external", "external_gte").
        grpc_target: gRPC server address (default "localhost:9400").

    Returns:
        A Python dict matching the opensearch-py response format.
    """
    print(f"[simpledoc_gRPC] INDEX: index={index}, id={id}")
    print(f"[simpledoc_gRPC] Document body: {body}")

    # Step 1: Build the operation metadata
    meta = {"_index": index}
    if id is not None:
        meta["_id"] = id
    if routing is not None:
        meta["routing"] = routing
    if pipeline is not None:
        meta["pipeline"] = pipeline
    if require_alias is not None:
        meta["require_alias"] = require_alias
    if if_primary_term is not None:
        meta["if_primary_term"] = if_primary_term
    if if_seq_no is not None:
        meta["if_seq_no"] = if_seq_no
    if version is not None:
        meta["version"] = version
    if version_type is not None:
        meta["version_type"] = version_type

    # Step 2: Convert to protobuf and send
    request = _build_single_request("index", meta, body, refresh=refresh, timeout=timeout)
    print(f"[simpledoc_gRPC] Converted to protobuf BulkRequest with 1 operation")

    # Step 3: Send over gRPC and get response
    response = _send_grpc_request(request, grpc_target)

    # Step 4: Convert protobuf response back to Python dict
    result = ResponseConverter.from_bulk_response(response)
    print(f"[simpledoc_gRPC] Response converted back to Python dict: {result}")
    return result


def create_document(index, body, id=None, routing=None, pipeline=None,
                    refresh=None, timeout=None, require_alias=None,
                    grpc_target="localhost:9400"):
    """
    Create a single document via gRPC (fails if document already exists).

    Mirrors: client.create(index=..., body=..., id=..., ...)

    Args:
        index: Name of the index.
        body: The document as a Python dict.
        id: Optional document ID.
        routing: Custom routing value.
        pipeline: Ingest pipeline ID.
        refresh: Refresh policy.
        timeout: Request timeout.
        require_alias: If True, index must be an alias.
        grpc_target: gRPC server address.

    Returns:
        A Python dict matching the opensearch-py response format.
    """
    print(f"[simpledoc_gRPC] CREATE: index={index}, id={id}")
    print(f"[simpledoc_gRPC] Document body: {body}")

    meta = {"_index": index}
    if id is not None:
        meta["_id"] = id
    if routing is not None:
        meta["routing"] = routing
    if pipeline is not None:
        meta["pipeline"] = pipeline
    if require_alias is not None:
        meta["require_alias"] = require_alias

    request = _build_single_request("create", meta, body, refresh=refresh, timeout=timeout)
    print(f"[simpledoc_gRPC] Converted to protobuf BulkRequest with 1 operation")

    response = _send_grpc_request(request, grpc_target)

    result = ResponseConverter.from_bulk_response(response)
    print(f"[simpledoc_gRPC] Response converted back to Python dict: {result}")
    return result


def update_document(index, id, body, routing=None, refresh=None,
                    timeout=None, require_alias=None,
                    if_primary_term=None, if_seq_no=None,
                    retry_on_conflict=None,
                    grpc_target="localhost:9400"):
    """
    Update a single document via gRPC.

    Mirrors: client.update(index=..., id=..., body=..., ...)

    The body should contain update instructions, e.g.:
        {"doc": {"field": "new_value"}}
        {"doc": {"field": "value"}, "doc_as_upsert": True}

    Args:
        index: Name of the index.
        id: Document ID (required for updates).
        body: Update instructions as a Python dict.
        routing: Custom routing value.
        refresh: Refresh policy.
        timeout: Request timeout.
        require_alias: If True, index must be an alias.
        if_primary_term: Optimistic concurrency — primary term.
        if_seq_no: Optimistic concurrency — sequence number.
        retry_on_conflict: Number of retries on version conflict.
        grpc_target: gRPC server address.

    Returns:
        A Python dict matching the opensearch-py response format.
    """
    print(f"[simpledoc_gRPC] UPDATE: index={index}, id={id}")
    print(f"[simpledoc_gRPC] Update body: {body}")

    meta = {"_index": index, "_id": id}
    if routing is not None:
        meta["routing"] = routing
    if require_alias is not None:
        meta["require_alias"] = require_alias
    if if_primary_term is not None:
        meta["if_primary_term"] = if_primary_term
    if if_seq_no is not None:
        meta["if_seq_no"] = if_seq_no
    if retry_on_conflict is not None:
        meta["retry_on_conflict"] = retry_on_conflict

    request = _build_single_request("update", meta, body, refresh=refresh, timeout=timeout)
    print(f"[simpledoc_gRPC] Converted to protobuf BulkRequest with 1 operation")

    response = _send_grpc_request(request, grpc_target)

    result = ResponseConverter.from_bulk_response(response)
    print(f"[simpledoc_gRPC] Response converted back to Python dict: {result}")
    return result


def delete_document(index, id, routing=None, refresh=None, timeout=None,
                    if_primary_term=None, if_seq_no=None,
                    version=None, version_type=None,
                    grpc_target="localhost:9400"):
    """
    Delete a single document via gRPC.

    Mirrors: client.delete(index=..., id=..., ...)

    Args:
        index: Name of the index.
        id: Document ID (required for deletes).
        routing: Custom routing value.
        refresh: Refresh policy.
        timeout: Request timeout.
        if_primary_term: Optimistic concurrency — primary term.
        if_seq_no: Optimistic concurrency — sequence number.
        version: Explicit version for external versioning.
        version_type: Version type.
        grpc_target: gRPC server address.

    Returns:
        A Python dict matching the opensearch-py response format.
    """
    print(f"[simpledoc_gRPC] DELETE: index={index}, id={id}")

    meta = {"_index": index, "_id": id}
    if routing is not None:
        meta["routing"] = routing
    if if_primary_term is not None:
        meta["if_primary_term"] = if_primary_term
    if if_seq_no is not None:
        meta["if_seq_no"] = if_seq_no
    if version is not None:
        meta["version"] = version
    if version_type is not None:
        meta["version_type"] = version_type

    request = _build_single_request("delete", meta, None, refresh=refresh, timeout=timeout)
    print(f"[simpledoc_gRPC] Converted to protobuf BulkRequest with 1 operation")

    response = _send_grpc_request(request, grpc_target)

    result = ResponseConverter.from_bulk_response(response)
    print(f"[simpledoc_gRPC] Response converted back to Python dict: {result}")
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# gRPC TRANSPORT — Sends protobuf over the wire and receives response
# ═══════════════════════════════════════════════════════════════════════════════


def _send_grpc_request(request, grpc_target):
    """
    Open a gRPC channel, send the BulkRequest, and return the BulkResponse.

    This is the actual network transport step — the protobuf bytes go over
    the wire to OpenSearch's gRPC endpoint.
    """
    print(f"[simpledoc_gRPC] Sending protobuf over gRPC to {grpc_target}...")

    channel = grpc.insecure_channel(grpc_target)
    stub = DocumentServiceStub(channel)

    # The Bulk RPC accepts a BulkRequest and returns a BulkResponse
    response = stub.Bulk(request)

    print(f"[simpledoc_gRPC] Received protobuf BulkResponse from server")
    print(f"[simpledoc_gRPC]   errors={response.errors}, took={response.took}ms, items={len(response.items)}")

    channel.close()
    return response

