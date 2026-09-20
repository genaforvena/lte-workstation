#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$ROOT/scripts/mesh-note3-gfxinfo"
td="$(mktemp -d -t mesh-note3-gfxinfo-test.XXXXXX)"
trap 'rm -rf "$td"' EXIT
fixture=$'Applications Graphics Acceleration Info:\nGraphics info for pid 4242 [com.example.ui]:\nProfile data in ms:\nDraw:\nView hierarchy:\n  ViewRootImpl #0: 22 views'
out="$(HOME="$td" MESH_DIR="$td/.mesh" MESH_EVIDENCE_ROOT="$td/.mesh/evidence" MESH_NOTE3_GFXINFO_RAW_OVERRIDE="$fixture" "$SCRIPT")"
printf '%s\n' "$out" | grep -q 'status=OK observed_at=.* age_s=0 pid=4242|package=com.example.ui'
test -s "$td/.mesh/.note3-gfxinfo.state"
test -s "$td/.mesh/evidence/note3-gfxinfo-20260920/gfxinfo.raw"
if HOME="$td" MESH_DIR="$td/.mesh-unknown" MESH_NOTE3_SERIAL=missing "$SCRIPT" >/dev/null 2>&1; then
  echo 'FAIL: missing ADB was not UNKNOWN' >&2
  exit 1
else
  test "$?" -eq 2
fi
printf '%s\n' 'PASS: mesh-note3-gfxinfo fixture, fresh sample, and UNKNOWN path'
