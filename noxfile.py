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


from typing import Any

import nox

SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "opensearchpy/",
    "test_opensearchpy/",
    "utils/",
    "samples/",
    "benchmarks/",
    "docs/",
)


@nox.session(python=["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"])  # type: ignore
def test(session: Any) -> None:
    # pylint: disable=missing-function-docstring
    session.install(".")
    # ensure client can be imported without aiohttp
    session.run("python", "-c", "import opensearchpy\nprint(opensearchpy.OpenSearch())")
    # ensure client can be imported with aiohttp
    session.install(".[async]")
    session.run(
        "python", "-c", "import opensearchpy\nprint(opensearchpy.AsyncOpenSearch())"
    )

    session.install("-r", "dev-requirements.txt")

    session.run("python", "setup.py", "test")


@nox.session(python=["3.7"])  # type: ignore
def format(session: Any) -> None:
    # pylint: disable=missing-function-docstring
    session.install(".")
    session.install("black", "isort")

    session.run("isort", *SOURCE_FILES)
    session.run("black", *SOURCE_FILES)
    session.run("python", "utils/license_headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session(python=["3.7"])  # type: ignore
def lint(session: Any) -> None:
    # pylint: disable=missing-function-docstring
    session.install(
        "flake8",
        "black",
        "mypy",
        "isort",
        "pylint",
        "types-requests",
        "types-six",
        "types-simplejson",
        "types-python-dateutil",
        "types-PyYAML",
        "types-mock",
        "types-pytz",
    )

    session.run("isort", "--check", *SOURCE_FILES)
    session.run("black", "--check", *SOURCE_FILES)
    session.run("flake8", *SOURCE_FILES)
    if (
        # run export NOXFILE_PYLINT_PARAMS_FEATURE=true on the command line to run this code
        "NOXFILE_PYLINT_PARAMS_FEATURE" in session.env
        and session.env["NOXFILE_PYLINT_PARAMS_FEATURE"]
    ):
        lint_per_folder(session)
    else:
        session.run("pylint", *SOURCE_FILES)

    session.run("python", "utils/license_headers.py", "check", *SOURCE_FILES)

    # Workaround to make '-r' to still work despite uninstalling aiohttp below.
    session.run("python", "-m", "pip", "install", "aiohttp")

    # Run mypy on the package and then the type examples separately for
    # the two different mypy use-cases, ourselves and our users.
    session.run("mypy", "--strict", *SOURCE_FILES)
    session.run("mypy", "--strict", "test_opensearchpy/test_types/sync_types.py")
    session.run("mypy", "--strict", "test_opensearchpy/test_types/async_types.py")

    # Make sure we don't require aiohttp to be installed for users to
    # receive type hint information from mypy.
    session.run("python", "-m", "pip", "uninstall", "--yes", "aiohttp")
    session.run("mypy", "--strict", "opensearchpy/")
    session.run("mypy", "--strict", "test_opensearchpy/test_types/sync_types.py")


def lint_per_folder(session: Any) -> None:
    """
    allows configuration of pylint rules per folder and runs a pylint command for each folder
    :param session: the current nox session
    """
    # tests should not require function docstrings - tests function names describe themselves;
    # opensearchpy is generated; may require in the generator code some places
    default_enable = [
        "line-too-long",
        "invalid-name",
        "pointless-statement",
        "unspecified-encoding",
        "missing-function-docstring",
    ]
    override_enable = {
        "test_opensearchpy/": [
            "line-too-long",
            # "invalid-name", lots of short functions with one or two character names
            "pointless-statement",
            "unspecified-encoding",
            "redefined-outer-name",
        ],
        # "opensearchpy/": [""],
    }
    # import-outside-toplevel
    # enable = line-too-long, invalid-name, pointless-statement, unspecified-encoding,
    # missing-function-docstring
    # should fail the build: redefined-outer-name, , line-too-long, invalid-name,
    # pointless-statement,
    # import-outside-toplevel, unused-variable, unexpected-keyword-arg,
    # raise-missing-from, invalid-unary-operand-type,
    # attribute-defined-outside-init, unspecified-encoding
    # should be warnings: super-with-arguments, too-few-public-methods, redefined-builtin,
    # too-many-arguments
    # (how many is too many?), useless-object-inheritance, too-many-locals,
    # too-many-branches, dangerous-default-value,
    # arguments-renamed
    # warn, then fail later (low priority): too-many-locals, unnecessary-dunder-call,
    # too-many-public-methods,
    # no-else-return, invalid-overridden-method, cyclic-import
    # does this conflict with isort? wrong-import-position
    for source_file in SOURCE_FILES:
        args = ["--disable=all"]
        if source_file in override_enable:
            args.append(f"--enable={','.join(override_enable[source_file])}")
        else:
            args.append(f"--enable={','.join(default_enable)}")
        args.append(source_file)
        session.run("pylint", *args)


@nox.session()  # type: ignore
def docs(session: Any) -> None:
    # pylint: disable=missing-function-docstring
    session.install(".")
    session.install(".[docs]")
    with session.chdir("docs"):
        session.run("make", "html")


@nox.session()  # type: ignore
def generate(session: Any) -> None:
    # pylint: disable=missing-function-docstring
    session.install("-rdev-requirements.txt")
    session.run("python", "utils/generate_api.py")
    format(session)
