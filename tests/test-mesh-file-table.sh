#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-file-table"

out="$("$TOOL" --json)"
python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["source"] == "/proc/sys/fs/file-nr"; assert d["allocated"] >= 0; assert d["unused"] >= 0; assert d["maximum"] > 0; assert 0 <= d["allocated_pct"] <= 100' <<<"$out"

set +e
MESH_FILE_NR_PATH="$ROOT/tests/fixtures/mesh-file-table/missing" "$TOOL" --json >/dev/null 2>&1
rc=$?
set -e
[ "$rc" -eq 2 ] || { echo "expected unreachable source exit 2, got $rc" >&2; exit 1; }

"$TOOL" --test
