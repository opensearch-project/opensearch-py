# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""
Generate TypedDict models from the OpenSearch OpenAPI specification.

Run via ``nox -s generate`` (before ``utils/generate_api.py``) or directly:

    python utils/generate_types.py
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import warnings
from pathlib import Path
from typing import Any, Dict, cast

import requests
import yaml
from datamodel_code_generator import DataModelType, InputFileType, generate
from datamodel_code_generator.format import PythonVersion
from type_naming import schema_key_to_type_name, schema_ref_to_key

CODE_ROOT = Path(__file__).resolve().parent.parent
TYPES_DIR = CODE_ROOT / "opensearchpy" / "_types"
CACHE_DIR = CODE_ROOT / "utils" / ".cache"
OPENAPI_URL = (
    "https://github.com/opensearch-project/opensearch-api-specification/"
    "releases/download/main-latest/opensearch-openapi.yaml"
)
OPENAPI_CACHE = CACHE_DIR / "opensearch-openapi.yaml"
TYPE_INDEX_PATH = CACHE_DIR / "type_index.json"
GENERATED_HEADER = (
    (CODE_ROOT / "utils" / "generated_file_headers.txt")
    .read_text(encoding="utf-8")
    .rstrip()
)
SPDX_LICENSE_HEADER = """# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
"""


def download_openapi() -> Dict[str, Any]:
    """Download and parse the OpenSearch OpenAPI specification."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not OPENAPI_CACHE.exists():
        response = requests.get(OPENAPI_URL, timeout=120)
        response.raise_for_status()
        OPENAPI_CACHE.write_bytes(response.content)
    with OPENAPI_CACHE.open(encoding="utf-8") as handle:
        return cast(Dict[str, Any], yaml.safe_load(handle))


def inline_request_body_schemas(data: Dict[str, Any]) -> None:
    """Promote inline requestBody schemas into components/schemas for codegen."""
    schemas = data.setdefault("components", {}).setdefault("schemas", {})
    for _name, request_body in (
        data.get("components", {}).get("requestBodies", {}).items()
    ):
        for content in request_body.get("content", {}).values():
            schema = content.get("schema", {})
            if "$ref" in schema:
                continue
            if "properties" not in schema and "allOf" not in schema:
                continue
            title = schema.get("title")
            if not title:
                continue
            if title not in schemas:
                schemas[title] = schema
            content["schema"] = {"$ref": f"#/components/schemas/{title}"}


def run_datamodel_codegen(openapi_path: Path, output_dir: Path) -> None:
    """Generate TypedDict modules from an OpenAPI file via datamodel-code-generator."""
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="Field name .* is duplicated",
            category=UserWarning,
            module="datamodel_code_generator.model.base",
        )
        warnings.filterwarnings(
            "ignore",
            message=".*formatters.*",
            category=FutureWarning,
            module="datamodel_code_generator.format",
        )
        generate(
            openapi_path,
            input_file_type=InputFileType.OpenAPI,
            output=output_dir,
            output_model_type=DataModelType.TypingTypedDict,
            target_python_version=PythonVersion.PY_310,
            use_standard_collections=True,
            use_union_operator=True,
            use_closed_typed_dict=False,
            disable_timestamp=True,
        )


def build_type_index(output_dir: Path) -> Dict[str, Dict[str, str]]:
    """Map TypedDict class name -> {module: filename without .py}."""
    index: Dict[str, Dict[str, str]] = {}
    for path in sorted(output_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        module = path.stem
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"^class (\w+)\(", content, re.MULTILINE):
            index[match.group(1)] = {"module": module}
        for match in re.finditer(
            r"^(\w+) = TypedDict\(\s*\n\s*['\"](\w+)['\"]",
            content,
            re.MULTILINE,
        ):
            index[match.group(2)] = {"module": module}
    return index


def _defined_names(stmt: ast.stmt) -> set[str]:
    """Return top-level names defined by a module statement."""
    if isinstance(stmt, ast.ClassDef):
        return {stmt.name}
    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
        return {stmt.target.id}
    if isinstance(stmt, ast.Assign):
        return {target.id for target in stmt.targets if isinstance(target, ast.Name)}
    return set()


def _collect_type_names(node: ast.AST, names: set[str]) -> None:
    """Collect identifier names referenced in a type expression AST node."""
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        names.add(node.id)
    elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        _collect_type_names(node.left, names)
        _collect_type_names(node.right, names)
    elif isinstance(node, ast.Subscript):
        _collect_type_names(node.value, names)
        _collect_type_names(node.slice, names)
    elif isinstance(node, ast.Tuple):
        for elt in node.elts:
            _collect_type_names(elt, names)
    elif isinstance(node, ast.List):
        for elt in node.elts:
            _collect_type_names(elt, names)
    elif isinstance(node, ast.Call):
        for arg in node.args:
            _collect_type_names(arg, names)
        for keyword in node.keywords:
            _collect_type_names(keyword.value, names)
    elif isinstance(node, ast.Dict):
        for value in node.values:
            if value is not None:
                _collect_type_names(value, names)


def _used_names(stmt: ast.stmt) -> set[str]:
    """Return names referenced at import time by a module statement."""
    names: set[str] = set()
    if isinstance(stmt, ast.ClassDef):
        for base in stmt.bases:
            _collect_type_names(base, names)
    else:
        for node in ast.walk(stmt):
            _collect_type_names(node, names)
    return (
        names
        - _defined_names(stmt)
        - set(dir(ast))
        - {
            "TypedDict",
            "NotRequired",
            "Literal",
            "Union",
            "Any",
            "TypeAlias",
            "Optional",
            "list",
            "dict",
            "tuple",
            "set",
            "bool",
            "int",
            "float",
            "str",
            "bytes",
        }
    )


def _topological_sort(stmts: list[ast.stmt]) -> list[ast.stmt]:
    """Order statements so runtime dependencies are defined first."""
    defined: dict[str, int] = {}
    for index, stmt in enumerate(stmts):
        defined.update({name: index for name in _defined_names(stmt)})

    edges: dict[int, set[int]] = {i: set() for i in range(len(stmts))}
    for index, stmt in enumerate(stmts):
        for name in _used_names(stmt):
            dep = defined.get(name)
            if dep is not None and dep != index:
                edges[index].add(dep)

    ordered: list[int] = []
    visiting: set[int] = set()
    visited: set[int] = set()

    def visit(node: int) -> None:
        if node in visited:
            return
        if node in visiting:
            return
        visiting.add(node)
        for dep in sorted(edges[node]):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
        ordered.append(node)

    for index in range(len(stmts)):
        visit(index)

    return [stmts[i] for i in ordered]


def _stmt_source(content: str, stmt: ast.stmt) -> str:
    """Extract the source text for a top-level statement."""
    segment = ast.get_source_segment(content, stmt)
    if segment is None:
        raise RuntimeError(f"Could not extract source for {type(stmt).__name__}")
    return segment.rstrip() + "\n\n"


def fix_self_referential_functional_typeddicts(path: Path) -> None:
    """Quote forward references inside ``Name = TypedDict(...)`` for self ``Name``."""
    content = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^(\w+) = TypedDict\(\n.*?\n\)\n", re.MULTILINE | re.DOTALL)

    def fix_block(match: re.Match[str]) -> str:
        block = match.group(0)
        name = match.group(1)
        block = re.sub(
            rf"NotRequired\[{re.escape(name)}\]",
            f"NotRequired['{name}']",
            block,
        )
        block = re.sub(
            rf"dict\[str, {re.escape(name)}\]",
            f"dict[str, '{name}']",
            block,
        )
        block = re.sub(
            rf"\b{re.escape(name)} \|",
            f"'{name}' |",
            block,
        )
        block = re.sub(
            rf"\| {re.escape(name)}\b",
            f"| '{name}'",
            block,
        )
        return block

    path.write_text(pattern.sub(fix_block, content), encoding="utf-8")


def reorder_module_definitions(path: Path) -> None:
    """
    Topologically sort top-level definitions so import-time dependencies resolve.

    datamodel-code-generator can emit TypedDicts, TypeAliases, and classes in an
    order that causes NameError at import time (unlike annotations deferred via
    ``from __future__ import annotations``).
    """
    content = path.read_text(encoding="utf-8")
    tree = ast.parse(content)

    prefix: list[str] = []
    reorderable: list[ast.stmt] = []
    for stmt in tree.body:
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            prefix.append(_stmt_source(content, stmt))
        elif (
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Constant)
            and isinstance(stmt.value.value, str)
        ):
            prefix.append(_stmt_source(content, stmt))
        elif (
            len(reorderable) == 0
            and isinstance(stmt, ast.ImportFrom)
            and stmt.module == "__future__"
        ):
            prefix.append(_stmt_source(content, stmt))
        else:
            reorderable.append(stmt)

    if not reorderable:
        return

    sorted_stmts = _topological_sort(reorderable)
    if [id(s) for s in sorted_stmts] == [id(s) for s in reorderable]:
        return

    body = "".join(_stmt_source(content, stmt) for stmt in sorted_stmts)
    path.write_text(
        "".join(prefix).rstrip() + "\n\n\n" + body.rstrip() + "\n", encoding="utf-8"
    )


def apply_license_headers(output_dir: Path) -> None:
    """Replace datamodel-codegen headers with the project license header."""
    for path in output_dir.glob("*.py"):
        body = path.read_text(encoding="utf-8")
        body = re.sub(
            r"^# generated by datamodel-codegen:.*?(?=^from __future__)",
            "",
            body,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
        path.write_text(
            f"{SPDX_LICENSE_HEADER}\n\n{GENERATED_HEADER}\n\n{body.lstrip()}",
            encoding="utf-8",
        )


def write_types_package(output_dir: Path) -> None:
    """Post-process staged types and copy them into ``opensearchpy/_types``."""
    TYPES_DIR.mkdir(parents=True, exist_ok=True)
    for path in output_dir.glob("*.py"):
        if path.name != "__init__.py":
            reorder_module_definitions(path)
            fix_self_referential_functional_typeddicts(path)
        shutil.copy2(path, TYPES_DIR / path.name)
    staging_init = output_dir / "__init__.py"
    if staging_init.exists():
        init_body = staging_init.read_text(encoding="utf-8")
        init_body = re.sub(
            r"^# generated by datamodel-codegen:.*?(?=^from \.)",
            "",
            init_body,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
        init_body = re.sub(
            rf"^{re.escape(GENERATED_HEADER)}\n+",
            "",
            init_body,
            count=1,
        )
        (TYPES_DIR / "__init__.py").write_text(
            f"{SPDX_LICENSE_HEADER}\n\n{GENERATED_HEADER}\n\n{init_body.lstrip()}",
            encoding="utf-8",
        )


def resolve_schema_type(
    schema: Dict[str, Any],
    components: Dict[str, Any],
    type_index: Dict[str, Dict[str, str]],
) -> str | None:
    """Map an OpenAPI schema object to a generated TypedDict name, if known."""
    if "$ref" in schema:
        key = schema_ref_to_key(schema["$ref"])
        if key is None:
            return None
        type_name = schema_key_to_type_name(key)
        return type_name if type_name in type_index else None
    return None


def build_operation_type_map(
    data: Dict[str, Any], type_index: Dict[str, Dict[str, str]]
) -> Dict[str, Dict[str, str | None]]:
    """Map x-operation-group -> request/response TypedDict names."""
    operation_types: Dict[str, Dict[str, str | None]] = {}
    components = data.get("components", {})
    responses = components.get("responses", {})
    request_bodies = components.get("requestBodies", {})

    for _path, path_item in data.get("paths", {}).items():
        for method_dict in path_item.values():
            if not isinstance(method_dict, dict):
                continue
            op_group = method_dict.get("x-operation-group")
            if not op_group:
                continue

            request_type: str | None = None
            response_type: str | None = None

            request_body = method_dict.get("requestBody")
            if isinstance(request_body, dict) and "$ref" in request_body:
                rb = request_bodies.get(request_body["$ref"].split("/")[-1], {})
                for content in rb.get("content", {}).values():
                    schema = content.get("schema", {})
                    request_type = resolve_schema_type(schema, components, type_index)
                    if request_type:
                        break

            for status in ("200", "201", "202"):
                resp = method_dict.get("responses", {}).get(status)
                if not isinstance(resp, dict):
                    continue
                if "$ref" in resp:
                    resp = responses.get(resp["$ref"].split("/")[-1], {})
                content = resp.get("content", {}).get("application/json", {})
                schema = content.get("schema", {})
                response_type = resolve_schema_type(schema, components, type_index)
                if response_type:
                    break

            existing = operation_types.get(op_group)
            if existing:
                if request_type and not existing.get("request_type"):
                    existing["request_type"] = request_type
                if response_type and not existing.get("response_type"):
                    existing["response_type"] = response_type
            else:
                operation_types[op_group] = {
                    "request_type": request_type,
                    "response_type": response_type,
                }

    return operation_types


def enrich_operation_types(
    operation_types: Dict[str, Dict[str, str | None]],
    type_index: Dict[str, Dict[str, str]],
) -> Dict[str, Dict[str, str | None]]:
    """Attach module names for request/response types in the operation map."""
    for entry in operation_types.values():
        for key in ("request_type", "response_type"):
            type_name = entry.get(key)
            if type_name and type_name in type_index:
                entry[f"{key.rsplit('_', 1)[0]}_module"] = type_index[type_name][
                    "module"
                ]
    return operation_types


def main() -> None:
    """Generate ``opensearchpy/_types`` and the operation type index."""
    data = download_openapi()
    inline_request_body_schemas(data)

    preprocessed = CACHE_DIR / "opensearch-openapi-preprocessed.yaml"
    with preprocessed.open("w", encoding="utf-8") as handle:
        yaml.dump(data, handle, sort_keys=False)

    staging = CACHE_DIR / "types_staging"
    run_datamodel_codegen(preprocessed, staging)
    apply_license_headers(staging)
    write_types_package(staging)
    shutil.rmtree(staging)

    type_index = build_type_index(TYPES_DIR)

    operation_types = build_operation_type_map(data, type_index)
    operation_types = enrich_operation_types(operation_types, type_index)

    TYPE_INDEX_PATH.write_text(
        json.dumps(
            {"types": type_index, "operations": operation_types},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {len(type_index)} types and {len(operation_types)} operation mappings"
    )


if __name__ == "__main__":
    main()
