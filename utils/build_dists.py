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


"""A command line tool for building and verifying releases
Can be used for building both 'opensearchpy' and 'opensearchpyX' dists.
Only requires 'name' in 'setup.py' and the directory to be changed.
"""

import contextlib
import os
import re
import shlex
import shutil
import sys
import tempfile
from typing import Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = None


@contextlib.contextmanager  # type: ignore
def set_tmp_dir() -> None:
    """
    makes and yields a temporary directory for any working files needed for a process during a build
    """
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp()
    yield TMP_DIR
    shutil.rmtree(TMP_DIR)
    TMP_DIR = None


def run(*argv: Any, expect_exit_code: int = 0) -> None:
    """
    runs a command within this script
    :param argv: command to run e.g. "git" "checkout" "--" "setup.py" "opensearchpy/"
    :param expect_exit_code: code to compare with actual exit code from command.
    will exit the process if they do not
    match the proper exit code
    """
    global TMP_DIR
    if TMP_DIR is None:
        os.chdir(BASE_DIR)
    else:
        os.chdir(TMP_DIR)

    cmd = " ".join(shlex.quote(x) for x in argv)
    print("$ " + cmd)
    exit_code = os.system(cmd)
    if exit_code != expect_exit_code:
        print(
            "Command exited incorrectly: should have been %d was %d"
            % (expect_exit_code, exit_code)
        )
        exit(exit_code or 1)


def test_dist(dist: Any) -> None:
    """
    validate that the distribution created works
    :param dist: base directory of the distribution
    """
    with set_tmp_dir() as tmp_dir:  # type: ignore
        dist_name = re.match(  # type: ignore
            r"^(opensearchpy\d*)-",
            os.path.basename(dist)
            .replace("opensearch-py", "opensearchpy")
            .replace("opensearch_py", "opensearchpy"),
        ).group(1)

        # Build the venv and install the dist
        run("python", "-m", "venv", os.path.join(tmp_dir, "venv"))
        venv_python = os.path.join(tmp_dir, "venv/bin/python")
        run(venv_python, "-m", "pip", "install", "-U", "pip", "mypy")
        run(venv_python, "-m", "pip", "install", dist)

        # Test the sync namespaces
        run(venv_python, "-c", f"from {dist_name} import OpenSearch, Q")
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import scan, bulk, streaming_bulk, reindex",
        )
        run(venv_python, "-c", f"from {dist_name} import OpenSearch")
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import scan, bulk, streaming_bulk, reindex",
        )

        # Ensure that async is not available yet
        run(
            venv_python,
            "-c",
            f"from {dist_name} import AsyncOpenSearch",
            expect_exit_code=256,
        )

        # Ensure async helpers are available regardless of aiohttp installation
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import async_scan, async_bulk, async_streaming_bulk, async_reindex",
        )

        # Install aiohttp and see that async is now available
        run(venv_python, "-m", "pip", "install", "aiohttp")
        run(venv_python, "-c", f"from {dist_name} import AsyncOpenSearch")
        run(
            venv_python,
            "-c",
            f"from {dist_name}.helpers import async_scan, async_bulk, async_streaming_bulk, async_reindex",
        )

        # Only need to test 'async_types' for non-aliased package
        # since 'aliased_types' tests both async and sync.
        if dist_name == "opensearchpy":
            run(
                venv_python,
                "-m",
                "mypy",
                "--strict",
                os.path.join(BASE_DIR, "test_opensearchpy/test_types/async_types.py"),
            )

        # Ensure that the namespaces are correct for the dist
        for suffix in ("", "1", "2", "5", "6", "7", "8", "9", "10"):
            distx_name = f"opensearchpy{suffix}"
            run(
                venv_python,
                "-c",
                f"import {distx_name}",
                expect_exit_code=256 if distx_name != dist_name else 0,
            )

        # Check that sync types work for 'opensearchpy' and
        # that aliased types work for 'opensearchpyX'
        if dist_name == "opensearchpy":
            run(
                venv_python,
                "-m",
                "mypy",
                "--strict",
                os.path.join(BASE_DIR, "test_opensearchpy/test_types/sync_types.py"),
            )
        else:
            run(
                venv_python,
                "-m",
                "mypy",
                "--strict",
                os.path.join(BASE_DIR, "test_opensearchpy/test_types/aliased_types.py"),
            )

        # Uninstall the dist, see that we can't import things anymore
        run(
            venv_python,
            "-m",
            "pip",
            "uninstall",
            "--yes",
            dist_name.replace("opensearchpy", "opensearch-py"),
        )
        run(
            venv_python,
            "-c",
            f"from {dist_name} import OpenSearch,Q",
            expect_exit_code=256,
        )


def main() -> None:
    """
    creates a distribution given of the OpenSearch python client
    Notes: does not run on MacOS; this script is generally driven by a GitHub Action located in
    .github/workflows/unified-release.yml
    """
    run("git", "checkout", "--", "setup.py", "opensearchpy/")
    run("rm", "-rf", "build/", "dist/*", "*.egg-info", ".eggs")
    run("python", "setup.py", "sdist", "bdist_wheel")

    # Grab the major version to be used as a suffix.
    version_path = os.path.join(BASE_DIR, "opensearchpy/_version.py")
    with open(version_path, encoding="utf-8") as file:
        data = file.read()
        version_match = re.search(
            r"^__versionstr__: str\s+=\s+[\"\']([^\"\']+)[\"\']", data, re.M
        )
        if version_match:
            version = version_match.group(1)
        else:
            raise Exception(f"Invalid version: {data}")

    major_version = version.split(".")[0]

    # If we're handed a version from the build manager we
    # should check that the version is correct or write
    # a new one.
    if len(sys.argv) >= 2:
        # 'build_version' is what the release manager wants,
        # 'expect_version' is what we're expecting to compare
        # the package version to before building the dists.
        build_version = expect_version = sys.argv[1]

        # Any prefixes in the version specifier mean we're making
        # a pre-release which will modify __versionstr__ locally
        # and not produce a git tag.
        if any(x in build_version for x in ("-SNAPSHOT", "-rc", "-alpha", "-beta")):
            # If a snapshot, then we add '+dev'
            if "-SNAPSHOT" in build_version:
                version = version + "+dev"
            # alpha/beta/rc -> aN/bN/rcN
            else:
                pre_number = re.search(r"-(a|b|rc)(?:lpha|eta|)(\d+)$", expect_version)
                version = version + pre_number.group(1) + pre_number.group(2)  # type: ignore

            expect_version = re.sub(
                r"(?:-(?:SNAPSHOT|alpha\d+|beta\d+|rc\d+))+$", "", expect_version
            )
            if expect_version.endswith(".x"):
                expect_version = expect_version[:-1]

            # For snapshots we ensure that the version in the package
            # at least *starts* with the version. This is to support
            # build_version='7.x-SNAPSHOT'.
            if not version.startswith(expect_version):
                print(
                    "Version of package (%s) didn't match the "
                    "expected release version (%s)" % (version, build_version)
                )
                exit(1)

        # A release that will be tagged, we want
        # there to be no '+dev', etc.
        elif expect_version != version:
            print(
                "Version of package (%s) didn't match the "
                "expected release version (%s)" % (version, build_version)
            )
            exit(1)

    for suffix in ("", major_version):
        run("rm", "-rf", "build/", "*.egg-info", ".eggs")

        # Rename the module to fit the suffix.
        shutil.move(
            os.path.join(BASE_DIR, "opensearchpy"),
            os.path.join(BASE_DIR, "opensearchpy%s" % suffix),
        )

        # Ensure that the version within 'opensearchpy/_version.py' is correct.
        version_path = os.path.join(BASE_DIR, f"opensearchpy{suffix}/_version.py")
        with open(version_path, encoding="utf-8") as file:
            version_data = file.read()
        version_data = re.sub(
            r"__versionstr__: str = \"[^\"]+\"",
            '__versionstr__: str = "%s"' % version,
            version_data,
        )
        with open(version_path, "w", encoding="utf-8") as file:
            file.truncate()
            file.write(version_data)

        # Rewrite setup.py with the new name.
        setup_py_path = os.path.join(BASE_DIR, "setup.py")
        with open(setup_py_path, encoding="utf-8") as file:
            setup_py = file.read()
        with open(setup_py_path, "w", encoding="utf-8") as file:
            file.truncate()
            assert 'PACKAGE_NAME = "opensearch-py"' in setup_py
            file.write(
                setup_py.replace(
                    'PACKAGE_NAME = "opensearch-py"',
                    'PACKAGE_NAME = "opensearch-py%s"' % suffix,
                )
            )

        # Build the sdist/wheels
        run("python", "setup.py", "sdist", "bdist_wheel")

        # Clean up everything.
        run("git", "checkout", "--", "setup.py", "opensearchpy/")
        if suffix:
            run("rm", "-rf", "opensearchpy%s/" % suffix)

    # Test everything that got created
    dists = os.listdir(os.path.join(BASE_DIR, "dist"))
    assert len(dists) == 4
    for dist in dists:
        test_dist(os.path.join(BASE_DIR, "dist", dist))
    os.system("chmod a+w dist/*")

    # After this run 'python -m twine upload dist/*'
    print(
        "\n\n"
        "===============================\n\n"
        "    * Releases are ready! *\n\n"
        "$ python -m twine upload dist/*\n\n"
        "==============================="
    )


if __name__ == "__main__":
    main()
