# OpenSearch Python Samples

Most samples can be run using OpenSearch installed locally with Docker.

## Admin User Password

Add the default `admin` password to the environment.

```
export OPENSEARCH_PASSWORD=myStrongPassword123!
```

## Start the Container

```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e OPENSEARCH_INITIAL_ADMIN_PASSWORD=$OPENSEARCH_PASSWORD -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

## Install Python Prerequisites

Install [poetry](https://python-poetry.org/docs/).

## Run Samples

```
poetry install
poetry run python hello/hello.py
```
