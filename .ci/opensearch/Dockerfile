ARG OPENSEARCH_VERSION
FROM opensearchproject/opensearch:$OPENSEARCH_VERSION

ARG opensearch_path=/usr/share/opensearch
ARG opensearch_yml=$opensearch_path/config/opensearch.yml

ARG SECURE_INTEGRATION
RUN if [ "$SECURE_INTEGRATION" != "true" ] ; then echo "plugins.security.disabled: true" >> $opensearch_yml; fi

ARG OPENSEARCH_VERSION
RUN if echo "$OPENSEARCH_VERSION" | grep -qE "^3\."; then \
      if [ "$SECURE_INTEGRATION" = "true" ]; then \
        echo "aux.transport.types: [secure-transport-grpc]" >> $opensearch_yml; \
      else \
        echo "aux.transport.types: [transport-grpc]" >> $opensearch_yml; \
      fi \
      && echo "aux.transport.transport-grpc.port: 9400-9500" >> $opensearch_yml \
      && echo "grpc.host: 0.0.0.0" >> $opensearch_yml; \
    fi
