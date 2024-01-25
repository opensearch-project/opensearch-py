# CHANGELOG
Inspired from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
- Added pylint `unspecified-encoding` and `missing-function-docstring` and ignored opensearchpy for lints (([#643](https://github.com/opensearch-project/opensearch-py/pull/643)))
- Added pylint `line-too-long` and `invalid-name` ([#590](https://github.com/opensearch-project/opensearch-py/pull/590))
- Added pylint `pointless-statement` ([#611](https://github.com/opensearch-project/opensearch-py/pull/611))
- Added a log collection guide ([#579](https://github.com/opensearch-project/opensearch-py/pull/579))
- Added GHA release ([#614](https://github.com/opensearch-project/opensearch-py/pull/614))
- Incorporated API generation into CI workflow and fixed 'generate' nox session ([#660](https://github.com/opensearch-project/opensearch-py/pull/660))
### Changed
- Updated the `get_policy` API in the index_management plugin to allow the policy_id argument as optional ([#633](https://github.com/opensearch-project/opensearch-py/pull/633))
- Updated the `point_in_time.md` guide with examples demonstrating the usage of the new APIs as alternatives to the deprecated ones. ([#661](https://github.com/opensearch-project/opensearch-py/pull/661))
### Deprecated
### Removed
- Removed unnecessary `# -*- coding: utf-8 -*-` headers from .py files ([#615](https://github.com/opensearch-project/opensearch-py/pull/615), [#617](https://github.com/opensearch-project/opensearch-py/pull/617))
### Fixed
- Fix KeyError when scroll return no hits ([#616](https://github.com/opensearch-project/opensearch-py/pull/616))
- Fix reuse of `OpenSearch` using `Urllib3HttpConnection` and `AsyncOpenSearch` after calling `close` ([#639](https://github.com/opensearch-project/opensearch-py/pull/639))
### Security
### Dependencies
- Bumps `pytest-asyncio` from <=0.21.1 to <=0.23.3
- Bumps `urllib3` from >=1.26.18 to >=1.26.18, <2 ([#632](https://github.com/opensearch-project/opensearch-py/pull/632))

## [2.4.2]
### Added
### Changed
### Deprecated
### Removed
### Fixed
- Fix `TypeError` on `parallel_bulk` ([#601](https://github.com/opensearch-project/opensearch-py/pull/601))
- Fix Amazon OpenSearch Serverless integration with LangChain ([#603](https://github.com/opensearch-project/opensearch-py/pull/603))
- Fix type of `Field.__setattr__` ([604](https://github.com/opensearch-project/opensearch-py/pull/604))
### Security

## [2.4.1]
### Added
### Changed
### Deprecated
### Removed
### Fixed
- Fix dependency on `aiohttp` ([#594](https://github.com/opensearch-project/opensearch-py/pull/594))
### Security

## [2.4.0]
### Added
- Added generating imports and headers to API generator ([#467](https://github.com/opensearch-project/opensearch-py/pull/467))
- Added point-in-time APIs (create_pit, delete_pit, delete_all_pits, get_all_pits) and Security Client APIs (health and update_audit_configuration) ([#502](https://github.com/opensearch-project/opensearch-py/pull/502))
- Added guide on using index templates ([#531](https://github.com/opensearch-project/opensearch-py/pull/531))
- Added `pool_maxsize` for `Urllib3HttpConnection` ([#535](https://github.com/opensearch-project/opensearch-py/pull/535))
- Added benchmarks ([#537](https://github.com/opensearch-project/opensearch-py/pull/537))
- Added guide on making raw JSON REST requests ([#542](https://github.com/opensearch-project/opensearch-py/pull/542))
- Added support for AWS SigV4 for urllib3 ([#547](https://github.com/opensearch-project/opensearch-py/pull/547))
- Added `remote store` client APIs ([#552](https://github.com/opensearch-project/opensearch-py/pull/552))
- Added `nox -rs generate` ([#554](https://github.com/opensearch-project/opensearch-py/pull/554))
- Added a utf-8 header to all .py files ([#557](https://github.com/opensearch-project/opensearch-py/pull/557))
- Added `samples`, `benchmarks` and `docs` to `nox -rs format` ([#556](https://github.com/opensearch-project/opensearch-py/pull/556))
- Added guide on the document lifecycle API(s) ([#559](https://github.com/opensearch-project/opensearch-py/pull/559))
- Added Windows CI ([#569](https://github.com/opensearch-project/opensearch-py/pull/569))
- Added `client.http` JSON REST request API helpers ([#544](https://github.com/opensearch-project/opensearch-py/pull/544))
### Changed
- Generate `tasks` client from API specs ([#508](https://github.com/opensearch-project/opensearch-py/pull/508))
- Generate `ingest` client from API specs ([#513](https://github.com/opensearch-project/opensearch-py/pull/513))
- Generate `dangling_indices` client from API specs ([#511](https://github.com/opensearch-project/opensearch-py/pull/511))
- Generate `cluster` client from API specs ([#530](https://github.com/opensearch-project/opensearch-py/pull/530))
- Generate `nodes` client from API specs ([#514](https://github.com/opensearch-project/opensearch-py/pull/514))
- Generate `cat` client from API specs ([#529](https://github.com/opensearch-project/opensearch-py/pull/529))
- Use API generator for all APIs ([#551](https://github.com/opensearch-project/opensearch-py/pull/551))
- Merge `.pyi` type stubs inline ([#563](https://github.com/opensearch-project/opensearch-py/pull/563))
- Expanded type coverage to benchmarks, samples and tests ([#566](https://github.com/opensearch-project/opensearch-py/pull/566))
- Defaulted `enable_cleanup_closed=True` in `aiohttp.TCPConnector` to prevent TLS connection leaks ([#468](https://github.com/opensearch-project/opensearch-py/pull/468))
- Expanded `nox -rs docs` to generate docs ([#568](https://github.com/opensearch-project/opensearch-py/pull/568))
### Deprecated
- Deprecated point-in-time APIs (list_all_point_in_time, create_point_in_time, delete_point_in_time) and Security Client APIs (health_check and update_audit_config) ([#502](https://github.com/opensearch-project/opensearch-py/pull/502))
### Removed
- Removed leftover support for Python 2.7 ([#548](https://github.com/opensearch-project/opensearch-py/pull/548))
### Fixed
- Fixed automatically built and deployed docs ([575](https://github.com/opensearch-project/opensearch-py/pull/575))
- Avoid decoding request body unless it needs to be logged ([#571](https://github.com/opensearch-project/opensearch-py/pull/571))
### Security
### Dependencies
- Bumps `sphinx` from <7.1 to <7.3
- Bumps `coverage` from <7.0.0 to <8.0.0

## [2.3.2]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
### Dependencies
- Bumps `urllib3` from >=1.21.1, <2 to >=1.26.9 ([#518](https://github.com/opensearch-project/opensearch-py/pull/518))
- Bumps `urllib3` from >=1.26.17 to >=1.26.18 ([#576](https://github.com/opensearch-project/opensearch-py/pull/576))

## [2.3.1]
### Added
### Changed
### Deprecated
### Removed
### Fixed
- Fixed race condition in AWSV4SignerAuth & AWSV4SignerAsyncAuth when using refreshable credentials ([#470](https://github.com/opensearch-project/opensearch-py/pull/470))
### Security
### Dependencies
- Bumps `urllib3` from >= 1.26.9 to >= 1.26.17 [#533](https://github.com/opensearch-project/opensearch-py/pull/533)

## [2.3.0]
### Added
- Added async support for helpers that are merged from opensearch-dsl-py ([#329](https://github.com/opensearch-project/opensearch-py/pull/329))
- Added search.md to guides ([#356](https://github.com/opensearch-project/opensearch-py/pull/356))
- Added index lifecycle guide ([#362](https://github.com/opensearch-project/opensearch-py/pull/362))
- Added point in time APIs to the pyi files in sync and async client ([#378](https://github.com/opensearch-project/opensearch-py/pull/378))
- Added MacOS and Windows CI workflows ([#390](https://github.com/opensearch-project/opensearch-py/pull/390))
- Added support for the security plugin ([#399](https://github.com/opensearch-project/opensearch-py/pull/399))
- Supports OpenSearch 2.1.0 - 2.6.0 ([#381](https://github.com/opensearch-project/opensearch-py/pull/381))
- Added `allow_redirects` to `RequestsHttpConnection#perform_request` ([#401](https://github.com/opensearch-project/opensearch-py/pull/401))
- Enhanced YAML test runner to use OpenSearch `rest-api-spec` YAML tests ([#414](https://github.com/opensearch-project/opensearch-py/pull/414))
- Added `Search#collapse` ([#409](https://github.com/opensearch-project/opensearch-py/issues/409))
- Added support for the ISM API ([#398](https://github.com/opensearch-project/opensearch-py/pull/398))
- Added `trust_env` to `AIOHttpConnection` ([#398](https://github.com/opensearch-project/opensearch-py/pull/438))
- Added support for latest OpenSearch versions 2.7.0, 2.8.0 ([#445](https://github.com/opensearch-project/opensearch-py/pull/445))
- Added samples ([#447](https://github.com/opensearch-project/opensearch-py/pull/447))
- Improved CI performance of integration with unreleased OpenSearch ([#318](https://github.com/opensearch-project/opensearch-py/pull/318))
- Added k-NN guide and samples ([#449](https://github.com/opensearch-project/opensearch-py/pull/449))
- Added the ability to run tests matching a pattern to `.ci/run-tests` ([#454](https://github.com/opensearch-project/opensearch-py/pull/454))
### Changed
- Moved security from `plugins` to `clients` ([#442](https://github.com/opensearch-project/opensearch-py/pull/442))
- Updated Security Client APIs ([#450](https://github.com/opensearch-project/opensearch-py/pull/450))
### Deprecated
### Removed
- Removed support for Python 2.7 ([#421](https://github.com/opensearch-project/opensearch-py/pull/421))
- Removed support for Python 3.5 ([#533](https://github.com/opensearch-project/opensearch-py/pull/533))
### Fixed
- Fixed flaky CI tests by replacing httpbin with a simple http_server ([#395](https://github.com/opensearch-project/opensearch-py/pull/395))
- Fixed import cycle when importing async helpers ([#311](https://github.com/opensearch-project/opensearch-py/pull/311))
- Fixed `make docs` with sphinx([#433](https://github.com/opensearch-project/opensearch-py/pull/433))
- Fixed user guide for async client ([#340](https://github.com/opensearch-project/opensearch-py/pull/340))
- Include parsed error info in `TransportError` in async connections ([#226](https://github.com/opensearch-project/opensearch-py/pull/226))
- Enhanced existing API generator to use OpenSearch OpenAPI spec ([#412](https://github.com/opensearch-project/opensearch-py/pull/412))
- Fix crash when attempting to authenticate with an async connection ([#424](https://github.com/opensearch-project/opensearch-py/pull/424))
- Fixed poetry run command issue on Windows/Mac machines ([#494](https://github.com/opensearch-project/opensearch-py/pull/494))
### Security
- Fixed CVE-2022-23491 reported in opensearch-dsl-py ([#295](https://github.com/opensearch-project/opensearch-py/pull/295))
### Dependencies
- Bumps `pytest-asyncio` to 0.21.0 ([#339](https://github.com/opensearch-project/opensearch-py/pull/339))
- Bumps `sphinx` from <1.7 to <7.1
- Bumps `pytest-asyncio` from <=0.21.0 to <=0.21.1

## [2.2.0]
### Added
- Merged opensearch-dsl-py into opensearch-py ([#287](https://github.com/opensearch-project/opensearch-py/pull/287))
- Added UPGRADING.md and updated it for opensearch-py 2.2.0 release ([#293](https://github.com/opensearch-project/opensearch-py/pull/293))
### Changed
### Deprecated
### Removed
- Removed 'out/opensearchpy' folder which was produced while generating pyi files for plugins ([#288](https://github.com/opensearch-project/opensearch-py/pull/288))
- Removed low-level and high-level client terminology from guides ([#298](https://github.com/opensearch-project/opensearch-py/pull/298))
### Fixed
- Fixed CVE-2022-23491 ([#295](https://github.com/opensearch-project/opensearch-py/pull/295))
### Security

## [2.1.1]
### Added
### Changed
### Deprecated
### Removed
### Fixed
- Fixed SigV4 Signing for Managed Service ([#279](https://github.com/opensearch-project/opensearch-py/pull/279))
- Fixed SigV4 Signing for Async Requests with QueryStrings ([#272](https://github.com/opensearch-project/opensearch-py/pull/279))
### Security

## [2.1.0]
### Added
- Added Support for AOSS ([#268](https://github.com/opensearch-project/opensearch-py/pull/268))
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [2.0.1]
### Added
- Added point in time support ([#191](https://github.com/opensearch-project/opensearch-py/pull/191))
- Added `pool_maxsize` for `RequestsHttpConnection` ([#216](https://github.com/opensearch-project/opensearch-py/pull/216))
- Added Github workflow for CHANGELOG verification ([#218](https://github.com/opensearch-project/opensearch-py/pull/218))
- Added overload decorators to `helpers-actions.pyi-bulk` ([#239](https://github.com/opensearch-project/opensearch-py/pull/239))
- Documented Keberos authentication ([214](https://github.com/opensearch-project/opensearch-py/pull/214))
- Added release workflows ([#240](https://github.com/opensearch-project/opensearch-py/pull/240))
- Added SigV4 support for async ([#254](https://github.com/opensearch-project/opensearch-py/pull/254))
- Compatibility with OpenSearch 2.1.0 - 2.4.1 ([#257](https://github.com/opensearch-project/opensearch-py/pull/257))
- Added explicit parameters for `AIOHttpConnection` and `AsyncTransport` ([#276](https://github.com/opensearch-project/opensearch-py/pull/276))
- Added support for a custom signing service name for AWS SigV4 ([#268](https://github.com/opensearch-project/opensearch-py/pull/268))
### Changed
- Updated getting started in user guide ([#233](https://github.com/opensearch-project/opensearch-py/pull/233))
- Updated CA certificate handling to check OpenSSL environment variables before defaulting to certifi ([#196](https://github.com/opensearch-project/opensearch-py/pull/196))
- Updated `master` to `cluster_manager` to be inclusive ([#242](https://github.com/opensearch-project/opensearch-py/pull/242))
- Updated CI tests to make them work locally ([#275](https://github.com/opensearch-project/opensearch-py/pull/275))
- Fixed bug with validation of `timeout` ([#387](https://github.com/opensearch-project/opensearch-py/issues/387))
### Deprecated
### Removed
- Removed patch versions in integration tests for OpenSearch 1.0.0 - 2.3.0 to reduce Github Action jobs ([#262](https://github.com/opensearch-project/opensearch-py/pull/262))
### Fixed
- Fixed DeprecationWarning emitted from urllib3 1.26.13+ ([#246](https://github.com/opensearch-project/opensearch-py/pull/246))
- Fixed Wrong return type hint in `async_scan` ([520](https://github.com/opensearch-project/opensearch-py/pull/520))
### Security

[Unreleased]: https://github.com/opensearch-project/opensearch-py/compare/v2.4.2...HEAD
[2.4.2]: https://github.com/opensearch-project/opensearch-py/compare/v2.4.0...v2.4.2
[2.4.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.4.0...v2.4.1
[2.4.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.3.2...v2.4.0
[2.3.2]: https://github.com/opensearch-project/opensearch-py/compare/v2.3.1...v2.3.2
[2.3.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.1.1...v2.2.0
[2.1.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.0.0...v2.0.1