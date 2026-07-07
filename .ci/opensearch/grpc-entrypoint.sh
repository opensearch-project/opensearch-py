#!/bin/bash
# Wrapper entrypoint for gRPC TLS support in CI.
#
# Problem: The demo installer checks for "plugins.security" in opensearch.yml.
# If found, it says "already configured" and skips cert generation.
# We need gRPC TLS settings (plugins.security.ssl.aux.*) but they must be added
# AFTER the demo installer runs.
#
# Solution: Start a background watcher that adds gRPC TLS settings once the
# demo installer has created cert files, then call the original entrypoint.
# The original entrypoint runs the demo installer then starts OpenSearch.
# OpenSearch takes ~15-20s to start, giving the watcher time to patch the config.

OPENSEARCH_YML="/usr/share/opensearch/config/opensearch.yml"

if [ -f /tmp/.grpc_secure ]; then
  (
    # Wait for demo installer to generate certs
    for i in $(seq 1 60); do
      if [ -f /usr/share/opensearch/config/esnode.pem ]; then
        # Certs exist - add gRPC TLS settings
        if ! grep -q "plugins.security.ssl.aux.secure-transport-grpc.enabled" "$OPENSEARCH_YML"; then
          echo "plugins.security.ssl.aux.secure-transport-grpc.enabled: true" >> "$OPENSEARCH_YML"
          echo "plugins.security.ssl.aux.secure-transport-grpc.pemcert_filepath: esnode.pem" >> "$OPENSEARCH_YML"
          echo "plugins.security.ssl.aux.secure-transport-grpc.pemkey_filepath: esnode-key.pem" >> "$OPENSEARCH_YML"
          echo "plugins.security.ssl.aux.secure-transport-grpc.pemtrustedcas_filepath: root-ca.pem" >> "$OPENSEARCH_YML"
        fi
        break
      fi
      sleep 0.5
    done
  ) &
fi

exec /usr/share/opensearch/opensearch-docker-entrypoint.sh "$@"
