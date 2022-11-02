- [Getting Started with the OpenSearch Python Client](#getting-started-with-the-opensearch-python-client)
  - [Setup](#setup)
  - [Sample code](#sample-code)
    - [Creating a client](#creating-a-client)
    - [Creating an index](#creating-an-index)
    - [Adding a document to an index](#adding-a-document-to-an-index)
    - [Adding documents in bulk](#adding-documents-in-bulk)
    - [Adding documents in bulk using helper functions](#adding-documents-in-bulk-using-helper-functions)
    - [Searching for a document](#searching-for-a-document)
    - [Deleting a document](#deleting-a-document)
    - [Deleting an index](#deleting-an-index)
  - [Making API Calls](#making-api-calls)
    - [Point in Time API](#point-in-time-api-calls)
  - [Using plugins](#using-plugins)
    - [Alerting plugin](#alerting-plugin)
      - [**Searching for monitors**](#searching-for-monitors)
      - [**Getting a monitor**](#getting-a-monitor)
      - [**Creating a monitor**](#creating-a-monitor)
      - [**Creating a destination**](#creating-a-destination)
      - [**Getting alerts**](#getting-alerts)
      - [**Acknowledge alerts**](#acknowledge-alerts)
  - [Using IAM credentials for authentication](#using-iam-credentials-for-authentication)
      - [Pre-requisites to use `AWSV4SignerAuth`](#pre-requisites-to-use-awsv4signerauth)

# User guide of OpenSearch Python Client

## Setup

To add the client to your project, install it using [pip](https://pip.pypa.io/):

```bash
pip install opensearch-py
```

Then import it like any other module:

```python
from opensearchpy import OpenSearch
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
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

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
docs = '{"index": {"_index": "index-2022-06-08", "_id": "1"}} \n 
{"name": "foo"} \n 
{"index": {"_index": "index-2022-06-09", "_id": "2"}} \n 
{"name": "bar"} \n 
{"index": {"_index": "index-2022-06-10", "_id": "3"}} \n 
{"name": "baz"}'

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
## Making API Calls

### Point in Time API

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
## Using IAM credentials for authentication

Refer the AWS documentation regarding usage of IAM credentials to sign requests to OpenSearch APIs - [Signing HTTP requests to Amazon OpenSearch Service.](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/request-signing.html#request-signing-python)

Opensearch-py client library also provides an in-house IAM based authentication feature, `AWSV4SignerAuth` that will help users to connect to their opensearch clusters by making use of IAM roles.

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
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region)
index_name = 'python-test-index3'

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
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