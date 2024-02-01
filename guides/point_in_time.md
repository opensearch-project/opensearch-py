- [Point-in-Time - Deprecated Implementation Examples](#point-in-time---deprecated-implementation-examples)
- [Point-in-Time - Updated Implementation Examples](#point-in-time---updated-implementation-examples)

### Point-in-Time - Deprecated Implementation Examples

[Point in Time (PIT)](https://opensearch.org/docs/latest/search-plugins/point-in-time/) lets you run different queries against a dataset that is fixed in time.

Create a point in time on an index.

```python
index_name = "test-index"
response = client.create_point_in_time(
    index=index_name,
    keep_alive="1m"
)

pit_id = response.get("pit_id")
print('\n Point in time ID:')
print(pit_id)
```

List all point in time which are alive in the cluster.

```python
response = client.list_all_point_in_time()
print(response)
```

Delete a point in time.

```python
pit_body = {
    "pit_id": [pit_id]
}
response = client.delete_point_in_time(body=pit_body)
print(response)
```

Delete all point in time.

```python
response = client.delete_point_in_time(body=None, all=True)
print(response)
```


### Point-in-Time - Updated Implementation Examples

Create a point in time on an index.

```python
index_name = "test-index"
response = client.create_pit(
    index=index_name,
    params={"keep_alive": "1m"}
)

pit_id = response.get("pit_id")
print('\n Point in time ID:')
print(pit_id)
```


List all point in time which are alive in the cluster.

```python
response = client.get_all_pits()
print(response)
```

Delete a point in time.

```python
pit_body = {"pit_id": pit_id}
response = client.delete_pit(body=pit_body)
print(response)
```

Delete all point in time.

```python
response = client.delete_all_pits()
print(response)
```
