#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh/chains"
printf 'alpha\twork\tproduce a durable artifact\n' >"$td/plan.tsv"

cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
printf '%s\n' "$1" >>"$TEST_BOARD"
EOF
chmod +x "$td/bin/mesh-chat"

base=(MESH_DIR="$td/mesh" MESH_TASK_DIR="$td/mesh/chains" MESH_TASK_CHAT_CMD="$td/bin/mesh-chat" MESH_TASK_HANDOFF_CMD=/bin/true TEST_BOARD="$td/board")
env "${base[@]}" MESH_TASK_ACTOR=alpha python3 "$repo/scripts/mesh-task" create demo "$td/plan.tsv" >/dev/null

# A successful first delivery is scheduled work, not an orphan: it has a bounded
# owner-receipt window before the witness requeues it.
env "${base[@]}" python3 "$repo/scripts/mesh-task" audit | grep -Fq $'QUEUED\talpha\tdemo/work'

# A sent-but-unclaimed current step is not terminal: it must mint a fresh task
# delivery with the exact take command.
env "${base[@]}" MESH_TASK_ACTOR=witness python3 "$repo/scripts/mesh-task" reschedule demo >/dev/null
[[ "$(grep -Fc '[task]' "$td/board")" -eq 2 ]]
grep -Fq 'Run: mesh-task take demo work' "$td/board"

# An expired active claim remains visible as overdue, but it is never silently
# reclaimed. The owner must explicitly reject or complete it.
env "${base[@]}" MESH_TASK_ACTOR=alpha MESH_TASK_LEASE_SECONDS=-1 python3 "$repo/scripts/mesh-task" take demo work >/dev/null
if env "${base[@]}" MESH_TASK_ACTOR=witness python3 "$repo/scripts/mesh-task" reschedule demo >"$td/expired.out" 2>&1; then
  echo 'FAIL: witness silently re-scheduled an active task after its lease expired' >&2
  exit 1
fi
grep -Fq 'an active task never expires' "$td/expired.out"
env "${base[@]}" python3 "$repo/scripts/mesh-task" audit | grep -Fq $'OVERDUE\talpha\tdemo/work'
python3 - "$td/mesh/chains/demo.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
assert d['status'] == 'active', d
assert d['steps'][0]['status'] == 'active', d
PY
[[ "$(grep -Fc '[task]' "$td/board")" -eq 2 ]]

echo 'test-mesh-task-reschedule: PASS (unclaimed work re-schedules; expired active work stays visible and owner-held)'
