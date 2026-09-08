#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"; td="$(mktemp -d)"; trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"
for name in mesh-promises mesh-board mesh-dispatch; do
  printf '#!/bin/sh\nexit 0\n' >"$td/bin/$name"; chmod +x "$td/bin/$name"
done
cat >"$td/bin/mesh-task" <<'EOF'
#!/bin/sh
if [ "$1" = reschedule-task ]; then
  printf '%s\n' "$2" >>"$TEST_RESCHEDULED"
  exit 0
fi
printf '%s\n' \
 'DONE	genome	tinyfleet-specialists/audit-current-repo	artifact=/tmp/audit.md' \
 'DONE	witness	tinyfleet-specialists/review-eval-method	artifact=/tmp/review.md' \
 'OPEN_UNOWNED	genome	tinyfleet-specialists/mood-lora-bench	dispatch=sent' \
 'EXPIRED	adint	self-adint/device-export	lease=old' \
 'ABANDONED	job	job/operator-ask	lease=old' \
 'BLOCKED	adint	self-adint/device-export	operator-input event:csv'
EOF
cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >>"$TEST_BOARD"
EOF
chmod +x "$td/bin/mesh-task" "$td/bin/mesh-chat"
export PATH="$td/bin:$PATH" MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/mesh/chat.log"
export MESH_WITNESS_PROMISE_STATE="$td/mesh/state" TEST_BOARD="$td/board" TEST_RESCHEDULED="$td/rescheduled"
export MESH_WITNESS_COORDINATION_SUMMARY="$td/mesh/coordination.summary"
: >"$MESH_CHAT_LOG"
"$repo/scripts/mesh-witness-promises" >/dev/null
[[ "$(sort "$TEST_RESCHEDULED")" == $'job/operator-ask\nself-adint/device-export\ntinyfleet-specialists/mood-lora-bench' ]]
[[ "$(wc -l <"$TEST_BOARD")" -eq 3 ]]
grep -q 'tinyfleet-specialists/mood-lora-bench.*OPEN_UNOWNED' "$TEST_BOARD"
grep -q 'self-adint/device-export.*EXPIRED' "$TEST_BOARD"
grep -q 'job/operator-ask.*ABANDONED' "$TEST_BOARD"
! grep -q 'state=BLOCKED' "$TEST_BOARD"
grep -q 'chain_steps=6 findings=4 status=FAIL' "$MESH_WITNESS_COORDINATION_SUMMARY"
grep -q $'DONE\tgenome\ttinyfleet-specialists/audit-current-repo\tartifact=/tmp/audit.md' "$MESH_WITNESS_COORDINATION_SUMMARY"
grep -q 'tinyfleet-specialists/mood-lora-bench' "$MESH_WITNESS_COORDINATION_SUMMARY"
"$repo/scripts/mesh-witness-promises" >/dev/null
[[ "$(wc -l <"$TEST_RESCHEDULED")" -eq 6 ]]
[[ "$(wc -l <"$TEST_BOARD")" -eq 3 ]]
printf 'test-mesh-witness-lifecycle: PASS (adint/tiny-fleet/job alerts, blocked hold, dedup)\n'
