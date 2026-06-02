"""
translation.py — gRPC Translation Layer

Two classes handle the full round-trip:

    RequestConverter  — Python client dict → Protobuf BulkRequest
    ResponseConverter — Protobuf BulkResponse → Python client dict

RequestConverter handles both single and bulk operations through one interface.
ResponseConverter converts server responses back to the format the client sent in.
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


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST CONVERTER — Python client dict → Protobuf BulkRequest
# ═══════════════════════════════════════════════════════════════════════════════


class RequestConverter:
    """
    Converts Python client operations into a protobuf BulkRequest.

    Supports both single-doc and bulk operations through one unified interface.
    Queue operations with index(), create(), update(), delete(), then call build().

    Single document usage:
        req = RequestConverter(index="my-index", refresh="true")
        req.index(body={"title": "Hello"}, id="1")
        proto_request = req.build()

    Bulk usage:
        req = RequestConverter(index="my-index", refresh="true")
        req.index(body={"title": "Doc 1"}, id="1")
        req.index(body={"title": "Doc 2"}, id="2")
        req.create(body={"title": "Doc 3"}, id="3")
        req.update(id="1", body={"doc": {"title": "Updated"}})
        req.delete(id="2")
        proto_request = req.build()

    From raw body (NDJSON string or list of action/source dicts):
        req = RequestConverter.from_body(body, index="my-index", refresh="true")
        proto_request = req.build()
    """

    def __init__(self, index=None, refresh=None, timeout=None,
                 pipeline=None, routing=None, require_alias=None):
        self._index = index
        self._refresh = refresh
        self._timeout = timeout
        self._pipeline = pipeline
        self._routing = routing
        self._require_alias = require_alias
        self._operations = []

    def index(self, body, index=None, id=None, routing=None, pipeline=None,
              require_alias=None, if_primary_term=None, if_seq_no=None,
              version=None, version_type=None):
        """Queue an index operation. Mirrors client.index()."""
        meta = {"_index": index or self._index}
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
        self._operations.append(("index", meta, body))
        return self

    def create(self, body, index=None, id=None, routing=None, pipeline=None,
               require_alias=None):
        """Queue a create operation. Mirrors client.create()."""
        meta = {"_index": index or self._index}
        if id is not None:
            meta["_id"] = id
        if routing is not None:
            meta["routing"] = routing
        if pipeline is not None:
            meta["pipeline"] = pipeline
        if require_alias is not None:
            meta["require_alias"] = require_alias
        self._operations.append(("create", meta, body))
        return self

    def update(self, id, body, index=None, routing=None, require_alias=None,
               if_primary_term=None, if_seq_no=None, retry_on_conflict=None):
        """Queue an update operation. Mirrors client.update()."""
        meta = {"_index": index or self._index, "_id": id}
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
        self._operations.append(("update", meta, body))
        return self

    def delete(self, id, index=None, routing=None,
               if_primary_term=None, if_seq_no=None,
               version=None, version_type=None):
        """Queue a delete operation. Mirrors client.delete()."""
        meta = {"_index": index or self._index, "_id": id}
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
        self._operations.append(("delete", meta, None))
        return self

    def build(self):
        """Build the protobuf BulkRequest from all queued operations."""
        request = BulkRequest()

        if self._index is not None:
            request.index = self._index
        if self._refresh is not None:
            request.refresh = _map_refresh(self._refresh)
        if self._timeout is not None:
            request.timeout = self._timeout
        if self._pipeline is not None:
            request.pipeline = self._pipeline
        if self._routing is not None:
            request.routing = self._routing
        if self._require_alias is not None:
            request.require_alias = self._require_alias

        for op_type, meta, source in self._operations:
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

    @classmethod
    def from_body(cls, body, index=None, refresh=None, timeout=None,
                  pipeline=None, routing=None, require_alias=None):
        """
        Create a RequestConverter from raw bulk body (list of dicts or NDJSON string).

        Mirrors: client.bulk(body=..., index=..., ...)
        """
        converter = cls(index=index, refresh=refresh, timeout=timeout,
                        pipeline=pipeline, routing=routing, require_alias=require_alias)

        if isinstance(body, str):
            lines = [line.strip() for line in body.split("\n") if line.strip()]
            body = [json.loads(line) for line in lines]

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

            converter._operations.append((op_type, meta, source))

        return converter

    def __len__(self):
        return len(self._operations)


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE CONVERTER — Protobuf BulkResponse → Python client dict
# ═══════════════════════════════════════════════════════════════════════════════


class ResponseConverter:
    """
    Converts protobuf responses back to the Python client format.

    The client sent data as Python dicts. After the server processes it via gRPC,
    this class converts the protobuf response back to the same representation.

    Usage:
        # Convert server response to client format
        result = ResponseConverter.from_bulk_response(response)

        # Reconstruct what the client originally sent
        original = ResponseConverter.from_proto_request(request)
    """

    @staticmethod
    def from_bulk_response(response):
        """
        Convert protobuf BulkResponse → Python dict (opensearch-py format).

        For single-doc operations, returns the one item as a dict.
        For bulk operations, returns the full bulk response structure.

        Single-doc output:
            {"_index": "idx", "_id": "1", "result": "created", "_version": 1, ...}

        Bulk output:
            {"took": 50, "errors": False, "items": [{"index": {...}}, ...]}
        """
        if len(response.items) == 1:
            return ResponseConverter._convert_single_item(response)
        else:
            return ResponseConverter._convert_bulk_items(response)

    @staticmethod
    def _convert_single_item(response):
        """Convert a single-item response to opensearch-py dict format."""
        item = response.items[0]

        for op_type in ("index", "create", "update", "delete"):
            if item.HasField(op_type):
                resp_item = getattr(item, op_type)
                break
        else:
            return {"error": "Unknown response type"}

        result = {
            "_index": resp_item.x_index,
            "_id": resp_item.x_id if resp_item.x_id else None,
            "result": resp_item.result if resp_item.result else None,
            "_version": resp_item.x_version if resp_item.HasField("x_version") else None,
            "_seq_no": resp_item.x_seq_no if resp_item.HasField("x_seq_no") else None,
            "_primary_term": resp_item.x_primary_term if resp_item.HasField("x_primary_term") else None,
        }

        if resp_item.HasField("x_shards"):
            result["_shards"] = {
                "total": resp_item.x_shards.total,
                "successful": resp_item.x_shards.successful,
                "failed": resp_item.x_shards.failed,
            }

        if resp_item.HasField("error"):
            result["error"] = {
                "type": resp_item.error.type,
                "reason": resp_item.error.reason if resp_item.error.HasField("reason") else None,
            }

        return {k: v for k, v in result.items() if v is not None}

    @staticmethod
    def _convert_bulk_items(response):
        """Convert a multi-item bulk response to opensearch-py dict format."""
        items = []
        for item in response.items:
            for op_type in ("index", "create", "update", "delete"):
                if item.HasField(op_type):
                    resp_item = getattr(item, op_type)
                    item_dict = {
                        "_index": resp_item.x_index,
                        "_id": resp_item.x_id if resp_item.x_id else None,
                        "result": resp_item.result if resp_item.result else None,
                        "_version": resp_item.x_version if resp_item.HasField("x_version") else None,
                        "_seq_no": resp_item.x_seq_no if resp_item.HasField("x_seq_no") else None,
                        "_primary_term": resp_item.x_primary_term if resp_item.HasField("x_primary_term") else None,
                        "status": resp_item.status,
                    }
                    if resp_item.HasField("x_shards"):
                        item_dict["_shards"] = {
                            "total": resp_item.x_shards.total,
                            "successful": resp_item.x_shards.successful,
                            "failed": resp_item.x_shards.failed,
                        }
                    if resp_item.HasField("error"):
                        item_dict["error"] = {
                            "type": resp_item.error.type,
                            "reason": resp_item.error.reason if resp_item.error.HasField("reason") else None,
                        }
                    item_dict = {k: v for k, v in item_dict.items() if v is not None}
                    items.append({op_type: item_dict})
                    break

        return {
            "took": response.took,
            "errors": response.errors,
            "items": items,
        }

    @staticmethod
    def from_proto_request(request):
        """
        Reconstruct the original Python client request from protobuf.

        Returns what the client originally sent, in the same format they sent it.

        Single-doc output:
            {"operation": "index", "index": "my-index", "id": "doc-1", "body": {"title": "Hello"}}

        Bulk output:
            [
                {"operation": "index", "index": "my-index", "id": "1", "body": {"title": "Doc 1"}},
                {"operation": "delete", "index": "my-index", "id": "2"},
            ]
        """
        results = []
        for bulk_body in request.bulk_request_body:
            op_container = bulk_body.operation_container

            if op_container.HasField("index"):
                op, op_type = op_container.index, "index"
            elif op_container.HasField("create"):
                op, op_type = op_container.create, "create"
            elif op_container.HasField("update"):
                op, op_type = op_container.update, "update"
            elif op_container.HasField("delete"):
                op, op_type = op_container.delete, "delete"
            else:
                results.append({"error": "Unknown operation type"})
                continue

            original = {
                "operation": op_type,
                "index": op.x_index if op.x_index else request.index,
                "id": op.x_id if op.x_id else None,
            }

            if bulk_body.HasField("object") and bulk_body.object:
                original["body"] = json.loads(bulk_body.object.decode("utf-8"))
            elif bulk_body.HasField("update_action"):
                update_body = {}
                action = bulk_body.update_action
                if action.HasField("doc") and action.doc:
                    update_body["doc"] = json.loads(action.doc.decode("utf-8"))
                if action.HasField("doc_as_upsert"):
                    update_body["doc_as_upsert"] = action.doc_as_upsert
                if action.HasField("upsert") and action.upsert:
                    update_body["upsert"] = json.loads(action.upsert.decode("utf-8"))
                if action.HasField("scripted_upsert"):
                    update_body["scripted_upsert"] = action.scripted_upsert
                if action.HasField("detect_noop"):
                    update_body["detect_noop"] = action.detect_noop
                original["body"] = update_body

            original = {k: v for k, v in original.items() if v is not None}
            results.append(original)

        # Single doc: return just the one item. Bulk: return the list.
        if len(results) == 1:
            return results[0]
        return results


# ═══════════════════════════════════════════════════════════════════════════════
# INTERNAL HELPERS — Operation builders and enum mappers
# ═══════════════════════════════════════════════════════════════════════════════


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


# ─── Backward Compatibility ──────────────────────────────────────────────────
# These keep existing code working without changes.

BulkRequestBuilder = RequestConverter


def toProtoBulkRequest(body, index=None, pipeline=None, routing=None,
                       refresh=None, timeout=None, require_alias=None):
    """Legacy function — use RequestConverter.from_body() instead."""
    return RequestConverter.from_body(
        body, index=index, refresh=refresh, timeout=timeout,
        pipeline=pipeline, routing=routing, require_alias=require_alias
    ).build()


def toProtoIndexRequest(index, body, id=None, **kwargs):
    """Legacy function — use RequestConverter().index().build() instead."""
    return RequestConverter(index=index, **{k: v for k, v in kwargs.items() if k in ('refresh', 'timeout')}).index(body=body, id=id, **{k: v for k, v in kwargs.items() if k not in ('refresh', 'timeout')}).build()


def _build_single_request(op_type, meta, source, refresh=None, timeout=None):
    """Legacy internal function — kept for simpledoc_gRPC compatibility."""
    req = RequestConverter(index=meta.get("_index"), refresh=refresh, timeout=timeout)
    if op_type == "index":
        req._operations.append(("index", meta, source))
    elif op_type == "create":
        req._operations.append(("create", meta, source))
    elif op_type == "update":
        req._operations.append(("update", meta, source))
    elif op_type == "delete":
        req._operations.append(("delete", meta, None))
    return req.build()
