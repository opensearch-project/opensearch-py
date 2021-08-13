#!/usr/bin/env bash

# Called by entry point `run-test` use this script to add your repository specific test commands
# Once called opensearch is up and running and the following parameters are available to this script

# OPENSEARCH_VERSION -- version e.g Major.Minor.Patch(-Prelease)
# OPENSEARCH_URL -- The url at which opensearch is reachable
# network_name -- The docker network name
# NODE_NAME -- The docker container name also used as opensearch node name

# When run in CI the test-matrix is used to define additional variables
# TEST_SUITE -- defaults to `oss` in `run-tests`

set -e

echo -e "\033[34;1mINFO:\033[0m URL ${opensearch_url}\033[0m"
echo -e "\033[34;1mINFO:\033[0m VERSION ${OPENSEARCH_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m TEST_SUITE ${TEST_SUITE}\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_VERSION ${PYTHON_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_CONNECTION_CLASS ${PYTHON_CONNECTION_CLASS}\033[0m"

echo -e "\033[1m>>>>> Build [opensearch-project/opensearch-py container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

docker build \
       --file .ci/Dockerfile.client \
       --tag opensearch-project/opensearch-py \
       --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
       .

echo -e "\033[1m>>>>> Run [opensearch-project/opensearch-py container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

mkdir -p junit
docker run \
  --network=${network_name} \
  --env "STACK_VERSION=${STACK_VERSION}" \
  --env "OPENSEARCH_URL=${opensearch_url}" \
  --env "TEST_SUITE=${TEST_SUITE}" \
  --env "PYTHON_CONNECTION_CLASS=${PYTHON_CONNECTION_CLASS}" \
  --env "TEST_TYPE=server" \
  --name opensearch-py \
  --rm \
  opensearch-project/opensearch-py \
  python setup.py test
