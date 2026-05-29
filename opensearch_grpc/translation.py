"""Translation layer: opensearch-py single document operations → protobuf BulkRequest.

Single document operations (index, create, update, delete) are transported
as a BulkRequest containing one BulkRequestBody. This will be extended
later for multi-document bulk requests.
"""

import json

from opensearch_grpc.proto_adapter import (
    BulkRequest,
    BulkRequestBody,
    OperationContainer,
    IndexOperation,
    WriteOperation,
    UpdateOperation,
    DeleteOperation,
    UpdateAction,
    REFRESH_TRUE,
    REFRESH_FALSE,
    REFRESH_WAIT_FOR,
    REFRESH_UNSPECIFIED,
    VERSION_TYPE_INTERNAL,
    VERSION_TYPE_EXTERNAL,
    VERSION_TYPE_EXTERNAL_GTE,
    VERSION_TYPE_UNSPECIFIED,
)


# ─── Single Document Operations ──────────────────────────────────────────────


def toProtoIndexRequest(index, body, id=None, routing=None, pipeline=None,
                        refresh=None, timeout=None, require_alias=None,
                        if_primary_term=None, if_seq_no=None,
                        version=None, version_type=None):
    """
    Convert a single index operation to a protobuf BulkRequest.

    Mirrors: client.index(index=..., body=..., id=..., ...)
    """
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

    return _build_single_request("index", meta, body, refresh=refresh, timeout=timeout)


def toProtoCreateRequest(index, body, id=None, routing=None, pipeline=None,
                         refresh=None, timeout=None, require_alias=None):
    """
    Convert a single create operation to a protobuf BulkRequest.

    Mirrors: client.create(index=..., body=..., id=..., ...)
    """
    meta = {"_index": index}
    if id is not None:
        meta["_id"] = id
    if routing is not None:
        meta["routing"] = routing
    if pipeline is not None:
        meta["pipeline"] = pipeline
    if require_alias is not None:
        meta["require_alias"] = require_alias

    return _build_single_request("create", meta, body, refresh=refresh, timeout=timeout)


def toProtoUpdateRequest(index, id, body, routing=None, refresh=None,
                         timeout=None, require_alias=None,
                         if_primary_term=None, if_seq_no=None,
                         retry_on_conflict=None):
    """
    Convert a single update operation to a protobuf BulkRequest.

    Mirrors: client.update(index=..., id=..., body=..., ...)
    """
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

    return _build_single_request("update", meta, body, refresh=refresh, timeout=timeout)


def toProtoDeleteRequest(index, id, routing=None, refresh=None, timeout=None,
                         if_primary_term=None, if_seq_no=None,
                         version=None, version_type=None):
    """
    Convert a single delete operation to a protobuf BulkRequest.

    Mirrors: client.delete(index=..., id=..., ...)
    """
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

    return _build_single_request("delete", meta, None, refresh=refresh, timeout=timeout)


# ─── Internal Helpers ─────────────────────────────────────────────────────────


def _build_single_request(op_type, meta, source, refresh=None, timeout=None):
    """Build a BulkRequest with a single operation."""
    request = BulkRequest()
    request.index = meta["_index"]

    if refresh is not None:
        request.refresh = _map_refresh(refresh)
    if timeout is not None:
        request.timeout = timeout

    body = BulkRequestBody()
    op_container = OperationContainer()
    _OP_BUILDERS[op_type](op_container, meta)
    body.operation_container.CopyFrom(op_container)

    if op_type == "update" and source is not None:
        body.update_action.CopyFrom(_build_update_action(source))
    elif source is not None:
        body.object = json.dumps(source).encode("utf-8")

    request.bulk_request_body.append(body)
    return request


def _map_refresh(value):
    mapping = {
        "true": REFRESH_TRUE,
        "false": REFRESH_FALSE,
        "wait_for": REFRESH_WAIT_FOR,
        True: REFRESH_TRUE,
        False: REFRESH_FALSE,
    }
    return mapping.get(value, REFRESH_UNSPECIFIED)


def _map_version_type(value):
    mapping = {
        "internal": VERSION_TYPE_INTERNAL,
        "external": VERSION_TYPE_EXTERNAL,
        "external_gte": VERSION_TYPE_EXTERNAL_GTE,
    }
    return mapping.get(value, VERSION_TYPE_UNSPECIFIED)


def _build_index_op(container, meta):
    op = IndexOperation()
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
    op = WriteOperation()
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
    op = UpdateOperation()
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
    op = DeleteOperation()
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
    action = UpdateAction()
    if "doc" in source:
        action.doc = json.dumps(source["doc"]).encode("utf-8")
    if "doc_as_upsert" in source:
        action.doc_as_upsert = source["doc_as_upsert"]
    if "upsert" in source:
        action.upsert = json.dumps(source["upsert"]).encode("utf-8")
    if "scripted_upsert" in source:
        action.scripted_upsert = source["scripted_upsert"]
    if "detect_noop" in source:
        action.detect_noop = source["detect_noop"]
    return action


_OP_BUILDERS = {
    "index": _build_index_op,
    "create": _build_create_op,
    "update": _build_update_op,
    "delete": _build_delete_op,
}


# ─── Bulk Request (multi-document) ────────────────────────────────────────────


def toProtoBulkRequest(body, index=None, pipeline=None, routing=None,
                       refresh=None, timeout=None, require_alias=None):
    """
    Convert an opensearch-py bulk body (list of action/source dicts or NDJSON string)
    into a protobuf BulkRequest.

    Mirrors: client.bulk(body=..., index=..., ...)
    """
    request = BulkRequest()
    body = _normalize_body(body)

    if index is not None:
        request.index = index
    if pipeline is not None:
        request.pipeline = pipeline
    if routing is not None:
        request.routing = routing
    if timeout is not None:
        request.timeout = timeout
    if require_alias is not None:
        request.require_alias = require_alias
    if refresh is not None:
        request.refresh = _map_refresh(refresh)

    i = 0
    while i < len(body):
        action_dict = body[i]
        i += 1
        op_type = next(iter(action_dict))
        meta = action_dict[op_type]

        source = None
        if op_type != "delete" and i < len(body):
            source = body[i]
            i += 1

        bulk_body = BulkRequestBody()
        op_container = OperationContainer()
        _OP_BUILDERS[op_type](op_container, meta)
        bulk_body.operation_container.CopyFrom(op_container)

        if op_type == "update" and source is not None:
            bulk_body.update_action.CopyFrom(_build_update_action(source))
        elif source is not None:
            bulk_body.object = json.dumps(source).encode("utf-8")

        request.bulk_request_body.append(bulk_body)

    return request


def _normalize_body(body):
    if isinstance(body, str):
        lines = [line.strip() for line in body.split("\n") if line.strip()]
        return [json.loads(line) for line in lines]
    return body
