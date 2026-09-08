#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"; td="$(mktemp -d)"; trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"
for name in mesh-promises mesh-board mesh-dispatch; do
  printf '#!/bin/sh\nexit 0\n' >"$td/bin/$name"; chmod +x "$td/bin/$name"
done
cat >"$td/bin/mesh-task" <<'EOF'
#!/bin/sh
printf '%s\n' \
 'DONE	genome	tinyfleet-specialists/audit-current-repo	artifact=/tmp/audit.md' \
 'DONE	witness	tinyfleet-specialists/review-eval-method	artifact=/tmp/review.md' \
 'OPEN_UNOWNED	genome	tinyfleet-specialists/mood-lora-bench	dispatch=sent' \
 'REJECTED	adint	self-adint/device-export	reason=operator-declined' \
 'REJECTED	job	job/operator-ask	reason=duplicate-task' \
 'RUNNING	adint	self-adint/device-export	progress=waiting-on-csv'
EOF
cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >>"$TEST_BOARD"
EOF
chmod +x "$td/bin/mesh-task" "$td/bin/mesh-chat"
export PATH="$td/bin:$PATH" MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/mesh/chat.log"
export MESH_WITNESS_COORDINATION_SUMMARY="$td/mesh/coordination.summary"
: >"$MESH_CHAT_LOG"
"$repo/scripts/mesh-task-journal" >/dev/null
grep -q 'chain_steps=6 findings=1 status=FAIL' "$MESH_WITNESS_COORDINATION_SUMMARY"
grep -q $'DONE\tgenome\ttinyfleet-specialists/audit-current-repo\tartifact=/tmp/audit.md' "$MESH_WITNESS_COORDINATION_SUMMARY"
grep -q 'tinyfleet-specialists/mood-lora-bench' "$MESH_WITNESS_COORDINATION_SUMMARY"
grep -q $'REJECTED	adint	self-adint/device-export	reason=operator-declined' "$MESH_WITNESS_COORDINATION_SUMMARY"
! grep -qE 'EXPIRED|ABANDONED|BLOCKED' "$MESH_WITNESS_COORDINATION_SUMMARY"
"$repo/scripts/mesh-task-journal" >/dev/null
printf 'test-mesh-witness-lifecycle: PASS (task-only done/rejected/active rows; no legacy expiry states)\n'
