# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import filecmp
import os
import shutil

import requests


def main() -> None:
    """
    Update CHANGELOG.md when API generator produces new code differing from existing.
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    after_paths = [
        os.path.join(root_dir, f"opensearchpy/{folder}")
        for folder in ["client", "_async/client"]
    ]

    before_paths = [
        os.path.join(root_dir, f"before_generate/{folder}")
        for folder in ["client", "async_client"]
    ]

    # Compare only .py files and take their union for client and async_client directories
    before_files_client = set(
        file for file in os.listdir(before_paths[0]) if file.endswith(".py")
    )
    after_files_client = set(
        file for file in os.listdir(after_paths[0]) if file.endswith(".py")
    )

    before_files_async_client = set(
        file for file in os.listdir(before_paths[1]) if file.endswith(".py")
    )
    after_files_async_client = set(
        file for file in os.listdir(after_paths[1]) if file.endswith(".py")
    )

    all_files_union_client = before_files_client.union(after_files_client)
    all_files_union_async_client = before_files_async_client.union(
        after_files_async_client
    )

    # Compare files and check for mismatches or errors for client and async_client directories
    mismatch_client, errors_client = filecmp.cmpfiles(
        before_paths[0], after_paths[0], all_files_union_client, shallow=True
    )[1:]
    mismatch_async_client, errors_async_client = filecmp.cmpfiles(
        before_paths[1], after_paths[1], all_files_union_async_client, shallow=True
    )[1:]

    if mismatch_client or errors_client or mismatch_async_client or errors_async_client:
        print("Changes detected")
        response = requests.get(
            "https://api.github.com/repos/opensearch-project/opensearch-api-specification/commits"
        )
        if response.ok:
            commit_info = response.json()[0]
            commit_url = commit_info["html_url"]
            latest_commit_sha = commit_info.get("sha")
        else:
            raise Exception(
                f"Failed to fetch opensearch-api-specification commit information. Status code: {response.status_code}"
            )

        with open("CHANGELOG.md", "r+", encoding="utf-8") as file:
            content = file.read()
            if commit_url not in content:
                if "### Updated APIs" in content:
                    file_content = content.replace(
                        "### Updated APIs",
                        f"### Updated APIs\n- Updated opensearch-py APIs to reflect [opensearch-api-specification@{latest_commit_sha[:7]}]({commit_url})",
                        1,
                    )
                    file.seek(0)
                    file.write(file_content)
                    file.truncate()
                else:
                    raise Exception(
                        "'Updated APIs' section is not present in CHANGELOG.md"
                    )
    else:
        print("No changes detected")

    # Clean up
    for path in before_paths:
        shutil.rmtree(path)


if __name__ == "__main__":
    main()
