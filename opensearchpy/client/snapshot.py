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


# ----------------------------------------------------
# THIS CODE IS GENERATED. MANUAL EDITS WILL BE LOST.
# ----------------------------------------------------
# <auto-generated-code>
#  The code was automatically generated using a [Python generator](https://github.com/saimedhi/opensearch-py/blob/Python-Client-Generator/utils/generate-api.py) with the assistance of [ninja templates](https://github.com/saimedhi/opensearch-py/tree/Python-Client-Generator/utils/templates), using [OpenAPI specifications](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) as input.
#  Modifying this file can lead to incorrect behavior and any changes will be overwritten upon code regeneration.
#  To contribute, please make the necessary changes to either the [Python generator](https://github.com/saimedhi/opensearch-py/blob/Python-Client-Generator/utils/generate-api.py) or the [OpenAPI specifications](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) as needed.
# </auto-generated-code>

from .utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class SnapshotClient(NamespacedClient):
    @query_params("cluster_manager_timeout", "master_timeout", "wait_for_completion")
    def create(self, repository, snapshot, body=None, params=None, headers=None):
        """
        Creates a snapshot in a repository.


        :arg repository: Repository name.
        :arg snapshot: Snapshot name.
        :arg body:
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning.
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, snapshot),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("cluster_manager_timeout", "master_timeout")
    def delete(self, repository, snapshot, params=None, headers=None):
        """
        Deletes a snapshot.


        :arg repository: Repository name.
        :arg snapshot: Snapshot name.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_snapshot", repository, snapshot),
            params=params,
            headers=headers,
        )

    @query_params(
        "cluster_manager_timeout", "ignore_unavailable", "master_timeout", "verbose"
    )
    def get(self, repository, snapshot, params=None, headers=None):
        """
        Returns information about a snapshot.


        :arg repository: Repository name.
        :arg snapshot: Comma-separated list of snapshot names.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg ignore_unavailable: Whether to ignore unavailable
            snapshots, defaults to false which means a SnapshotMissingException is
            thrown.
        :arg master_timeout: Operation timeout for connection to master
            node.
        :arg verbose: Whether to show verbose snapshot info or only show
            the basic info found in the repository index blob.
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "GET",
            _make_path("_snapshot", repository, snapshot),
            params=params,
            headers=headers,
        )

    @query_params("cluster_manager_timeout", "master_timeout", "timeout")
    def delete_repository(self, repository, params=None, headers=None):
        """
        Deletes a repository.


        :arg repository: Name of the snapshot repository to unregister.
            Wildcard (`*`) patterns are supported.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        :arg timeout: Operation timeout.
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'repository'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_snapshot", repository),
            params=params,
            headers=headers,
        )

    @query_params("cluster_manager_timeout", "local", "master_timeout")
    def get_repository(self, repository=None, params=None, headers=None):
        """
        Returns information about a repository.


        :arg repository: Comma-separated list of repository names.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg local: Return local information, do not retrieve the state
            from cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        """
        return self.transport.perform_request(
            "GET", _make_path("_snapshot", repository), params=params, headers=headers
        )

    @query_params("cluster_manager_timeout", "master_timeout", "timeout", "verify")
    def create_repository(self, repository, body, params=None, headers=None):
        """
        Creates a repository.


        :arg repository: Repository name.
        :arg body:
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        :arg timeout: Operation timeout.
        :arg verify: Whether to verify the repository after creation.
        """
        for param in (repository, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("cluster_manager_timeout", "master_timeout", "wait_for_completion")
    def restore(self, repository, snapshot, body=None, params=None, headers=None):
        """
        Restores a snapshot.


        :arg repository: Repository name.
        :arg snapshot: Snapshot name.
        :arg body:
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning.
        """
        for param in (repository, snapshot):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, snapshot, "_restore"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("cluster_manager_timeout", "ignore_unavailable", "master_timeout")
    def status(self, repository=None, snapshot=None, params=None, headers=None):
        """
        Returns information about the status of a snapshot.


        :arg repository: Repository name.
        :arg snapshot: Comma-separated list of snapshot names.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg ignore_unavailable: Whether to ignore unavailable
            snapshots, defaults to false which means a SnapshotMissingException is
            thrown.
        :arg master_timeout: Operation timeout for connection to master
            node.
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_snapshot", repository, snapshot, "_status"),
            params=params,
            headers=headers,
        )

    @query_params("cluster_manager_timeout", "master_timeout", "timeout")
    def verify_repository(self, repository, params=None, headers=None):
        """
        Verifies a repository.


        :arg repository: Repository name.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        :arg timeout: Operation timeout.
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'repository'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, "_verify"),
            params=params,
            headers=headers,
        )

    @query_params("cluster_manager_timeout", "master_timeout", "timeout")
    def cleanup_repository(self, repository, params=None, headers=None):
        """
        Removes stale data from repository.


        :arg repository: Repository name.
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        :arg timeout: Operation timeout.
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'repository'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, "_cleanup"),
            params=params,
            headers=headers,
        )

    @query_params("cluster_manager_timeout", "master_timeout")
    def clone(
        self, repository, snapshot, target_snapshot, body, params=None, headers=None
    ):
        """
        Clones indices from one snapshot into another snapshot in the same repository.


        :arg repository: Repository name.
        :arg snapshot: Snapshot name.
        :arg target_snapshot: The name of the cloned snapshot to create.
        :arg body:
        :arg cluster_manager_timeout: Operation timeout for connection
            to cluster-manager node.
        :arg master_timeout: Operation timeout for connection to master
            node.
        """
        for param in (repository, snapshot, target_snapshot, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_snapshot", repository, snapshot, "_clone", target_snapshot),
            params=params,
            headers=headers,
            body=body,
        )
