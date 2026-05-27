"""Translation layer: opensearch-py bulk dict → protobuf BulkRequest."""

import json
from typing import Any, Union

from opensearch_grpc.proto import common_pb2


def toProtoBulkRequest(
    body: Union[str, list],
    index: str = None,
    pipeline: str = None,
    routing: str = None,
    refresh: str = None,
    timeout: str = None,
    require_alias: bool = None,
) -> common_pb2.BulkRequest:
    """Convert opensearch-py bulk body into a protobuf BulkRequest."""
    request = common_pb2.BulkRequest()
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
        op_type, meta = _parse_action(action_dict)

        source = None
        if op_type != "delete" and i < len(body):
            source = body[i]
            i += 1

        bulk_body = _build_bulk_request_body(op_type, meta, source)
        request.bulk_request_body.append(bulk_body)

    return request


def _normalize_body(body):
    if isinstance(body, str):
        lines = [line.strip() for line in body.split("\n") if line.strip()]
        return [json.loads(line) for line in lines]
    return body


def _parse_action(action_dict):
    op_type = next(iter(action_dict))
    return op_type, action_dict[op_type]


def _map_refresh(value):
    mapping = {
        "true": common_pb2.REFRESH_TRUE,
        "false": common_pb2.REFRESH_FALSE,
        "wait_for": common_pb2.REFRESH_WAIT_FOR,
        True: common_pb2.REFRESH_TRUE,
        False: common_pb2.REFRESH_FALSE,
    }
    return mapping.get(value, common_pb2.REFRESH_UNSPECIFIED)


def _map_version_type(value):
    mapping = {
        "internal": common_pb2.VERSION_TYPE_INTERNAL,
        "external": common_pb2.VERSION_TYPE_EXTERNAL,
        "external_gte": common_pb2.VERSION_TYPE_EXTERNAL_GTE,
    }
    return mapping.get(value, common_pb2.VERSION_TYPE_UNSPECIFIED)


def _build_bulk_request_body(op_type, meta, source):
    body = common_pb2.BulkRequestBody()
    op_container = common_pb2.OperationContainer()
    _OP_BUILDERS[op_type](op_container, meta)
    body.operation_container.CopyFrom(op_container)

    if op_type == "update" and source is not None:
        body.update_action.CopyFrom(_build_update_action(source))
    elif source is not None:
        body.object = json.dumps(source).encode("utf-8")

    return body


def _build_index_op(container, meta):
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
    action = common_pb2.UpdateAction()
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
