# Log Collection Guide
  - [Import Required Modules](#import-required-modules)
  - [Setup Connection with OpenSearch Cluster](#setup-connection-with-opensearch-cluster)
  - [Initialize Logger](#initialize-logger)
  - [Define Custom Handler for OpenSearch](#define-custom-handler-for-opensearch)
  - [Create OpenSearch Handler and Add to Logger](#create-opensearch-handler-and-add-to-logger)
  - [Setup Asynchronous Logging Using Queues](#setup-asynchronous-logging-using-queues)
  - [Clean Up](#clean-up)

# Log Collection Guide
In this guide, we will look at how to collect logs from your application and send them to OpenSearch.

# Import Required Modules
Let's import the required modules:

```python
import urllib3
urllib3.disable_warnings()
from datetime import datetime
import logging
import queue
from opensearchpy import OpenSearch
from logging.handlers import QueueHandler, QueueListener
```

# Setup Connection with OpenSearch

Run the following commands to install the docker image:
```
docker pull opensearchproject/opensearch:latest
```

Create a client instance:
```python
client = OpenSearch(
		hosts=['https://@localhost:9200'],
		use_ssl=True,
		verify_certs=False,
		http_auth=('admin', 'admin')
)
```

# Initialize Logger
Set the OpenSearch logger level top INFO:

```python
# Initialize a logger named "OpenSearchLogs" for OpenSearch & set log level to INFO
print("Initializing logger...")
os_logger = logging.getLogger("OpenSearchLogs")
os_logger.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Add console handler to the logger
os_logger.addHandler(console_handler)
```

# Custom Handler For Logs
Define a custom handler that logs to OpenSearch:

```python
class OpenSearchHandler(logging.Handler):
    # Initializer / Instance attributes
    def __init__(self, opensearch_client):
        logging.Handler.__init__(self)
        self.os_client = opensearch_client

    # Build index name (e.g., "logs-YYYY-MM-DD")
    def _build_index_name(self):
        return f"logs-{datetime.date(datetime.now())}"

    # Emit logs to the OpenSearch cluster
	def emit(self, record):
        document = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "source": {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            },
            "process": {"id": record.process, "name": record.processName},
            "thread": {"id": record.thread, "name": record.threadName},
        }

        # Write the log entry to OpenSearch, handle exceptions
        try:
            self.os_client.index(
                index=self._build_index_name(),
                body=document,
            )
        except Exception as e:
            print(f"Failed to send log to OpenSearch: {e}")
```

# Create OpenSearch Handler and Add to Logger
Create an instance of OpenSearchHandler and add it to the logger:

```python
print("Creating an instance of OpenSearchHandler and adding it to the logger...")
# Create an instance of OpenSearchHandler and add it to the logger
os_handler = OpenSearchHandler(opensearch_client)
os_logger.addHandler(os_handler)
```

# Setup Asynchronous Logging Using Queues
Finally, let's setup asynchronous logging using Queues:

```python
print("Setting up asynchronous logging using Queues...")
# Setup asynchronous logging using Queues
log_queue = queue.Queue(-1)  # no limit on size
os_queue_handler = QueueHandler(log_queue)
os_queue_listener = QueueListener(log_queue, os_handler)

# Add queue handler to the logger
os_logger.addHandler(os_queue_handler)

# Start listening on the queue using the os_queue_listener
os_queue_listener.start()
```

# Clean Up
Finally, let's clean up by stopping the queue listener:

```python
print("Cleaning up...")
# Stop listening on the queue
os_queue_listener.stop()
print("Log Collection Guide has completed running")
```

# Sample Code
See [log_collection_sample.py](/samples/logging/log_collection_sample.py) for a working sample of the concepts in this guide. This Python script is a guide for setting up and running a custom log collection system using the OpenSearch service. The script will create a logger named "OpenSearchLogs" and set the log level to INFO. It will then create an instance of OpenSearchHandler and add it to the logger. Finally, it will setup asynchronous logging using Queues and send a test log to the OpenSearch cluster.

Exptected Output From Running [log_collection_sample.py](/samples/logging/log_collection_sample.py):
```python
"""
	Running Log Collection Guide
	Setting up connection with OpenSearch cluster...
	Initializing logger...
	Creating an instance of OpenSearchHandler and adding it to the logger...
	Setting up asynchronous logging using Queues...
	Logger is set up and listener has started. Sending a test log...
	This is a test log message
	Cleaning up...
	Log Collection Guide has completed running
"""
```