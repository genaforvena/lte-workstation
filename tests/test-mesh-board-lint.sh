#!/usr/bin/env bash
# test-mesh-board-lint — thin wrapper: runs the gate self-test.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
exec "$REPO/scripts/mesh-board-lint" --test
