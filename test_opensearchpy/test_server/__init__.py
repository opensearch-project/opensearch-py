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
from unittest import SkipTest

from opensearchpy.helpers import test
from opensearchpy.helpers.test import OpenSearchTestCase as BaseTestCase

CLIENT: Any = None


def get_client(**kwargs: Any) -> Any:
    global CLIENT
    if CLIENT is False:
        raise SkipTest("No client is available")
    if CLIENT is not None and not kwargs:
        return CLIENT

    try:
        new_client = test.get_test_client(**kwargs)
    except SkipTest:
        CLIENT = False
        raise

    if not kwargs:
        CLIENT = new_client

    return new_client


def setup_module() -> None:
    get_client()


class OpenSearchTestCase(BaseTestCase):
    @staticmethod
    def _get_client(**kwargs: Any) -> Any:
        return get_client(**kwargs)
