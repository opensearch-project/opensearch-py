- [User guide of OpenSearch Python client](#user-guide-of-opensearch-python-client)
  - [Setup](#setup)
  - [Example](#example)
    - [Creating a client](#creating-a-client)
    - [Creating an index](#creating-an-index)
    - [Adding a document to an index](#adding-a-document-to-an-index)
    - [Adding documents in bulk](#adding-documents-in-bulk)
    - [Adding documents in bulk using helper functions](#adding-documents-in-bulk-using-helper-functions)
    - [Searching for a document](#searching-for-a-document)
    - [Deleting a document](#deleting-a-document)
    - [Deleting an index](#deleting-an-index)
  - [Making API calls](#making-api-calls)
    - [Point in time API](#point-in-time-api)
  - [Using DSL features from opensearch-dsl-py](#using-dsl-features-from-opensearch-dsl-py)
    - [Searching for documents with filters](#searching-for-documents-with-filters)
  - [Using plugins](#using-plugins)
    - [Alerting plugin](#alerting-plugin)
      - [**Searching for monitors**](#searching-for-monitors)
      - [**Getting a monitor**](#getting-a-monitor)
      - [**Creating a monitor**](#creating-a-monitor)
      - [**Creating a destination**](#creating-a-destination)
      - [**Getting alerts**](#getting-alerts)
      - [**Acknowledge alerts**](#acknowledge-alerts)
    - [Index management plugin](#index-management-plugin)
      - [Creating a policy](#creating-a-policy)
      - [Getting a policy](#getting-a-policy)
      - [Deleting a policy](#deleting-a-policy)
    - [Security plugin](#security-plugin)
      - [Creating a role](#creating-a-role)
      - [Getting a role](#getting-a-role)
      - [Creating a user](#creating-a-user)
      - [Getting a user](#getting-a-user)
  - [Using different authentication methods](#using-different-authentication-methods)
    - [Using IAM credentials](#using-iam-credentials)
      - [Pre-requisites to use `AWSV4SignerAuth`](#pre-requisites-to-use-awsv4signerauth)
  - [Using IAM authentication with an async client](#using-iam-authentication-with-an-async-client)
    - [Using Kerberos](#using-kerberos)
  - [Using environment settings for proxy configuration](#using-environment-settings-for-proxy-configuration)

# User guide of OpenSearch Python client

## Setup

To add the client to your project, install it using [pip](https://pip.pypa.io/):

```bash
pip install opensearch-py
```

Then import it like any other module:

```python
from opensearchpy import OpenSearch
```

To add the async client to your project, install it using [pip](https://pip.pypa.io/):

```bash
pip install opensearch-py[async]
```

If you prefer to add the client manually or just want to examine the source code, see [opensearch-py on GitHub](https://github.com/opensearch-project/opensearch-py).


## Example
In the example given below, we create a client, an index with non-default settings, insert a 
document in the index, search for the document, delete the document and finally delete the index.

### Creating a client

```python
from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

# Provide a CA bundle if you use intermediate CAs with your root CA.
# If this is not given, the CA bundle is is discovered from the first available
# following options:
# - OpenSSL environment variables SSL_CERT_FILE and SSL_CERT_DIR
# - certifi bundle (https://pypi.org/project/certifi/)
# - default behavior of the connection backend (most likely system certs)
ca_certs_path = '/full/path/to/root-ca.pem'

# Optional client certificates if you don't want to use HTTP basic authentication.
# client_cert_path = '/full/path/to/client.pem'
# client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path
)
```

### Creating an index
```python
# Create an index with non-default settings.
index_name = 'python-test-index3'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index_name, body=index_body)
print('\nCreating index:')
print(response)
```

### Adding a document to an index
```python
document = {
  'title': 'Moneyball',
  'director': 'Bennett Miller',
  'year': '2011'
}
id = '1'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print('\nAdding document:')
print(response)
```

### Adding documents in bulk
```python
docs = '''{"index": {"_index": "index-2022-06-08", "_id": "1"}}
{"name": "foo"} 
{"index": {"_index": "index-2022-06-09", "_id": "2"}}
{"name": "bar"}
{"index": {"_index": "index-2022-06-10", "_id": "3"}}
{"name": "baz"}'''

response = client.bulk(docs)

print('\nAdding bulk documents:')
print(response)
```

### Adding documents in bulk using helper functions
```python
docs = []
def generate_data():
    mywords = ['foo', 'bar', 'baz']
    for index, word in enumerate(mywords):
        docs.append({
            "_index": "mywords",
            "word": word,
            "_id": index
        })
    return docs

response = helpers.bulk(client, generate_data(), max_retries=3)

print('\nAdding bulk documents using helper:')
print(response)
```

### Searching for a document
```python
q = 'miller'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

response = client.search(
    body = query,
    index = index_name
)
print('\nSearch results:')
print(response)
```

### Deleting a document
```python
response = client.delete(
    index = index_name,
    id = id
)

print('\nDeleting document:')
print(response)
```

### Deleting an index
```python
response = client.indices.delete(
    index = index_name
)

print('\nDeleting index:')
print(response)
```
## Making API calls

### Point in time API

```python
# create a point in time on a index
index_name = "test-index"
response = client.create_point_in_time(index=index_name,
                                       keep_alive="1m")

pit_id = response.get("pit_id")
print('\n Point in time ID:')
print(pit_id)

# To list all point in time which are alive in the cluster
response = client.list_all_point_in_time()
print('\n List of all Point in Time:')
print(response)

# To delete point in time
pit_body = {
    "pit_id": [pit_id]
}

# To delete all point in time 
# client.delete_point_in_time(body=None, all=True)
response = client.delete_point_in_time(body=pit_body)

print('\n The deleted point in time:')
print(response)
```

## Using DSL features from opensearch-dsl-py
opensearch-dsl-py client is now merged into the opensearch-py client. Thus, opensearch-py supports creating and indexing documents, searching with and without filters, and updating documents using queries. See [opensearch-dsl-py client documentation](https://opensearch.org/docs/latest/clients/python-high-level/) for details.

All the APIs newly added from opensearch-dsl-py are listed in [docs](https://github.com/opensearch-project/opensearch-py/tree/main/docs/source/api-ref). 

In the below example, [Search API](https://github.com/opensearch-project/opensearch-py/blob/main/opensearchpy/helpers/search.py) from opensearch-dsl-py client is used. 

### Searching for documents with filters

```python
from opensearchpy import OpenSearch, Search

    # Use the above mentioned examples for creating client. 
    # Then,create an index
    # Add a document to the index.

    # Search for the document.
    s = Search(using=client, index=index_name) \
        .filter("term", category="search") \
        .query("match", title="python")

    response = s.execute()

    print('\nSearch results:')
    for hit in response:
        print(hit.meta.score, hit.title)

    # Delete the document.
    # Delete the index.
```

## Using plugins

Plugin client definitions can be found here -- 

### Alerting plugin

#### **Searching for monitors**
[API definition](https://opensearch.org/docs/latest/monitoring-plugins/alerting/api/#search-monitors)
```python
print('\Searching for monitors:')

query = {
  "query": {
    "match" : {
      "monitor.name": "test-monitor"
    }
  }
}

response = client.plugins.alerting.search_monitor(query)
print(response)
```

#### **Getting a monitor**
[API definition](https://opensearch.org/docs/latest/monitoring-plugins/alerting/api/#get-monitor)
```python
print('\Getting a monitor:')

response = client.plugins.alerting.get_monitor("monitorID")
print(response)
```

#### **Creating a monitor**
[API definition](https://opensearch.org/docs/latest/monitoring-plugins/alerting/api/#create-a-bucket-level-monitor)
```python
print('\Creating a bucket level monitor:')

query = {
  "type": "monitor",
  "name": "Demo bucket-level monitor",
  "monitor_type": "bucket_level_monitor",
  "enabled": True,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "search": {
        "indices": [
          "python-test-index3"
        ],
        "query": {
          "size": 0,
          "query": {
            "bool": {
              "filter": [
                {
                  "range": {
                    "order_date": {
                      "from": "||-1h",
                      "to": "",
                      "include_lower": True,
                      "include_upper": True,
                      "format": "epoch_millis"
                    }
                  }
                }
              ]
            }
          },
          "aggregations": {
            "composite_agg": {
              "composite": {
                "sources": [
                  {
                    "user": {
                      "terms": {
                        "field": "user"
                      }
                    }
                  }
                ]
              },
              "aggregations": {
                "avg_products_base_price": {
                  "avg": {
                    "field": "products.base_price"
                  }
                }
              }
            }
          }
        }
      }
    }
  ],
}

response = client.plugins.alerting.create_monitor(query)
print(response)
```

#### **Creating a destination**
[API definition](https://opensearch.org/docs/latest/monitoring-plugins/alerting/api/#create-destination)
```python
print('\Creating an email destination:')

query = {
  "type": "email",
  "name": "my-email-destination",
  "email": {
    "email_account_id": "YjY7mXMBx015759_IcfW",
    "recipients": [
      {
        "type": "email_group",
        "email_group_id": "YzY-mXMBx015759_dscs"
      },
      {
        "type": "email",
        "email": "example@email.com"
      }
    ]
  }
}

response = client.plugins.alerting.create_destination(query)
print(response)
```

#### **Getting alerts**
[API definition](https://opensearch.org/docs/latest/monitoring-plugins/alerting/api/#get-alerts)
```python
print('\Getting alerts:')

response = client.plugins.alerting.get_alerts()
print(response)
```

#### **Acknowledge alerts**
[API definition](https://opensearch.org/docs/latest/monitoring-plugins/alerting/api/#acknowledge-alert)
```python
print('\Acknowledge alerts:')

query = {
  "alerts": ["eQURa3gBKo1jAh6qUo49"]
}

response = client.plugins.alerting.acknowledge_alert(query)
print(response)
```

### Index management plugin

#### Creating a policy
[API definition](https://opensearch.org/docs/latest/im-plugin/ism/api/#create-policy)
```python
print('\Creating a policy:')

policy_name = "test-policy"
policy_content = {
    "policy": {
        "description": "hot warm delete workflow",
        "default_state": "hot",
        "schema_version": 1,
        "states": [
            {
                "name": "hot",
                "actions": [{"rollover": {"min_index_age": "1d"}}],
                "transitions": [{"state_name": "warm"}],
            },
            {
                "name": "warm",
                "actions": [{"replica_count": {"number_of_replicas": 5}}],
                "transitions": [{"state_name": "delete", "conditions": {"min_index_age": "30d"}}],
            },
            {
                "name": "delete",
                "actions": [
                    {
                        "notification": {
                            "destination": {"chime": {"url": "<URL>"}},
                            "message_template": {"source": "The index {{ctx.index}} is being deleted"},
                        }
                    },
                    {"delete": {}},
                ],
            },
        ],
        "ism_template": {"index_patterns": ["log*"], "priority": 100},
    }
}

response = client.index_managment.put_policy(policy_name, body=policy_content)
print(response)
```

#### Getting a policy
[API definition](https://opensearch.org/docs/latest/im-plugin/ism/api/#get-policy)
```python
print('\Getting a policy:')

policy_name = "test-policy"

response = client.index_managment.get_policy(policy_name)
print(response)
```

#### Deleting a policy
[API definition](https://opensearch.org/docs/latest/index_managment/access-control/api/#create-user)
```python
print('\Deleting a policy:')

policy_name = "test-policy"

response = client.index_managment.delete_policy(policy_name)
print(response)
```

### Security plugin

#### Creating a role
[API definition](https://opensearch.org/docs/latest/security/access-control/api/#create-role)
```python
print('\Creating a role:')

role_name = "test-role"
role_content = {
  "cluster_permissions": ["cluster_monitor"],
  "index_permissions": [
      {
          "index_patterns": ["index", "test-*"],
          "allowed_actions": [
              "data_access",
              "indices_monitor",
          ],
      }
  ],
}

response = client.security.put_role(role_name, body=role_content)
print(response)
```

#### Getting a role
[API definition](https://opensearch.org/docs/latest/security/access-control/api/#get-role)
```python
print('\Getting a role:')

role_name = "test-role"

response = client.security.get_role(role_name)
print(response)
```

#### Creating a user
[API definition](https://opensearch.org/docs/latest/security/access-control/api/#create-user)
```python
print('\Creating a user:')

user_name = "test-user"
user_content = {"password": "test_password", "opendistro_security_roles": []}

response = client.security.put_role(user_name, body=user_content)
print(response)
```

#### Getting a user
[API definition](https://opensearch.org/docs/latest/security/access-control/api/#get-user)
```python
print('\Getting a user:')

user_name = "test-user"

response = client.security.get_user(user_name)
print(response)
```

## Using different authentication methods

It is possible to use different methods for the authentication to OpenSearch. The parameters of `connection_class` and `http_auth` can be used for this. The following examples show how to authenticate using IAM credentials and using Kerberos.

### Using IAM credentials

Refer the AWS documentation regarding usage of IAM credentials to sign requests to OpenSearch APIs - [Signing HTTP requests to Amazon OpenSearch Service.](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/request-signing.html#request-signing-python)

Opensearch-py client library also provides an in-house IAM based authentication feature, `AWSV4SignerAuth` that will help users to connect to their opensearch clusters by making use of IAM roles.

`AWSV4SignerAuth` uses RequestHttpConnection as transport class for communication with opensearch clusters. Opensearch-py client library provides `pool_maxsize` option to modify default connection-pool size.

#### Pre-requisites to use `AWSV4SignerAuth`
 - Python version 3.6 or above,
 - Install [botocore](https://pypi.org/project/botocore/) using pip

   `pip install botocore`

Here is the sample code that uses `AWSV4SignerAuth` -

```python
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3

host = '' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-west-2'
service = 'es' # 'aoss' for OpenSearch Serverless
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)
index_name = 'python-test-index3'

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    pool_maxsize = 20
)

q = 'miller'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

response = client.search(
    body = query,
    index = index_name
)

print('\nSearch results:')
print(response)
```

## Using IAM authentication with an async client

Make sure to use `AsyncOpenSearch` with the `AsyncHttpConnection` connection class with the async `AWSV4SignerAsyncAuth` signer.

- Requires opensearch-py[async]


Here is the sample code that uses `AWSV4SignerAsyncAuth` -

```python
from opensearchpy import AsyncOpenSearch, AsyncHttpConnection, AWSV4SignerAsyncAuth
import boto3

host = '' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-west-2'
service = 'es' # 'aoss' for OpenSearch Serverless
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAsyncAuth(credentials, region, service)
index_name = 'python-test-index3'

client = AsyncOpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = AsyncHttpConnection
)

async def search():
  q = 'miller'
  query = {
    'size': 5,
    'query': {
      'multi_match': {
        'query': q,
        'fields': ['title^2', 'director']
      }
    }
  }

  response = await client.search(
      body = query,
      index = index_name
  )

  print('\nSearch results:')
  print(response)

search()
```

### Using Kerberos

There are several python packages that provide Kerberos support over HTTP connections, such as [requests-kerberos](http://pypi.org/project/requests-kerberos) and [requests-gssapi](https://pypi.org/project/requests-gssapi). The following example shows how to setup the authentication. Note that some of the parameters, such as `mutual_authentication` might depend on the server settings.

```python

from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

client = OpenSearch(
    ['htps://...'],
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    http_auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL)
)

health = client.cluster.health()
```

## Using environment settings for proxy configuration

Tell connection to get proxy information from `HTTP_PROXY` / `HTTPS_PROXY` environment variables or `~/.netrc` file if present.

```python
from opensearchpy import OpenSearch, RequestsHttpConnection


OpenSearch(
    hosts=["htps://..."],
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    trust_env=True,
)
```


```python
from opensearchpy import AsyncOpenSearch, AIOHttpConnection

client = AsyncOpenSearch(
    hosts=["htps://..."],
    use_ssl=True,
    verify_certs=True,
    connection_class=AIOHttpConnection,
    trust_env=True,
)
```
