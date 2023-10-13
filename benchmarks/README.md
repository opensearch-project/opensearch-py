- [Benchmarks](#benchmarks)
  - [Start OpenSearch](#start-opensearch)
  - [Install Prerequisites](#install-prerequisites)
  - [Run Benchmarks](#run-benchmarks)

## Benchmarks

Python client benchmarks using [richbench](https://github.com/tonybaloney/rich-bench).

### Start OpenSearch

```
docker run -p 9200:9200 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

### Install Prerequisites

Install [poetry](https://python-poetry.org/docs/), then install package dependencies.

```
poetry install
```

Benchmarks use the code in this repository by specifying the dependency as `opensearch-py = { path = "..", develop=true, extras=["async"] }` in [pyproject.toml](pyproject.toml).

### Run Benchmarks

Run all benchmarks available as follows.

```
$ poetry run richbench . --repeat 1 --times 1

                                             Benchmarks, repeat=1, number=1                                              
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃                         Benchmark ┃ Min     ┃ Max     ┃ Mean    ┃ Min (+)         ┃ Max (+)         ┃ Mean (+)        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1 client vs. more clients (async) │ 1.640   │ 1.640   │ 1.640   │ 1.102 (1.5x)    │ 1.102 (1.5x)    │ 1.102 (1.5x)    │
│    1 thread vs. 32 threads (sync) │ 5.526   │ 5.526   │ 5.526   │ 1.626 (3.4x)    │ 1.626 (3.4x)    │ 1.626 (3.4x)    │
│    1 thread vs. 32 threads (sync) │ 4.639   │ 4.639   │ 4.639   │ 3.363 (1.4x)    │ 3.363 (1.4x)    │ 3.363 (1.4x)    │
│                sync vs. async (8) │ 3.198   │ 3.198   │ 3.198   │ 0.966 (3.3x)    │ 0.966 (3.3x)    │ 0.966 (3.3x)    │
└───────────────────────────────────┴─────────┴─────────┴─────────┴─────────────────┴─────────────────┴─────────────────┘
```

Run a specific benchmark, e.g. [bench_sync.py](bench_sync.py) by specifying `--benchmark [name]`.

```
$ poetry run richbench . --repeat 1 --times 1 --benchmark sync

                                            Benchmarks, repeat=1, number=1                                            
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃                      Benchmark ┃ Min     ┃ Max     ┃ Mean    ┃ Min (+)         ┃ Max (+)         ┃ Mean (+)        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1 thread vs. 32 threads (sync) │ 6.804   │ 6.804   │ 6.804   │ 3.409 (2.0x)    │ 3.409 (2.0x)    │ 3.409 (2.0x)    │
└────────────────────────────────┴─────────┴─────────┴─────────┴─────────────────┴─────────────────┴─────────────────┘
```
