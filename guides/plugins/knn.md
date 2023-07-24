- [k-NN Plugin](#k-nn-plugin)
  - [Basic Approximate k-NN](#basic-approximate-k-nn)
    - [Create an Index](#create-an-index)
    - [Index Vectors](#index-vectors)
    - [Search for Nearest Neighbors](#search-for-nearest-neighbors)
  - [Approximate k-NN with a Boolean Filter](#approximate-k-nn-with-a-boolean-filter)
  - [Approximate k-NN with a Lucene Filter](#approximate-k-nn-with-a-lucene-filter)

# k-NN Plugin

Short for k-nearest neighbors, the k-NN plugin enables users to search for the k-nearest neighbors to a query point across an index of vectors. See [documentation](https://opensearch.org/docs/latest/search-plugins/knn/index/) for more information.

## Basic Approximate k-NN

In the following example we create a 5-dimensional k-NN index with random data. You can find a synchronous version of this working sample in [samples/knn/knn-basics.py](../../samples/knn/knn-basics.py) and an asynchronous one in [samples/knn/knn-async-basics.py](../../samples/knn/knn-async-basics.py).

```bash
$ poetry run knn/knn-basics.py

Searching for [0.61, 0.05, 0.16, 0.75, 0.49] ...
{'_index': 'my-index', '_id': '3', '_score': 0.9252405, '_source': {'values': [0.64, 0.3, 0.27, 0.68, 0.51]}}
{'_index': 'my-index', '_id': '4', '_score': 0.802375, '_source': {'values': [0.49, 0.39, 0.21, 0.42, 0.42]}}
{'_index': 'my-index', '_id': '8', '_score': 0.7826564, '_source': {'values': [0.33, 0.33, 0.42, 0.97, 0.56]}}
```

### Create an Index

```python
dimensions = 5
client.indices.create(index_name, 
    body={
        "settings":{
            "index.knn": True
        },
        "mappings":{
            "properties": {
                "values": {
                    "type": "knn_vector", 
                    "dimension": dimensions
                },
            }
        }
    }
)
```

### Index Vectors

Create 10 random vectors and insert them using the bulk API.

```python
vectors = []
for i in range(10):
    vec = []
    for j in range(dimensions): 
        vec.append(round(random.uniform(0, 1), 2)) 
  
    vectors.append({
        "_index": index_name,
        "_id": i,
        "values": vec,
    })

helpers.bulk(client, vectors)

client.indices.refresh(index=index_name)
```

### Search for Nearest Neighbors

Create a random vector of the same size and search for its nearest neighbors.

```python
vec = []
for j in range(dimensions): 
    vec.append(round(random.uniform(0, 1), 2)) 

search_query = {
    "query": {
        "knn": {
            "values": {
                "vector": vec, 
                "k": 3
            }
        }
    }
}

results = client.search(index=index_name, body=search_query)
for hit in results["hits"]["hits"]:
    print(hit)
```

## Approximate k-NN with a Boolean Filter

In [the boolean-filter.py sample](../../samples/knn/knn-boolean-filter.py) we create a 5-dimensional k-NN index with random data and a `metadata` field that contains a book genre (e.g. `fiction`). The search query is a k-NN search filtered by genre. The filter clause is outside the k-NN query clause and is applied after the k-NN search.

```bash
$ poetry run knn/knn-boolean-filter.py 

Searching for [0.08, 0.42, 0.04, 0.76, 0.41] with the 'romance' genre ...

{'_index': 'my-index', '_id': '445', '_score': 0.95886475, '_source': {'values': [0.2, 0.54, 0.08, 0.87, 0.43], 'metadata': {'genre': 'romance'}}}
{'_index': 'my-index', '_id': '2816', '_score': 0.95256233, '_source': {'values': [0.22, 0.36, 0.01, 0.75, 0.57], 'metadata': {'genre': 'romance'}}}
```

## Approximate k-NN with an Efficient Filter

In [the lucene-filter.py sample](../../samples/knn/knn-efficient-filter.py) we implement the example in [the k-NN documentation](https://opensearch.org/docs/latest/search-plugins/knn/filter-search-knn/), which creates an index that uses the Lucene engine and HNSW as the method in the mapping, containing hotel location and parking data, then search for the top three hotels near the location with the coordinates `[5, 4]` that are rated between 8 and 10, inclusive, and provide parking.

```bash
$ poetry run knn/knn-efficient-filter.py

{'_index': 'hotels-index', '_id': '3', '_score': 0.72992706, '_source': {'location': [4.9, 3.4], 'parking': 'true', 'rating': 9}}
{'_index': 'hotels-index', '_id': '6', '_score': 0.3012048, '_source': {'location': [6.4, 3.4], 'parking': 'true', 'rating': 9}}
{'_index': 'hotels-index', '_id': '5', '_score': 0.24154587, '_source': {'location': [3.3, 4.5], 'parking': 'true', 'rating': 8}}
```