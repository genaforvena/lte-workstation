#!/usr/bin/env bash
# wrapper: runs the gate self-test
set -uo pipefail
exec "$(dirname "$0")/../scripts/mesh-test-quality-gate" --test
