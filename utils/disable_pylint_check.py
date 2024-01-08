# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
import os
import re
from typing import Generator

import black


def test_files() -> Generator[str, None, None]:
    """
    generator to yield full paths to files that look like unit tests
    """
    # TODO should support tests in __init__.py files
    test_source_files_re = re.compile(r".*test_[^/]+\.py$")
    include_dirs = ["test_opensearchpy", "samples", "benchmarks"]
    for top in include_dirs:
        for root, dirs, files in os.walk(top, topdown=True):
            for name in files:
                full_path = os.path.join(root, name)
                if test_source_files_re.match(full_path):
                    yield full_path


if __name__ == "__main__":
    """
    adds a disable instruction for test_ methods for missing-function-docstring.
    test methods typically have good names and can go without docstring for
    comments. this is destructive so use git as part of the process.
    """
    MISSING_FUNCTION_DOCSTRING_DISABLE = "# pylint: disable=missing-function-docstring"
    test_method_re = re.compile(
        r"(?P<leading_space>[^\S\r\n]*)(?P<async_keyword>async)*"
        r"(?P<function_declaration>\s*def\stest_.*:)"
        r"(?P<whitespace>(\n|.)*?)(?P<pylint_disable_declaration>\s*#\spylint.*)*",
        flags=re.MULTILINE,
    )
    for file in test_files():
        new_file_contents = ""  # pylint: disable=C0103
        with open(file, encoding="utf-8") as test_file:
            print(f"Working on {file}")
            full_file = test_file.read()
            # TODO multiline function declarations are not supported
            new_file_contents = re.sub(
                test_method_re,
                r"\g<leading_space>\g<async_keyword>\g<function_declaration>\n\g<leading_space>\g<leading_space>"  # pylint: disable=line-too-long
                + MISSING_FUNCTION_DOCSTRING_DISABLE,
                full_file,
            )
            new_file_contents = black.format_str(
                new_file_contents, mode=black.FileMode()
            )
        with open(f"{file}", "w", encoding="utf-8") as new_file:
            new_file.write(new_file_contents)
