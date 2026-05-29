#!/usr/bin/env python3
"""
upload_file.py — Upload files to OpenSearch via gRPC (like a regular Python client)

Supports:
    - JSON files (single doc or array of docs)
    - CSV files (each row becomes a document)
    - NDJSON files (newline-delimited JSON, one doc per line)

Usage:
    source ../.venv/bin/activate
    python upload_file.py <filepath> --index <index_name>

Examples:
    python upload_file.py data/products.json --index products
    python upload_file.py data/logs.csv --index logs
    python upload_file.py data/bulk.ndjson --index bulk-data
"""

import argparse
import csv
import json
import os
import sys

from opensearch_grpc.simpledoc_gRPC import index_document


def upload_json(filepath, index, grpc_target, id_field=None):
    """
    Upload a JSON file. Handles both single objects and arrays.

    If the file contains a JSON array, each element is indexed as a separate doc.
    If it contains a single object, it's indexed as one doc.
    """
    print(f"[upload] Reading JSON file: {filepath}")
    with open(filepath, "r") as f:
        data = json.load(f)

    # Normalize to a list of documents
    if isinstance(data, dict):
        docs = [data]
    elif isinstance(data, list):
        docs = data
    else:
        print(f"[upload] ERROR: Unexpected JSON type: {type(data)}")
        return

    print(f"[upload] Found {len(docs)} document(s) to index")
    _index_docs(docs, index, grpc_target, id_field)


def upload_csv(filepath, index, grpc_target, id_field=None):
    """
    Upload a CSV file. Each row becomes a document.

    The first row is used as field names (headers).
    """
    print(f"[upload] Reading CSV file: {filepath}")
    docs = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric strings to numbers where possible
            doc = {}
            for key, val in row.items():
                try:
                    doc[key] = int(val)
                except (ValueError, TypeError):
                    try:
                        doc[key] = float(val)
                    except (ValueError, TypeError):
                        doc[key] = val
            docs.append(doc)

    print(f"[upload] Found {len(docs)} row(s) to index")
    _index_docs(docs, index, grpc_target, id_field)


def upload_ndjson(filepath, index, grpc_target, id_field=None):
    """
    Upload an NDJSON file (one JSON object per line).
    """
    print(f"[upload] Reading NDJSON file: {filepath}")
    docs = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                docs.append(json.loads(line))

    print(f"[upload] Found {len(docs)} document(s) to index")
    _index_docs(docs, index, grpc_target, id_field)


def _index_docs(docs, index, grpc_target, id_field=None):
    """Index a list of documents one at a time via gRPC."""
    success = 0
    errors = 0

    for i, doc in enumerate(docs):
        # Use a field from the doc as the ID if specified
        doc_id = str(doc.pop(id_field)) if id_field and id_field in doc else None

        result = index_document(
            index=index,
            body=doc,
            id=doc_id,
            refresh="false",  # Don't refresh per doc for performance
            grpc_target=grpc_target,
        )

        if "error" in result:
            errors += 1
            print(f"[upload] ERROR doc {i}: {result['error']}")
        else:
            success += 1

    # Final refresh to make all docs searchable
    print(f"\n[upload] Complete: {success} indexed, {errors} errors, {len(docs)} total")


def main():
    parser = argparse.ArgumentParser(description="Upload files to OpenSearch via gRPC")
    parser.add_argument("filepath", help="Path to file (JSON, CSV, or NDJSON)")
    parser.add_argument("--index", required=True, help="Target index name")
    parser.add_argument("--id-field", help="Document field to use as _id")
    parser.add_argument("--grpc-target", default="localhost:9400", help="gRPC endpoint")
    args = parser.parse_args()

    filepath = args.filepath
    if not os.path.exists(filepath):
        print(f"[upload] ERROR: File not found: {filepath}")
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".json":
        upload_json(filepath, args.index, args.grpc_target, args.id_field)
    elif ext == ".csv":
        upload_csv(filepath, args.index, args.grpc_target, args.id_field)
    elif ext in (".ndjson", ".jsonl"):
        upload_ndjson(filepath, args.index, args.grpc_target, args.id_field)
    else:
        print(f"[upload] ERROR: Unsupported file type: {ext}")
        print("[upload] Supported: .json, .csv, .ndjson, .jsonl")
        sys.exit(1)


if __name__ == "__main__":
    main()
