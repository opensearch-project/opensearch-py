"""
translation.py — gRPC Translation Layer

Two classes handle the full round-trip:

    BulkRequestProtoBuilder  — Python client dict → Protobuf BulkRequest
    ResponseConverter — Protobuf BulkResponse → Python client dict

BulkRequestProtoBuilder handles both single and bulk operations through one interface.
ResponseConverter converts server responses back to the format the client sent in.
"""

import json
from typing import Any, Dict, List, Optional, Tuple, Union

from opensearch.protobufs.schemas.common_pb2 import (
    OP_TYPE_CREATE,
    OP_TYPE_INDEX,
    REFRESH_FALSE,
    REFRESH_TRUE,
    REFRESH_UNSPECIFIED,
    REFRESH_WAIT_FOR,
    VERSION_TYPE_EXTERNAL,
    VERSION_TYPE_EXTERNAL_GTE,
    VERSION_TYPE_INTERNAL,
    VERSION_TYPE_UNSPECIFIED,
    WAIT_FOR_ACTIVE_SHARD_OPTIONS_ALL,
    BulkRequest,
    BulkRequestBody,
    DeleteOperation,
    IndexOperation,
    InlineScript,
    OperationContainer,
    Script,
    SourceConfig,
    SourceConfigParam,
    SourceFilter,
    StoredScriptId,
    StringArray,
    UpdateAction,
    UpdateOperation,
    WaitForActiveShards,
    WriteOperation,
)

# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST CONVERTER — Python client dict → Protobuf BulkRequest
# ═══════════════════════════════════════════════════════════════════════════════


class BulkRequestProtoBuilder:
    """
    Converts Python client operations into a protobuf BulkRequest.

    Supports both single-doc and bulk operations through one unified interface.
    Queue operations with index(), create(), update(), delete(), then call build().

    Single document usage:
        req = BulkRequestProtoBuilder(index="my-index", refresh="true")
        req.index(body={"title": "Hello"}, id="1")
        proto_request = req.build()

    Bulk usage:
        req = BulkRequestProtoBuilder(index="my-index", refresh="true")
        req.index(body={"title": "Doc 1"}, id="1")
        req.index(body={"title": "Doc 2"}, id="2")
        req.create(body={"title": "Doc 3"}, id="3")
        req.update(id="1", body={"doc": {"title": "Updated"}})
        req.delete(id="2")
        proto_request = req.build()

    From raw body (NDJSON string or list of action/source dicts):
        req = BulkRequestProtoBuilder.from_body(body, index="my-index", refresh="true")
        proto_request = req.build()
    """

    def __init__(
        self,
        index: Optional[str] = None,
        refresh: Optional[str] = None,
        timeout: Optional[str] = None,
        pipeline: Optional[str] = None,
        routing: Optional[str] = None,
        require_alias: Optional[bool] = None,
        x_source: Optional[Union[bool, List[str]]] = None,
        x_source_excludes: Optional[List[str]] = None,
        x_source_includes: Optional[List[str]] = None,
        wait_for_active_shards: Optional[Union[int, str]] = None,
    ) -> None:
        self._index = index
        self._refresh = refresh
        self._timeout = timeout
        self._pipeline = pipeline
        self._routing = routing
        self._require_alias = require_alias
        self._x_source = x_source
        self._x_source_excludes = x_source_excludes
        self._x_source_includes = x_source_includes
        self._wait_for_active_shards = wait_for_active_shards
        self._operations: List[Tuple[str, Dict[str, Any], Optional[Dict[str, Any]]]] = (
            []
        )

    def index(
        self,
        body: Dict[str, Any],
        index: Optional[str] = None,
        id: Optional[str] = None,
        routing: Optional[str] = None,
        pipeline: Optional[str] = None,
        require_alias: Optional[bool] = None,
        if_primary_term: Optional[int] = None,
        if_seq_no: Optional[int] = None,
        version: Optional[int] = None,
        version_type: Optional[str] = None,
        op_type: Optional[str] = None,
    ) -> "BulkRequestProtoBuilder":
        """Queue an index operation. Mirrors client.index()."""
        meta: Dict[str, Any] = {"_index": index or self._index}
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
        if op_type is not None:
            meta["op_type"] = op_type
        self._operations.append(("index", meta, body))
        return self

    def create(
        self,
        body: Dict[str, Any],
        index: Optional[str] = None,
        id: Optional[str] = None,
        routing: Optional[str] = None,
        pipeline: Optional[str] = None,
        require_alias: Optional[bool] = None,
    ) -> "BulkRequestProtoBuilder":
        """Queue a create operation. Mirrors client.create()."""
        meta: Dict[str, Any] = {"_index": index or self._index}
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

    def update(
        self,
        id: str,
        body: Dict[str, Any],
        index: Optional[str] = None,
        routing: Optional[str] = None,
        require_alias: Optional[bool] = None,
        if_primary_term: Optional[int] = None,
        if_seq_no: Optional[int] = None,
        retry_on_conflict: Optional[int] = None,
    ) -> "BulkRequestProtoBuilder":
        """Queue an update operation. Mirrors client.update()."""
        meta: Dict[str, Any] = {"_index": index or self._index, "_id": id}
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

    def delete(
        self,
        id: str,
        index: Optional[str] = None,
        routing: Optional[str] = None,
        if_primary_term: Optional[int] = None,
        if_seq_no: Optional[int] = None,
        version: Optional[int] = None,
        version_type: Optional[str] = None,
    ) -> "BulkRequestProtoBuilder":
        """Queue a delete operation. Mirrors client.delete()."""
        meta: Dict[str, Any] = {"_index": index or self._index, "_id": id}
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

    def build(self) -> Any:
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
        if self._x_source is not None:
            source_param = SourceConfigParam()
            if isinstance(self._x_source, bool):
                source_param.fetch = self._x_source
            elif isinstance(self._x_source, list):
                source_param.fields.CopyFrom(StringArray(string_array=self._x_source))
            request.x_source.CopyFrom(source_param)
        if self._x_source_excludes:
            request.x_source_excludes.extend(self._x_source_excludes)
        if self._x_source_includes:
            request.x_source_includes.extend(self._x_source_includes)
        if self._wait_for_active_shards is not None:
            wfas = WaitForActiveShards()
            if isinstance(self._wait_for_active_shards, int):
                wfas.count = self._wait_for_active_shards
            elif self._wait_for_active_shards == "all":
                wfas.option = WAIT_FOR_ACTIVE_SHARD_OPTIONS_ALL
            request.wait_for_active_shards.CopyFrom(wfas)

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
    def from_body(
        cls,
        body: Union[str, List[Dict[str, Any]]],
        index: Optional[str] = None,
        refresh: Optional[str] = None,
        timeout: Optional[str] = None,
        pipeline: Optional[str] = None,
        routing: Optional[str] = None,
        require_alias: Optional[bool] = None,
        x_source: Optional[Union[bool, List[str]]] = None,
        x_source_excludes: Optional[List[str]] = None,
        x_source_includes: Optional[List[str]] = None,
        wait_for_active_shards: Optional[Union[int, str]] = None,
    ) -> "BulkRequestProtoBuilder":
        """
        Create a BulkRequestProtoBuilder from raw bulk body (list of dicts or NDJSON string).

        Mirrors: client.bulk(body=..., index=..., ...)
        """
        converter = cls(
            index=index,
            refresh=refresh,
            timeout=timeout,
            pipeline=pipeline,
            routing=routing,
            require_alias=require_alias,
            x_source=x_source,
            x_source_excludes=x_source_excludes,
            x_source_includes=x_source_includes,
            wait_for_active_shards=wait_for_active_shards,
        )

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

    def __len__(self) -> int:
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

    """

    @staticmethod
    def from_bulk_response(response: Any) -> Dict[str, Any]:
        """
        Convert protobuf BulkResponse → Python dict (opensearch-py format).

        Always returns the bulk response structure:
            {"took": 50, "errors": False, "items": [{"index": {...}}, ...]}
        """
        return ResponseConverter._convert_bulk_items(response)

    @staticmethod
    def _convert_bulk_items(response: Any) -> Dict[str, Any]:
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
                        "_version": (
                            resp_item.x_version
                            if resp_item.HasField("x_version")
                            else None
                        ),
                        "_seq_no": (
                            resp_item.x_seq_no
                            if resp_item.HasField("x_seq_no")
                            else None
                        ),
                        "_primary_term": (
                            resp_item.x_primary_term
                            if resp_item.HasField("x_primary_term")
                            else None
                        ),
                        "status": _grpc_to_rest_status(
                            resp_item.status,
                            resp_item.result if resp_item.result else None,
                        ),
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
                            "reason": (
                                resp_item.error.reason
                                if resp_item.error.HasField("reason")
                                else None
                            ),
                        }
                    # forced_refresh: Whether the doc was force-refreshed
                    if resp_item.HasField("forced_refresh"):
                        item_dict["forced_refresh"] = resp_item.forced_refresh
                    # get: Inline get with document source
                    if resp_item.HasField("get"):
                        get_dict: Dict[str, Any] = {"found": resp_item.get.found}
                        if resp_item.get.HasField("x_seq_no"):
                            get_dict["_seq_no"] = resp_item.get.x_seq_no
                        if resp_item.get.HasField("x_primary_term"):
                            get_dict["_primary_term"] = resp_item.get.x_primary_term
                        if resp_item.get.HasField("x_source"):
                            get_dict["_source"] = resp_item.get.x_source.decode("utf-8")
                        item_dict["get"] = get_dict
                    # _shards.failures: Shard failure details
                    if resp_item.HasField("x_shards") and resp_item.x_shards.failures:
                        failures = []
                        for f in resp_item.x_shards.failures:
                            failure: Dict[str, Any] = {
                                "shard": f.shard,
                                "primary": f.primary,
                                "reason": {
                                    "type": f.reason.type,
                                    "reason": (
                                        f.reason.reason
                                        if f.reason.HasField("reason")
                                        else None
                                    ),
                                },
                            }
                            if f.HasField("index"):
                                failure["index"] = f.index
                            if f.HasField("node"):
                                failure["node"] = f.node
                            failures.append(failure)
                        item_dict["_shards"]["failures"] = failures
                    item_dict = {k: v for k, v in item_dict.items() if v is not None}
                    items.append({op_type: item_dict})
                    break

        result: Dict[str, Any] = {
            "took": response.took,
            "errors": response.errors,
            "items": items,
        }
        # ingest_took: Time in ms spent processing documents through ingest pipeline
        if response.HasField("ingest_took"):
            result["ingest_took"] = response.ingest_took
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# INTERNAL HELPERS — Operation builders and enum mappers
# ═══════════════════════════════════════════════════════════════════════════════


def _grpc_to_rest_status(grpc_code: int, result: Optional[str] = None) -> int:
    """Convert gRPC status code to REST HTTP status code.

    gRPC uses different status codes than REST. The mapping is based on the
    OpenSearch server's RestToGrpcStatusConverter.java:
    https://github.com/opensearch-project/OpenSearch/blob/main/modules/transport-grpc/
    src/main/java/org/opensearch/transport/grpc/util/RestToGrpcStatusConverter.java

    For OK (0), the result field disambiguates the specific REST code:
    - "created" -> 201
    - "updated", "deleted", "noop" -> 200

    See: https://grpc.io/docs/guides/status-codes/
    """
    if grpc_code == 0:  # OK - disambiguate using result field
        if result == "created":
            return 201
        return 200
    # Non-OK gRPC codes map to REST error codes
    mapping = {
        1: 499,  # CANCELLED
        2: 500,  # UNKNOWN
        3: 400,  # INVALID_ARGUMENT (BAD_REQUEST, CONFLICT)
        4: 408,  # DEADLINE_EXCEEDED (REQUEST_TIMEOUT, GATEWAY_TIMEOUT)
        5: 404,  # NOT_FOUND (NOT_FOUND, GONE)
        6: 409,  # ALREADY_EXISTS (CONFLICT for create operations)
        7: 403,  # PERMISSION_DENIED (UNAUTHORIZED, FORBIDDEN)
        8: 429,  # RESOURCE_EXHAUSTED (TOO_MANY_REQUESTS)
        9: 412,  # FAILED_PRECONDITION (redirects, LOCKED, FAILED_DEPENDENCY)
        10: 409,  # ABORTED
        11: 400,  # OUT_OF_RANGE
        12: 501,  # UNIMPLEMENTED (METHOD_NOT_ALLOWED, NOT_IMPLEMENTED)
        13: 500,  # INTERNAL (INTERNAL_SERVER_ERROR)
        14: 503,  # UNAVAILABLE (BAD_GATEWAY, SERVICE_UNAVAILABLE)
        15: 500,  # DATA_LOSS
        16: 401,  # UNAUTHENTICATED (PROXY_AUTHENTICATION)
    }
    return mapping.get(grpc_code, 500)


def _map_refresh(value: Union[str, bool, bytes]) -> Any:
    # opensearch-py may pass refresh as bytes (b"true") from query params
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    mapping = {
        "true": REFRESH_TRUE,
        "false": REFRESH_FALSE,
        "wait_for": REFRESH_WAIT_FOR,
        True: REFRESH_TRUE,
        False: REFRESH_FALSE,
    }
    return mapping.get(value, REFRESH_UNSPECIFIED)


def _map_version_type(value: str) -> Any:
    mapping = {
        "internal": VERSION_TYPE_INTERNAL,
        "external": VERSION_TYPE_EXTERNAL,
        "external_gte": VERSION_TYPE_EXTERNAL_GTE,
    }
    return mapping.get(value, VERSION_TYPE_UNSPECIFIED)


def _build_index_op(container: Any, meta: Dict[str, Any]) -> None:
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
    if "op_type" in meta:
        op.op_type = _map_op_type(meta["op_type"])
    container.index.CopyFrom(op)


def _build_create_op(container: Any, meta: Dict[str, Any]) -> None:
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


def _build_update_op(container: Any, meta: Dict[str, Any]) -> None:
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


def _build_delete_op(container: Any, meta: Dict[str, Any]) -> None:
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


def _build_update_action(source: Dict[str, Any]) -> Any:
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
    if "script" in source:
        action.script.CopyFrom(_build_script(source["script"]))
    # _source: Controls which fields to return in the update response
    if "_source" in source:
        src = source["_source"]
        source_config = SourceConfig()
        if isinstance(src, bool):
            source_config.fetch = src
        elif isinstance(src, dict):
            sf = SourceFilter()
            if "includes" in src:
                sf.includes.extend(src["includes"])
            if "excludes" in src:
                sf.excludes.extend(src["excludes"])
            source_config.filter.CopyFrom(sf)
        action.x_source.CopyFrom(source_config)
    return action


def _map_op_type(value: str) -> Any:
    """Map op_type string to protobuf OpType enum."""
    mapping = {
        "index": OP_TYPE_INDEX,
        "create": OP_TYPE_CREATE,
    }
    return mapping.get(value, OP_TYPE_INDEX)


def _build_script(script_dict: Dict[str, Any]) -> Any:
    """Build a Script protobuf from a script dict."""
    script = Script()
    if "source" in script_dict:
        inline = InlineScript()
        inline.source = script_dict["source"]
        if "lang" in script_dict:
            inline.lang.custom = script_dict["lang"]
        script.inline.CopyFrom(inline)
    elif "id" in script_dict:
        stored = StoredScriptId()
        stored.id = script_dict["id"]
        script.stored.CopyFrom(stored)
    return script


_OP_BUILDERS = {
    "index": _build_index_op,
    "create": _build_create_op,
    "update": _build_update_op,
    "delete": _build_delete_op,
}


# ─── Backward Compatibility ──────────────────────────────────────────────────
# These keep existing code working without changes.

BulkRequestBuilder = BulkRequestProtoBuilder


def toProtoBulkRequest(
    body: Union[str, List[Dict[str, Any]]],
    index: Optional[str] = None,
    pipeline: Optional[str] = None,
    routing: Optional[str] = None,
    refresh: Optional[str] = None,
    timeout: Optional[str] = None,
    require_alias: Optional[bool] = None,
) -> Any:
    """Legacy function — use BulkRequestProtoBuilder.from_body() instead."""
    return BulkRequestProtoBuilder.from_body(
        body,
        index=index,
        refresh=refresh,
        timeout=timeout,
        pipeline=pipeline,
        routing=routing,
        require_alias=require_alias,
    ).build()
