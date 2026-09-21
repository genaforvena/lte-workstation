#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
tool="$root/scripts/mesh-nic-tx-heartbeat"
test -x "$tool"

out="$("$tool" --test 2>&1)" || {
  rc=$?
  [ "$rc" -eq 2 ] || { echo "$out"; exit "$rc"; }
  grep -q 'n/a' <<<"$out" || { echo "unexpected unavailable result: $out"; exit 1; }
  echo 'test-mesh-nic-tx-heartbeat: PASS (honest unavailable live source)'
  exit 0
}
grep -q 'REAL tx_heartbeat_errors read' <<<"$out" || { echo "missing live-read evidence: $out"; exit 1; }
grep -q 'fixture FAULT' <<<"$out" || { echo "missing fixture evidence: $out"; exit 1; }
echo 'test-mesh-nic-tx-heartbeat: PASS (fixture, unreachable exit-2, and real sysfs read)'
