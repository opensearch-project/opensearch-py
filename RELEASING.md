- [Overview](#overview)
- [Branching](#branching)
  - [Release Branching](#release-branching)
  - [Feature Branches](#feature-branches)
- [Release Labels](#release-labels)
- [Releasing](#releasing)

## Overview

This document explains the release strategy for artifacts in this organization.

## Branching

### Release Branching

Given the current major release of 1.0, projects in this organization maintain the following active branches.

* **main**: The next _major_ release. This is the branch where all merges take place and code moves fast.
* **1.x**: The next _minor_ release. Once a change is merged into `main`, decide whether to backport it to `1.x`.
* **1.0**: The _current_ release. In between minor releases, only hotfixes (e.g. security) are backported to `1.0`.

Label PRs with the next major version label (e.g. `2.0.0`) and merge changes into `main`. Label PRs that you believe need to be backported as `1.x` and `1.0`. Backport PRs by checking out the versioned branch, cherry-pick changes and open a PR against each target backport branch.

### Feature Branches

Do not creating branches in the upstream repo, use your fork, for the exception of long lasting feature branches that require active collaboration from multiple developers. Name feature branches `feature/<thing>`. Once the work is merged to `main`, please make sure to delete the feature branch.

## Release Labels

Repositories create consistent release labels, such as `v1.0.0`, `v1.1.0` and `v2.0.0`, as well as `patch` and `backport`. Use release labels to target an issue or a PR for a given release. See [MAINTAINERS](MAINTAINERS.md#triage-open-issues) for more information on triaging issues.

## Releasing

The release process is standard across repositories in this org and is run by a release manager volunteering from amongst [maintainers](MAINTAINERS.md).

1. Update the version in [CHANGELOG](CHANGELOG.md), [_version.py](opensearchpy/_version.py) and [unified-release.yml](.github/workflows/unified-release.yml), make a pull request and have it merged. See [example](https://github.com/opensearch-project/opensearch-py/pull/799).
2. Check out the [upstream repo](https://github.com/opensearch-project/opensearch-py), make sure it's up-to-date with `git pull origin main`, create a tag, e.g. `git tag v2.1.0`, and push it to GitHub with `git push origin --tags`.
3. The [release-drafter#draft-a-release](.github/workflows/release-drafter.yml) workflow will be automatically kicked off and a draft release will be created along with a release issue that requires approval from another maintainer. See [example](https://github.com/opensearch-project/opensearch-py/issues/801).
4. The [release-drafter#pypi-publish](.github/workflows/release-drafter.yml) workflow will publish the release to [PyPi](https://pypi.org/project/opensearch-py/).
5. Add an "Unreleased" section to [CHANGELOG](CHANGELOG.md), update the [COMPATIBILITY](COMPATIBILITY.md) matrix, and increment version in [_version.py](opensearchpy/_version.py) to the next patch release, e.g. v2.1.1. See [example](https://github.com/opensearch-project/opensearch-py/pull/802).