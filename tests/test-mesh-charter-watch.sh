#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
set +e
out="$($root/scripts/mesh-charter-watch --test 2>&1)"
rc=$?
set -e
[ "$rc" -eq 0 ] || { echo "$out" >&2; echo "test-mesh-charter-watch: FAIL (tool test rc=$rc)" >&2; exit 1; }
grep -q 'missing charter repaired' <<<"$out"
grep -q 'divergent charter preserved' <<<"$out"
grep -q 'run row written' <<<"$out"
grep -q 'PASS' <<<"$out"
grep -q 'reflex-cadence:' "$root/scripts/mesh-charter-watch"
echo 'test-mesh-charter-watch: PASS'
