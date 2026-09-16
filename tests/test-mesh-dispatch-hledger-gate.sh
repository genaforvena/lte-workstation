#!/usr/bin/env bash
set -euo pipefail

# Compatibility entrypoint: canonical task queries replaced the retired promise feed.
repo="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$repo/tests/test-mesh-dispatch-query-failure.py"
