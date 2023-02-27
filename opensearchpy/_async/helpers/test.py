import os
import time
from unittest import SkipTest, TestCase

from opensearchpy import AsyncOpenSearch
from opensearchpy.exceptions import ConnectionError

if "OPENSEARCH_URL" in os.environ:
    OPENSEARCH_URL = os.environ["OPENSEARCH_URL"]
else:
    OPENSEARCH_URL = "https://admin:admin@localhost:9200"


async def get_test_client(nowait=False, **kwargs):
    # construct kwargs from the environment
    kw = {"timeout": 30}

    if "PYTHON_CONNECTION_CLASS" in os.environ:
        from opensearchpy import connection

        kw["connection_class"] = getattr(
            connection, os.environ["PYTHON_CONNECTION_CLASS"]
        )

    kw.update(kwargs)
    client = AsyncOpenSearch(OPENSEARCH_URL, **kw)

    # wait for yellow status
    for _ in range(1 if nowait else 100):
        try:
            client.cluster.health(wait_for_status="yellow")
            return client
        except ConnectionError:
            time.sleep(0.1)
    else:
        # timeout
        raise SkipTest("OpenSearch failed to start.")
