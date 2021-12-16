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

from __future__ import print_function

import subprocess
import sys
from os import environ
from os.path import abspath, dirname, exists, join, pardir


def fetch_opensearch_repo():
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

    # add a remote
    subprocess.check_call(
        "cd %s && git remote add origin https://github.com/opensearch-project/opensearch.git"
        % repo_path,
        shell=True,
    )

    # fetch the sha commit, version from info()
    print("Fetching opensearch repo...")
    subprocess.check_call("cd %s && git fetch origin %s" % (repo_path, sha), shell=True)


def run_all(argv=None):
    sys.exitfunc = lambda: sys.stderr.write("Shutting down....\n")

    # fetch yaml tests anywhere that's not GitHub Actions
    if "GITHUB_ACTION" not in environ:
        fetch_opensearch_repo()

    # always insert coverage when running tests
    if argv is None:
        junit_xml = join(
            abspath(dirname(dirname(__file__))), "junit", "opensearch-py-junit.xml"
        )
        argv = [
            "pytest",
            "--cov=opensearch",
            "--junitxml=%s" % junit_xml,
            "--log-level=DEBUG",
            "--cache-clear",
            "-vv",
        ]

        secured = False
        if environ.get("OPENSEARCH_URL", "").startswith("https://"):
            secured = True

        ignores = []
        # Python 3.6+ is required for async
        if sys.version_info < (3, 6):
            ignores.append("test_opensearchpy/test_async/")

        # GitHub Actions, run non-server tests
        if "GITHUB_ACTION" in environ:
            ignores.extend(
                [
                    "test_opensearchpy/test_server/",
                    "test_opensearchpy/test_server_secured/",
                    "test_opensearchpy/test_async/test_server/",
                ]
            )

        # Jenkins/Github actions, only run server tests
        if environ.get("TEST_TYPE") == "server":
            test_dir = abspath(dirname(__file__))
            if secured:
                argv.append(join(test_dir, "test_server_secured"))
                ignores.extend(
                    [
                        "test_opensearchpy/test_server/",
                        "test_opensearchpy/test_async/test_server/",
                    ]
                )
            else:
                argv.append(join(test_dir, "test_server"))
                if sys.version_info >= (3, 6):
                    argv.append(join(test_dir, "test_async/test_server"))
                ignores.extend(
                    [
                        "test_opensearchpy/test_server_secured/",
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
