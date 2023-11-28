# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

"""Script which verifies that all source files have a license header.
Has two modes: 'fix' and 'check'. 'fix' fixes problems, 'check' will
error out if 'fix' would have changed the file.
"""

import os
import re
import sys
from typing import Iterator, List

LINES_TO_KEEP = ["#!/usr/bin/env python"]

LICENSE_HEADER = """
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
""".strip()


def find_files_to_fix(sources: List[str]) -> Iterator[str]:
    """Iterates over all files and dirs in 'sources' and returns
    only the filepaths that need fixing.
    """
    for source in sources:
        if os.path.isfile(source) and does_file_need_fix(source):
            yield source
        elif os.path.isdir(source):
            for root, _, filenames in os.walk(source):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    if does_file_need_fix(filepath):
                        yield filepath


def does_file_need_fix(filepath: str) -> bool:
    if not re.search(r"\.py$", filepath):
        return False
    existing_header = ""
    with open(filepath, mode="r") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0 or line in LINES_TO_KEEP:
                pass
            elif line[0] == "#":
                existing_header += line
                existing_header += "\n"
            else:
                break
    return not existing_header.startswith(LICENSE_HEADER)


def add_header_to_file(filepath: str) -> None:
    with open(filepath, mode="r") as f:
        lines = list(f)
    i = 0
    for i, line in enumerate(lines):
        if len(line) > 0 and line not in LINES_TO_KEEP:
            break
    lines = lines[:i] + [LICENSE_HEADER] + lines[i:]
    with open(filepath, mode="w") as f:
        f.truncate()
        f.write("".join(lines))
    print(f"Fixed {os.path.relpath(filepath, os.getcwd())}")


def main() -> None:
    mode = sys.argv[1]
    assert mode in ("fix", "check")
    sources = [os.path.abspath(x) for x in sys.argv[2:]]
    files_to_fix = find_files_to_fix(sources)

    if mode == "fix":
        for filepath in files_to_fix:
            add_header_to_file(filepath)
    else:
        no_license_headers = list(files_to_fix)
        if no_license_headers:
            print("No license header found in:")
            cwd = os.getcwd()
            [
                print(f" - {os.path.relpath(filepath, cwd)}")
                for filepath in no_license_headers
            ]
            sys.exit(1)
        else:
            print("All files had license header")


if __name__ == "__main__":
    main()
