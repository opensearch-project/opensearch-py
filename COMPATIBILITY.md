- [Compatibility with OpenSearch](#compatibility-with-opensearch)
- [Upgrading](#upgrading)

## Compatibility with OpenSearch

The below matrix shows the compatibility of the [`opensearch-py`](https://pypi.org/project/opensearch-py/) with versions of [`OpenSearch`](https://opensearch.org/downloads.html#opensearch).

| Client Version | OpenSearch Version | Notes |
| --- | --- | --- |
| 1.0.0 | 1.0.0-1.2.4 | |
| 1.1.0 | 1.3.0-1.3.7 | |
| 2.0.x | 1.0.0-2.10.0 | client works against Opensearch Version 1.x as long as features removed in 2.0 are not used |
| 2.1.x | 1.0.0-2.10.0 | client works against Opensearch Version 1.x as long as features removed in 2.0 are not used |
| 2.2.0 | 1.0.0-2.10.0 | client works against Opensearch Version 1.x as long as features removed in 2.0 are not used |
| 2.3.0 | 1.0.0-2.10.0 | client works against Opensearch Version 1.x as long as features removed in 2.0 are not used |
| 2.3.1 | 1.0.0-2.10.0 | client works against Opensearch Version 1.x as long as features removed in 2.0 are not used |
| 2.3.2 | 1.0.0-2.10.0 | client works against Opensearch Version 1.x as long as features removed in 2.0 are not used |

## Upgrading

Major versions of OpenSearch introduce breaking changes that require careful upgrades of the client. While `opensearch-py-client` 2.0.0 works against the latest OpenSearch 1.x, certain deprecated features removed in OpenSearch 2.0 have also been removed from the client. Please refer to the [OpenSearch documentation](https://opensearch.org/docs/latest/clients/index/) for more information.
