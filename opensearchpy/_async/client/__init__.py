# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


# ------------------------------------------------------------------------------------------
# THIS CODE IS AUTOMATICALLY GENERATED AND MANUAL EDITS WILL BE LOST
#
# To contribute, kindly make modifications in the opensearch-py client generator
# or in the OpenSearch API specification, and run `nox -rs generate`. See DEVELOPER_GUIDE.md
# and https://github.com/opensearch-project/opensearch-api-specification for details.
# -----------------------------------------------------------------------------------------+


#replace_token#


from __future__ import unicode_literals

import logging
from typing import Any, Type

from ..transport import AsyncTransport, TransportError
from .cat import CatClient
from .client import Client
from .cluster import ClusterClient
from .dangling_indices import DanglingIndicesClient
from .features import FeaturesClient
from .http import HttpClient
from .indices import IndicesClient
from .ingest import IngestClient
from .nodes import NodesClient
from .plugins import PluginsClient
from .remote import RemoteClient
from .remote_store import RemoteStoreClient
from .security import SecurityClient
from .snapshot import SnapshotClient
from .tasks import TasksClient

logger = logging.getLogger("opensearch")


class AsyncOpenSearch(Client):
    """
    OpenSearch client. Provides a straightforward mapping from
    Python to OpenSearch REST endpoints.

    The instance has attributes ``cat``, ``cluster``, ``indices``, ``ingest``,
    ``nodes``, ``snapshot`` and ``tasks`` that provide access to instances of
    :class:`~opensearchpy.client.CatClient`,
    :class:`~opensearchpy.client.ClusterClient`,
    :class:`~opensearchpy.client.IndicesClient`,
    :class:`~opensearchpy.client.IngestClient`,
    :class:`~opensearchpy.client.NodesClient`,
    :class:`~opensearchpy.client.SnapshotClient` and
    :class:`~opensearchpy.client.TasksClient` respectively. This is the
    preferred (and only supported) way to get access to those classes and their
    methods.

    You can specify your own connection class which should be used by providing
    the ``connection_class`` parameter::

        # create connection to localhost using the ThriftConnection
        client = OpenSearch(connection_class=ThriftConnection)

    If you want to turn on sniffing you have several options (described
    in :class:`~opensearchpy.Transport`)::

        # create connection that will automatically inspect the cluster to get
        # the list of active nodes. Start with nodes running on
        # 'opensearchnode1' and 'opensearchnode2'
        client = OpenSearch(
            ['opensearchnode1', 'opensearchnode2'],
            # sniff before doing anything
            sniff_on_start=True,
            # refresh nodes after a node fails to respond
            sniff_on_connection_fail=True,
            # and also every 60 seconds
            sniffer_timeout=60
        )

    Different hosts can have different parameters, use a dictionary per node to
    specify those::

        # connect to localhost directly and another node using SSL on port 443
        # and an url_prefix. Note that ``port`` needs to be an int.
        client = OpenSearch([
            {'host': 'localhost'},
            {'host': 'othernode', 'port': 443, 'url_prefix': 'opensearch', 'use_ssl': True},
        ])

    If using SSL, there are several parameters that control how we deal with
    certificates (see :class:`~opensearchpy.Urllib3HttpConnection` for
    detailed description of the options)::

        client = OpenSearch(
            ['localhost:443', 'other_host:443'],
            # turn on SSL
            use_ssl=True,
            # make sure we verify SSL certificates
            verify_certs=True,
            # provide a path to CA certs on disk
            ca_certs='/path/to/CA_certs'
        )

    If using SSL, but don't verify the certs, a warning message is showed
    optionally (see :class:`~opensearchpy.Urllib3HttpConnection` for
    detailed description of the options)::

        client = OpenSearch(
            ['localhost:443', 'other_host:443'],
            # turn on SSL
            use_ssl=True,
            # no verify SSL certificates
            verify_certs=False,
            # don't show warnings about ssl certs verification
            ssl_show_warn=False
        )

    SSL client authentication is supported
    (see :class:`~opensearchpy.Urllib3HttpConnection` for
    detailed description of the options)::

        client = OpenSearch(
            ['localhost:443', 'other_host:443'],
            # turn on SSL
            use_ssl=True,
            # make sure we verify SSL certificates
            verify_certs=True,
            # provide a path to CA certs on disk
            ca_certs='/path/to/CA_certs',
            # PEM formatted SSL client certificate
            client_cert='/path/to/clientcert.pem',
            # PEM formatted SSL client key
            client_key='/path/to/clientkey.pem'
        )

    Alternatively you can use RFC-1738 formatted URLs, as long as they are not
    in conflict with other options::

        client = OpenSearch(
            [
                'http://user:secret@localhost:9200/',
                'https://user:secret@other_host:443/production'
            ],
            verify_certs=True
        )

    By default, `JSONSerializer
    <https://github.com/opensearch-project/opensearch-py/blob/master/opensearch/serializer.py#L24>`_
    is used to encode all outgoing requests.
    However, you can implement your own custom serializer::

        from opensearchpy.serializer import JSONSerializer

        class SetEncoder(JSONSerializer):
            def default(self, obj):
                if isinstance(obj, set):
                    return list(obj)
                if isinstance(obj, Something):
                    return 'CustomSomethingRepresentation'
                return JSONSerializer.default(self, obj)

        client = OpenSearch(serializer=SetEncoder())

    """

    # include PIT functions inside _patch.py
    from ._patch import (  # type: ignore
        create_point_in_time,
        delete_point_in_time,
        list_all_point_in_time,
    )

    def __init__(
        self,
        hosts: Any = None,
        transport_class: Type[AsyncTransport] = AsyncTransport,
        **kwargs: Any
    ) -> None:
        """
        :arg hosts: list of nodes, or a single node, we should connect to.
            Node should be a dictionary ({"host": "localhost", "port": 9200}),
            the entire dictionary will be passed to the :class:`~opensearchpy.Connection`
            class as kwargs, or a string in the format of ``host[:port]`` which will be
            translated to a dictionary automatically.  If no value is given the
            :class:`~opensearchpy.Connection` class defaults will be used.

        :arg transport_class: :class:`~opensearchpy.Transport` subclass to use.

        :arg kwargs: any additional arguments will be passed on to the
            :class:`~opensearchpy.Transport` class and, subsequently, to the
            :class:`~opensearchpy.Connection` instances.
        """
        super().__init__(hosts, transport_class, **kwargs)

        # namespaced clients for compatibility with API names
        self.cat = CatClient(self)
        self.cluster = ClusterClient(self)
        self.dangling_indices = DanglingIndicesClient(self)
        self.indices = IndicesClient(self)
        self.ingest = IngestClient(self)
        self.nodes = NodesClient(self)
        self.remote = RemoteClient(self)
        self.security = SecurityClient(self)
        self.snapshot = SnapshotClient(self)
        self.tasks = TasksClient(self)
        self.remote_store = RemoteStoreClient(self)

        self.features = FeaturesClient(self)
        self.plugins = PluginsClient(self)
        self.http = HttpClient(self)

    def __repr__(self) -> Any:
        try:
            # get a list of all connections
            cons: Any = self.transport.hosts
            # truncate to 5 if there are too many
            if len(cons) > 5:
                cons = cons[:5] + ["..."]
            return "<{cls}({cons})>".format(cls=self.__class__.__name__, cons=cons)
        except Exception:
            # probably operating on custom transport and connection_pool, ignore
            return super(AsyncOpenSearch, self).__repr__()

    async def __aenter__(self) -> Any:
        if hasattr(self.transport, "_async_call"):
            await self.transport._async_call()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Closes the Transport and all internal connections"""
        await self.transport.close()

    # AUTO-GENERATED-API-DEFINITIONS #