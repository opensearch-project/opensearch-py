# CHANGELOG
Inspired from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
- Added async support for helpers that are merged from opensearch-dsl-py ([#329](https://github.com/opensearch-project/opensearch-py/pull/329))
- Added index lifecycle guide ([#362](https://github.com/opensearch-project/opensearch-py/pull/362))
### Changed
- Upgrading pytest-asyncio to latest version - 0.21.0 ([#339](https://github.com/opensearch-project/opensearch-py/pull/339))
### Deprecated
### Removed
### Fixed
- Fixed import cycle when importing async helpers ([#311](https://github.com/opensearch-project/opensearch-py/pull/311))
- Fixed userguide for async client ([#340](https://github.com/opensearch-project/opensearch-py/pull/340))
### Security
- Fixed CVE-2022-23491 reported in opensearch-dsl-py ([#295](https://github.com/opensearch-project/opensearch-py/pull/295))
- Update ci workflows ([#318](https://github.com/opensearch-project/opensearch-py/pull/318))

## [2.2.0]
### Added
- Merging opensearch-dsl-py into opensearch-py ([#287](https://github.com/opensearch-project/opensearch-py/pull/287))
- Added upgrading.md file and updated it for opensearch-py 2.2.0 release ([#293](https://github.com/opensearch-project/opensearch-py/pull/293))
### Changed
### Deprecated
### Removed
- Removed 'out/opensearchpy' folder which was produced while generating pyi files for plugins ([#288](https://github.com/opensearch-project/opensearch-py/pull/288))
- Removed low-level and high-level client terminology from guides ([#298](https://github.com/opensearch-project/opensearch-py/pull/298))
### Fixed
- Fixed CVE - issue 86 mentioned in opensearch-dsl-py repo ([#295](https://github.com/opensearch-project/opensearch-py/pull/295))
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
- Added Point in time API rest API([#191](https://github.com/opensearch-project/opensearch-py/pull/191))
- Added pool_maxsize for RequestsHttpConnection ([#216](https://github.com/opensearch-project/opensearch-py/pull/216))
- Github workflow for changelog verification ([#218](https://github.com/opensearch-project/opensearch-py/pull/218))
- Added overload decorators to helpers-actions.pyi-"bulk" ([#239](https://github.com/opensearch-project/opensearch-py/pull/239))
- Document Keberos authenticaion ([214](https://github.com/opensearch-project/opensearch-py/pull/214))
- Add release workflows ([#240](https://github.com/opensearch-project/opensearch-py/pull/240))
- Added SigV4 support for Async Opensearch Client ([#254](https://github.com/opensearch-project/opensearch-py/pull/254))
- Compatibility with OpenSearch 2.1.0 - 2.4.1 ([#257](https://github.com/opensearch-project/opensearch-py/pull/257))
- Adding explicit parameters for AIOHttpConnection and AsyncTransport ([#276](https://github.com/opensearch-project/opensearch-py/pull/276))
### Changed
- Updated getting started to user guide ([#233](https://github.com/opensearch-project/opensearch-py/pull/233))
- Updated CA certificate handling to check OpenSSL environment variables before defaulting to certifi ([#196](https://github.com/opensearch-project/opensearch-py/pull/196))
- Updates `master` to `cluster_manager` to be inclusive ([#242](https://github.com/opensearch-project/opensearch-py/pull/242))
- Support a custom signing service name for AWS SigV4 ([#268](https://github.com/opensearch-project/opensearch-py/pull/268))
- Updated CI tests to make them work locally ([#275](https://github.com/opensearch-project/opensearch-py/pull/275))
### Deprecated

### Removed
- Removed patch versions in integration tests for OpenSearch 1.0.0 - 2.3.0 to reduce Github Action jobs ([#262](https://github.com/opensearch-project/opensearch-py/pull/262))
### Fixed
- Fixed DeprecationWarning emitted from urllib3 1.26.13+ ([#246](https://github.com/opensearch-project/opensearch-py/pull/246))
### Security


[Unreleased]: https://github.com/opensearch-project/opensearch-py/compare/v2.2.0...HEAD
[2.0.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.0.0...v2.0.1
[2.1.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.0.1...v2.1.0
[2.1.1]: https://github.com/opensearch-project/opensearch-py/compare/v2.1.0...v2.1.1
[2.2.0]: https://github.com/opensearch-project/opensearch-py/compare/v2.1.1...v2.2.0
