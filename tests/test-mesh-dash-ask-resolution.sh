#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.local/bin" "$td/.mesh"
cat >"$td/.local/bin/mesh-witness" <<'EOF'
#!/bin/sh
echo '== witness == self-measurement ledger'
echo '-- ledger tail (last 1 of 1 rows) --'
echo '  2026-09-07T18:20:00Z ask_open=3 ask_stale_h=12.5 ask_resolve=0.750 ask_den=4 ask_p90_h=10.0 ask_unknown=0'
echo '-- pane live: fixture --'
EOF
chmod +x "$td/.local/bin/mesh-witness"
printf '%s\n' '2026-09-07T18:20:00Z nodes=1/1 ask_open=3 ask_stale_h=12.5 ask_resolve=0.750 ask_den=4 ask_p90_h=10.0 ask_unknown=0' >"$td/.mesh/witness.log"
: >"$td/.mesh/chat.log"

out="$(HOME="$td" MESH_DIR="$td/.mesh" PATH="$td/.local/bin:$PATH" bash "$ROOT/scripts/mesh-dash" --once chat 2>&1)"
printf '%s\n' "$out" | grep -F -- '-- ask resolution (age/denominator-gated; UNKNOWN-safe) --' >/dev/null \
  || { echo 'FAIL: dash lacks ask resolution section'; exit 1; }
printf '%s\n' "$out" | grep -F -- 'open=3 oldest_stale_h=12.5 resolved=0.750 denominator=4 p90_h=10.0 unknown=0' >/dev/null \
  || { echo 'FAIL: dash ask resolution values are missing or wrong'; exit 1; }

printf '%s\n' '2026-09-07T18:21:00Z ask_open=UNKNOWN ask_stale_h=UNKNOWN ask_resolve=UNKNOWN ask_den=UNKNOWN ask_p90_h=UNKNOWN ask_unknown=1' >"$td/.mesh/witness.log"
unknown="$(HOME="$td" MESH_DIR="$td/.mesh" PATH="$td/.local/bin:$PATH" bash "$ROOT/scripts/mesh-dash" --once chat 2>&1)"
printf '%s\n' "$unknown" | grep -F -- 'open=UNKNOWN oldest_stale_h=UNKNOWN resolved=UNKNOWN denominator=UNKNOWN p90_h=UNKNOWN unknown=UNKNOWN' >/dev/null \
  || { echo 'FAIL: gated witness values did not remain UNKNOWN'; exit 1; }
printf '%s\n' 'test-mesh-dash-ask-resolution: PASS'

td2="$(mktemp -d)"
trap 'rm -rf "$td" "$td2"' EXIT
mkdir -p "$td2/.local/bin" "$td2/.mesh"
cat >"$td2/.local/bin/mesh-mind-state" <<'EOF'
#!/bin/sh
case "$1" in
  --watch) while :; do sleep 1; done ;;
  *) printf 'IDLE\ttest\n' ;;
esac
EOF
cat >"$td2/.local/bin/mesh-forage" <<'EOF'
#!/bin/sh
printf '{"assigned_tasks":1,"intended_evenness_J":-1,"evenness_J":1,"dominant_lane":"tg","dominant_share":1}\n'
EOF
chmod +x "$td2/.local/bin/mesh-mind-state" "$td2/.local/bin/mesh-forage"
printf 'dispatch 0 300 0 0 ready\n' >"$td2/.mesh/.pace-dispatch.cache"
bounded="$(timeout -k 2 12s env HOME="$td2" MESH_DIR="$td2/.mesh" MESH_DASH_FAST=1 MESH_DASH_PACE_CACHE_ONLY=1 PATH="$td2/.local/bin:$PATH" bash "$ROOT/scripts/mesh-dash" --once minds 2>&1)"
[ "$?" -eq 0 ] || { echo 'FAIL: minds frame did not complete when mesh-mind-state --watch hung'; exit 1; }
printf '%s\n' "$bounded" | grep -F -- '-- division of labour: intended (owner:) vs realized ([done]) allocation (mesh-forage) --' >/dev/null || { echo 'FAIL: minds frame omitted forage section after bounded watch'; exit 1; }
printf '%s\n' "$bounded" | grep -F -- 'intended J=n/a(1 lane)' >/dev/null || { echo 'FAIL: minds frame omitted forage output after bounded watch'; exit 1; }
printf '%s\n' "$bounded" | grep -F -- 'fast render: secondary budget/context probes skipped' >/dev/null || { echo 'FAIL: fast minds frame did not declare its bounded secondary-probe surface'; exit 1; }
printf '%s\n' 'test-mesh-dash-ask-resolution: PASS (bounded minds watch)'
