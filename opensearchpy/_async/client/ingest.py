# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from .utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class IngestClient(NamespacedClient):
    @query_params("master_timeout", "summary")
    async def get_pipeline(self, id=None, params=None, headers=None):
        """
        Returns a pipeline.


        :arg id: Comma separated list of pipeline ids. Wildcards
            supported
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg summary: Return pipelines without their definitions
            (default: false)
        """
        return await self.transport.perform_request(
            "GET", _make_path("_ingest", "pipeline", id), params=params, headers=headers
        )

    @query_params("master_timeout", "timeout")
    async def put_pipeline(self, id, body, params=None, headers=None):
        """
        Creates or updates a pipeline.


        :arg id: Pipeline ID
        :arg body: The ingest definition
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_ingest", "pipeline", id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("master_timeout", "timeout")
    async def delete_pipeline(self, id, params=None, headers=None):
        """
        Deletes a pipeline.


        :arg id: Pipeline ID
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_ingest", "pipeline", id),
            params=params,
            headers=headers,
        )

    @query_params("verbose")
    async def simulate(self, body, id=None, params=None, headers=None):
        """
        Allows to simulate a pipeline with example documents.


        :arg body: The simulate definition
        :arg id: Pipeline ID
        :arg verbose: Verbose mode. Display data output for each
            processor in executed pipeline
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST",
            _make_path("_ingest", "pipeline", id, "_simulate"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def processor_grok(self, params=None, headers=None):
        """
        Returns a list of the built-in patterns.

        """
        return await self.transport.perform_request(
            "GET", "/_ingest/processor/grok", params=params, headers=headers
        )

    @query_params()
    async def geo_ip_stats(self, params=None, headers=None):
        """
        Returns statistical information about geoip databases

        """
        return await self.transport.perform_request(
            "GET", "/_ingest/geoip/stats", params=params, headers=headers
        )
