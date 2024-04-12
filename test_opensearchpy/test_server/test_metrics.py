# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from __future__ import unicode_literals

import time

from opensearchpy import RequestsHttpConnection
from opensearchpy.metrics.metrics_events import MetricsEvents
from opensearchpy.metrics.metrics_none import MetricsNone

from . import OpenSearchTestCase, get_client


class TestMetrics(OpenSearchTestCase):
    def tearDown(self) -> None:
        client = get_client()
        client.indices.delete(index=["test-index"], ignore_unavailable=True)

    def test_metrics_default_behavior(self) -> None:
        # Test default behavior when metrics is not passed to the client
        client = get_client()
        index_name = "test-index"
        index_body = {"settings": {"index": {"number_of_shards": 4}}}
        try:
            client.indices.create(index=index_name, body=index_body)
        except Exception as e:
            assert False, f"Error creating index: {e}"

    def test_metrics_none_behavior(self) -> None:
        # Test behavior when metrics is an instance of MetricsNone
        metrics = MetricsNone()
        client = get_client(metrics=metrics)
        index_name = "test-index"
        index_body = {"settings": {"index": {"number_of_shards": 4}}}
        client.indices.create(index=index_name, body=index_body)
        assert metrics.service_time is None


class TestMetricsEvents(OpenSearchTestCase):
    def tearDown(self) -> None:
        client = get_client()
        client.indices.delete(index=["test-index"], ignore_unavailable=True)

    def test_metrics_events_with_urllib3_connection(self) -> None:
        # Test MetricsEvents behavior with urllib3 connection
        metrics = MetricsEvents()
        client = get_client(metrics=metrics)

        # Calculate service time for create index operation
        index_name = "test-index"
        index_body = {"settings": {"index": {"number_of_shards": 4}}}
        start1 = time.perf_counter()
        client.indices.create(index=index_name, body=index_body)
        duration1 = time.perf_counter() - start1
        create_index_service_time = metrics.service_time
        assert (
            isinstance(create_index_service_time, float)
            and create_index_service_time < duration1
        )

        # Calculate service time for adding document operation
        document = {"title": "Moneyball", "director": "Bennett Miller", "year": "2011"}
        id = "1"
        start2 = time.perf_counter()
        client.index(index=index_name, body=document, id=id, refresh=True)
        duration2 = time.perf_counter() - start2
        assert (
            isinstance(metrics.service_time, float)
            and metrics.service_time < duration2
            and metrics.service_time != create_index_service_time
            # Above check is to confirm service time differs from the previous API call.
        )

    def test_metrics_events_with_requests_http_connection(self) -> None:
        # Test MetricsEvents behavior with requests HTTP connection
        metrics = MetricsEvents()
        client = get_client(metrics=metrics, connection_class=RequestsHttpConnection)

        # Calculate service time for create index operation
        index_name = "test-index"
        index_body = {"settings": {"index": {"number_of_shards": 4}}}
        start1 = time.perf_counter()
        client.indices.create(index_name, body=index_body)
        duration1 = time.perf_counter() - start1
        create_index_service_time = metrics.service_time
        assert (
            isinstance(create_index_service_time, float)
            and create_index_service_time < duration1
        )

        # Calculate service time for adding document operation
        document = {"title": "Moneyball", "director": "Bennett Miller", "year": "2011"}
        id = "1"
        start2 = time.perf_counter()
        client.index(index=index_name, body=document, id=id, refresh=True)
        duration2 = time.perf_counter() - start2
        assert (
            isinstance(metrics.service_time, float)
            and metrics.service_time < duration2
            and metrics.service_time != create_index_service_time
            # Above check is to confirm service time differs from the previous API call.
        )
