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

## Integration Tests
To run the integration tests locally, run:

```
./.ci/run-tests opensearch true
```

The first argument, `opensearch` tells the server type to run integration test against. Valid values are `opensearch` and `opendistro`. The second argument tells whether to run server with security plugin enabled or not.

Note that integration tests require docker to be installed and running, and downloads quite a bit of data from over the internet and hence take few minutes to complete.

## Build the Documentation with Sphinx
This are the steps to build the documentation with [Sphinx](https://www.sphinx-doc.org/):

1. change into the `opensearch-py` directory where `setup.py` is located
2. install opensearch-py - we recommend [editable mode](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e
    - with bash: `pip install -e .[docs]`
    - with zsh: `pip install -e .\[docs]`
4. change into the `docs` directory
5. execute `make html`
6. use your favorite web browser to open the file called `opensearch-py/docs/build/html/index.html`
