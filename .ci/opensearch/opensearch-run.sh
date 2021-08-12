#!/bin/bash
set -ex

/usr/share/opensearch/bin/opensearch -Ediscovery.type=single-node
