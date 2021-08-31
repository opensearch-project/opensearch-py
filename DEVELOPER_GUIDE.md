Run the linter and test suite to ensure your changes do not break existing code:

```
# Install Nox for task management
$ python -m pip install nox

# Auto-format and lint your changes
$ nox -rs format

# Run the test suite
$ nox -rs test
```

To run the integration tests locally, run:

```
./.ci/run-tests opensearch true
```

The first argument, `opensearch` tells the server type to run integration test against. Valid values are `opensearch` and `opendistro`. The second argument tells whether to run server with security plugin enabled or not.

Note that integration tests require docker to be installed and running, and downloads quite a bit of data from over the internet and hence take few minutes to complete.
