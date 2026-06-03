#!/usr/bin/env python3
"""
client_upload.py — Consumer-side OpenSearch Client (gRPC)

This script simulates a company user uploading document data to OpenSearch.
It mirrors the opensearch-py low-level client API but transports over gRPC.

Usage:
    source ../.venv/bin/activate
    python client_upload.py

Reference: https://docs.opensearch.org/latest/clients/python-low-level/
"""

from opensearch_grpc.simpledoc_gRPC import (
    index_document,
    create_document,
    update_document,
    delete_document,
)

# ─── Configuration (same pattern as opensearch-py) ────────────────────────────

host = "localhost"
grpc_port = 9400
grpc_host = f"{host}:{grpc_port}"

index_name = "company-products"


# ─── Create an index (via REST for now, gRPC doesn't support index creation) ──

print("=" * 60)
print("OpenSearch Client — Document Upload (gRPC Transport)")
print("=" * 60)
print(f"Target: {grpc_host}")
print(f"Index:  {index_name}")
print()

# ─── Index documents (like client.index()) ────────────────────────────────────

print("─" * 60)
print("Indexing company product documents...")
print("─" * 60)
print()

# Document 1
response = index_document(
    index=index_name,
    body={
        "name": "Wireless Headphones",
        "category": "Electronics",
        "price": 79.99,
        "in_stock": True,
        "description": "Noise-cancelling over-ear headphones with 30hr battery",
    },
    id="product-1",
    refresh="true",
    grpc_host=grpc_host,
)
print(f"Result: {response}\n")

# Document 2
response = index_document(
    index=index_name,
    body={
        "name": "Mechanical Keyboard",
        "category": "Electronics",
        "price": 129.99,
        "in_stock": True,
        "description": "RGB mechanical keyboard with Cherry MX switches",
    },
    id="product-2",
    refresh="true",
    grpc_host=grpc_host,
)
print(f"Result: {response}\n")

# Document 3
response = index_document(
    index=index_name,
    body={
        "name": "Standing Desk",
        "category": "Furniture",
        "price": 499.99,
        "in_stock": False,
        "description": "Electric height-adjustable standing desk, 60 inch",
    },
    id="product-3",
    refresh="true",
    grpc_host=grpc_host,
)
print(f"Result: {response}\n")

# ─── Create a document (like client.create()) ─────────────────────────────────

print("─" * 60)
print("Creating a new product (fails if already exists)...")
print("─" * 60)
print()

response = create_document(
    index=index_name,
    body={
        "name": "USB-C Hub",
        "category": "Accessories",
        "price": 49.99,
        "in_stock": True,
        "description": "7-in-1 USB-C hub with HDMI, SD card, and USB 3.0",
    },
    id="product-4",
    refresh="true",
    grpc_host=grpc_host,
)
print(f"Result: {response}\n")

# ─── Update a document (like client.update()) ─────────────────────────────────

print("─" * 60)
print("Updating product price and stock status...")
print("─" * 60)
print()

response = update_document(
    index=index_name,
    id="product-3",
    body={"doc": {"price": 449.99, "in_stock": True}},
    refresh="true",
    grpc_host=grpc_host,
)
print(f"Result: {response}\n")

# ─── Delete a document (like client.delete()) ─────────────────────────────────

print("─" * 60)
print("Deleting discontinued product...")
print("─" * 60)
print()

response = delete_document(
    index=index_name,
    id="product-4",
    refresh="true",
    grpc_host=grpc_host,
)
print(f"Result: {response}\n")

# ─── Summary ──────────────────────────────────────────────────────────────────

print("=" * 60)
print("Upload complete.")
print("=" * 60)
print(f"""
Documents in '{index_name}':
  product-1: Wireless Headphones  ($79.99)
  product-2: Mechanical Keyboard  ($129.99)
  product-3: Standing Desk        ($449.99, updated)
  product-4: USB-C Hub            (deleted)
""")
