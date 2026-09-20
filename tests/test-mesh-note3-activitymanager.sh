#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT/scripts/mesh-note3-activitymanager"
test -x "$SCRIPT"
bash -n "$SCRIPT"
fixture=$'realActivity=com.sec.android.mmapp/.AudioPreview\n  mResumedActivity: ActivityRecord{abc u0 com.sec.android.mmapp/.AudioPreview t249}'
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
out="$(HOME="$td" MESH_DIR="$td/.mesh" MESH_EVIDENCE_ROOT="$td/.mesh/evidence" MESH_NOTE3_ACTIVITYMANAGER_RAW_OVERRIDE="$fixture" "$SCRIPT" --log)"
grep -q '^status=OK ' <<<"$out"
grep -q 'component=com.sec.android.mmapp/.AudioPreview' <<<"$out"
grep -q 'package=com.sec.android.mmapp' <<<"$out"
test -s "$td/.mesh/.note3-activitymanager.state"
test -s "$td/.mesh/evidence/note3-activitymanager-20260920/activity.raw"
set +e
unknown="$(HOME="$td" MESH_DIR="$td/other" MESH_NOTE3_SERIAL=missing "$SCRIPT" --log 2>&1)"
rc=$?
set -e
[ "$rc" -eq 2 ]
grep -q '^status=UNKNOWN ' <<<"$unknown"
printf '%s\n' 'PASS: mesh-note3-activitymanager fixture, unavailable path, and artifact writes'
