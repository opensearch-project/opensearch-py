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
import yaml
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

IGNORED_PARAM_REFS = [
    # https://github.com/opensearch-project/opensearch-api-specification/pull/416
    "#/components/parameters/nodes.info::path.node_id_or_metric",
]

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


@lru_cache
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
        self.header = "from typing import Any\n\n"
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
                    content = content.replace(
                        "super().__init__(client)\n",
                        f"super().__init__(client)\n\n        self.{self.namespace} = {self.namespace_new}Client(client)",  # pylint: disable=line-too-long
                        1,
                    )
                    content = content.replace(
                        "from .client import Client",
                        f"from ..plugins.{self.namespace} import {self.namespace_new}Client\nfrom .client import Client",  # pylint: disable=line-too-long
                        1,
                    )
                    content = content.replace(
                        "class PluginsClient(NamespacedClient):\n",
                        f"class PluginsClient(NamespacedClient): \n    {self.namespace}: Any\n",  # pylint: disable=line-too-long
                        1,
                    )
                    content = content.replace(
                        "plugins = [", f'plugins = [\n            "{self.namespace}",\n'
                    )
                    file.seek(0)
                    file.write(content)
                    file.truncate()

            else:
                with open(
                    "opensearchpy/_async/client/__init__.py", "r+", encoding="utf-8"
                ) as file:
                    content = file.read()
                    file_content = content.replace(
                        "# namespaced clients for compatibility with API names",
                        f"# namespaced clients for compatibility with API names\n        self.{self.namespace} = {self.namespace_new}Client(self)",  # pylint: disable=line-too-long
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
            with open(self.filepath, encoding="utf-8") as file:
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
        with open(generated_file_header_path, encoding="utf-8") as header_file:
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

        module_content = ""
        if update_header is True:
            module_content += (
                self.header[:license_position]
                + "\n"
                + header_content
                + "\n\n"
                + "#replace_token#\n"
                + self.header[license_position:]
            )
        else:
            module_content += (
                self.header[:header_position]
                + "\n"
                + "#replace_token#\n"
                + self.header[header_position:]
            )
        for api in self._apis:
            module_content += api.to_python()

        # Generating imports for each module
        utils_imports = ""

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
        present_keywords = [
            keyword for keyword in keywords if keyword in module_content
        ]

        if present_keywords:
            utils_imports = "from " + utils + " import"
            result = f"{utils_imports} {', '.join(present_keywords)}"
            utils_imports = result
        module_content = module_content.replace("#replace_token#", utils_imports)

        with open(self.filepath, "w", encoding="utf-8") as file:
            file.write(module_content)

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

            # Workaround to prevent lint error: invalid escape sequence '\`'
            if (
                self.namespace == "indices"
                and self.name == "create_data_stream"
                and part == "name"
            ):
                # Replace the string in the description
                parts["name"]["description"] = parts["name"]["description"].replace(
                    r"`\`, ", ""
                )
                if "backslash" not in parts["name"]["description"]:
                    parts["name"]["description"] = parts["name"]["description"].replace(
                        "`:`", "`:`, backslash"
                    )

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
    https://github.com/opensearch-project/opensearch-api-specification/releases/download/main-latest/opensearch-openapi.yaml
    and parses it into one or more API modules
    :return: a dict of API objects
    """
    modules = {}

    # Load the OpenAPI specification file
    response = requests.get(
        "https://github.com/opensearch-project/opensearch-api-specification/releases/download/main-latest/opensearch-openapi.yaml"
    )
    data = yaml.safe_load(response.text)

    list_of_dicts = []

    for path in data["paths"]:
        for method in data["paths"][path]:
            # Workaround for excluding deprecated path of 'nodes.hot_threads'
            if data["paths"][path][method]["x-operation-group"] == "nodes.hot_threads":
                if "deprecated" in data["paths"][path][method]:
                    continue

            data["paths"][path][method].update({"path": path, "method": method})
            list_of_dicts.append(data["paths"][path][method])

    # 'list_of_dicts' contains dictionaries, each representing a possible API endpoint

    # Update parameters  in each endpoint
    for endpoint in list_of_dicts:
        if "parameters" in endpoint:
            params = []
            parts = []

            # Iterate over the list of parameters and update them
            for param_ref in endpoint["parameters"]:

                if param_ref["$ref"] in IGNORED_PARAM_REFS:
                    continue

                param_ref = param_ref["$ref"].split("/")[-1]
                param = data["components"]["parameters"][param_ref]

                if "schema" in param and "$ref" in param["schema"]:
                    schema_path_ref = param["schema"]["$ref"].split("/")[-1]
                    param["schema"] = data["components"]["schemas"][schema_path_ref]
                    if "oneOf" in param["schema"]:
                        for element in param["schema"]["oneOf"]:
                            if "$ref" in element:
                                common_schema_path_ref = element["$ref"].split("/")[-1]
                                param["schema"] = data["components"]["schemas"][
                                    common_schema_path_ref
                                ]

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

            for param in params:
                param_dict: Dict[str, Any] = {}
                if "description" in param:
                    param_dict.update(
                        description=param["description"].replace("\n", " ")
                    )

                if "type" in param["schema"]:
                    param_dict.update({"type": param["schema"]["type"]})

                if "default" in param["schema"]:
                    param_dict.update({"default": param["schema"]["default"]})

                if "enum" in param["schema"]:
                    param_dict.update({"type": "enum"})
                    param_dict.update({"options": param["schema"]["enum"]})

                if "deprecated" in param:
                    param_dict.update({"deprecated": param["deprecated"]})

                if "x-deprecation-message" in param:
                    param_dict.update(
                        {"deprecation_message": param["x-deprecation-message"]}
                    )
                params_new.update({param["name"]: param_dict})

            # Removing the deprecated "type"
            if (
                endpoint["x-operation-group"] != "nodes.hot_threads"
                and "type" in params_new
            ):
                params_new.pop("type")

            if (
                endpoint["x-operation-group"] == "cluster.health"
                and "ensure_node_commissioned" in params_new
            ):
                params_new.pop("ensure_node_commissioned")

            if bool(params_new):
                endpoint.update({"params": params_new})

            for part in parts:
                parts_dict: Dict[str, Any] = {}
                if "type" in part["schema"]:
                    parts_dict.update(type=part["schema"]["type"])

                if "description" in part:
                    parts_dict.update(
                        {"description": part["description"].replace("\n", " ")}
                    )

                if "x-enum-options" in part["schema"]:
                    parts_dict.update({"options": part["schema"]["x-enum-options"]})

                if "deprecated" in part:
                    parts_dict.update({"deprecated": part["deprecated"]})

                parts_new.update({part["name"]: parts_dict})

            if bool(parts_new):
                endpoint.update({"parts": parts_new})

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

        # FIXME: we have a hard-coded index_management that needs to be deprecated in favor of the auto-generated one
        if namespace == "ism":
            continue

        # Group the data in the current group by the "path" key
        paths = []
        all_paths_have_deprecation = True

        for path, path_dicts in groupby(value, key=itemgetter("path")):
            # Extract the HTTP methods from the data in the current subgroup
            methods = []
            parts_final = {}
            for method_dict in path_dicts:
                methods.append(method_dict["method"].upper())

                # Update 'api' dictionary
                if "documentation" not in api:
                    documentation = {"description": method_dict["description"]}
                    api.update({"documentation": documentation})

                if "x-deprecation-message" in method_dict:
                    x_deprecation_message = method_dict["x-deprecation-message"]
                else:
                    all_paths_have_deprecation = False

                if "params" not in api and "params" in method_dict:
                    api.update({"params": method_dict["params"]})

                if (
                    "body" not in api
                    and "requestBody" in method_dict
                    and "$ref" in method_dict["requestBody"]
                ):
                    requestbody_ref = method_dict["requestBody"]["$ref"].split("/")[-1]
                    body = {"required": False}
                    if (
                        "required"
                        in data["components"]["requestBodies"][requestbody_ref]
                    ):
                        body.update(
                            {
                                "required": data["components"]["requestBodies"][
                                    requestbody_ref
                                ]["required"]
                            }
                        )

                    if (
                        "application/x-ndjson"
                        in data["components"]["requestBodies"][requestbody_ref][
                            "content"
                        ]
                    ):
                        requestbody_schema = data["components"]["requestBodies"][
                            requestbody_ref
                        ]["content"]["application/x-ndjson"]["schema"]
                        body.update({"serialize": True})
                    else:
                        requestbody_schema = data["components"]["requestBodies"][
                            requestbody_ref
                        ]["content"]["application/json"]["schema"]

                    if "description" in requestbody_schema:
                        body.update({"description": requestbody_schema["description"]})

                    api.update({"body": body})

                if "parts" in method_dict:
                    parts_final.update(method_dict["parts"])

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

            if bool(parts_final):
                paths.append({"path": path, "methods": methods, "parts": parts_final})
            else:
                paths.append({"path": path, "methods": methods})

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
    dump_modules(read_modules())
