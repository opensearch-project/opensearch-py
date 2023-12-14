- [Log Collection Guide](#log-collection-guide)
- [Import Required Modules](#import-required-modules)
- [Download and Start OpenSearch](#download-and-start-opensearch)
- [Setup Connection with OpenSearch](#setup-connection-with-opensearch)
- [Initialize Logger](#initialize-logger)
- [Custom Handler For Logs](#custom-handler-for-logs)
- [Create OpenSearch Handler and Add to Logger](#create-opensearch-handler-and-add-to-logger)
- [Setup Asynchronous Logging Using Queues](#setup-asynchronous-logging-using-queues)
- [Clean Up](#clean-up)
- [Sample Code](#sample-code)


## Log Collection Guide
In this guide, we will look at how to collect logs from your application and send them to OpenSearch.

## Import Required Modules
Let's import the required modules:

```python
import logging
import queue
from datetime import datetime
from logging.handlers import QueueHandler, QueueListener
from typing import Any

import urllib3

from opensearchpy import OpenSearch

urllib3.disable_warnings()
```

## Download and Start OpenSearch
```
docker pull opensearchproject/opensearch:latest
```

```
docker run -d -p 9200:9200 -p 9600:9600 --name opensearch_opensearch_1 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<admin password>" opensearchproject/opensearch:latest 
```

## Setup Connection with OpenSearch

Create a client instance:
```python
    opensearch_client: Any = OpenSearch(
        "https://admin:<admin password>@localhost:9200",
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
        http_auth=("admin", "<admin password>"),
    )
```

## Initialize Logger
Initialize a logger, named "OpenSearchLogs", that emits logs to OpenSearch, and a console handler, both set to the INFO level, are initialized. The console handler is then added to the logger. For every log line processed by this setup, a corresponding OpenSearch document is created. This approach supports structured and comprehensive logging because each document can include extensive metadata within it.

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

## Custom Handler For Logs
Define a custom handler that logs to OpenSearch:

```python
class OpenSearchHandler(logging.Handler):
    # Initializer / Instance attributes
    def __init__(self, opensearch_client):
        logging.Handler.__init__(self)
        self.opensearch_client = opensearch_client

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
            "process": {
                "id": record.process,
                "name": record.processName
            },
            "thread": {
                "id": record.thread,
                "name": record.threadName
            },
        }

    # Write the log entry to OpenSearch, handle exceptions
    self.opensearch_client.index(
        index=self._build_index_name(),
        body=document,
    )
```

## Create OpenSearch Handler and Add to Logger
Create an instance of OpenSearchHandler and add it to the logger:

```python
    print("Creating an instance of OpenSearchHandler and adding it to the logger...")
    # Create an instance of OpenSearchHandler and add it to the logger
    os_handler = OpenSearchHandler(opensearch_client)
    os_logger.addHandler(os_handler)
```

## Setup Asynchronous Logging Using Queues
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

## Clean Up
Finally, let's clean up by stopping the queue listener:

```python
    print("Cleaning up...")
    # Stop listening on the queue
    os_queue_listener.stop()
    print("Log Collection Guide has completed running")
```

## Sample Code
See [log_collection_sample.py](/samples/logging/log_collection_sample.py) for a working sample of the concepts in this guide. The script will create a logger named "OpenSearchLogs" and set the log level to INFO. It will then create an instance of OpenSearchHandler and add it to the logger. Finally, it will setup asynchronous logging using Queues and send a test log to the OpenSearch cluster.

Exptected Output From Running [log_collection_sample.py](/samples/logging/log_collection_sample.py):

```
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