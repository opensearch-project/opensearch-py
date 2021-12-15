ARG OPENSEARCH_VERSION=1.0.0
FROM opensearchproject/opensearch:$OPENSEARCH_VERSION

ARG opensearch_path=/usr/share/opensearch
ARG opensearch_yml=$opensearch_path/config/opensearch.yml

ARG SECURE_INTEGRATION
RUN if [ "$SECURE_INTEGRATION" != "true" ] ; then echo "plugins.security.disabled: true" >> $opensearch_yml; fi

COPY --chown=opensearch:opensearch .ci/opensearch/opensearch-run.sh $opensearch_path/

CMD /usr/share/opensearch/opensearch-run.sh
