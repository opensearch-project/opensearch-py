#!/usr/bin/env python
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

import os
import re
from functools import lru_cache
from itertools import chain, groupby
from operator import itemgetter
from pathlib import Path

import black
import requests
import unasync
import urllib3
from click.testing import CliRunner
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

http = urllib3.PoolManager()

# line to look for in the original source file
SEPARATOR = "    # AUTO-GENERATED-API-DEFINITIONS #"
# global substitutions for python keywords
SUBSTITUTIONS = {"type": "doc_type", "from": "from_"}


# api path(s)
BRANCH_NAME = "7.x"
CODE_ROOT = Path(__file__).absolute().parent.parent
GLOBAL_QUERY_PARAMS = {
    "pretty": "Optional[bool]",
    "human": "Optional[bool]",
    "error_trace": "Optional[bool]",
    "format": "Optional[str]",
    "filter_path": "Optional[Union[str, Collection[str]]]",
    "request_timeout": "Optional[Union[int, float]]",
    "ignore": "Optional[Union[int, Collection[int]]]",
    "opaque_id": "Optional[str]",
    "http_auth": "Optional[Union[str, Tuple[str, str]]]",
    "api_key": "Optional[Union[str, Tuple[str, str]]]",
}

jinja_env = Environment(
    autoescape=select_autoescape(["html", "xml"]),
    loader=FileSystemLoader([CODE_ROOT / "utils" / "templates"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def blacken(filename):
    runner = CliRunner()
    result = runner.invoke(black.main, [str(filename)])
    assert result.exit_code == 0, result.output


@lru_cache()
def is_valid_url(url):
    return 200 <= http.request("HEAD", url).status < 400


class Module:
    def __init__(self, namespace, is_pyi=False):
        self.namespace = namespace
        self.is_pyi = is_pyi
        self._apis = []
        self.parse_orig()

        if not is_pyi:
            self.pyi = Module(namespace, is_pyi=True)
            self.pyi.orders = self.orders[:]

    def add(self, api):
        self._apis.append(api)

    def parse_orig(self):
        self.orders = []
        self.header = ""
        if self.is_pyi is True:
            self.header = "from typing import Any, Collection, MutableMapping, Optional, Tuple, Union\n\n"

        namespace_new = "".join(word.capitalize() for word in self.namespace.split("_"))
        self.header = (
            self.header + "class " + namespace_new + "Client(NamespacedClient):"
        )
        if os.path.exists(self.filepath):
            with open(self.filepath) as f:
                content = f.read()
                header_lines = []
                for line in content.split("\n"):
                    header_lines.append(line)
                    if line == SEPARATOR:
                        break
                # no separator found
                else:
                    header_lines = []
                    for line in content.split("\n"):
                        header_lines.append(line)
                        if line.startswith("class"):
                            if (
                                "security.py" in str(self.filepath)
                                and not self.filepath.suffix == ".pyi"
                            ):
                                header_lines.append(
                                    "    from ._patch import health_check, update_audit_config"
                                )
                            break
                self.header = "\n".join(header_lines)
                self.orders = re.findall(
                    r"\n    (?:async )?def ([a-z_]+)\(", content, re.MULTILINE
                )

    def _position(self, api):
        try:
            return self.orders.index(api.name)
        except ValueError:
            return len(self.orders)

    def sort(self):
        self._apis.sort(key=self._position)

    def dump(self):
        self.sort()

        # This code snippet adds headers to each generated module indicating that the code is generated.
        header_separator = "# -----------------------------------------------------"
        License_header_end_1 = "# GitHub history for details."
        License_header_end_2 = "#  under the License."

        update_header = True
        License_position = 0

        # Identifying the insertion point for the "THIS CODE IS GENERATED" header.
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                content = f.read()
            if header_separator in content:
                update_header = False
                header_end_position = (
                    content.find(header_separator) + len(header_separator) + 2
                )
                header_position = content.rfind("\n", 0, header_end_position) + 1
            if License_header_end_1 in content:
                if License_header_end_2 in content:
                    position = (
                        content.find(License_header_end_2)
                        + len(License_header_end_2)
                        + 2
                    )
                else:
                    position = (
                        content.find(License_header_end_1)
                        + len(License_header_end_1)
                        + 2
                    )
                License_position = content.rfind("\n", 0, position) + 1

        current_script_folder = os.path.dirname(os.path.abspath(__file__))
        generated_file_header_path = os.path.join(
            current_script_folder, "generated_file_headers.txt"
        )
        with open(generated_file_header_path, "r") as header_file:
            header_content = header_file.read()

        # Imports are temporarily removed from the header and are regenerated later to ensure imports are updated after code generation.
        self.header = "\n".join(
            line for line in self.header.split("\n") if "from .utils import" not in line
        )

        with open(self.filepath, "w") as f:
            if update_header is True:
                f.write(
                    self.header[:License_position]
                    + "\n"
                    + header_content
                    + "\n\n"
                    + "#replace_token#\n"
                    + self.header[License_position:]
                )
            else:
                f.write(
                    self.header[:header_position]
                    + "\n"
                    + "#replace_token#\n"
                    + self.header[header_position:]
                )
            for api in self._apis:
                f.write(api.to_python())

        # Generating imports for each module
        utils_imports = ""
        file_content = ""
        with open(self.filepath, "r") as f:
            content = f.read()
            keywords = [
                "SKIP_IN_PATH",
                "_normalize_hosts",
                "_escape",
                "_make_path",
                "query_params",
                "_bulk_body",
                "_base64_auth_header",
                "NamespacedClient",
                "AddonClient",
            ]
            present_keywords = [keyword for keyword in keywords if keyword in content]

            if present_keywords:
                utils_imports = "from .utils import"
                result = f"{utils_imports} {', '.join(present_keywords)}"
                utils_imports = result
            file_content = content.replace("#replace_token#", utils_imports)

        with open(self.filepath, "w") as f:
            f.write(file_content)

        if not self.is_pyi:
            self.pyi.dump()

    @property
    def filepath(self):
        return (
            CODE_ROOT
            / f"opensearchpy/_async/client/{self.namespace}.py{'i' if self.is_pyi else ''}"
        )


class API:
    def __init__(self, namespace, name, definition, is_pyi=False):
        self.namespace = namespace
        self.name = name
        self.is_pyi = is_pyi

        # overwrite the dict to maintain key order
        definition["params"] = {
            SUBSTITUTIONS.get(p, p): v for p, v in definition.get("params", {}).items()
        }

        self._def = definition
        self.description = ""
        self.doc_url = ""
        self.stability = self._def.get("stability", "stable")
        self.deprecation_message = self._def.get("deprecation_message")

        if isinstance(definition["documentation"], str):
            self.doc_url = definition["documentation"]
        else:
            # set as attribute so it may be overridden by Module.add
            self.description = (
                definition["documentation"].get("description", "").strip()
            )
            self.doc_url = definition["documentation"].get("url", "")

        # Filter out bad URL refs like 'TODO'
        # and serve all docs over HTTPS.
        if self.doc_url:
            if not self.doc_url.startswith("http"):
                self.doc_url = ""
            if self.doc_url.startswith("http://"):
                self.doc_url = self.doc_url.replace("http://", "https://")

            # Try setting doc refs like 'current' and 'master' to our branches ref.
            if BRANCH_NAME is not None:
                revised_url = re.sub(
                    "/opensearchpy/reference/[^/]+/",
                    f"/opensearchpy/reference/{BRANCH_NAME}/",
                    self.doc_url,
                )
                if is_valid_url(revised_url):
                    self.doc_url = revised_url
                else:
                    print(f"URL {revised_url!r}, falling back on {self.doc_url!r}")

    @property
    def all_parts(self):
        parts = {}
        for url in self._def["url"]["paths"]:
            parts.update(url.get("parts", {}))

        for p in parts:
            parts[p]["required"] = all(
                p in url.get("parts", {}) for url in self._def["url"]["paths"]
            )
            parts[p]["type"] = "Any"

            # This piece of logic corresponds to calling
            # client.tasks.get() w/o a task_id which was erroneously
            # allowed in the 7.1 client library. This functionality
            # is deprecated and will be removed in 8.x.
            if self.namespace == "tasks" and self.name == "get":
                parts["task_id"]["required"] = False

        for k, sub in SUBSTITUTIONS.items():
            if k in parts:
                parts[sub] = parts.pop(k)

        dynamic, components = self.url_parts

        def ind(item):
            try:
                return components.index(item[0])
            except ValueError:
                return len(components)

        parts = dict(sorted(parts.items(), key=ind))
        return parts

    @property
    def params(self):
        parts = self.all_parts
        params = self._def.get("params", {})
        return chain(
            ((p, parts[p]) for p in parts if parts[p]["required"]),
            (("body", self.body),) if self.body else (),
            (
                (p, parts[p])
                for p in parts
                if not parts[p]["required"] and p not in params
            ),
            sorted(params.items(), key=lambda x: (x[0] not in parts, x[0])),
        )

    @property
    def body(self):
        b = self._def.get("body", {})
        if b:
            b.setdefault("required", False)
        return b

    @property
    def query_params(self):
        return (
            k
            for k in sorted(self._def.get("params", {}).keys())
            if k not in self.all_parts
        )

    @property
    def all_func_params(self):
        """Parameters that will be in the '@query_params' decorator list
        and parameters that will be in the function signature.
        This doesn't include
        """
        params = list(self._def.get("params", {}).keys())
        for url in self._def["url"]["paths"]:
            params.extend(url.get("parts", {}).keys())
        if self.body:
            params.append("body")
        return params

    @property
    def path(self):
        return max(
            (path for path in self._def["url"]["paths"]),
            key=lambda p: len(re.findall(r"\{([^}]+)\}", p["path"])),
        )

    @property
    def method(self):
        # To adhere to the HTTP RFC we shouldn't send
        # bodies in GET requests.
        default_method = self.path["methods"][0]
        if self.name == "refresh" or self.name == "flush":
            return "POST"
        if self.body and default_method == "GET" and "POST" in self.path["methods"]:
            return "POST"
        if "POST" and "PUT" in self.path["methods"] and self.name != "bulk":
            return "PUT"
        return default_method

    @property
    def url_parts(self):
        path = self.path["path"]

        dynamic = "{" in path
        if not dynamic:
            return dynamic, path

        parts = []
        for part in path.split("/"):
            if not part:
                continue

            if part[0] == "{":
                part = part[1:-1]
                parts.append(SUBSTITUTIONS.get(part, part))
            else:
                parts.append(f"'{part}'")

        return dynamic, parts

    @property
    def required_parts(self):
        parts = self.all_parts
        required = [p for p in parts if parts[p]["required"]]
        if self.body.get("required"):
            required.append("body")
        return required

    def to_python(self):
        if self.is_pyi:
            t = jinja_env.get_template("base_pyi")
        else:
            try:
                t = jinja_env.get_template(f"overrides/{self.namespace}/{self.name}")
            except TemplateNotFound:
                t = jinja_env.get_template("base")

        return t.render(
            api=self,
            substitutions={v: k for k, v in SUBSTITUTIONS.items()},
            global_query_params=GLOBAL_QUERY_PARAMS,
        )


def read_modules():
    modules = {}

    # Load the OpenAPI specification file
    response = requests.get(
        "https://raw.githubusercontent.com/opensearch-project/opensearch-api-specification/main/OpenSearch.openapi.json"
    )
    data = response.json()

    list_of_dicts = []

    for path in data["paths"]:
        for x in data["paths"][path]:
            if data["paths"][path][x]["x-operation-group"] == "nodes.hot_threads":
                if "deprecated" in data["paths"][path][x]:
                    continue
            data["paths"][path][x].update({"path": path, "method": x})
            list_of_dicts.append(data["paths"][path][x])

    # Update parameters  in each endpoint
    for p in list_of_dicts:
        if "parameters" in p:
            params = []
            parts = []

            # Iterate over the list of parameters and update them
            for x in p["parameters"]:
                if "schema" in x and "$ref" in x["schema"]:
                    schema_path_ref = x["schema"]["$ref"].split("/")[-1]
                    x["schema"] = data["components"]["schemas"][schema_path_ref]
                    params.append(x)
                else:
                    params.append(x)

            # Iterate over the list of updated parameters to separate "parts" from "params"
            k = params.copy()
            for q in k:
                if q["in"] == "path":
                    parts.append(q)
                    params.remove(q)

            # Convert "params" and "parts" into the structure required for generator.
            params_new = {}
            parts_new = {}

            for m in params:
                A = dict(type=m["schema"]["type"], description=m["description"])

                if "default" in m["schema"]:
                    A.update({"default": m["schema"]["default"]})

                if "enum" in m["schema"]:
                    A.update({"type": "enum"})
                    A.update({"options": m["schema"]["enum"]})

                if "deprecated" in m["schema"]:
                    A.update({"deprecated": m["schema"]["deprecated"]})
                    A.update(
                        {"deprecation_message": m["schema"]["x-deprecation-message"]}
                    )
                params_new.update({m["name"]: A})

            # Removing the deprecated "type"
            if p["x-operation-group"] != "nodes.hot_threads" and "type" in params_new:
                params_new.pop("type")

            if bool(params_new):
                p.update({"params": params_new})

            p.pop("parameters")

            for n in parts:
                B = dict(type=n["schema"]["type"])

                if "description" in n:
                    B.update({"description": n["description"]})

                if "x-enum-options" in n["schema"]:
                    B.update({"options": n["schema"]["x-enum-options"]})

                deprecated_new = {}
                if "deprecated" in n:
                    B.update({"deprecated": n["deprecated"]})

                    if "x-deprecation-version" in n:
                        deprecated_new.update({"version": n["x-deprecation-version"]})

                    if "x-deprecation-description" in n:
                        deprecated_new.update(
                            {"description": n["x-deprecation-description"]}
                        )

                parts_new.update({n["name"]: B})

            if bool(parts_new):
                p.update({"parts": parts_new})

    # Sort the input list by the value of the "x-operation-group" key
    list_of_dicts = sorted(list_of_dicts, key=itemgetter("x-operation-group"))

    # Group the input list by the value of the "x-operation-group" key
    for key, value in groupby(list_of_dicts, key=itemgetter("x-operation-group")):
        api = {}

        # Extract the namespace and name from the 'x-operation-group'
        if "." in key:
            namespace, name = key.rsplit(".", 1)
        else:
            namespace = "__init__"
            name = key

        # Group the data in the current group by the "path" key
        paths = []
        for key2, value2 in groupby(value, key=itemgetter("path")):
            # Extract the HTTP methods from the data in the current subgroup
            methods = []
            parts_final = {}
            for z in value2:
                methods.append(z["method"].upper())

                # Update 'api' dictionary
                if "documentation" not in api:
                    documentation = {"description": z["description"]}
                    api.update({"documentation": documentation})

                if "deprecation_message" not in api and "x-deprecation-message" in z:
                    api.update({"deprecation_message": z["x-deprecation-message"]})

                if "params" not in api and "params" in z:
                    api.update({"params": z["params"]})

                if "body" not in api and "requestBody" in z:
                    body = {"required": False}
                    if "required" in z["requestBody"]:
                        body.update({"required": z["requestBody"]["required"]})
                    q = z["requestBody"]["content"]["application/json"]["schema"][
                        "$ref"
                    ].split("/")[-1]
                    if "description" in data["components"]["schemas"][q]:
                        body.update(
                            {
                                "description": data["components"]["schemas"][q][
                                    "description"
                                ]
                            }
                        )
                    if "x-serialize" in data["components"]["schemas"][q]:
                        body.update(
                            {
                                "serialize": data["components"]["schemas"][q][
                                    "x-serialize"
                                ]
                            }
                        )

                    api.update({"body": body})

                if "parts" in z:
                    parts_final.update(z["parts"])

            if "POST" in methods or "PUT" in methods:
                api.update(
                    {
                        "stability": "stable",
                        "visibility": "public",
                        "headers": {
                            "accept": ["application/json"],
                            "content_type": ["application/json"],
                        },
                    }
                )
            else:
                api.update(
                    {
                        "stability": "stable",
                        "visibility": "public",
                        "headers": {"accept": ["application/json"]},
                    }
                )

            if bool(deprecated_new) and bool(parts_final):
                paths.append(
                    {
                        "path": key2,
                        "methods": methods,
                        "parts": parts_final,
                        "deprecated": deprecated_new,
                    }
                )
            elif bool(parts_final):
                paths.append({"path": key2, "methods": methods, "parts": parts_final})
            else:
                paths.append({"path": key2, "methods": methods})

        api.update({"url": {"paths": paths}})

        if namespace not in modules:
            modules[namespace] = Module(namespace)

        modules[namespace].add(API(namespace, name, api))
        modules[namespace].pyi.add(API(namespace, name, api, is_pyi=True))

    return modules


def dump_modules(modules):
    for mod in modules.values():
        mod.dump()

    # Unasync all the generated async code
    additional_replacements = {
        # We want to rewrite to 'Transport' instead of 'SyncTransport', etc
        "AsyncTransport": "Transport",
        "AsyncOpenSearch": "OpenSearch",
        # We don't want to rewrite this class
        "AsyncSearchClient": "AsyncSearchClient",
    }
    rules = [
        unasync.Rule(
            fromdir="/opensearchpy/_async/client/",
            todir="/opensearchpy/client/",
            additional_replacements=additional_replacements,
        ),
    ]

    filepaths = []
    for root, _, filenames in os.walk(CODE_ROOT / "opensearchpy/_async"):
        for filename in filenames:
            if filename.rpartition(".")[-1] in (
                "py",
                "pyi",
            ) and not filename.startswith("utils.py"):
                filepaths.append(os.path.join(root, filename))

    unasync.unasync_files(filepaths, rules)
    blacken(CODE_ROOT / "opensearchpy")


if __name__ == "__main__":
    dump_modules(read_modules())
