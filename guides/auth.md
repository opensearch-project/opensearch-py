- [Authentication](#authentication)
  - [IAM Authentication](#iam-authentication)
  - [IAM Authentication with an Async Client](#iam-authentication-with-an-async-client)
  - [Kerberos](#kerberos)

# Authentication

OpenSearch allows you to use different methods for the authentication via `connection_class` and `http_auth` parameters.

## IAM Authentication

Opensearch-py supports IAM-based authentication via `AWSV4SignerAuth`, which uses `RequestHttpConnection` as the transport class for communicating with OpenSearch clusters running in Amazon Managed OpenSearch and OpenSearch Serverless, and works in conjunction with [botocore](https://pypi.org/project/botocore/).

```python
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3

host = '' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-west-2'
service = 'es' # 'aoss' for OpenSearch Serverless
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    pool_maxsize = 20
)

index_name = 'test-index'

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

## IAM Authentication with an Async Client

Use `AsyncOpenSearch` with the `AsyncHttpConnection` connection class and the async `AWSV4SignerAsyncAuth` signer.

```python
from opensearchpy import AsyncOpenSearch, AsyncHttpConnection, AWSV4SignerAsyncAuth
import boto3

host = '' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
region = 'us-west-2'
service = 'es' # 'aoss' for OpenSearch Serverless
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAsyncAuth(credentials, region, service)

client = AsyncOpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = AsyncHttpConnection
)

async def search():
    index_name = 'test-index'

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

    print(response)

search()
```

## Kerberos

There are several python packages that provide Kerberos support over HTTP, such as [requests-kerberos](http://pypi.org/project/requests-kerberos) and [requests-gssapi](https://pypi.org/project/requests-gssapi). The following example shows how to setup Kerberos authentication. 

Note that some of the parameters, such as `mutual_authentication` might depend on the server settings.

```python
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

client = OpenSearch(
    ['htps://...'],
    use_ssl=True,
    verify_certs=True,
    http_auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL)
)

health = client.cluster.health()
```
