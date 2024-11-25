# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

# ------------------------------------------------------------------------------------------
# THIS CODE IS AUTOMATICALLY GENERATED AND MANUAL EDITS WILL BE LOST
#
# To contribute, kindly make modifications in the opensearch-py client generator
# or in the OpenSearch API specification, and run `nox -rs generate`. See DEVELOPER_GUIDE.md
# and https://github.com/opensearch-project/opensearch-api-specification for details.
# -----------------------------------------------------------------------------------------+


from typing import Any

from ..client.utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class ReplicationClient(NamespacedClient):
    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def autofollow_stats(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Gets information about auto-follow activity and any replication rules
        configured on the specified cluster.


        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return self.transport.perform_request(
            "GET",
            "/_plugins/_replication/autofollow_stats",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def create_replication_rule(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Automatically starts replication on indexes matching a specified pattern.


        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            "/_plugins/_replication/_autofollow",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def delete_replication_rule(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Deletes the specified replication rule.


        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "DELETE",
            "/_plugins/_replication/_autofollow",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def follower_stats(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Gets information about follower (syncing) indexes on a specified cluster.


        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return self.transport.perform_request(
            "GET",
            "/_plugins/_replication/follower_stats",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def leader_stats(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Gets information about replicated leader indexes on a specified cluster.


        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        return self.transport.perform_request(
            "GET", "/_plugins/_replication/leader_stats", params=params, headers=headers
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def pause(
        self,
        index: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Pauses replication of the leader index.


        :arg index: Name of the data stream, index, or index alias to
            perform bulk actions on.
        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_plugins", "_replication", index, "_pause"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def resume(
        self,
        index: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Resumes replication of the leader index.


        :arg index: Name of the data stream, index, or index alias to
            perform bulk actions on.
        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_plugins", "_replication", index, "_resume"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def start(
        self,
        index: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Initiate replication of an index from the leader cluster to the follower
        cluster.


        :arg index: Name of the data stream, index, or index alias to
            perform bulk actions on.
        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_replication", index, "_start"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def status(
        self,
        index: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Gets the status of index replication.


        :arg index: Name of the data stream, index, or index alias to
            perform bulk actions on.
        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_replication", index, "_status"),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def stop(
        self,
        index: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Terminates replication and converts the follower index to a standard index.


        :arg index: Name of the data stream, index, or index alias to
            perform bulk actions on.
        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_plugins", "_replication", index, "_stop"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def update_settings(
        self,
        index: Any,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Updates settings on the follower index.


        :arg index: Name of the data stream, index, or index alias to
            perform bulk actions on.
        :arg error_trace: Whether to include the stack trace of returned
            errors. Default is false.
        :arg filter_path: Used to reduce the response. This parameter
            takes a comma-separated list of filters. It supports using wildcards to
            match any field or part of a field’s name. You can also exclude fields
            with "-".
        :arg human: Whether to return human readable values for
            statistics. Default is True.
        :arg pretty: Whether to pretty format the returned JSON
            response. Default is false.
        :arg source: The URL-encoded request definition. Useful for
            libraries that do not accept a request body for non-POST requests.
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_replication", index, "_update"),
            params=params,
            headers=headers,
            body=body,
        )
