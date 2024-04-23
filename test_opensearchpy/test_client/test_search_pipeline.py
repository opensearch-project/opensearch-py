# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from test_opensearchpy.test_cases import OpenSearchTestCase


class TestSearchPipeline(OpenSearchTestCase):
    def test_create_search_pipeline(self) -> None:
        body = {
            "request_processors": [
                {
                    "filter_query": {
                        "tag": "tag1",
                        "description": "This processor returns only publicly visible documents",
                        "query": {"term": {"visibility": "public"}},
                    }
                }
            ],
            "response_processors": [
                {"rename_field": {"field": "message", "target_field": "notification"}}
            ],
        }

        self.client.search_pipeline.put("my_pipeline", body)
        self.assert_url_called("PUT", "/_search/pipeline/my_pipeline")

    def test_get_search_pipeline(self) -> None:
        self.client.search_pipeline.get("my_pipeline")
        self.assert_url_called("GET", "/_search/pipeline/my_pipeline")
