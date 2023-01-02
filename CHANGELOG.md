# CHANGELOG
Inspired from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
- Added Point in time API rest API([#191](https://github.com/opensearch-project/opensearch-py/pull/191))
- Added pool_maxsize for RequestsHttpConnection ([#216](https://github.com/opensearch-project/opensearch-py/pull/216))
- Github workflow for changelog verification ([#218](https://github.com/opensearch-project/opensearch-py/pull/218))
- Added overload decorators to helpers-actions.pyi-"bulk" ([#239](https://github.com/opensearch-project/opensearch-py/pull/239))
- Document Keberos authenticaion ([214](https://github.com/opensearch-project/opensearch-py/pull/214))
- Add release workflows ([#240](https://github.com/opensearch-project/opensearch-py/pull/240))
- Added SigV4 support for Async Opensearch Client ([#254](https://github.com/opensearch-project/opensearch-py/pull/254))
### Changed
- Updated getting started to user guide ([#233](https://github.com/opensearch-project/opensearch-py/pull/233))
- Updated CA certificate handling to check OpenSSL environment variables before defaulting to certifi ([#196](https://github.com/opensearch-project/opensearch-py/pull/196))
- Updates `master` to `cluster_manager` to be inclusive ([#242](https://github.com/opensearch-project/opensearch-py/pull/242))
### Deprecated

### Removed

### Fixed
- Fixed DeprecationWarning emitted from urllib3 1.26.13+ ([#246](https://github.com/opensearch-project/opensearch-py/pull/246))
### Security


[Unreleased]: https://github.com/opensearch-project/opensearch-py/compare/2.0...HEAD
