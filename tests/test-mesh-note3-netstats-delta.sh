#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$ROOT/scripts/mesh-note3-netstats-delta"
test -x "$SCRIPT"
bash -n "$SCRIPT"
grep -q 'status=UNKNOWN' "$SCRIPT"
grep -q 'dumpsys netstats --detail' "$SCRIPT"
grep -q 'rxBytes' "$SCRIPT"
grep -q 'txPackets' "$SCRIPT"
printf 'ok: mesh-note3-netstats-delta static gate\n'
