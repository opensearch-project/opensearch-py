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


"""
Dynamically generated set of TestCases based on set of yaml files describing
some integration tests. These files are shared among all official OpenSearch
clients.
"""
import io
import os
import re
import warnings
import zipfile
from typing import Any

import pytest
import urllib3
import yaml

from opensearchpy import OpenSearchWarning, TransportError
from opensearchpy.client.utils import _base64_auth_header
from opensearchpy.compat import string_types
from opensearchpy.helpers.test import _get_version

from . import get_client

# some params had to be changed in python, keep track of them so we can rename
# those in the tests accordingly
PARAMS_RENAMES = {"type": "doc_type", "from": "from_"}

# mapping from catch values to http status codes
CATCH_CODES = {"missing": 404, "conflict": 409, "unauthorized": 401}

# test features we have implemented
IMPLEMENTED_FEATURES = {
    "gtelte",
    "stash_in_path",
    "headers",
    "catch_unauthorized",
    "default_shards",
    "warnings",
    "allowed_warnings",
    "contains",
    "arbitrary_key",
    "transform_and_set",
}

# broken YAML tests on some releases
SKIP_TESTS = {
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/cat/nodes/10_basic[1]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/cat/nodeattrs/10_basic[1]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/cluster/put_settings/10_basic[2]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/cluster/put_settings/10_basic[3]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/cat/indices/10_basic[2]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/cluster/health/10_basic[6]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/cluster/health/20_request_timeout",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/search/aggregation/20_terms[4]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/tasks/list/10_basic[0]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/index/90_unsigned_long[1]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/indices/stats/50_noop_update[0]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/search/340_doc_values_field[0]",
    "OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/search/340_doc_values_field[1]",
}


OPENSEARCH_VERSION = None
RUN_ASYNC_REST_API_TESTS = (
    os.environ.get("PYTHON_CONNECTION_CLASS") == "RequestsHttpConnection"
)

FALSEY_VALUES = ("", None, False, 0, 0.0)


class YamlRunner:
    def __init__(self, client: Any) -> None:
        self.client = client
        self.last_response: Any = None

        self._run_code: Any = None
        self._setup_code: Any = None
        self._teardown_code: Any = None
        self._state: Any = {}

    def use_spec(self, test_spec: Any) -> None:
        self._setup_code = test_spec.pop("setup", None)
        self._run_code = test_spec.pop("run", None)
        self._teardown_code = test_spec.pop("teardown", None)

    def setup(self) -> Any:
        """Pull skips from individual tests to not do unnecessary setup."""
        skip_code: Any = []
        for action in self._run_code:
            assert len(action) == 1
            action_type, _ = list(action.items())[0]
            if action_type == "skip":
                skip_code.append(action)
            else:
                break

        if self._setup_code or skip_code:
            self.section("setup")
        if skip_code:
            self.run_code(skip_code)
        if self._setup_code:
            self.run_code(self._setup_code)

    def teardown(self) -> Any:
        if self._teardown_code:
            self.section("teardown")
            self.run_code(self._teardown_code)

    def opensearch_version(self) -> Any:
        global OPENSEARCH_VERSION
        if OPENSEARCH_VERSION is None:
            version_string = (self.client.info())["version"]["number"]
            if "." not in version_string:
                return ()
            version = version_string.strip().split(".")
            OPENSEARCH_VERSION = tuple(int(v) if v.isdigit() else 99 for v in version)
        return OPENSEARCH_VERSION

    def section(self, name: str) -> None:
        print(("=" * 10) + " " + name + " " + ("=" * 10))

    def run(self) -> Any:
        try:
            self.setup()
            self.section("test")
            self.run_code(self._run_code)
        finally:
            try:
                self.teardown()
            except Exception:
                pass

    def run_code(self, test: Any) -> Any:
        """Execute an instruction based on its type."""
        for action in test:
            assert len(action) == 1
            action_type, action = list(action.items())[0]
            print(action_type, action)

            if hasattr(self, "run_" + action_type):
                getattr(self, "run_" + action_type)(action)
            else:
                raise RuntimeError("Invalid action type %r" % (action_type,))

    def run_do(self, action: Any) -> Any:
        api = self.client
        headers = action.pop("headers", None)
        catch = action.pop("catch", None)
        warn = action.pop("warnings", ())
        allowed_warnings = action.pop("allowed_warnings", ())
        assert len(action) == 1

        # Remove the x_pack_rest_user authentication
        # if it's given via headers. We're already authenticated
        # via the 'elastic' user.
        if (
            headers
            and headers.get("Authorization", None)
            == "Basic eF9wYWNrX3Jlc3RfdXNlcjp4LXBhY2stdGVzdC1wYXNzd29yZA=="
        ):
            headers.pop("Authorization")

        method, args = list(action.items())[0]
        args["headers"] = headers

        # locate api endpoint
        for m in method.split("."):
            assert hasattr(api, m)
            api = getattr(api, m)

        # some parameters had to be renamed to not clash with python builtins,
        # compensate
        for k in PARAMS_RENAMES:
            if k in args:
                args[PARAMS_RENAMES[k]] = args.pop(k)

        # resolve vars
        for k in args:
            args[k] = self._resolve(args[k])

        warnings.simplefilter("always", category=OpenSearchWarning)
        with warnings.catch_warnings(record=True) as caught_warnings:
            try:
                self.last_response = api(**args)
            except Exception as e:
                if not catch:
                    raise
                self.run_catch(catch, e)
            else:
                if catch:
                    raise AssertionError(
                        "Failed to catch %r in %r." % (catch, self.last_response)
                    )

        # Filter out warnings raised by other components.
        caught_warnings = [
            str(w.message)  # type: ignore
            for w in caught_warnings
            if w.category == OpenSearchWarning
            and str(w.message) not in allowed_warnings
        ]

        # Sorting removes the issue with order raised. We only care about
        # if all warnings are raised in the single API call.
        if warn and sorted(warn) != sorted(caught_warnings):  # type: ignore
            raise AssertionError(
                "Expected warnings not equal to actual warnings: expected=%r actual=%r"
                % (warn, caught_warnings)
            )

    def run_catch(self, catch: Any, exception: Any) -> None:
        if catch == "param":
            assert isinstance(exception, TypeError)
            return

        assert isinstance(exception, TransportError)
        if catch in CATCH_CODES:
            assert CATCH_CODES[catch] == exception.status_code
        elif catch[0] == "/" and catch[-1] == "/":
            assert (
                re.search(catch[1:-1], exception.error + " " + repr(exception.info)),
                "%s not in %r" % (catch, exception.info),
            ) is not None
        self.last_response = exception.info

    def run_skip(self, skip: Any) -> Any:
        global IMPLEMENTED_FEATURES

        if "features" in skip:
            features = skip["features"]
            if not isinstance(features, (tuple, list)):
                features = [features]
            for feature in features:
                if feature in IMPLEMENTED_FEATURES:
                    continue
                pytest.skip("feature '%s' is not supported" % feature)

        if "version" in skip:
            version, reason = skip["version"], skip["reason"]
            if version == "all":
                pytest.skip(reason)
            min_version, max_version = version.split("-")
            min_version = _get_version(min_version) or (0,)
            max_version = _get_version(max_version) or (999,)
            if min_version <= (self.opensearch_version()) <= max_version:
                pytest.skip(reason)

    def run_gt(self, action: Any) -> None:
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) > value

    def run_gte(self, action: Any) -> None:
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) >= value

    def run_lt(self, action: Any) -> None:
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) < value

    def run_lte(self, action: Any) -> None:
        for key, value in action.items():
            value = self._resolve(value)
            assert self._lookup(key) <= value

    def run_set(self, action: Any) -> None:
        for key, value in action.items():
            value = self._resolve(value)
            self._state[value] = self._lookup(key)

    def run_is_false(self, action: Any) -> None:
        try:
            value = self._lookup(action)
        except AssertionError:
            pass
        else:
            assert value in FALSEY_VALUES

    def run_is_true(self, action: Any) -> None:
        value = self._lookup(action)
        assert value not in FALSEY_VALUES

    def run_length(self, action: Any) -> None:
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)
            assert expected == len(value)

    def run_match(self, action: Any) -> None:
        for path, expected in action.items():
            value = self._lookup(path)
            expected = self._resolve(expected)

            if (
                isinstance(expected, str)
                and expected.strip().startswith("/")
                and expected.strip().endswith("/")
            ):
                expected = re.compile(expected.strip()[1:-1], re.VERBOSE | re.MULTILINE)
                assert expected.search(value), "%r does not match %r" % (
                    value,
                    expected,
                )
            else:
                self._assert_match_equals(value, expected)

    def run_contains(self, action: Any) -> None:
        for path, expected in action.items():
            value = self._lookup(path)  # list[dict[str,str]] is returned
            expected = self._resolve(expected)  # dict[str, str]

            if expected not in value:
                raise AssertionError("%s is not contained by %s" % (expected, value))

    def run_transform_and_set(self, action: Any) -> None:
        for key, value in action.items():
            # Convert #base64EncodeCredentials(id,api_key) to ["id", "api_key"]
            if "#base64EncodeCredentials" in value:
                value = value.replace("#base64EncodeCredentials", "")
                value = value.replace("(", "").replace(")", "").split(",")
                self._state[key] = _base64_auth_header(
                    (self._lookup(value[0]), self._lookup(value[1]))
                )

    def _resolve(self, value: Any) -> Any:
        # resolve variables
        if isinstance(value, string_types) and "$" in value:
            for k, v in self._state.items():
                for key_replace in ("${" + k + "}", "$" + k):
                    if value == key_replace:
                        value = v
                        break
                    # We only do the in-string replacement if using ${...}
                    elif (
                        key_replace.startswith("${")
                        and isinstance(value, string_types)
                        and key_replace in value
                    ):
                        value = value.replace(key_replace, v)
                        break

        if isinstance(value, dict):
            value = dict((k, self._resolve(v)) for (k, v) in value.items())
        elif isinstance(value, list):
            value = list(map(self._resolve, value))
        return value

    def _lookup(self, path: str) -> Any:
        # fetch the possibly nested value from last_response
        value: Any = self.last_response
        if path == "$body":
            return value
        path = path.replace(r"\.", "\1")
        step: Any
        for step in path.split("."):
            if not step:
                continue
            step = step.replace("\1", ".")
            step = self._resolve(step)

            if (
                isinstance(step, string_types)
                and step.isdigit()
                and isinstance(value, list)
            ):
                step = int(step)
                assert isinstance(value, list)
                assert len(value) > step
            elif step == "_arbitrary_key_":
                return list(value.keys())[0]
            else:
                assert step in value
            value = value[step]
        return value

    def _feature_enabled(self, name: str) -> Any:
        return False

    def _assert_match_equals(self, a: Any, b: Any) -> None:
        # Handle for large floating points with 'E'
        if isinstance(b, string_types) and isinstance(a, float) and "e" in repr(a):
            a = repr(a).replace("e+", "E")

        assert a == b, "%r does not match %r" % (a, b)


@pytest.fixture(scope="function")  # type: ignore
def sync_runner(sync_client: Any) -> Any:
    return YamlRunner(sync_client)


YAML_TEST_SPECS = []

client = get_client()


def load_rest_api_tests() -> None:
    """Try loading the REST API test specs from OpenSearch core."""
    try:
        # Construct the HTTP and OpenSearch client
        http = urllib3.PoolManager(retries=10)

        package_url = (
            "https://github.com/opensearch-project/OpenSearch/archive/main.zip"
        )

        # Download the zip and start reading YAML from the files in memory
        package_zip = zipfile.ZipFile(io.BytesIO(http.request("GET", package_url).data))
        for yaml_file in package_zip.namelist():
            if not re.match(
                r"^OpenSearch-main/rest-api-spec/src/main/resources/rest-api-spec/test/.*\.ya?ml$",
                yaml_file,
            ):
                continue
            yaml_tests = list(yaml.safe_load_all(package_zip.read(yaml_file)))

            # Each file may have a "test" named 'setup' or 'teardown',
            # these sets of steps should be run at the beginning and end
            # of every other test within the file so we do one pass to capture those.
            setup_steps = teardown_steps = None
            test_numbers_and_steps = []
            test_number = 0

            for yaml_test in yaml_tests:
                test_name, test_step = yaml_test.popitem()
                if test_name == "setup":
                    setup_steps = test_step
                elif test_name == "teardown":
                    teardown_steps = test_step
                else:
                    test_numbers_and_steps.append((test_number, test_step))
                    test_number += 1

            # Now we combine setup, teardown, and test_steps into
            # a set of pytest.param() instances
            for test_number, test_step in test_numbers_and_steps:
                # Build the id from the name of the YAML file and
                # the number within that file. Most important step
                # is to remove most of the file path prefixes and
                # the .yml suffix.
                pytest_test_name = yaml_file.rpartition(".")[0].replace(".", "/")
                for prefix in ("rest-api-spec/", "test/", "oss/"):
                    if pytest_test_name.startswith(prefix):
                        pytest_test_name = pytest_test_name[len(prefix) :]
                pytest_param_id = "%s[%d]" % (pytest_test_name, test_number)

                pytest_param = {
                    "setup": setup_steps,
                    "run": test_step,
                    "teardown": teardown_steps,
                }
                # Skip either 'test_name' or 'test_name[x]'
                if pytest_test_name in SKIP_TESTS or pytest_param_id in SKIP_TESTS:
                    pytest_param["skip"] = True

                YAML_TEST_SPECS.append(pytest.param(pytest_param, id=pytest_param_id))

    except Exception as e:
        warnings.warn("Could not load REST API tests: %s" % (str(e),))


load_rest_api_tests()

if not RUN_ASYNC_REST_API_TESTS:

    @pytest.mark.parametrize("test_spec", YAML_TEST_SPECS)  # type: ignore
    def test_rest_api_spec(test_spec: Any, sync_runner: Any) -> None:
        if test_spec.get("skip", False):
            pytest.skip("Manually skipped in 'SKIP_TESTS'")
        sync_runner.use_spec(test_spec)
        sync_runner.run()
