![OpenSearch logo](OpenSearch.svg)

OpenSearch Python Client

- [Welcome!](#welcome)
- [Project Resources](#project-resources)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Copyright](#copyright)

## Welcome!

**opensearch-py** is [a community-driven, open source fork](https://aws.amazon.com/blogs/opensource/introducing-opensearch/) of elasticsearch-py licensed under the [Apache v2.0 License](LICENSE.txt). For more information, see [opensearch.org](https://opensearch.org/).

## Example use

```python

>>> from datetime import datetime
>>> from opensearch import OpenSearch

# by default we connect to localhost:9200
>>> client = OpenSearch()

# create an index in OpenSearch, ignore status code 400 (index already exists)
>>> client.indices.create(index='my-index', ignore=400)
{'acknowledged': True, 'shards_acknowledged': True, 'index': 'my-index'}

# datetimes will be serialized
>>> client.index(index="my-index", id=42, body={"any": "data", "timestamp": datetime.now()})
{'_index': 'my-index',
    '_type': '_doc',
    '_id': '42',
    '_version': 1,
    'result': 'created',
    '_shards': {'total': 2, 'successful': 1, 'failed': 0},
    '_seq_no': 0,
    '_primary_term': 1}

# but not deserialized
>>> client.get(index="my-index", id=42)['_source']
{'any': 'data', 'timestamp': '2019-05-17T17:28:10.329598'}

```


## Project Resources

* [Project Website](https://opensearch.org/)
* [Downloads](https://opensearch.org/downloads.html)
* [Documentation](https://opensearch.org/docs/)
* Need help? Try [Forums](https://discuss.opendistrocommunity.dev/)
* [Project Principles](https://opensearch.org/#principles)
* [Contributing to OpenSearch](CONTRIBUTING.md)
* [Maintainer Responsibilities](MAINTAINERS.md)
* [Release Management](RELEASING.md)
* [Admin Responsibilities](ADMINS.md)
* [Security](SECURITY.md)

## Code of Conduct

This project has adopted the [Amazon Open Source Code of Conduct](CODE_OF_CONDUCT.md). For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq), or contact [opensource-codeofconduct@amazon.com](mailto:opensource-codeofconduct@amazon.com) with any additional questions or comments.

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright OpenSearch Contributors. See [NOTICE](NOTICE.txt) for details.
