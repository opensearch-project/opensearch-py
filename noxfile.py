# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import nox

SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "opensearchpy/",
    "test_opensearchpy/",
    "utils/",
)


@nox.session(python=["2.7", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9"])
def test(session):
    session.install(".")
    session.install("-r", "dev-requirements.txt")

    session.run("python", "setup.py", "test")


@nox.session()
def format(session):
    session.install("black", "isort")

    session.run("isort", "--profile=black", *SOURCE_FILES)
    session.run("black", "--target-version=py27", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session()
def lint(session):
    session.install("flake8", "black", "mypy", "isort", "types-requests")

    session.run("isort", "--check", "--profile=black", *SOURCE_FILES)
    session.run("black", "--target-version=py33", "--check", *SOURCE_FILES)
    session.run("flake8", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "check", *SOURCE_FILES)

    # Workaround to make '-r' to still work despite uninstalling aiohttp below.
    session.run("python", "-m", "pip", "install", "aiohttp")

    # Run mypy on the package and then the type examples separately for
    # the two different mypy use-cases, ourselves and our users.
    session.run("mypy", "--strict", "opensearchpy/")
    session.run("mypy", "--strict", "test_opensearchpy/test_types/sync_types.py")
    session.run("mypy", "--strict", "test_opensearchpy/test_types/async_types.py")

    # Make sure we don't require aiohttp to be installed for users to
    # receive type hint information from mypy.
    session.run("python", "-m", "pip", "uninstall", "--yes", "aiohttp")
    session.run("mypy", "--strict", "opensearchpy/")
    session.run("mypy", "--strict", "test_opensearchpy/test_types/sync_types.py")


@nox.session()
def docs(session):
    session.install(".")
    session.install(
        "-rdev-requirements.txt", "sphinx-rtd-theme", "sphinx-autodoc-typehints"
    )
    session.run("python", "-m", "pip", "install", "sphinx-autodoc-typehints")
