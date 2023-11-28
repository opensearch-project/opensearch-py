## AWS SigV4 Samples

Create an OpenSearch domain in (AWS) which support IAM based AuthN/AuthZ.

```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=
export AWS_REGION=us-west-2

export SERVICE=es # use "aoss" for OpenSearch Serverless.
export ENDPOINT=https://....us-west-2.es.amazonaws.com

poetry run aws/search_urllib.py
```

This will output the version of OpenSearch and a search result.

```
opensearch: 2.3.0
{'director': 'Bennett Miller', 'title': 'Moneyball', 'year': 2011}
```
