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

from opensearch_grpc.proto import common_pb2, document_service_pb2_grpc


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
    result = _response_to_dict(response)
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

    result = _response_to_dict(response)
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

    result = _response_to_dict(response)
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

    result = _response_to_dict(response)
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
    stub = document_service_pb2_grpc.DocumentServiceStub(channel)

    # The Bulk RPC accepts a BulkRequest and returns a BulkResponse
    response = stub.Bulk(request)

    print(f"[simpledoc_gRPC] Received protobuf BulkResponse from server")
    print(f"[simpledoc_gRPC]   errors={response.errors}, took={response.took}ms, items={len(response.items)}")

    channel.close()
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE CONVERSION — Protobuf BulkResponse → Python dict
# ═══════════════════════════════════════════════════════════════════════════════


def _response_to_dict(response):
    """
    Convert a protobuf BulkResponse back into the Python dict format
    that the opensearch-py client would normally return.

    The opensearch-py client returns responses like:
        {
            "_index": "my-index",
            "_id": "doc-1",
            "_version": 1,
            "result": "created",
            "_shards": {"total": 2, "successful": 1, "failed": 0},
            "_seq_no": 0,
            "_primary_term": 1
        }

    This function reconstructs that dict from the protobuf response.
    """
    print(f"[simpledoc_gRPC] Converting protobuf response → Python dict...")

    # For single-doc operations, there's exactly one item in the response
    item = response.items[0]

    # Determine which operation type the response is for
    for op_type in ("index", "create", "update", "delete"):
        if item.HasField(op_type):
            resp_item = getattr(item, op_type)
            break
    else:
        return {"error": "Unknown response type"}

    # Build the Python dict matching opensearch-py format
    result = {
        "_index": resp_item.x_index,
        "_id": resp_item.x_id if resp_item.x_id else None,
        "result": resp_item.result if resp_item.result else None,
        "_version": resp_item.x_version if resp_item.HasField("x_version") else None,
        "_seq_no": resp_item.x_seq_no if resp_item.HasField("x_seq_no") else None,
        "_primary_term": resp_item.x_primary_term if resp_item.HasField("x_primary_term") else None,
    }

    # Add shard info if present
    if resp_item.HasField("x_shards"):
        result["_shards"] = {
            "total": resp_item.x_shards.total,
            "successful": resp_item.x_shards.successful,
            "failed": resp_item.x_shards.failed,
        }

    # Add error info if present
    if resp_item.HasField("error"):
        result["error"] = {
            "type": resp_item.error.type,
            "reason": resp_item.error.reason if resp_item.error.HasField("reason") else None,
        }

    # Remove None values for cleaner output
    result = {k: v for k, v in result.items() if v is not None}

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST CONVERSION — Python dict → Protobuf BulkRequest
# ═══════════════════════════════════════════════════════════════════════════════


def _build_single_request(op_type, meta, source, refresh=None, timeout=None):
    """
    Build a protobuf BulkRequest containing a single operation.

    This is where the Python dict gets converted into protobuf format
    for transport over gRPC.
    """
    request = common_pb2.BulkRequest()

    # Set the default index at the request level
    request.index = meta["_index"]

    # Set optional request-level parameters
    if refresh is not None:
        request.refresh = _map_refresh(refresh)
    if timeout is not None:
        request.timeout = timeout

    # Build the single BulkRequestBody
    body = common_pb2.BulkRequestBody()

    # Build the operation container (tells the server what operation to perform)
    op_container = common_pb2.OperationContainer()
    _OP_BUILDERS[op_type](op_container, meta)
    body.operation_container.CopyFrom(op_container)

    # Attach the document source or update action
    if op_type == "update" and source is not None:
        # Update operations have special structure (doc, upsert, script, etc.)
        body.update_action.CopyFrom(_build_update_action(source))
    elif source is not None:
        # Index/create operations: serialize the document as JSON bytes
        body.object = json.dumps(source).encode("utf-8")

    # Add the single operation to the request
    request.bulk_request_body.append(body)

    print(f"[simpledoc_gRPC] Built protobuf: op={op_type}, index={meta['_index']}, id={meta.get('_id', 'auto')}")
    return request


# ═══════════════════════════════════════════════════════════════════════════════
# ENUM MAPPERS — Convert Python strings to protobuf enum values
# ═══════════════════════════════════════════════════════════════════════════════


def _map_refresh(value):
    """Map refresh parameter string/bool to protobuf Refresh enum."""
    mapping = {
        "true": common_pb2.REFRESH_TRUE,
        "false": common_pb2.REFRESH_FALSE,
        "wait_for": common_pb2.REFRESH_WAIT_FOR,
        True: common_pb2.REFRESH_TRUE,
        False: common_pb2.REFRESH_FALSE,
    }
    return mapping.get(value, common_pb2.REFRESH_UNSPECIFIED)


def _map_version_type(value):
    """Map version_type string to protobuf VersionType enum."""
    mapping = {
        "internal": common_pb2.VERSION_TYPE_INTERNAL,
        "external": common_pb2.VERSION_TYPE_EXTERNAL,
        "external_gte": common_pb2.VERSION_TYPE_EXTERNAL_GTE,
    }
    return mapping.get(value, common_pb2.VERSION_TYPE_UNSPECIFIED)


# ═══════════════════════════════════════════════════════════════════════════════
# OPERATION BUILDERS — Populate protobuf operation messages from metadata
# ═══════════════════════════════════════════════════════════════════════════════


def _build_index_op(container, meta):
    """Build an IndexOperation protobuf from the action metadata dict."""
    op = common_pb2.IndexOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "pipeline" in meta:
        op.pipeline = meta["pipeline"]
    if "if_primary_term" in meta:
        op.if_primary_term = meta["if_primary_term"]
    if "if_seq_no" in meta:
        op.if_seq_no = meta["if_seq_no"]
    if "require_alias" in meta:
        op.require_alias = meta["require_alias"]
    if "version" in meta:
        op.version = meta["version"]
    if "version_type" in meta:
        op.version_type = _map_version_type(meta["version_type"])
    container.index.CopyFrom(op)


def _build_create_op(container, meta):
    """Build a WriteOperation (create) protobuf from the action metadata dict."""
    op = common_pb2.WriteOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "pipeline" in meta:
        op.pipeline = meta["pipeline"]
    if "require_alias" in meta:
        op.require_alias = meta["require_alias"]
    container.create.CopyFrom(op)


def _build_update_op(container, meta):
    """Build an UpdateOperation protobuf from the action metadata dict."""
    op = common_pb2.UpdateOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "if_primary_term" in meta:
        op.if_primary_term = meta["if_primary_term"]
    if "if_seq_no" in meta:
        op.if_seq_no = meta["if_seq_no"]
    if "require_alias" in meta:
        op.require_alias = meta["require_alias"]
    if "retry_on_conflict" in meta:
        op.retry_on_conflict = meta["retry_on_conflict"]
    container.update.CopyFrom(op)


def _build_delete_op(container, meta):
    """Build a DeleteOperation protobuf from the action metadata dict."""
    op = common_pb2.DeleteOperation()
    if "_id" in meta:
        op.x_id = meta["_id"]
    if "_index" in meta:
        op.x_index = meta["_index"]
    if "routing" in meta:
        op.routing = meta["routing"]
    if "if_primary_term" in meta:
        op.if_primary_term = meta["if_primary_term"]
    if "if_seq_no" in meta:
        op.if_seq_no = meta["if_seq_no"]
    if "version" in meta:
        op.version = meta["version"]
    if "version_type" in meta:
        op.version_type = _map_version_type(meta["version_type"])
    container.delete.CopyFrom(op)


def _build_update_action(source):
    """
    Build an UpdateAction protobuf from the update body dict.

    Update bodies have special fields like "doc", "upsert", "script"
    that are different from a normal document body.
    """
    action = common_pb2.UpdateAction()
    if "doc" in source:
        # Partial document to merge — serialized as JSON bytes
        action.doc = json.dumps(source["doc"]).encode("utf-8")
    if "doc_as_upsert" in source:
        # If True, use the doc as the upsert value
        action.doc_as_upsert = source["doc_as_upsert"]
    if "upsert" in source:
        # Document to insert if it doesn't exist
        action.upsert = json.dumps(source["upsert"]).encode("utf-8")
    if "scripted_upsert" in source:
        action.scripted_upsert = source["scripted_upsert"]
    if "detect_noop" in source:
        action.detect_noop = source["detect_noop"]
    return action


# Operation type → builder function mapping
_OP_BUILDERS = {
    "index": _build_index_op,
    "create": _build_create_op,
    "update": _build_update_op,
    "delete": _build_delete_op,
}
