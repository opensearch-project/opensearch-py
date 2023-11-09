# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


from threading import Thread
from typing import Any, Optional


class ThreadWithReturnValue(Thread):
    _target: Any
    _args: Any
    _kwargs: Any

    def __init__(
        self,
        group: Any = None,
        target: Any = None,
        name: Optional[str] = None,
        args: Any = (),
        kwargs: Any = {},
        Verbose: Optional[bool] = None,
    ) -> None:
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self) -> None:
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args: Any) -> Any:
        Thread.join(self, *args)
        return self._return
