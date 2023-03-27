- [Developer Guide](#developer-guide)
  - [Prerequisites](#prerequisites)
  - [Running Tests](#running-tests)
  - [Linter](#linter)
  - [Documentation](#documentation)
  - [Running Python Client Generator](#running-python-client-generator)

# Developer Guide

## Prerequisites

Python 3.6 or newer is required.

```
$ python --version
Python 3.11.1
```

Install [Nox](https://nox.thea.codes/en/stable/) for task management.

```
$ python -m pip install nox
```

## Running Tests

Tests require a live instance of OpenSearch running in docker.

This will start a new instance and run tests against the latest version of OpenSearch.

```
./.ci/run-tests
```

If your OpenSearch docker instance is running, you can execute the test suite directly.

```
$ nox -rs test

```

## Install and Run Docker Image
Note that integration tests require docker to be installed and running, and downloads quite a bit of data from over the internet and hence take few minutes to complete.

Run the following commands to download and run the docker image:
```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

## Install Docker Image
Integration tests require [docker](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/).

Run the following commands to install the docker image:
```
docker pull opensearchproject/opensearch:latest

```
Integration tests will auto-start the docker image. To start it manually:
```
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest

```


To run tests against different versions of OpenSearch, use `run-tests [with/without security] [version]`:

```
./.ci/run-tests true 1.3.0
```

The first argument tells whether to run server with security plugin enabled or not. The second argument specifies the version of OpenSearch the tests should run against, if not specified, the tests run against the latest version. You can also run tests against a current SNAPSHOT.

The following example runs tests against the latest SNAPSHOT build of OpenSearch without security.

```
./.ci/run-tests opensearch false SNAPSHOT
```


## Linter

Run the linter and test suite to ensure your changes do not break existing code. The following will auto-format your changes.

```
$ nox -rs format
```

## Documentation

To build the documentation with [Sphinx](https://www.sphinx-doc.org/).

```
pip install -e .[docs]
cd docs
make html
```

Open `opensearch-py/docs/build/html/index.html` to see results.

## Running Python Client Generator

The following code executes a python client generator that updates the client by utilizing the [openapi specifications](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) found in the "opensearch-api-specification" repository. This process allows for the automatic generation and synchronization of the client code with the latest API specifications.

```
cd opensearch-py
python utils/generate-api.py
```
