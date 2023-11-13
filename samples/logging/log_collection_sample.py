#!/usr/bin/env python

# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from datetime import datetime
import logging
import queue
from opensearchpy import OpenSearch
from logging.handlers import QueueHandler, QueueListener

# For cleaner output, comment in the two lines below to disable warnings and informational messages
# import urllib3
# urllib3.disable_warnings()


def run_log_collection_guide() -> None:
    print("Running Log Collection Guide")

    # Setup connection with the OpenSearch cluster
    print("Setting up connection with OpenSearch cluster...")
    opensearch_client = OpenSearch(
        "https://admin:admin@localhost:9200",
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
        http_auth=("admin", "admin"),
    )

    # Initialize a logger named "OpenSearchLogs" for OpenSearch
    print("Initializing logger...")
    os_logger = logging.getLogger("OpenSearchLogs")
    os_logger.setLevel(logging.INFO)

    # Define a custom handler that logs to OpenSearch
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
                    index="movies",
                    id=1,
                    body={"title": "Beauty and the Beast", "year": 1991},
                )
            except Exception as e:
                print(f"Failed to send log to OpenSearch: {e}")

    print("Creating an instance of OpenSearchHandler and adding it to the logger...")
    # Create an instance of OpenSearchHandler and add it to the logger
    os_handler = OpenSearchHandler(opensearch_client)
    os_logger.addHandler(os_handler)

    print("Setting up asynchronous logging using Queues...")
    # Setup asynchronous logging using Queues
    log_queue = queue.Queue(-1)  # no limit on size
    os_queue_handler = QueueHandler(log_queue)
    os_queue_listener = QueueListener(log_queue, os_handler)

    # Add queue handler to the logger
    os_logger.addHandler(os_queue_handler)

    # Start listening on the queue using the os_queue_listener
    os_queue_listener.start()

    print("Logger is set up and listener has started. Sending a test log...")
    # Logging a test message
    os_logger.info("This is a test log message")

    print("Cleaning up...")
    # Stop listening on the queue
    os_queue_listener.stop()
    print("Log Collection Guide has completed running")


if __name__ == "__main__":
    run_log_collection_guide()
