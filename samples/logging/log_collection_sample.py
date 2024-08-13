#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import logging
import os
import queue
from datetime import datetime
from logging.handlers import QueueHandler, QueueListener
from typing import Any

import urllib3

from opensearchpy import OpenSearch

urllib3.disable_warnings()


def main() -> None:
    """
    sample for custom logging; this shows how to create a
    console handler, connect to OpenSearch, define a custom
    logger, and log to an OpenSearch index
    """
    print("Collecting logs.")

    # Create a console handler
    console_handler: logging.StreamHandler = logging.StreamHandler()  # type: ignore
    console_handler.setLevel(logging.INFO)

    # Setup connection with the OpenSearch cluster
    print("Setting up connection with OpenSearch cluster...")
    opensearch_client: Any = OpenSearch(
        "https://admin:admin@localhost:9200",
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
        http_auth=("admin", os.getenv("OPENSEARCH_PASSWORD", "admin")),
    )

    # Initialize a logger named "OpenSearchLogs" for OpenSearch
    print("Initializing logger...")
    os_logger: logging.Logger = logging.getLogger("OpenSearchLogs")
    os_logger.setLevel(logging.INFO)

    # Add console handler to the logger
    os_logger.addHandler(console_handler)

    class OpenSearchHandler(logging.Handler):
        """
        define a custom handler that logs to opensearch
        """

        # Initializer / Instance attributes
        def __init__(self, opensearch_client: Any) -> None:
            super().__init__()
            self.os_client = opensearch_client

        def _build_index_name(self) -> str:
            """
            Build index name (e.g., "logs-YYYY-MM-DD")
            :rtype: bool
            :return: a str with date formatted as 'logs-YYYY-MM-DD'
            """
            return f"logs-{datetime.date(datetime.now())}"

        # Emit logs to the OpenSearch cluster
        def emit(self, record: logging.LogRecord) -> None:
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

            try:
                self.os_client.index(
                    index=self._build_index_name(),
                    body=document,
                )
            except Exception as ex:
                print(f"Failed to send log to OpenSearch: {ex}")
                logging.warning(f"Failed to send log to OpenSearch: {ex}")
                raise

    print("Creating an instance of OpenSearchHandler and adding it to the logger...")
    # Create an instance of OpenSearchHandler and add it to the logger
    os_handler: OpenSearchHandler = OpenSearchHandler(opensearch_client)
    os_logger.addHandler(os_handler)

    print("Setting up asynchronous logging using Queues...")
    # Setup asynchronous logging using Queues
    log_queue: queue.Queue[logging.LogRecord] = queue.Queue(-1)  # no limit on size
    os_queue_handler: logging.Handler = QueueHandler(log_queue)
    os_queue_listener: QueueListener = QueueListener(log_queue, os_handler)

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
    main()
