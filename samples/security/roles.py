#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


# A basic OpenSearch sample that create and manage roles.

from opensearchpy import OpenSearch

# connect to OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_show_warn = False
)

# Create a Role

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

# Get a Role

role_name = "test-role"

response = client.security.get_role(role_name)
print(response)
