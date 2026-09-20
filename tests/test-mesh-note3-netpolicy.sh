#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT/scripts/mesh-note3-netpolicy"
test -x "$SCRIPT"
bash -n "$SCRIPT"
fixture=$'Restrict background: false\nNetwork policies:\n  NetworkPolicy[NetworkTemplate: matchRule=MOBILE_ALL]: cycleDay=15, warningBytes=2147483648, limitBytes=-1, metered=true\n  NetworkPolicy[NetworkTemplate: matchRule=MOBILE_ALL]: cycleDay=4, warningBytes=2147483648, limitBytes=-1, metered=true\nMetered ifaces: {rmnet0}'
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
out="$(HOME="$td" MESH_DIR="$td/.mesh" MESH_EVIDENCE_ROOT="$td/.mesh/evidence" MESH_NOTE3_NETPOLICY_RAW_OVERRIDE="$fixture" "$SCRIPT" --log)"
grep -q '^status=OK ' <<<"$out"
grep -q 'metered_ifaces=rmnet0' <<<"$out"
grep -q 'policy_rows=2' <<<"$out"
grep -q 'metered_policy_rows=2' <<<"$out"
test -s "$td/.mesh/.note3-netpolicy.state"
test -s "$td/.mesh/evidence/note3-netpolicy-20260920/netpolicy.raw"
set +e
unknown="$(HOME="$td" MESH_DIR="$td/other" MESH_NOTE3_SERIAL=missing "$SCRIPT" --log 2>&1)"
rc=$?
set -e
[ "$rc" -eq 2 ]
grep -q 'status=UNKNOWN' <<<"$unknown"
grep -q 'reason=adb_unreachable\|reason=empty_capture' <<<"$unknown"
printf '%s\n' 'PASS: mesh-note3-netpolicy fixture, unavailable path, and artifact writes'
