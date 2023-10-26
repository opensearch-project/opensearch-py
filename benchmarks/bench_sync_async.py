#!/usr/bin/env python

# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import bench_async
import bench_sync

__benchmarks__ = [(bench_sync.test_32, bench_async.test_8, "sync vs. async (8)")]
