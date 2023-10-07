Python client benchmarks using [richbench](https://github.com/tonybaloney/rich-bench).

### Start OpenSearch

```
docker run -p 9200:9200 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

### Install Prerequisites

```
poetry install
```

### Run Benchmarks

```
poetry run richbench . --repeat 1 --times 1
```

```
poetry run richbench . --repeat 1 --times 1 --benchmark sync
```
