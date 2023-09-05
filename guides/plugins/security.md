- [Security Plugin](#security-plugin)
  - [Create a Role](#create-a-role)
  - [Get a Role](#get-a-role)
  - [Create a User](#create-a-user)
  - [Get a User](#get-a-user)

### Security Plugin

The [Security Plugin API](https://opensearch.org/docs/latest/security/access-control/api/) lets you programmatically create and manage users, roles, role mappings, action groups, and tenants.

#### Create a Role

```python
role_name = "test-role"

role_content = {
  "cluster_permissions": ["cluster_monitor"],
  "index_permissions": [
      {
          "index_patterns": ["index", "test-*"],
          "allowed_actions": [
              "data_access",
              "indices_monitor",
          ],
      }
  ],
}

response = client.security.create_role(role_name, body=role_content)
print(response)
```

#### Get a Role

```python
role_name = "test-role"

response = client.security.get_role(role_name)
print(response)
```

#### Create a User

```python
user_name = "test-user"
user_content = {"password": "test_password", "opendistro_security_roles": []}

response = client.security.create_user(user_name, body=user_content)
print(response)
```

#### Get a User

```python
user_name = "test-user"

response = client.security.get_user(user_name)
print(response)
```
