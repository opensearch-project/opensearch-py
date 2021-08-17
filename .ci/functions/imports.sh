#!/usr/bin/env bash
#
# Sets up all the common variables and imports relevant functions
#
# Version 1.0.1
# - Initial version after refactor

if [[ -z $opensearch_node_name ]]; then
  # only set these once
  set -euo pipefail
  export TEST_SUITE=${TEST_SUITE-oss}
  export RUNSCRIPTS=${RUNSCRIPTS-}
  export DETACH=${DETACH-false}
  export CLEANUP=${CLEANUP-false}
  export OPENSEARCH_URL_EXTENSION=${OPENSEARCH_URL_EXTENSION-http}

  export opensearch_node_name=instance
  export opensearch_image=opensearchproject/opensearch
  if [[ "$CLUSTER" == "opendistro" ]]; then
    export opensearch_image=amazon/opendistro-for-elasticsearch
  fi

  export opensearch_url=$OPENSEARCH_URL_EXTENSION://${opensearch_node_name}:9200
  export external_opensearch_url=${opensearch_url/$opensearch_node_name/localhost}

  export network_name=search-rest-test

  export ssl_cert="${script_path}/certs/testnode.crt"
  export ssl_key="${script_path}/certs/testnode.key"
  export ssl_ca="${script_path}/certs/ca.crt"

fi

  export script_path=$(dirname $(realpath -s $0))
  source $script_path/functions/cleanup.sh
  source $script_path/functions/wait-for-container.sh
  trap "cleanup_trap ${network_name}" EXIT


if [[ "$CLEANUP" == "true" ]]; then
  cleanup_all_in_network $network_name
  exit 0
fi

echo -e "\033[34;1mINFO:\033[0m Creating network $network_name if it does not exist already \033[0m"
docker network inspect "$network_name" > /dev/null 2>&1 || docker network create "$network_name"
