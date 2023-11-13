- [Developer Guide](#developer-guide)
  - [Prerequisites](#prerequisites)
  - [Install Docker Image](#install-docker-image)
  - [Running Tests](#running-tests)
  - [Linter](#linter)
  - [Documentation](#documentation)
  - [Client Code Generator](#client-code-generator)

# Developer Guide

## Forking and Cloning

Fork this repository on GitHub, and clone locally with `git clone`.


## Building

### Install Pyenv

Use pyenv to manage multiple versions of Python. This can be installed with [pyenv-installer](https://github.com/pyenv/pyenv-installer) on Linux and MacOS, and [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation) on Windows.

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

### Install Python 3.6 or Newer

Python projects in this repository use at a minimum Python 3.6, but 3.9 is recommended for development. See the [Python Beginners Guide](https://wiki.python.org/moin/BeginnersGuide) if you have never worked with the language.

```
$ python --version
Python 3.9.16
```

If you are using pyenv.

```
pyenv install 3.9
pyenv global 3.9
```

### Install Poetry

This project uses [poetry](https://python-poetry.org/), which is typically installed with `curl -sSL https://install.python-poetry.org | python3 -`. Poetry automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your `pyproject.toml` as you install/uninstall packages. It also generates the ever-important `poetry.lock`, which is used to produce deterministic builds.

```
$ python -m pip install poetry

$ poetry --version
Poetry (version 1.5.1)
```

### Install Dependencies

```
poetry install
```

## Testing

### Install Docker Image

Integration tests require [docker](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/).

Run the following commands to install the docker image:

```
docker pull opensearchproject/opensearch:latest
```

Integration tests will auto-start the docker image. To start it manually:

```
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

### Run Tests

Run tests and ensure they pass.

```
poetry run pytest -v
```

Warnings such as `urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)` are expected.

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

Note that integration tests require docker to be installed and running, and downloads quite a bit of data from over the internet and hence take few minutes to complete.

## Linter

Run the linter and test suite to ensure your changes do not break existing code. The following will auto-format your changes.

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

OpenSearch publishes an [OpenAPI specification](https://github.com/opensearch-project/opensearch-api-specification/blob/main/OpenSearch.openapi.json) in the [opensearch-api-specification](https://github.com/opensearch-project/opensearch-api-specification) repository, which is used to auto-generate the less interesting parts of the client.

```
nox -rs generate
```
