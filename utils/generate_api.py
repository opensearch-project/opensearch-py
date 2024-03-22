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
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch b.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch b.V. licenses this file to you under
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

import json
import os
import re
import shutil
from functools import lru_cache
from itertools import chain, groupby
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict

import black
import deepmerge
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


def blacken(filename: Any) -> None:
    """
    runs 'black' https://pypi.org/project/black/ on the given file
    :param filename: file to reformant
    """
    runner = CliRunner()
    result = runner.invoke(black.main, [str(filename)])
    assert result.exit_code == 0, result.output


@lru_cache()
def is_valid_url(url: str) -> bool:
    """
    makes a call to the url
    :param url: url to check
    :return: True if status code is between HTTP 200 inclusive and 400 exclusive; False otherwise
    """
    return 200 <= http.request("HEAD", url).status < 400


class Module:
    def __init__(self, namespace: str, is_plugin: bool) -> None:
        self.namespace: Any = namespace
        self._apis: Any = []
        self.is_plugin: bool = is_plugin
        self.parse_orig()

    def add(self, api: Any) -> None:
        """
        add an API to the list of modules
        :param api: an API object
        """
        self._apis.append(api)

    def parse_orig(self) -> None:
        """
        reads the written module and updates with important code specific to this client
        """
        self.orders = []
        if self.is_plugin:
            self.header = "from typing import Any\n\n"
        else:
            self.header = (
                "from typing import Any, Collection, Optional, Tuple, Union\n\n"
            )

        self.namespace_new = "".join(
            word.capitalize() for word in self.namespace.split("_")
        )
        self.header += "class " + self.namespace_new + "Client(NamespacedClient):"
        if os.path.exists(self.filepath):
            with open(self.filepath, encoding="utf-8") as file:
                content = file.read()
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
                            if "security.py" in str(self.filepath):
                                # TODO: FIXME, import code
                                header_lines.append(
                                    "    from ._patch import health_check, update_audit_config  # type: ignore"  # pylint: disable=line-too-long
                                )
                            break
                self.header = "\n".join(header_lines)
                self.orders = re.findall(
                    r"\n    (?:async )?def ([a-z_]+)\(", content, re.MULTILINE
                )

    def _position(self, api: Any) -> Any:
        try:
            return self.orders.index(api.name)
        except ValueError:
            return len(self.orders)

    def sort(self) -> None:
        """
        sorts the list of APIs by the Module._position key
        """
        self._apis.sort(key=self._position)

    def dump(self) -> None:
        """
        writes the module out to disk
        """
        self.sort()
        if not os.path.exists(self.filepath):
            # Imports added for new namespaces in appropriate files.
            if self.is_plugin:
                with open(
                    "opensearchpy/_async/client/plugins.py", "r+", encoding="utf-8"
                ) as file:
                    content = file.read()
                    file_content = content.replace(
                        "super(PluginsClient, self).__init__(client)",
                        f"super(PluginsClient, self).__init__(client)\n        self.{self.namespace} = {self.namespace_new}Client(client)",  # pylint: disable=line-too-long
                        1,
                    )
                    new_file_content = file_content.replace(
                        "from .client import Client",
                        f"from ..plugins.{self.namespace} import {self.namespace_new}Client\nfrom .client import Client",  # pylint: disable=line-too-long
                        1,
                    )
                    file.seek(0)
                    file.write(new_file_content)
                    file.truncate()

            else:
                with open(
                    "opensearchpy/_async/client/__init__.py", "r+", encoding="utf-8"
                ) as file:
                    content = file.read()
                    file_content = content.replace(
                        "# namespaced clients for compatibility with API names",
                        f"# namespaced clients for compatibility with API names\n        self.{self.namespace} = {self.namespace_new}Client(client)",  # pylint: disable=line-too-long
                        1,
                    )
                    new_file_content = file_content.replace(
                        "from .utils import",
                        f"from .{self.namespace} import {self.namespace_new}Client\nfrom .utils import",  # pylint: disable=line-too-long
                        1,
                    )
                    file.seek(0)
                    file.write(new_file_content)
                    file.truncate()
        # This code snippet adds headers to each generated module indicating
        # that the code is generated.The separator is the last line in the
        # "THIS CODE IS AUTOMATICALLY GENERATED" header.
        header_separator = "# -----------------------------------------------------------------------------------------+"  # pylint: disable=line-too-long
        license_header_end_1 = "# GitHub history for details."
        license_header_end_2 = "#  under the License."

        update_header = True
        license_position = 0

        # Identifying the insertion point for the "THIS CODE IS AUTOMATICALLY GENERATED" header.
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as file:
                content = file.read()
            if header_separator in content:
                update_header = False
                header_end_position = (
                    content.find(header_separator) + len(header_separator) + 2
                )
                header_position = content.rfind("\n", 0, header_end_position) + 1
            if license_header_end_1 in content:
                if license_header_end_2 in content:
                    position = (
                        content.find(license_header_end_2)
                        + len(license_header_end_2)
                        + 2
                    )
                else:
                    position = (
                        content.find(license_header_end_1)
                        + len(license_header_end_1)
                        + 2
                    )
                license_position = content.rfind("\n", 0, position) + 1

        current_script_folder = os.path.dirname(os.path.abspath(__file__))
        generated_file_header_path = os.path.join(
            current_script_folder, "generated_file_headers.txt"
        )
        with open(generated_file_header_path, "r", encoding="utf-8") as header_file:
            header_content = header_file.read()

        # Imports are temporarily removed from the header and are regenerated
        # later to ensure imports are updated after code generation.
        utils = ".utils"
        if self.is_plugin:
            utils = "..client.utils"

        self.header = "\n".join(
            line
            for line in self.header.split("\n")
            if "from " + utils + " import" not in line
        )

        with open(self.filepath, "w", encoding="utf-8") as file:
            if update_header is True:
                file.write(
                    self.header[:license_position]
                    + "\n"
                    + header_content
                    + "\n\n"
                    + "#replace_token#\n"
                    + self.header[license_position:]
                )
            else:
                file.write(
                    self.header[:header_position]
                    + "\n"
                    + "#replace_token#\n"
                    + self.header[header_position:]
                )
            for api in self._apis:
                file.write(api.to_python())

        # Generating imports for each module
        utils_imports = ""
        file_content = ""
        with open(self.filepath, "r", encoding="utf-8") as file:
            content = file.read()
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
                utils_imports = "from " + utils + " import"
                result = f"{utils_imports} {', '.join(present_keywords)}"
                utils_imports = result
            file_content = content.replace("#replace_token#", utils_imports)

        with open(self.filepath, "w", encoding="utf-8") as file:
            file.write(file_content)

    @property
    def filepath(self) -> Any:
        """
        :return: absolute path to the module
        """
        if self.is_plugin:
            return CODE_ROOT / f"opensearchpy/_async/plugins/{self.namespace}.py"
        else:
            return CODE_ROOT / f"opensearchpy/_async/client/{self.namespace}.py"


class API:
    def __init__(self, namespace: str, name: str, definition: Any) -> None:
        self.namespace = namespace
        self.name = name

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
    def all_parts(self) -> Dict[str, str]:
        """
        updates the url parts from the specification
        :return: dict of updated parts
        """
        parts = {}
        for url in self._def["url"]["paths"]:
            parts.update(url.get("parts", {}))

        for part in parts:
            if "required" not in parts[part]:
                parts[part]["required"] = all(
                    part in url.get("parts", {}) for url in self._def["url"]["paths"]
                )
            parts[part]["type"] = "Any"

            # This piece of logic corresponds to calling
            # client.tasks.get() w/o a task_id which was erroneously
            # allowed in the 7.1 client library. This functionality
            # is deprecated and will be removed in 8.x.
            if self.namespace == "tasks" and self.name == "get":
                parts["task_id"]["required"] = False

        for k, sub in SUBSTITUTIONS.items():
            if k in parts:
                parts[sub] = parts.pop(k)

        _, components = self.url_parts

        def ind(item: Any) -> Any:
            try:
                return components.index(item[0])
            except ValueError:
                return len(components)

        parts = dict(sorted(parts.items(), key=ind))
        return parts

    @property
    def params(self) -> Any:
        """
        :return: itertools.chain of required parts of the API
        """
        parts = self.all_parts
        params = self._def.get("params", {})
        return chain(
            ((p, parts[p]) for p in parts if parts[p]["required"]),  # type: ignore
            (("body", self.body),) if self.body else (),
            (
                (p, parts[p])
                for p in parts
                if not parts[p]["required"] and p not in params  # type: ignore
            ),
            sorted(params.items(), key=lambda x: (x[0] not in parts, x[0])),
        )

    @property
    def body(self) -> Any:
        """
        :return: body of the API spec
        """
        body_api_spec = self._def.get("body", {})
        if body_api_spec:
            body_api_spec.setdefault("required", False)
        return body_api_spec

    @property
    def query_params(self) -> Any:
        """
        :return: any query string parameters from the specification
        """
        return (
            key
            for key in sorted(self._def.get("params", {}).keys())
            if key not in self.all_parts
        )

    @property
    def all_func_params(self) -> Any:
        """
        Parameters that will be in the '@query_params' decorator list
        and parameters that will be in the function signature.
        """
        params = list(self._def.get("params", {}).keys())
        for url in self._def["url"]["paths"]:
            params.extend(url.get("parts", {}).keys())
        if self.body:
            params.append("body")
        return params

    @property
    def path(self) -> Any:
        """
        :return: the first lexically ordered path in url.paths
        """
        return max(
            (path for path in self._def["url"]["paths"]),
            key=lambda p: len(re.findall(r"\{([^}]+)\}", p["path"])),
        )

    @property
    def method(self) -> Any:
        """
        To adhere to the HTTP RFC we shouldn't send
        bodies in GET requests.
        :return: an updated HTTP method to use to communicate with the OpenSearch API
        """

        default_method = self.path["methods"][0]
        if self.name == "refresh" or self.name == "flush":
            return "POST"
        if self.body and default_method == "GET" and "POST" in self.path["methods"]:
            return "POST"
        if "POST" and "PUT" in self.path["methods"] and self.name != "bulk":
            return "PUT"
        return default_method

    @property
    def url_parts(self) -> Any:
        """
        :return tuple of boolean (if the path is dynamic), list of url parts
        """
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
    def required_parts(self) -> Any:
        """
        :return: list of parts of the url that are required plus the body
        """
        parts = self.all_parts
        required = [p for p in parts if parts[p]["required"]]  # type: ignore
        if self.body.get("required"):
            required.append("body")
        return required

    def to_python(self) -> Any:
        """
        :return: rendered Jinja template
        """
        try:
            template = jinja_env.get_template(f"overrides/{self.namespace}/{self.name}")
        except TemplateNotFound:
            template = jinja_env.get_template("base")

        return template.render(
            api=self,
            substitutions={v: k for k, v in SUBSTITUTIONS.items()},
            global_query_params=GLOBAL_QUERY_PARAMS,
        )


def read_modules() -> Any:
    """
    checks the opensearch-api spec at
    https://raw.githubusercontent.com/opensearch-project/opensearch-api-specification/main/OpenSearch.openapi.json
    and parses it into one or more API modules
    :return: a dict of API objects
    """
    modules = {}

    # Load the OpenAPI specification file
    response = requests.get(
        "https://raw.githubusercontent.com/opensearch-project/opensearch-api-"
        "specification/main/OpenSearch.openapi.json"
    )
    data = response.json()

    list_of_dicts = []

    for path in data["paths"]:
        for param in data["paths"][path]:  # pylint: disable=invalid-name
            if data["paths"][path][param]["x-operation-group"] == "nodes.hot_threads":
                if "deprecated" in data["paths"][path][param]:
                    continue
            data["paths"][path][param].update({"path": path, "method": param})
            list_of_dicts.append(data["paths"][path][param])

    # Update parameters  in each endpoint
    for param_dict in list_of_dicts:
        if "parameters" in param_dict:
            params = []
            parts = []

            # Iterate over the list of parameters and update them
            for param in param_dict["parameters"]:
                if "schema" in param and "$ref" in param["schema"]:
                    schema_path_ref = param["schema"]["$ref"].split("/")[-1]
                    param["schema"] = data["components"]["schemas"][schema_path_ref]
                    params.append(param)
                else:
                    params.append(param)

            # Iterate over the list of updated parameters to separate "parts" from "params"
            params_copy = params.copy()
            for param in params_copy:
                if param["in"] == "path":
                    parts.append(param)
                    params.remove(param)

            # Convert "params" and "parts" into the structure required for generator.
            params_new = {}
            parts_new = {}

            for m in params:  # pylint: disable=invalid-name
                a = dict(  # pylint: disable=invalid-name
                    type=m["schema"]["type"], description=m["description"]
                )  # pylint: disable=invalid-name

                if "default" in m["schema"]:
                    a.update({"default": m["schema"]["default"]})

                if "enum" in m["schema"]:
                    a.update({"type": "enum"})
                    a.update({"options": m["schema"]["enum"]})

                if "deprecated" in m["schema"]:
                    a.update({"deprecated": m["schema"]["deprecated"]})
                    a.update(
                        {"deprecation_message": m["schema"]["x-deprecation-message"]}
                    )
                params_new.update({m["name"]: a})

            # Removing the deprecated "type"
            if (
                param_dict["x-operation-group"] != "nodes.hot_threads"
                and "type" in params_new
            ):
                params_new.pop("type")

            if (
                param_dict["x-operation-group"] == "cluster.health"
                and "ensure_node_commissioned" in params_new
            ):
                params_new.pop("ensure_node_commissioned")

            if bool(params_new):
                param_dict.update({"params": params_new})

            param_dict.pop("parameters")

            for n in parts:  # pylint: disable=invalid-name
                b = dict(type=n["schema"]["type"])  # pylint: disable=invalid-name

                if "description" in n:
                    b.update({"description": n["description"]})

                if "x-enum-options" in n["schema"]:
                    b.update({"options": n["schema"]["x-enum-options"]})

                deprecated_new = {}
                if "deprecated" in n:
                    b.update({"deprecated": n["deprecated"]})

                    if "x-deprecation-version" in n:
                        deprecated_new.update({"version": n["x-deprecation-version"]})

                    if "x-deprecation-description" in n:
                        deprecated_new.update(
                            {"description": n["x-deprecation-description"]}
                        )

                parts_new.update({n["name"]: b})

            if bool(parts_new):
                param_dict.update({"parts": parts_new})

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
        all_paths_have_deprecation = True

        for key2, value2 in groupby(value, key=itemgetter("path")):
            # Extract the HTTP methods from the data in the current subgroup
            methods = []
            parts_final = {}
            for z in value2:  # pylint: disable=invalid-name
                methods.append(z["method"].upper())

                # Update 'api' dictionary
                if "documentation" not in api:
                    documentation = {"description": z["description"]}
                    api.update({"documentation": documentation})

                if "x-deprecation-message" in z:
                    x_deprecation_message = z["x-deprecation-message"]
                else:
                    all_paths_have_deprecation = False

                if "params" not in api and "params" in z:
                    api.update({"params": z["params"]})

                if "body" not in api and "requestBody" in z:
                    body = {"required": False}
                    if "required" in z["requestBody"]:
                        body.update({"required": z["requestBody"]["required"]})
                    q = z["requestBody"]["content"][  # pylint: disable=invalid-name
                        "application/json"
                    ]["schema"]["$ref"].split("/")[-1]
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
                        "stability": "stable",  # type: ignore
                        "visibility": "public",  # type: ignore
                        "headers": {
                            "accept": ["application/json"],
                            "content_type": ["application/json"],
                        },
                    }
                )
            else:
                api.update(
                    {
                        "stability": "stable",  # type: ignore
                        "visibility": "public",  # type: ignore
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
        if all_paths_have_deprecation and x_deprecation_message is not None:
            api.update({"deprecation_message": x_deprecation_message})

        api = apply_patch(namespace, name, api)

        is_plugin = False
        if "_plugins" in api["url"]["paths"][0]["path"] and namespace != "security":
            is_plugin = True

        if namespace not in modules:
            modules[namespace] = Module(namespace, is_plugin)

        modules[namespace].add(API(namespace, name, api))

    return modules


def apply_patch(namespace: str, name: str, api: Any) -> Any:
    """
    applies patches as specified in {name}.json
    :param namespace: directory containing overrides
    :param name: file to be prepended to ".json" containing override instructions
    :param api: specific api to override
    :return: modified api
    """
    override_file_path = (
        CODE_ROOT / "utils/templates/overrides" / namespace / f"{name}.json"
    )
    if os.path.exists(override_file_path):
        with open(override_file_path, encoding="utf-8") as file:
            override_json = json.load(file)
            api = deepmerge.always_merger.merge(api, override_json)
    return api


def dump_modules(modules: Any) -> None:
    """
        writes out modules to disk
    :param modules: a list of python modules
    """
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
        unasync.Rule(
            fromdir="/opensearchpy/_async/plugins/",
            todir="/opensearchpy/plugins/",
            additional_replacements=additional_replacements,
        ),
    ]

    filepaths = []
    for root, _, filenames in os.walk(CODE_ROOT / "opensearchpy/_async"):
        for filename in filenames:
            if filename.rpartition(".")[-1] in ("py",) and filename not in (
                "utils.py",
                "index_management.py",
                "alerting.py",
            ):
                filepaths.append(os.path.join(root, filename))

    unasync.unasync_files(filepaths, rules)
    blacken(CODE_ROOT / "opensearchpy")


if __name__ == "__main__":
    # Store directories for comparison pre-generation vs post-generation.
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    before_paths = [
        os.path.join(root_dir, f"before_generate/{folder}")
        for folder in ["client", "async_client"]
    ]

    for path in before_paths:
        if os.path.exists(path):
            shutil.rmtree(path)

    shutil.copytree(os.path.join(root_dir, "opensearchpy/client"), before_paths[0])
    shutil.copytree(
        os.path.join(root_dir, "opensearchpy/_async/client"), before_paths[1]
    )

    dump_modules(read_modules())
