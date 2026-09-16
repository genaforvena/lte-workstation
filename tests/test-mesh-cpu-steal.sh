#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-cpu-steal"

[ -x "$TOOL" ] || { echo "FAIL: mesh-cpu-steal is not executable" >&2; exit 1; }

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
out="$("$TOOL" --test 2>&1)" || rc=$?
rc="${rc:-0}"
[ "$rc" = 0 ] || [ "$rc" = 2 ] || {
  echo "FAIL: --test returned code fault rc=$rc, out=$out" >&2
  exit 1
}
[ "$rc" = 0 ] && printf '%s\n' "$out" | grep -q 'REAL /proc/stat cpu steal=' || {
  echo "FAIL: --test did not report a real /proc/stat reading: $out" >&2
  exit 1
}

echo "test-mesh-cpu-steal: PASS (real-read gate rc=$rc)"
