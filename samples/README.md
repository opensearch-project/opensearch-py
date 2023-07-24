# OpenSearch Python Samples

Most samples can be run using OpenSearch installed locally with docker.

```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

## Prerequisites

Install [poetry](https://python-poetry.org/docs/).

## Run Samples

```
poetry install
poetry run hello/hello.py
```
