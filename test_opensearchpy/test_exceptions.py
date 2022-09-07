# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from opensearchpy.exceptions import TransportError

from .test_cases import TestCase


class TestTransformError(TestCase):
    def test_transform_error_parse_with_error_reason(self):
        e = TransportError(
            500,
            "InternalServerError",
            {"error": {"root_cause": [{"type": "error", "reason": "error reason"}]}},
        )

        self.assertEqual(
            str(e), "TransportError(500, 'InternalServerError', 'error reason')"
        )

    def test_transform_error_parse_with_error_string(self):
        e = TransportError(
            500, "InternalServerError", {"error": "something error message"}
        )

        self.assertEqual(
            str(e),
            "TransportError(500, 'InternalServerError', 'something error message')",
        )
