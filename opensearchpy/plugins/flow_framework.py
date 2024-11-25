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


class FlowFrameworkClient(NamespacedClient):
    @query_params(
        "error_trace",
        "filter_path",
        "human",
        "pretty",
        "provision",
        "reprovision",
        "source",
        "update_fields",
        "use_case",
        "validation",
    )
    def create(
        self,
        body: Any = None,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Create a workflow.


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
        :arg use_case: To use a workflow template, specify it in the
            `use_case` query parameter when creating a workflow.
        """
        return self.transport.perform_request(
            "POST",
            "/_plugins/_flow_framework/workflow",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "clear_status", "error_trace", "filter_path", "human", "pretty", "source"
    )
    def delete(
        self,
        workflow_id: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Delete a workflow.


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
        if workflow_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'workflow_id'."
            )

        return self.transport.perform_request(
            "DELETE",
            _make_path("_plugins", "_flow_framework", "workflow", workflow_id),
            params=params,
            headers=headers,
        )

    @query_params(
        "allow_delete", "error_trace", "filter_path", "human", "pretty", "source"
    )
    def deprovision(
        self,
        workflow_id: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Deprovision workflow's resources when you no longer need it.


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
        if workflow_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'workflow_id'."
            )

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_plugins", "_flow_framework", "workflow", workflow_id, "_deprovision"
            ),
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def get(
        self,
        workflow_id: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Get a workflow.


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
        if workflow_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'workflow_id'."
            )

        return self.transport.perform_request(
            "GET",
            _make_path("_plugins", "_flow_framework", "workflow", workflow_id),
            params=params,
            headers=headers,
        )

    @query_params("all", "error_trace", "filter_path", "human", "pretty", "source")
    def get_status(
        self,
        workflow_id: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Get the provisioning deployment status until it is complete.


        :arg all: The all parameter specifies whether the response
            should return all fields. Default is false.
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
        if workflow_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'workflow_id'."
            )

        return self.transport.perform_request(
            "GET",
            _make_path(
                "_plugins", "_flow_framework", "workflow", workflow_id, "_status"
            ),
            params=params,
            headers=headers,
        )

    @query_params(
        "error_trace", "filter_path", "human", "pretty", "source", "workflow_step"
    )
    def get_steps(
        self,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Get a list of workflow steps.


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
            "/_plugins/_flow_framework/workflow/_steps",
            params=params,
            headers=headers,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def provision(
        self,
        workflow_id: Any,
        body: Any = None,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Provisioning a workflow. This API is also executed when the Create or Update
        Workflow API is called with the provision parameter set to true.


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
        if workflow_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'workflow_id'."
            )

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_plugins", "_flow_framework", "workflow", workflow_id, "_provision"
            ),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def search(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Search for workflows by using a query matching a field.


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
            "/_plugins/_flow_framework/workflow/_search",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("error_trace", "filter_path", "human", "pretty", "source")
    def search_state(
        self,
        body: Any,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Search for workflows by using a query matching a field.


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
            "/_plugins/_flow_framework/workflow/state/_search",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "error_trace",
        "filter_path",
        "human",
        "pretty",
        "provision",
        "reprovision",
        "source",
        "update_fields",
        "use_case",
        "validation",
    )
    def update(
        self,
        workflow_id: Any,
        body: Any = None,
        params: Any = None,
        headers: Any = None,
    ) -> Any:
        """
        Update a workflow. You can only update a complete workflow if it has not yet
        been provisioned.


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
        :arg use_case: To use a workflow template, specify it in the
            `use_case` query parameter when creating a workflow.
        """
        if workflow_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'workflow_id'."
            )

        return self.transport.perform_request(
            "PUT",
            _make_path("_plugins", "_flow_framework", "workflow", workflow_id),
            params=params,
            headers=headers,
            body=body,
        )
