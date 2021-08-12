FROM amazon/opendistro-for-elasticsearch:1.13.2
ARG SECURE_INTEGRATION
RUN if [ "$SECURE_INTEGRATION" != "true" ] ; then /usr/share/elasticsearch/bin/elasticsearch-plugin remove opendistro_security; fi
COPY --chown=elasticsearch:elasticsearch .ci/opendistro/elasticsearch.yml /usr/share/elasticsearch/config/
