- [Index Management Plugin](#index-management-plugin)
  - [Create a Policy](#create-a-policy)
  - [Get a Policy](#get-a-policy)
  - [Delete a Policy](#delete-a-policy)

### Index Management Plugin

You can use the [Index Management Plugin (ISM) API](https://opensearch.org/docs/latest/im-plugin/ism/api) to programmatically automate periodic, administrative operations on indexes by triggering them based on changes in the index age, index size, or number of documents.

#### Create a Policy

```python
policy_name = "test-policy"

policy_content = {
    "policy": {
        "description": "hot warm delete workflow",
        "default_state": "hot",
        "schema_version": 1,
        "states": [
            {
                "name": "hot",
                "actions": [{"rollover": {"min_index_age": "1d"}}],
                "transitions": [{"state_name": "warm"}],
            },
            {
                "name": "warm",
                "actions": [{"replica_count": {"number_of_replicas": 5}}],
                "transitions": [{"state_name": "delete", "conditions": {"min_index_age": "30d"}}],
            },
            {
                "name": "delete",
                "actions": [
                    {
                        "notification": {
                            "destination": {"chime": {"url": "<URL>"}},
                            "message_template": {"source": "The index {{ctx.index}} is being deleted"},
                        }
                    },
                    {"delete": {}},
                ],
            },
        ],
        "ism_template": {"index_patterns": ["log*"], "priority": 100},
    }
}

response = client.index_managment.put_policy(policy_name, body=policy_content)
print(response)
```

#### Get a Policy

```python
policy_name = "test-policy"

response = client.index_managment.get_policy(policy_name)
print(response)
```

#### Delete a Policy

```python
policy_name = "test-policy"

response = client.index_managment.delete_policy(policy_name)
print(response)
```
