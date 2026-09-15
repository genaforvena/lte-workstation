#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh" "$td/.local/bin"

cat >"$td/.local/bin/mesh-board" <<'EOF'
#!/usr/bin/env bash
echo 'FAIL: witness top pane must not query the sorted ledger queue' >&2
exit 1
EOF
chmod +x "$td/.local/bin/mesh-board"
cat >"$td/.local/bin/mesh-witness" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' '== witness tape ==' '  fixture=ok'
EOF
chmod +x "$td/.local/bin/mesh-witness"
for n in $(seq 1 40); do printf '2026-09-08T07:00:%02dZ  tester@mesh-home  ::  [fyi] chat-entry-%02d\n' "$n" "$n"; done >"$td/.mesh/chat.log"
cat >"$td/.mesh/tasks.journal" <<'EOF'
task_rows=6 unfinished_tasks=4 rejected_tasks=1 done_tasks=1
REJECTED	tester	rejected/task	reason=terminal history
DONE	tester	done/task	artifact=/tmp/done
BLOCKED	tester	blocked/task	blocker_type=dependency	retry=waiting-for-input
QUEUED	tester	queued/task	dispatch=sent
RUNNING	tester	running/task	lease=2099-01-01T00:00:00Z
HELD_EXPIRED	health	health-warning/expired/triage	retry=next fresh health warning
EOF

out="$(HOME="$td" MESH_DIR="$td/.mesh" MESH_DASH_FAST=1 \
  MESH_DASH_PANE_ROWS=50 MESH_DASH_PANE_COLS=120 \
  "$repo/scripts/mesh-dash" --once witness 2>/dev/null)"

lines="$(printf '%s\n' "$out" | wc -l)"
[ "$lines" -le 50 ] || {
  echo "FAIL: witness queue rendered $lines rows into a 50-row pane" >&2
  exit 1
}
grep -q 'chat.log: showing ' <<<"$out" || {
  echo "FAIL: witness chat view omitted its shown/total coverage line" >&2
  exit 1
}
grep -q 'chat-entry-40' <<<"$out" || {
  echo "FAIL: witness chat view hid the newest chat.log entry" >&2
  exit 1
}
grep -q $'QUEUED\ttester\tqueued/task' <<<"$out" || {
  echo "FAIL: witness omitted an unfinished task" >&2
  exit 1
}
grep -q $'BLOCKED\ttester\tblocked/task\tblocker_type=dependency\tretry=waiting-for-input' <<<"$out" || {
  echo "FAIL: witness omitted a blocked task" >&2
  exit 1
}
grep -q 'tasks: 6 total · 4 unfinished · 1 rejected · 1 done' <<<"$out" || {
  echo "FAIL: witness count omitted HELD_EXPIRED" >&2
  exit 1
}
grep -q $'HELD_EXPIRED\thealth\thealth-warning/expired/triage\tretry=next fresh health warning' <<<"$out" || {
  echo "FAIL: witness omitted HELD_EXPIRED retry semantics" >&2
  exit 1
}
if grep -qE 'rejected/task|done/task' <<<"$out"; then
  echo "FAIL: witness rendered a finished task in the unfinished list" >&2
  exit 1
fi
first="$(grep -o 'chat-entry-[0-9][0-9]' <<<"$out" | head -1)"
[ "$first" = chat-entry-21 ] || {
  echo "FAIL: witness chat view did not preserve chronological tail order (first=$first)" >&2
  exit 1
}
echo "PASS: witness chat.log tail fits the pane and reports coverage"
