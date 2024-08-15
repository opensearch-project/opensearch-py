FROM opensearchproject/opensearch:2.11.0

ARG OPENSEARCH_HOME=/usr/share/opensearch
ARG UID=1000
ARG GID=1000

RUN echo 'path.repo: ["/usr/share/opensearch/backups"]' >> $OPENSEARCH_HOME/config/opensearch.yml
RUN mkdir -p $OPENSEARCH_HOME/backups 
RUN chown -Rv $UID:$GID $OPENSEARCH_HOME/backups
