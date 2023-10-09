# CHANGELOG
Inspired from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
- Added generating imports and headers to API generator ([#467](https://github.com/opensearch-project/opensearch-py/pull/467))
- Added point-in-time APIs (create_pit, delete_pit, delete_all_pits, get_all_pits) and Security Client APIs (health and update_audit_configuration) ([#502](https://github.com/opensearch-project/opensearch-py/pull/502))
### Changed
- Generate `tasks` client from API specs ([#508](https://github.com/opensearch-project/opensearch-py/pull/508))
- Generate `ingest` client from API specs ([#513](https://github.com/opensearch-project/opensearch-py/pull/513))
- Generate `dangling_indices` client from API specs ([#511](https://github.com/opensearch-project/opensearch-py/pull/511))
- Generate `nodes` client from API specs ([#514](https://github.com/opensearch-project/opensearch-py/pull/514))
- Generate `cat` client from API specs ([#529](https://github.com/opensearch-project/opensearch-py/pull/529))
### Deprecated
- Deprecated point-in-time APIs (list_all_point_in_time, create_point_in_time, delete_point_in_time) and Security Client APIs (health_check and update_audit_config) ([#502](https://github.com/opensearch-project/opensearch-py/pull/502))
### Removed
### Fixed
### Security
### Dependencies
- Bumps `sphinx` from <7.1 to <7.3

## [2.3.2]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
### Dependencies
- Bumps `urllib3` from >=1.21.1, <2 to >=1.26.9 ([#518](https://github.com/opensearch-project/opensearch-py/pull/518))

## [2.3.1]
### Added
### Changed
### Deprecated
### Removed
### Fixed
- Fixed race condition in AWSV4SignerAuth & AWSV4SignerAsyncAuth when using refreshable credentials ([#470](https://github.com/opensearch-project/opensearch-py/pull/470))
### Security
### Dependencies

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
- Enhanced YAML test runner to use OpenSearch `rest-api-spec` YAML tests ([#414](https://github.com/opensearch-project/opensearch-py/pull/414)
- Added `Search#collapse` ([#409](https://github.com/opensearch-project/opensearch-py/issues/409))
- Added support for the ISM API ([#398](https://github.com/opensearch-project/opensearch-py/pull/398))
- Added `trust_env` to `AIOHttpConnection` ([#398](https://github.com/opensearch-project/opensearch-py/pull/438))
- Added support for latest OpenSearch versions 2.7.0, 2.8.0 ([#445](https://github.com/opensearch-project/opensearch-py/pull/445))
- Added samples ([#447](https://github.com/opensearch-project/opensearch-py/pull/447))
- Improved CI performance of integration with unreleased OpenSearch ([#318](https://github.com/opensearch-project/opensearch-py/pull/318))
- Added k-NN guide and samples ([#449](https://github.com/opensearch-project/opensearch-py/pull/449))
- Added the ability to run tests matching a pattern to `.ci/run-tests` ([#454](https://github.com/opensearch-project/opensearch-py/pull/454))
- Added a guide for taking snapshots ([#486](https://github.com/opensearch-project/opensearch-py/pull/429))
### Changed
- Moved security from `plugins` to `clients` ([#442](https://github.com/opensearch-project/opensearch-py/pull/442))
- Updated Security Client APIs ([#450](https://github.com/opensearch-project/opensearch-py/pull/450))
### Deprecated
### Removed
- Removed support for Python 2.7 ([#421](https://github.com/opensearch-project/opensearch-py/pull/421))
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

[Unreleased]: https://github.com/opensearch-project/opensearch-py/compare/v2.3.2...HEAD
[2.0.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.0.0...v2.0.1
[2.1.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.0.1...v2.1.0
[2.1.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.1.0...v2.1.1
[2.2.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.1.1...v2.2.0
[2.3.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.2.0...v2.3.0
[2.3.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.3.0...v2.3.1
[2.3.2]: https://github.com/opensearch-project/opensearch-py/compare/v2.3.1...v2.3.2
