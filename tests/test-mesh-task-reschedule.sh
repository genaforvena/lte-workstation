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

# An expired active claim likewise returns to the exact owner's queue; a live
# claim remains protected by the command's expiry guard.
env "${base[@]}" MESH_TASK_ACTOR=alpha MESH_TASK_LEASE_SECONDS=-1 python3 "$repo/scripts/mesh-task" take demo work >/dev/null
env "${base[@]}" MESH_TASK_ACTOR=witness python3 "$repo/scripts/mesh-task" reschedule demo >/dev/null
python3 - "$td/mesh/chains/demo.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
assert d['status'] == 'open', d
assert d['steps'][0]['status'] == 'open', d
assert d['dispatch'] == 'sent', d
PY
[[ "$(grep -Fc '[task]' "$td/board")" -eq 3 ]]
grep -Fq '[yield] demo/work: expired active claim re-scheduled to exact owner alpha' "$td/board"

# Receipt-before-save is the hostile ordering: the owner has written [taking],
# but its durable state transition has not returned from mesh-chat yet.  A
# witness recovery must wait, reload the canonical state, and withdraw rather
# than publish a stale yield/re-dispatch.
cat >"$td/bin/mesh-chat-held-take" <<'EOF'
#!/bin/sh
printf '%s\n' "$1" >>"$TEST_BOARD"
case "$1" in
  '[taking]'*)
    : >"$TAKE_RECEIPT"
    while [ ! -e "$RELEASE_TAKE" ]; do sleep 0.01; done
    ;;
esac
EOF
chmod +x "$td/bin/mesh-chat-held-take"
env "${base[@]}" MESH_TASK_CHAT_CMD="$td/bin/mesh-chat-held-take" \
  TAKE_RECEIPT="$td/take-receipt" RELEASE_TAKE="$td/release-take" \
  MESH_TASK_ACTOR=alpha python3 "$repo/scripts/mesh-task" take demo work >"$td/take.out" 2>"$td/take.err" &
take_pid=$!
while [ ! -e "$td/take-receipt" ]; do sleep 0.01; done
# A stalled receipt writer must not blind the witness.  This is a read-only
# snapshot and therefore needs no transition lock.
env "${base[@]}" python3 "$repo/scripts/mesh-task" status demo >"$td/status.out" 2>"$td/status.err" &
status_pid=$!
for _ in $(seq 1 200); do
  kill -0 "$status_pid" 2>/dev/null || break
  sleep 0.01
done
kill -0 "$status_pid" 2>/dev/null && {
  echo 'FAIL: read-only status waited behind the held owner receipt' >&2
  exit 1
}
wait "$status_pid"
grep -Fq 'demo [open]' "$td/status.out"
env "${base[@]}" MESH_TASK_ACTOR=witness python3 "$repo/scripts/mesh-task" reschedule demo >"$td/race.out" 2>"$td/race.err" &
race_pid=$!
sleep 0.05
kill -0 "$race_pid" 2>/dev/null || {
  echo 'FAIL: stale witness re-schedule completed while owner [taking] was held' >&2
  exit 1
}
: >"$td/release-take"
wait "$take_pid"
if wait "$race_pid"; then
  echo 'FAIL: witness re-scheduled a current owner claim' >&2
  exit 1
fi
python3 - "$td/mesh/chains/demo.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
assert d['status'] == 'active', d
assert d['steps'][0]['status'] == 'active', d
PY
[[ "$(grep -Fc '[task]' "$td/board")" -eq 3 ]]
! grep -Fq 'unclaimed dispatch re-scheduled' "$td/board"

echo 'test-mesh-task-reschedule: PASS (sent/unclaimed recovery and receipt race preserve exact owner claim)'
