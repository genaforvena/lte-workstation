#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-wakeup-events"
[ -x "$TOOL" ] || { echo 'FAIL: mesh-wakeup-events is not executable' >&2; exit 1; }
out="$($TOOL --test 2>&1)" || rc=$?
rc="${rc:-0}"
[ "$rc" = 0 ] || [ "$rc" = 2 ] || { echo "FAIL: --test code fault rc=$rc: $out" >&2; exit 1; }
[ "$rc" = 0 ] && grep -q 'REAL /sys/class/wakeup read:' <<<"$out" || {
  echo "FAIL: --test did not report a real wakeup-source read: $out" >&2; exit 1;
}
echo "test-mesh-wakeup-events: PASS (real-read gate rc=$rc)"
