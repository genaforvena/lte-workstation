#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

python3 "$ROOT/scripts/mesh-health-critical-wake" --test
python3 "$ROOT/scripts/mesh-health-warning-task" --test

echo 'test-mesh-health-critical-wake: PASS'
