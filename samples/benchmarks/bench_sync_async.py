import bench_async
import bench_sync

__benchmarks__ = [
    (bench_sync.test_32, bench_async.test_8, "sync vs. async (8)")
]