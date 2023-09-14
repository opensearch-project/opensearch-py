- [Developer Guide](#developer-guide)
  - [Prerequisites](#prerequisites)
    - [Install Docker Image](#docker-setup)
    - [Poetry](#poetry-setup)
    - [Install Dependencies](#dependencies)
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

You can install dev requirements with `pip install -r dev-requirements.txt`, but it's better to use the docker setup described below.

Install [Nox](https://nox.thea.codes/en/stable/) for task management.

```
$ python -m pip install nox
```

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
### Poetry 

This project uses [poetry](https://python-poetry.org/docs/), a modern Python dependency management tool. Poetry provides a simplified and efficient way to manage your project's dependencies, virtual environments, and packaging. It also generates the ever-important `poetry.lock`, which is used to produce deterministic builds. Here's how to get started with Poetry:

```
$ pip install poetry

$ poetry --version
Poetry (version 1.6.1)
```

### Install Dependencies

Install dependencies.

```
$ poetry install
Installing dependencies
Resolving dependencies...

Writing lock file
```
## Running Tests

Tests require a live instance of OpenSearch running in docker.

This will start a new instance and run tests against the latest version of OpenSearch.

Run the following while on the ```./opensearch-py``` directory.

```
$ poetry run pytest
```

You can also run individual tests matching a pattern (`pytest -k [pattern]`). 

```
$ poetry run pytest test_opensearchpy/test_async/test_server/test_helpers/test_search.py
============================================ test session starts ====================================================
platform win32 -- Python 3.9.7, pytest-7.4.2, pluggy-0.13.1
configfile: setup.cfg
plugins: anyio-2.2.0, asyncio-0.21.1, cov-4.1.0
asyncio: mode=auto
collected 8 items

test_opensearchpy\test_async\test_server\test_helpers\test_search.py ........                                 [100%]
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
nox -rs format
```
