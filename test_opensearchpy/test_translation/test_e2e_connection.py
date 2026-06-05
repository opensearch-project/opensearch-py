"""
test_e2e_connection.py — End-to-End Connection Tests for the Translation Layer

Verifies the complete pipeline works:
    Python Dict → RequestConverter → Protobuf → gRPC Channel → OpenSearch → Response → ResponseConverter → Python Dict

Tests:
    - Connection lifecycle (open, use, close, reopen)
    - Channel persistence across multiple flushes
    - Large batch throughput
    - Concurrent index and query verification
    - Round-trip data integrity (what you send is what you get back)

Run:
    OPENSEARCH_URL="http://localhost:9200" pytest test_opensearchpy/test_translation/test_e2e_connection.py -v -s
"""

import json
import os
import time
import urllib.request

import pytest

from opensearch_grpc.stream_client import StreamClient
from opensearch_grpc.translation import RequestConverter, ResponseConverter


@pytest.fixture(scope="session")
def grpc_host():
    opensearch_url = os.environ.get("OPENSEARCH_URL", "https://localhost:9200")
    grpc_port = os.environ.get("OPENSEARCH_GRPC_PORT", "9400")
    host = opensearch_url.split("://")[-1].split(":")[0].split("@")[-1]
    return f"{host}:{grpc_port}"


@pytest.fixture(scope="session")
def rest_url():
    return os.environ.get("OPENSEARCH_URL", "http://localhost:9200")


@pytest.fixture(scope="session")
def index_name():
    return "test-e2e-connection"


@pytest.fixture(autouse=True, scope="session")
def cleanup(index_name, rest_url):
    _rest_delete(rest_url, f"/{index_name}")
    yield
    _rest_delete(rest_url, f"/{index_name}")


def _rest_delete(base_url, path):
    try:
        req = urllib.request.Request(f"{base_url}{path}", method="DELETE")
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def _rest_get(base_url, path):
    try:
        req = urllib.request.Request(f"{base_url}{path}")
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except Exception:
        return None


class TestConnectionLifecycle:
    """Test that the gRPC connection opens, works, closes, and reopens correctly."""

    def test_connect_and_flush(self, grpc_host, index_name):
        """Basic: open channel, send one doc, get response, close."""
        print("\n[E2E] Testing basic connect → flush → close")
        client = StreamClient(grpc_host, refresh="true")
        client.connect()

        client.index(index_name, body={"test": "lifecycle"}, id="lc-1")
        responses = client.flush()

        assert len(responses) == 1
        assert responses[0]["index"]["result"] == "created"
        print(f"[E2E] ✅ Connected, flushed, got response: {responses[0]['index']['result']}")

        client.close()
        print("[E2E] ✅ Connection closed cleanly")

    def test_context_manager(self, grpc_host, index_name):
        """Context manager opens and closes the connection."""
        print("\n[E2E] Testing context manager lifecycle")
        with StreamClient(grpc_host, refresh="true") as client:
            client.index(index_name, body={"test": "context"}, id="lc-2")
            responses = client.flush()
            assert responses[0]["index"]["result"] == "created"
        print("[E2E] ✅ Context manager opened and closed connection")

    def test_reconnect_after_close(self, grpc_host, index_name):
        """Can reconnect and use client after closing."""
        print("\n[E2E] Testing reconnect after close")
        client = StreamClient(grpc_host, refresh="true")

        # First connection
        client.connect()
        client.index(index_name, body={"round": 1}, id="lc-3")
        client.flush()
        client.close()
        print("[E2E]   First connection done")

        # Second connection on same client
        client.connect()
        client.index(index_name, body={"round": 2}, id="lc-4")
        responses = client.flush()
        client.close()

        assert responses[0]["index"]["result"] == "created"
        print("[E2E] ✅ Reconnected successfully after close")


class TestChannelPersistence:
    """Test that a single channel handles multiple flush cycles."""

    def test_multiple_flushes_same_channel(self, grpc_host, index_name):
        """Send multiple batches on the same connection without reconnecting."""
        print("\n[E2E] Testing multiple flushes on one channel")
        with StreamClient(grpc_host, refresh="true") as client:
            # Batch 1
            client.index(index_name, body={"batch": 1}, id="ch-1")
            r1 = client.flush()
            print(f"[E2E]   Batch 1: {r1[0]['index']['result']}")

            # Batch 2
            client.index(index_name, body={"batch": 2}, id="ch-2")
            client.index(index_name, body={"batch": 3}, id="ch-3")
            r2 = client.flush()
            print(f"[E2E]   Batch 2: {len(r2)} docs")

            # Batch 3
            client.update(index_name, id="ch-1", body={"doc": {"batch": 99}})
            client.delete(index_name, id="ch-2")
            r3 = client.flush()
            print(f"[E2E]   Batch 3: update={r3[0]['update']['result']}, delete={r3[1]['delete']['result']}")

        assert r1[0]["index"]["result"] == "created"
        assert len(r2) == 2
        assert r3[0]["update"]["result"] in ("updated", "noop")
        assert r3[1]["delete"]["result"] == "deleted"
        print("[E2E] ✅ 3 batches on one channel — all succeeded")


class TestLargeBatch:
    """Test throughput with larger document batches."""

    def test_100_documents(self, grpc_host, index_name, rest_url):
        """Index 100 documents in one flush."""
        print("\n[E2E] Indexing 100 documents in one batch")
        start = time.time()

        with StreamClient(grpc_host, refresh="true") as client:
            for i in range(100):
                client.index(index_name, body={"seq": i, "data": f"doc-{i}"}, id=f"bulk-{i}")
            responses = client.flush()

        elapsed = time.time() - start
        print(f"[E2E]   Sent 100 docs in {elapsed:.2f}s ({100/elapsed:.0f} docs/sec)")

        assert len(responses) == 100
        errors = [r for r in responses if "error" in r.get("index", {})]
        assert len(errors) == 0
        print(f"[E2E] ✅ 100 documents indexed, 0 errors, {elapsed:.2f}s")

    def test_auto_flush_batching(self, grpc_host, index_name):
        """Auto-flush sends batches automatically at threshold."""
        print("\n[E2E] Testing auto-flush with batch_size=25")
        batches_flushed = 0

        with StreamClient(grpc_host, batch_size=25, refresh="true") as client:
            for i in range(60):
                result = client.index(index_name, body={"auto": i}, id=f"auto-{i}")
                if result:
                    batches_flushed += 1
                    print(f"[E2E]   Auto-flush #{batches_flushed}: {len(result)} docs")

        # 60 docs / 25 batch_size = 2 auto-flushes + 10 remaining on close
        assert batches_flushed == 2
        print(f"[E2E] ✅ Auto-flushed {batches_flushed} times (remaining flushed on close)")


class TestDataIntegrity:
    """Test that data survives the full round-trip without corruption."""

    def test_complex_document_round_trip(self, grpc_host, index_name, rest_url):
        """Send a complex document and verify every field comes back intact."""
        print("\n[E2E] Testing complex document round-trip")
        original = {
            "title": "Complex Document™",
            "nested": {"level1": {"level2": "deep value"}},
            "tags": ["python", "grpc", "opensearch"],
            "count": 42,
            "price": 9.99,
            "active": True,
            "empty_field": "",
            "unicode": "日本語テスト 🚀",
        }

        with StreamClient(grpc_host, refresh="true") as client:
            client.index(index_name, body=original, id="integrity-1")
            client.flush()

        # Verify via REST
        doc = _rest_get(rest_url, f"/{index_name}/_doc/integrity-1")
        source = doc["_source"]
        print(f"[E2E]   Sent:     {json.dumps(original, ensure_ascii=False)}")
        print(f"[E2E]   Received: {json.dumps(source, ensure_ascii=False)}")

        assert source["title"] == original["title"]
        assert source["nested"]["level1"]["level2"] == "deep value"
        assert source["tags"] == ["python", "grpc", "opensearch"]
        assert source["count"] == 42
        assert source["price"] == 9.99
        assert source["active"] is True
        assert source["unicode"] == "日本語テスト 🚀"
        print("[E2E] ✅ All fields survived round-trip intact (including unicode)")

    def test_request_converter_preserves_data(self, index_name):
        """RequestConverter → build → ResponseConverter.from_proto_request round-trip."""
        print("\n[E2E] Testing RequestConverter → protobuf → ResponseConverter")
        original_body = {"name": "Widget", "price": 29.99, "in_stock": True}

        # Convert to protobuf
        converter = RequestConverter(index=index_name, refresh="true")
        converter.index(body=original_body, id="conv-1")
        request = converter.build()

        # Reconstruct from protobuf
        reconstructed = ResponseConverter.from_proto_request(request)
        print(f"[E2E]   Original:      {original_body}")
        print(f"[E2E]   Reconstructed: {reconstructed['body']}")

        assert reconstructed["operation"] == "index"
        assert reconstructed["index"] == index_name
        assert reconstructed["id"] == "conv-1"
        assert reconstructed["body"] == original_body
        print("[E2E] ✅ Data preserved through protobuf conversion")


class TestErrorRecovery:
    """Test that the client handles errors without breaking the connection."""

    def test_error_doesnt_break_channel(self, grpc_host, index_name):
        """An error in one batch doesn't prevent the next batch from working."""
        print("\n[E2E] Testing error recovery — channel stays alive after error")
        with StreamClient(grpc_host, refresh="true") as client:
            # First: create a doc
            client.index(index_name, body={"x": 1}, id="err-1")
            r1 = client.flush()
            assert r1[0]["index"]["result"] == "created"
            print("[E2E]   Batch 1 (create): OK")

            # Second: try to create same doc (will error)
            client.create(index_name, body={"x": 2}, id="err-1")
            r2 = client.flush()
            assert "error" in r2[0]["create"]
            print(f"[E2E]   Batch 2 (duplicate): Got expected error")

            # Third: channel still works
            client.index(index_name, body={"x": 3}, id="err-2")
            r3 = client.flush()
            assert r3[0]["index"]["result"] == "created"
            print("[E2E]   Batch 3 (after error): OK")

        print("[E2E] ✅ Channel survived error — continued working")
