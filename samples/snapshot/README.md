Run this sample as follows.

```
cd samples
docker run --rm -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -it $(docker build -q snapshot )
poetry install
poetry run python snapshot/snapshot_sample.py 
```
