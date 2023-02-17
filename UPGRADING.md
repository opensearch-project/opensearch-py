- [Upgrading OpenSearch Python Client](#upgrading-opensearch-python-client)
  - [Upgrading to >= 2.2.0](#upgrading-to->=-2.2.0)
    - [Features from High-Level Python Client](#features-from-high-level-python-client)
    - [API Implementation differences for existing opensearch-dsl-py users](#api-implementation-differences-for-existing-opensearch-dsl-py-users)


# Upgrading OpenSearch Python Client

## Upgrading to >= 2.2.0

opensearch-py now includes [opensearch-dsl-py](https://pypi.org/project/opensearch-dsl/) features. opensearch-dsl-py was merged into opensearch-py preserving backwards compatibility with the previous opensearch-py version. (Refer [link](https://github.com/opensearch-project/opensearch-py/pull/287))


### Features from High-Level Python Client

opensearch-py functionalities that already exist are not altered. 

The opensearchpy [helpers](https://github.com/opensearch-project/opensearch-py/tree/main/opensearchpy/helpers) module now provides access to aggs, analysis, document, faceted search, field, function, index, mapping, query, search, update by query, utils, and wrappers. As a result, without importing opensearch-dsl-py, these functionalities can be imported directly from opensearch-py. 


### API Implementation differences for existing opensearch-dsl-py users 

The functionalities from opensearch-dsl-py are merged into this client. Refer to the [USER_GUIDE](https://github.com/opensearch-project/opensearch-py/blob/main/USER_GUIDE.md#using-high-level-python-client) for an example on how to implement a feature from the previously known high level Python client.

