#!/usr/bin/env bash
set -euo pipefail

tool="$(cd "$(dirname "$0")/.." && pwd)/scripts/mesh-task-journal"
out="$("$tool" --test 2>&1)"
grep -q '^task-only$' <<<"$out"
grep -q '^line-by-line-source-replay$' <<<"$out"
grep -q '^reasoned-rejection$' <<<"$out"
grep -q 'PASS' <<<"$out"
echo 'mesh-task-journal test: PASS (task-only materializer)'
