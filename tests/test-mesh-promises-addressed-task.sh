#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh/promises"
printf '%s\n' '2026-09-07T21:12:19Z  discover@mesh-home  ::  [@genome] [task] next owner:consume docs/design-tg-presence-and-ledger-dispatch-20260907.md for add-read-only-staffing-query' >"$td/.mesh/chat.log"

MESH_DIR="$td/.mesh" MESH_CHAT_LOG="$td/.mesh/chat.log" \
MESH_PROMISES_DIR="$td/.mesh/promises" MESH_PROMISE_BOARD_STORE="" \
MESH_PROMISE_ROSTER="genome discover witness" \
  "$root/scripts/mesh-promises" --feed >"$td/out" 2>"$td/err"

grep -q 'liabilities:promises:genome:next' "$td/.mesh/promises/promises.journal"
! grep -q 'liabilities:promises:unrouted:next' "$td/.mesh/promises/promises.journal"
printf 'test-mesh-promises-addressed-task: PASS\n'

# Old obligations remain in chat.log but are forgotten by the active ledger.
printf '%s\n' \
  '2026-08-01T00:00:00Z  discover@mesh-home  ::  [@genome] [task] ancient owner:genome stale-work' \
  '2026-09-08T00:00:00Z  discover@mesh-home  ::  [@genome] [task] fresh owner:genome current-work' \
  >>"$td/.mesh/chat.log"
MESH_PROMISE_RETIRE_H=168 \
MESH_DIR="$td/.mesh" MESH_CHAT_LOG="$td/.mesh/chat.log" \
MESH_PROMISES_DIR="$td/.mesh/promises" MESH_PROMISE_BOARD_STORE="" \
MESH_PROMISE_ROSTER="genome discover witness" \
  "$root/scripts/mesh-promises" --feed >"$td/retire-out" 2>"$td/retire-err"

grep -q 'liabilities:promises:genome:fresh' "$td/.mesh/promises/promises.journal"
! grep -q 'liabilities:promises:genome:ancient' "$td/.mesh/promises/promises.journal"
MESH_DIR="$td/.mesh" MESH_CHAT_LOG="$td/.mesh/chat.log" \
MESH_PROMISES_DIR="$td/.mesh/promises" MESH_PROMISE_BOARD_STORE="" \
MESH_PROMISE_ROSTER="genome discover witness" MESH_PROMISE_RETIRE_H=168 \
  "$root/scripts/mesh-promises" --report >"$td/retire-report" 2>/dev/null || true
grep -q 'retired 1 promise' "$td/retire-report"
grep -q 'ancient owner:genome stale-work' "$td/.mesh/chat.log"
printf 'test-mesh-promises-retention: PASS\n'
