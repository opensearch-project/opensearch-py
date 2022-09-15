#!/usr/bin/env bash
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# Check that source code files in this repo have the appropriate license
# header.

if [ "$TRACE" != "" ]; then
    export PS4='${BASH_SOURCE}:${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
    set -o xtrace
fi
set -o errexit
set -o pipefail

TOP=$(cd "$(dirname "$0")/.." >/dev/null && pwd)
NLINES_SC=$(wc -l ./.ci/license/license-sc.txt | awk '{print $1}')
NLINES_MC=$(wc -l ./.ci/license/license-mc.txt | awk '{print $1}')

function check_license_header {
    local fP
    f=$1
    if [[ $f == *.fs ]] && ! diff -a --strip-trailing-cr ./.ci/license/license-mc.txt <(head -$NLINES_MC "$f") >/dev/null; then
        echo $f
        echo "check-license-headers: error: '$f' does not have required license header, see 'diff -u ./.ci/license/license-mc.txt <(head -$NLINES_MC $f)'"
        return 1
    elif [[ $f != *.fs ]] && ! diff -a --strip-trailing-cr ./.ci/license/license-sc.txt <(head -$NLINES_SC "$f") >/dev/null; then
        echo "check-license-headers: error: '$f' does not have required license header, see 'diff -u ./.ci/license/license-sc.txt <(head -$NLINES_SC $f)'"
        return 1
    else
        return 0
    fi
}

cd "$TOP"
nErrors=0
for f in $(git ls-files | grep '\.py$'); do
    if ! check_license_header $f; then
        nErrors=$((nErrors+1))
    fi
done

for f in $(git ls-files | grep '\.pyi$'); do
    if ! check_license_header $f; then
        nErrors=$((nErrors+1))
    fi
done

if [[ $nErrors -eq 0 ]]; then
    exit 0
else
    exit 1
fi