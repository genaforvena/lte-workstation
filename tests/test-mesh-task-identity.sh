#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/mesh"
cat >"$td/board" <<'EOF'
2026-09-08T00:00:01Z  witness@test  ::  [task] board-repair-20260907-identity-chain-one/repair: first sibling instruction ; task:board-repair-20260907-identity-chain-one/repair, owner:hire, status:open
2026-09-08T00:00:02Z  witness@test  ::  [task] board-repair-20260907-identity-chain-two/repair: second sibling instruction ; task:board-repair-20260907-identity-chain-two/repair, owner:hire, status:open
2026-09-08T00:00:03Z  hire@test  ::  [@witness] [done] board-repair-20260907-identity-chain-two/repair: second sibling completed ; task:board-repair-20260907-identity-chain-two/repair
EOF

report="$(MESH_CHAT_LOG="$td/board" MESH_PROMISE_BOARD_STORE= MESH_PROMISES_DIR="$td/promises" \
  MESH_PROMISE_ROSTER=hire MESH_ASK_SINCE=2099-01-01T00:00:00Z \
  MESH_ASK_VOICE_IN="$td/no-voice" MESH_ASK_TG_SENT="$td/no-tg" \
  bash "$repo/scripts/mesh-promises" --json 2>&1)"

# The explicit canonical close must keep chain-one open and discharge chain-two.
grep -q 'board-repair-20260907-identity-chain-one-repair' <<<"$report" || {
  echo "FAIL: canonical sibling close discharged the wrong task" >&2
  printf '%s\n' "$report" >&2
  exit 1
}
if grep -q 'board-repair-20260907-identity-chain-two-repair' <<<"$report"; then
  echo "FAIL: canonical sibling close left its own task open" >&2
  printf '%s\n' "$report" >&2
  exit 1
fi

echo 'test-mesh-task-identity: PASS (addressed canonical task close preserves shared-prefix siblings)'
