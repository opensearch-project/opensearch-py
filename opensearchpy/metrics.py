# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import time
from abc import ABC, abstractmethod

from events import Events


class Metrics(ABC):
    @abstractmethod
    def request_start(self) -> None:
        pass

    @abstractmethod
    def request_end(self) -> None:
        pass

    @property
    @abstractmethod
    def start_time(self) -> float:
        pass

    @property
    @abstractmethod
    def service_time(self) -> float:
        pass


class MetricsEvents(Metrics):
    @property
    def start_time(self) -> float:
        return self._start_time

    @property
    def service_time(self) -> float:
        return self._service_time

    def __init__(self) -> None:
        self.events = Events()
        self._start_time = 0.0
        self._service_time = 0.0

        # Subscribe to the request_start and request_end events
        self.events.request_start += self._on_request_start
        self.events.request_end += self._on_request_end

    def request_start(self) -> None:
        self.events.request_start()

    def _on_request_start(self) -> None:
        self._start_time = time.perf_counter()

    def request_end(self) -> None:
        self.events.request_end()

    def _on_request_end(self) -> None:
        self._end_time = time.perf_counter()
        self._service_time = self._end_time - self._start_time
