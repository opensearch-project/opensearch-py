- [Alerting Plugin](#alerting-plugin)
  - [Creating a Monitor](#creating-a-monitor)
  - [Get a Monitor](#get-a-monitor)
  - [Search for a Monitor](#search-for-a-monitor)
  - [Create an Email Destination](#create-an-email-destination)
  - [Get Alerts](#get-alerts)
  - [Acknowledge Alerts](#acknowledge-alerts)

### Alerting Plugin

You can use the [Alerting Plugin API](https://opensearch.org/docs/latest/observing-your-data/alerting/api/) to programmatically create, update, and manage monitors and alerts.

#### Creating a Monitor

Create a bucket-level monitor. 

```python
query = {
  "type": "monitor",
  "name": "Demo bucket-level monitor",
  "monitor_type": "bucket_level_monitor",
  "enabled": True,
  "schedule": {
    "period": {
      "interval": 1,
      "unit": "MINUTES"
    }
  },
  "inputs": [
    {
      "search": {
        "indices": [
          "test-index"
        ],
        "query": {
          "size": 0,
          "query": {
            "bool": {
              "filter": [
                {
                  "range": {
                    "order_date": {
                      "from": "||-1h",
                      "to": "",
                      "include_lower": True,
                      "include_upper": True,
                      "format": "epoch_millis"
                    }
                  }
                }
              ]
            }
          },
          "aggregations": {
            "composite_agg": {
              "composite": {
                "sources": [
                  {
                    "user": {
                      "terms": {
                        "field": "user"
                      }
                    }
                  }
                ]
              },
              "aggregations": {
                "avg_products_base_price": {
                  "avg": {
                    "field": "products.base_price"
                  }
                }
              }
            }
          }
        }
      }
    }
  ],
}

response = client.plugins.alerting.create_monitor(query)
print(response)
```

#### Get a Monitor

```python
response = client.plugins.alerting.get_monitor("monitorID")
print(response)
```

#### Search for a Monitor

```python
query = {
  "query": {
    "match" : {
      "monitor.name": "test-monitor"
    }
  }
}

response = client.plugins.alerting.search_monitor(query)
print(response)
```

#### Create an Email Destination

```python
query = {
  "type": "email",
  "name": "my-email-destination",
  "email": {
    "email_account_id": "YjY7mXMBx015759_IcfW",
    "recipients": [
      {
        "type": "email_group",
        "email_group_id": "YzY-mXMBx015759_dscs"
      },
      {
        "type": "email",
        "email": "example@email.com"
      }
    ]
  }
}

response = client.plugins.alerting.create_destination(query)
print(response)
```

#### Get Alerts

```python
response = client.plugins.alerting.get_alerts()
print(response)
```

#### Acknowledge Alerts

```python
query = {
  "alerts": ["eQURa3gBKo1jAh6qUo49"]
}

response = client.plugins.alerting.acknowledge_alert(query)
print(response)
```
