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
import inspect
import warnings
from typing import Any

import pytest
from _pytest.mark.structures import MarkDecorator

from opensearchpy import OpenSearchWarning
from opensearchpy.helpers.test import _get_version

from ...test_server.test_rest_api_spec import (
    IMPLEMENTED_FEATURES,
    PARAMS_RENAMES,
    RUN_ASYNC_REST_API_TESTS,
    YAML_TEST_SPECS,
    YamlRunner,
)

pytestmark: MarkDecorator = pytest.mark.asyncio

OPENSEARCH_VERSION = None


async def await_if_coro(x: Any) -> Any:
    """
    awaits if x is a coroutine
    :return: x
    """
    if inspect.iscoroutine(x):
        return await x
    return x


class AsyncYamlRunner(YamlRunner):
    async def setup(self) -> None:
        # Pull skips from individual tests to not do unnecessary setup.
        skip_code = []
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
            await self.run_code(skip_code)
        if self._setup_code:
            await self.run_code(self._setup_code)

    async def teardown(self) -> Any:
        if self._teardown_code:
            self.section("teardown")
            await self.run_code(self._teardown_code)

    async def opensearch_version(self) -> Any:
        global OPENSEARCH_VERSION
        if OPENSEARCH_VERSION is None:
            version_string = (await self.client.info())["version"]["number"]
            if "." not in version_string:
                return ()
            version = version_string.strip().split(".")
            OPENSEARCH_VERSION = tuple(int(v) if v.isdigit() else 999 for v in version)
        return OPENSEARCH_VERSION

    def section(self, name: str) -> None:
        print(("=" * 10) + " " + name + " " + ("=" * 10))

    async def run(self) -> Any:
        try:
            await self.setup()
            self.section("test")
            await self.run_code(self._run_code)
        finally:
            try:
                await self.teardown()
            except Exception:
                pass

    async def run_code(self, test: Any) -> Any:
        """Execute an instruction based on its type."""
        for action in test:
            assert len(action) == 1
            action_type, action = list(action.items())[0]
            print(action_type, action)

            if hasattr(self, "run_" + action_type):
                await await_if_coro(getattr(self, "run_" + action_type)(action))
            else:
                raise RuntimeError("Invalid action type %r" % (action_type,))

    async def run_do(self, action: Any) -> Any:
        api = self.client
        headers = action.pop("headers", None)
        catch = action.pop("catch", None)
        warn = action.pop("warnings", ())
        allowed_warnings = action.pop("allowed_warnings", ())
        assert len(action) == 1

        # Remove the x_pack_rest_user authentication
        # if its given via headers. We're already authenticated
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
                self.last_response = await api(**args)
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

    async def run_skip(self, skip: Any) -> Any:
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
            if min_version <= (await self.opensearch_version()) <= max_version:
                pytest.skip(reason)

    async def _feature_enabled(self, name: str) -> Any:
        return False


@pytest.fixture(scope="function")  # type: ignore
def async_runner(async_client: Any) -> AsyncYamlRunner:
    return AsyncYamlRunner(async_client)


if RUN_ASYNC_REST_API_TESTS:

    @pytest.mark.parametrize("test_spec", YAML_TEST_SPECS)  # type: ignore
    async def test_rest_api_spec(test_spec: Any, async_runner: Any) -> None:
        if test_spec.get("skip", False):
            pytest.skip("Manually skipped in 'SKIP_TESTS'")
        async_runner.use_spec(test_spec)
        await async_runner.run()
