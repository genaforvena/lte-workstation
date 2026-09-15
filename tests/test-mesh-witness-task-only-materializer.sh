#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"

for legacy in mesh-promises mesh-board mesh-dispatch mesh-chat; do
  cat >"$td/bin/$legacy" <<'EOF'
#!/bin/sh
printf '%s\n' "$0 $*" >>"$LEGACY_CALLED"
exit 91
EOF
  chmod +x "$td/bin/$legacy"
done
cat >"$td/bin/mesh-task" <<'EOF'
#!/bin/sh
test "${1:-}" = audit || exit 92
printf '%b\n' \
  'DONE\talpha\tchain/done\tartifact=/proof' \
  'IGNORED\tbeta\tchain/rejected\treason=unsafe request' \
  'BLOCKED\tgamma\tchain/active\tdependency\twaiting-for-input' \
  'OVERDUE\tepsilon\tchain/overdue\tlease=2026-09-08T00:00:00Z' \
  'QUEUED\tdelta\tchain/queued\tcurrent=chain/active'
EOF
chmod +x "$td/bin/mesh-task"
printf '2026-09-08T07:00:00Z  raw@test  ::  [fyi] source line\n' >"$td/mesh/chat.log"

export LEGACY_CALLED="$td/legacy-called"
PATH="$td/bin:$PATH" MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/mesh/chat.log" \
MESH_WITNESS_COORDINATION_SUMMARY="$td/mesh/tasks.summary" \
  "$repo/scripts/mesh-task-journal" >/dev/null

test ! -e "$LEGACY_CALLED" || { echo 'FAIL: task materializer called legacy coordination tools' >&2; exit 1; }
grep -q '^task_source=PASS$' "$td/mesh/tasks.summary"
! grep -q 'promise_ledger' "$td/mesh/tasks.summary"
grep -Eq '^REJECTED[[:space:]]+beta[[:space:]]+chain/rejected[[:space:]]+reason=unsafe request$' "$td/mesh/tasks.summary"
grep -Eq '^BLOCKED[[:space:]]+gamma[[:space:]]+chain/active[[:space:]]+blocker_type=dependency[[:space:]]+retry=waiting-for-input$' "$td/mesh/tasks.summary"
grep -Eq '^OPEN_UNOWNED[[:space:]]+epsilon[[:space:]]+chain/overdue[[:space:]]+owner_receipt=overdue' "$td/mesh/tasks.summary"
grep -q '^task_rows=5 unfinished_tasks=3 rejected_tasks=1 done_tasks=1$' "$td/mesh/tasks.summary"

tail -n +2 "$td/mesh/tasks.summary" >"$td/first-replay"
PATH="$td/bin:$PATH" MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/mesh/chat.log" \
MESH_WITNESS_COORDINATION_SUMMARY="$td/mesh/tasks.summary" \
  "$repo/scripts/mesh-task-journal" >/dev/null
tail -n +2 "$td/mesh/tasks.summary" >"$td/second-replay"
cmp -s "$td/first-replay" "$td/second-replay" || {
  echo 'FAIL: replaying the same chat.log changed task rows or counts' >&2
  exit 1
}

cat >"$td/bin/mesh-task" <<'EOF'
#!/bin/sh
printf '%b\n' 'REJECTED\tbeta\tchain/bad-rejection\treason='
EOF
chmod +x "$td/bin/mesh-task"
cp "$td/mesh/tasks.summary" "$td/before"
if PATH="$td/bin:$PATH" MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/mesh/chat.log" \
  MESH_WITNESS_COORDINATION_SUMMARY="$td/mesh/tasks.summary" \
  "$repo/scripts/mesh-task-journal" >/dev/null 2>"$td/error"; then
  echo 'FAIL: reasonless REJECTED task was accepted' >&2
  exit 1
fi
cmp -s "$td/before" "$td/mesh/tasks.summary" || {
  echo 'FAIL: failed replay replaced the last valid task view' >&2
  exit 1
}
grep -q 'REJECTED requires reason=' "$td/error"
echo 'PASS: witness materializer is task-only and rejection reasons are mandatory'
