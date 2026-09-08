#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/promises"

cat >"$td/board" <<'EOF'
2026-09-08T00:00:01Z  witness@test  ::  [task] canonical subject: repair the identity parser ; task:wake-coordination-repair-20260908/promise-identity-integrity, owner:mesh-promises/wake, status:open
2026-09-08T00:00:02Z  witness@test  ::  [task] owner: prose fragment only; proof quotes owner:hire, not a work item; status:open
EOF

report="$(MESH_CHAT_LOG="$td/board" MESH_PROMISE_BOARD_STORE= MESH_PROMISES_DIR="$td/promises" \
  MESH_PROMISE_ROSTER=wake MESH_ASK_SINCE=2099-01-01T00:00:00Z \
  MESH_ASK_VOICE_IN="$td/no-voice" MESH_ASK_TG_SENT="$td/no-tg" \
  bash "$repo/scripts/mesh-promises" --json 2>&1)"

grep -q 'wake-coordination-repair-20260908-promise-identity-integrity' <<<"$report" || {
  echo 'FAIL: explicit canonical task key was not replayed' >&2
  printf '%s\n' "$report" >&2
  exit 1
}
if grep -q 'owner-prose-fragment' <<<"$report"; then
  echo 'FAIL: owner/free-text fragment became a standalone promise liability' >&2
  printf '%s\n' "$report" >&2
  exit 1
fi

echo 'test-mesh-promises-identity-integrity: PASS (canonical task tag wins; malformed owner prose is refused)'
