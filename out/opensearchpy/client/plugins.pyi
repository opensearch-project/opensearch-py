from ..plugins.alerting import AlertingClient as AlertingClient
from .utils import NamespacedClient as NamespacedClient
from typing import Any

class PluginsClient(NamespacedClient):
    alerting: Any
    def __init__(self, client) -> None: ...
