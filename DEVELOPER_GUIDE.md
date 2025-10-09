- [Developer Guide](#developer-guide)
  - [Prerequisites](#prerequisites)
  - [Install Docker Image](#install-docker-image)
  - [Running Tests](#running-tests)
  - [Linter](#linter)
  - [Documentation](#documentation)
  - [Client Code Generator](#client-code-generator)

# Developer Guide

## Prerequisites

Python 3.8 or newer is required.

```
$ python --version
Python 3.11.1
```

You can install dev requirements with `pip install -r dev-requirements.txt`, but it's better to use the docker setup described below.

Install [Nox](https://nox.thea.codes/en/stable/) for task management.

```
$ python -m pip install nox
```

## Install Docker Image

Integration tests require [docker](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/).

Run the following commands to install the docker image:

```
docker pull opensearchproject/opensearch:latest
```

Integration tests will auto-start the docker image. To start it manually:

```
docker run -d -p 9200:9200 -p 9600:9600 -e OPENSEARCH_INITIAL_ADMIN_PASSWORD=myStrongPassword123! -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

## Running Tests

Tests require a live instance of OpenSearch running in docker.

Set the password for your docker instance.

```
export OPENSEARCH_PASSWORD=myStrongPassword123!
```

If you have one running.

```
python test_opensearchpy/run_tests.py
```

To run tests in a specific test file.

```
python test_opensearchpy/run_tests.py -s test_opensearchpy/test_connection/test_base_connection.py
```

If you want to auto-start one, the following will start a new instance and run tests against the latest version of OpenSearch.

```
./.ci/run-tests
```

If your OpenSearch docker instance is running, you can execute the test suite directly.

```
$ nox -rs test-3.9
```

Substitute `3.9` with your Python version above, or use `nox -rs test` to run with multiple.

To run tests against different versions of OpenSearch, use `run-tests [with/without security] [version]`:

```
./.ci/run-tests true 1.3.0
```

The first argument tells whether to run server with security plugin enabled or not. The second argument specifies the version of OpenSearch the tests should run against, if not specified, the tests run against the latest version. You can also run tests against a current SNAPSHOT.

The following example runs tests against the latest SNAPSHOT build of OpenSearch without security.

```
./.ci/run-tests opensearch false SNAPSHOT
```

You can also run individual tests matching a pattern (`pytest -k [pattern]`). 

```
./.ci/run-tests true 1.3.0 test_no_http_compression

test_opensearchpy/test_connection.py::TestUrllib3HttpConnection::test_no_http_compression PASSED [ 33%]
test_opensearchpy/test_connection.py::TestRequestsConnection::test_no_http_compression PASSED [ 66%]
test_opensearchpy/test_async/test_connection.py::TestAIOHttpConnection::test_no_http_compression PASSED [100%]
```

```
./.ci/run-tests false 2.16.0 test_indices_lifecycle
```

Note that integration tests require docker to be installed and running, and downloads quite a bit of data from the internet and hence take few minutes to complete.

## Linter

This library uses a combination of [pylint](https://github.com/pylint-dev/pylint), [black](https://github.com/psf/black), and [isort](https://github.com/PyCQA/isort) to enforce some consistency in code formatting or naming conventions. 

Run the linters to ensure your changes do not break existing conventions. 

```
$ nox -rs lint
```

Use a formatter to auto-correct some common problems.

```
$ nox -rs format
```

## Documentation

To build the documentation with [Sphinx](https://www.sphinx-doc.org/).

```
$ nox -rs docs
```

Open `docs/build/html/index.html` to see results.

## Client Code Generator

OpenSearch publishes an [OpenAPI specification](https://github.com/opensearch-project/opensearch-api-specification/releases/download/main-latest/opensearch-openapi.yaml) in the [opensearch-api-specification](https://github.com/opensearch-project/opensearch-api-specification) repository, which is used to auto-generate the less interesting parts of the client.

```
nox -rs generate
```
