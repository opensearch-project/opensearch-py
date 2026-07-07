ARG OPENSEARCH_VERSION
FROM opensearchproject/opensearch:$OPENSEARCH_VERSION

ARG opensearch_path=/usr/share/opensearch
ARG opensearch_yml=$opensearch_path/config/opensearch.yml

ARG SECURE_INTEGRATION
RUN if [ "$SECURE_INTEGRATION" != "true" ] ; then echo "plugins.security.disabled: true" >> $opensearch_yml; fi

# For secure mode, run demo installer FIRST to generate certs.
# Must happen before adding gRPC settings that trigger "already configured" detection.
ARG SECURE_INTEGRATION
RUN if [ "$SECURE_INTEGRATION" = "true" ]; then \
      OPENSEARCH_INITIAL_ADMIN_PASSWORD="myStrongPassword123!" \
      $opensearch_path/plugins/opensearch-security/tools/install_demo_configuration.sh -y -i -s; \
    fi

# Now add gRPC transport settings (after demo certs exist)
ARG OPENSEARCH_VERSION
ARG SECURE_INTEGRATION
RUN if echo "$OPENSEARCH_VERSION" | grep -qE "^3\."; then \
      if [ "$SECURE_INTEGRATION" = "true" ]; then \
        echo "aux.transport.types: [secure-transport-grpc]" >> $opensearch_yml \
        && echo "plugins.security.ssl.aux.secure-transport-grpc.enabled: true" >> $opensearch_yml \
        && echo "plugins.security.ssl.aux.secure-transport-grpc.pemcert_filepath: esnode.pem" >> $opensearch_yml \
        && echo "plugins.security.ssl.aux.secure-transport-grpc.pemkey_filepath: esnode-key.pem" >> $opensearch_yml \
        && echo "plugins.security.ssl.aux.secure-transport-grpc.pemtrustedcas_filepath: root-ca.pem" >> $opensearch_yml; \
      else \
        echo "aux.transport.types: [transport-grpc]" >> $opensearch_yml; \
      fi \
      && echo "aux.transport.transport-grpc.port: 9400-9500" >> $opensearch_yml \
      && echo "grpc.host: 0.0.0.0" >> $opensearch_yml; \
    fi
