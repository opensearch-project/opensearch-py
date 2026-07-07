#!/bin/bash
# Wrapper entrypoint for gRPC TLS support in CI.
# Appends gRPC TLS cert settings to opensearch.yml, then delegates
# to the original entrypoint which runs the demo installer + starts OpenSearch.
#
# This works because the demo installer checks for "plugins.security" patterns
# but our aux settings don't trigger that check. The demo installer will still
# run, create certs, and THEN OpenSearch starts with the full config.

OPENSEARCH_YML="/usr/share/opensearch/config/opensearch.yml"

# Only add gRPC TLS settings if the marker file exists (set during docker build for 3.x secure)
if [ -f /tmp/.grpc_secure ]; then
  if ! grep -q "plugins.security.ssl.aux.secure-transport-grpc.enabled" "$OPENSEARCH_YML"; then
    echo "plugins.security.ssl.aux.secure-transport-grpc.enabled: true" >> "$OPENSEARCH_YML"
    echo "plugins.security.ssl.aux.secure-transport-grpc.pemcert_filepath: esnode.pem" >> "$OPENSEARCH_YML"
    echo "plugins.security.ssl.aux.secure-transport-grpc.pemkey_filepath: esnode-key.pem" >> "$OPENSEARCH_YML"
    echo "plugins.security.ssl.aux.secure-transport-grpc.pemtrustedcas_filepath: root-ca.pem" >> "$OPENSEARCH_YML"
  fi
fi

# Delegate to the original OpenSearch Docker entrypoint
exec /usr/share/opensearch/opensearch-docker-entrypoint.sh "$@"
