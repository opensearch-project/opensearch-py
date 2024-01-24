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


from __future__ import print_function

import subprocess
import sys
from os import environ
from os.path import abspath, dirname, exists, join, pardir
from subprocess import CalledProcessError
from typing import Any


def fetch_opensearch_repo() -> None:
    """
    runs a git fetch origin on configured opensearch core repo
    :return: None if environmental variables TEST_OPENSEARCH_YAML_DIR
    is set or TEST_OPENSEARCH_NOFETCH is set to False; else returns nothing
    """
    # user is manually setting YAML dir, don't tamper with it
    if "TEST_OPENSEARCH_YAML_DIR" in environ:
        return

    repo_path = environ.get(
        "TEST_OPENSEARCH_REPO",
        abspath(join(dirname(__file__), pardir, pardir, "opensearch")),
    )

    # set YAML test dir
    environ["TEST_OPENSEARCH_YAML_DIR"] = join(
        repo_path, "rest-api-spec", "src", "main", "resources", "rest-api-spec", "test"
    )

    # fetching of yaml tests disabled, we'll run with what's there
    if environ.get("TEST_OPENSEARCH_NOFETCH", False):
        return

    from test_opensearchpy.test_cases import SkipTest
    from test_opensearchpy.test_server import get_client

    # find out the sha of the running client
    try:
        client = get_client()
        sha = client.info()["version"]["build_hash"]
    except (SkipTest, KeyError):
        print("No running opensearch >1.X server...")
        return

    # no test directory
    if not exists(repo_path):
        subprocess.check_call("mkdir %s" % repo_path, shell=True)

    # make a new blank repository in the test directory
    subprocess.check_call("cd %s && git init" % repo_path, shell=True)

    try:
        # add a remote
        subprocess.check_call(
            "cd %s && git remote add origin https://github.com/opensearch-project/opensearch.git"
            % repo_path,
            shell=True,
        )
    except CalledProcessError as e:
        # if the run is interrupted from a previous run, it doesn't clean up, and the git add origin command
        # errors out; this allows the test to continue
        remote_origin_already_exists = 3
        if e.returncode == remote_origin_already_exists:
            print(
                "Consider setting TEST_OPENSEARCH_NOFETCH=true if you want to reuse the existing local OpenSearch repo"
            )
        else:
            print(e)
        sys.exit(1)

    # fetch the sha commit, version from info()
    print("Fetching opensearch repo...")
    subprocess.check_call("cd %s && git fetch origin %s" % (repo_path, sha), shell=True)


def run_all(argv: Any = None) -> None:
    """
    run all the tests given arguments and environment variables
    - sets defaults if argv is None, running "pytest --cov=opensearchpy
    --junitxml=<path to opensearch-py-junit.xml>
    --log-level=DEBUG --cache-clear -vv --cov-report=<path to output code coverage"
    * GITHUB_ACTION: fetches yaml tests if this is not in environment variables
    * TEST_PATTERN: specify a test to run
    * TEST_TYPE: "server" runs on TLS connection; None is unencrypted
    * OPENSEARCH_VERSION: "SNAPSHOT" does not do anything with plugins
    :param argv: if this is None, then the default arguments
    """
    sys.exitfunc = lambda: sys.stderr.write("Shutting down....\n")  # type: ignore
    # fetch yaml tests anywhere that's not GitHub Actions
    if "GITHUB_ACTION" not in environ:
        fetch_opensearch_repo()

    # always insert coverage when running tests
    if argv is None:
        junit_xml = join(
            abspath(dirname(dirname(__file__))), "junit", "opensearch-py-junit.xml"
        )
        codecov_xml = join(
            abspath(dirname(dirname(__file__))), "junit", "opensearch-py-codecov.xml"
        )

        argv = [
            "pytest",
            "--cov=opensearchpy",
            "--junitxml=%s" % junit_xml,
            "--log-level=DEBUG",
            "--cache-clear",
            "-vv",
            "--cov-report=xml:%s" % codecov_xml,
        ]
        if (
            "OPENSEARCHPY_GEN_HTML_COV" in environ
            and environ.get("OPENSEARCHPY_GEN_HTML_COV") == "true"
        ):
            codecov_html = join(abspath(dirname(dirname(__file__))), "junit", "html")
            argv.append("--cov-report=html:%s" % codecov_html)

        secured = False
        if environ.get("OPENSEARCH_URL", "").startswith("https://"):
            secured = True

        # check TEST_PATTERN env var for specific test to run
        test_pattern = environ.get("TEST_PATTERN")
        if test_pattern:
            argv.append("-k %s" % test_pattern)
        else:
            ignores = [
                "test_opensearchpy/test_server/",
                "test_opensearchpy/test_server_secured/",
                "test_opensearchpy/test_async/test_server/",
                "test_opensearchpy/test_async/test_server_secured/",
            ]

            # Jenkins/Github actions, only run server tests
            if environ.get("TEST_TYPE") == "server":
                test_dir = abspath(dirname(__file__))
                if secured:
                    argv.append(join(test_dir, "test_server_secured"))
                    argv.append(join(test_dir, "test_async/test_server_secured"))
                    ignores.extend(
                        [
                            "test_opensearchpy/test_server/",
                            "test_opensearchpy/test_async/test_server/",
                        ]
                    )
                else:
                    argv.append(join(test_dir, "test_server"))
                    argv.append(join(test_dir, "test_async/test_server"))
                    ignores.extend(
                        [
                            "test_opensearchpy/test_server_secured/",
                        ]
                    )

            # There are no plugins for unreleased versions of opensearch
            if environ.get("OPENSEARCH_VERSION") == "SNAPSHOT":
                ignores.extend(
                    [
                        "test_opensearchpy/test_server/test_plugins/",
                        "test_opensearchpy/test_async/test_server/test_plugins/",
                    ]
                )

            if ignores:
                argv.extend(["--ignore=%s" % ignore for ignore in ignores])

            # Not in CI, run all tests specified.
            else:
                argv.append(abspath(dirname(__file__)))

    exit_code = 0
    try:
        subprocess.check_call(argv, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        exit_code = e.returncode
    sys.exit(exit_code)


if __name__ == "__main__":
    run_all(sys.argv)
