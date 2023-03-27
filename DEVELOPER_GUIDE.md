- [Developer Guide](#developer-guide)
  - [Linter and Test Suite](#linter-and-test-suite)
  - [Integration Tests](#integration-tests)
  - [Build the Documentation with Sphinx](#build-the-documentation-with-sphinx)

# Developer Guide

## Linter and Test Suite 
Run the linter and test suite to ensure your changes do not break existing code:

```
# Install Nox for task management
$ python -m pip install nox

# Auto-format and lint your changes
$ nox -rs format

# Run the test suite
$ nox -rs test

```

## Install and Run Docker Image
Note that integration tests require docker to be installed and running, and downloads quite a bit of data from over the internet and hence take few minutes to complete.

Run the following commands to download and run the docker image:
```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

## Integration Tests
To run the integration tests locally, run:

```
./.ci/run-tests true 1.3.0
```

The first argument tells whether to run server with security plugin enabled or not.
The second argument specifies the version of OpenSearch the tests should run against, if not specified, the tests run against the latest version. 


## Build the Documentation with Sphinx
This are the steps to build the documentation with [Sphinx](https://www.sphinx-doc.org/):

1. change into the `opensearch-py` directory where `setup.py` is located
2. install opensearch-py - we recommend [editable mode](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e
    - with bash: `pip install -e .[docs]`
    - with zsh: `pip install -e .\[docs]`
4. change into the `docs` directory
5. execute `make html`
6. use your favorite web browser to open the file called `opensearch-py/docs/build/html/index.html`
