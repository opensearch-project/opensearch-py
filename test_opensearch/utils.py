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

import time

from opensearch import OpenSearch


def wipe_cluster(client):
    """Wipes a cluster clean between test cases"""
    close_after_wipe = False
    try:
        # If client is async we need to replace the client
        # with a synchronous one.
        from opensearch import AsyncOpenSearch

        if isinstance(client, AsyncOpenSearch):
            client = OpenSearch(client.transport.hosts, verify_certs=False)
            close_after_wipe = True
    except ImportError:
        pass

    wipe_snapshots(client)
    wipe_indices(client)

    client.indices.delete_template(name="*")
    client.indices.delete_index_template(name="*")
    client.cluster.delete_component_template(name="*")

    wipe_cluster_settings(client)

    wait_for_cluster_state_updates_to_finish(client)
    if close_after_wipe:
        client.close()


def wipe_cluster_settings(client):
    settings = client.cluster.get_settings()
    new_settings = {}
    for name, value in settings.items():
        if value:
            new_settings.setdefault(name, {})
            for key in value.keys():
                new_settings[name][key + ".*"] = None
    if new_settings:
        client.cluster.put_settings(body=new_settings)


def wipe_snapshots(client):
    """Deletes all the snapshots and repositories from the cluster"""
    in_progress_snapshots = []

    repos = client.snapshot.get_repository(repository="_all")
    for repo_name, repo in repos.items():
        if repo["type"] == "fs":
            snapshots = client.snapshot.get(
                repository=repo_name, snapshot="_all", ignore_unavailable=True
            )
            for snapshot in snapshots["snapshots"]:
                if snapshot["state"] == "IN_PROGRESS":
                    in_progress_snapshots.append(snapshot)
                else:
                    client.snapshot.delete(
                        repository=repo_name,
                        snapshot=snapshot["snapshot"],
                        ignore=404,
                    )

        client.snapshot.delete_repository(repository=repo_name, ignore=404)

    assert in_progress_snapshots == []


def wipe_data_streams(client):
    try:
        client.indices.delete_data_stream(name="*", expand_wildcards="all")
    except Exception:
        client.indices.delete_data_stream(name="*")


def wipe_indices(client):
    client.indices.delete(
        index="*,-.ds-ilm-history-*",
        expand_wildcards="all",
        ignore=404,
    )


def wipe_searchable_snapshot_indices(client):
    cluster_metadata = client.cluster.state(
        metric="metadata",
        filter_path="metadata.indices.*.settings.index.store.snapshot",
    )
    if cluster_metadata:
        for index in cluster_metadata["metadata"]["indices"].keys():
            client.indices.delete(index=index)


def wipe_slm_policies(client):
    for policy in client.slm.get_lifecycle():
        client.slm.delete_lifecycle(policy_id=policy["name"])


def wipe_auto_follow_patterns(client):
    for pattern in client.ccr.get_auto_follow_pattern()["patterns"]:
        client.ccr.delete_auto_follow_pattern(name=pattern["name"])


def wipe_node_shutdown_metadata(client):
    shutdown_status = client.shutdown.get_node()
    # If response contains these two keys the feature flag isn't enabled
    # on this cluster so skip this step now.
    if "_nodes" in shutdown_status and "cluster_name" in shutdown_status:
        return

    for shutdown_node in shutdown_status.get("nodes", []):
        node_id = shutdown_node["node_id"]
        client.shutdown.delete_node(node_id=node_id)


def wipe_tasks(client):
    tasks = client.tasks.list()
    for node_name, node in tasks.get("node", {}).items():
        for task_id in node.get("tasks", ()):
            client.tasks.cancel(task_id=task_id, wait_for_completion=True)


def wait_for_pending_tasks(client, filter, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        tasks = client.cat.tasks(detailed=True).split("\n")
        if not any(filter in task for task in tasks):
            break


def wait_for_pending_datafeeds_and_jobs(client, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if (
            client.ml.get_datafeeds(datafeed_id="*", allow_no_datafeeds=True)["count"]
            == 0
        ):
            break
    while time.time() < end_time:
        if client.ml.get_jobs(job_id="*", allow_no_jobs=True)["count"] == 0:
            break


def wait_for_cluster_state_updates_to_finish(client, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not client.cluster.pending_tasks().get("tasks", ()):
            break
