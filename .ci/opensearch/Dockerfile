ARG OPENSEARCH_VERSION
FROM opensearchproject/opensearch:$OPENSEARCH_VERSION

ARG opensearch_path=/usr/share/opensearch
ARG opensearch_yml=$opensearch_path/config/opensearch.yml

ARG SECURE_INTEGRATION
RUN if [ "$SECURE_INTEGRATION" != "true" ] ; then echo "plugins.security.disabled: true" >> $opensearch_yml; fi

RUN echo "aux.transport.types: [transport-grpc]" >> $opensearch_yml \
 && echo "aux.transport.transport-grpc.port: 9400" >> $opensearch_yml \
 && echo "grpc.host: 0.0.0.0" >> $opensearch_yml
