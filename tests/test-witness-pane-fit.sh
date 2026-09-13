#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT
mesh="$fixture/mesh"
mkdir -p "$mesh"

FIXTURE_JOURNAL="$mesh/tasks.journal" FIXTURE_CHAT="$mesh/chat.log" python3 - <<'PY'
import os
from pathlib import Path

journal = Path(os.environ["FIXTURE_JOURNAL"])
rows = [f"QUEUED\tgenome\tfixture-chain/task-{i:02d}\tcurrent=fixture-chain/task-{i:02d} dispatch=sent"
        for i in range(25)]
journal.write_text("\n".join(rows) + "\n", encoding="utf-8")
chat = Path(os.environ["FIXTURE_CHAT"])
chat.write_text("".join(f"2026-09-13T17:00:{i:02d}Z  fixture  :: raw-line-{i:02d}\n"
                        for i in range(20)), encoding="utf-8")
PY

rendered="$(MESH_DIR="$mesh" MESH_TASK_JOURNAL="$mesh/tasks.journal" \
  MESH_DASH_CHAT_LOG="$mesh/chat.log" MESH_DASH_PANE_ROWS=47 MESH_DASH_PANE_COLS=189 \
  "$ROOT/scripts/mesh-dash" --once witness 2>&1)"
viewport="$(printf '%s\n' "$rendered" | tail -n 47)"

printf '%s\n' "$viewport" | grep -q 'WITNESS TASKS — structured unfinished work' \
  || { echo 'FAIL: task heading is outside the 47-row viewport' >&2; exit 1; }
printf '%s\n' "$viewport" | grep -qE 'materialized view: .* · source age=[0-9]+s · authority=' \
  || { echo 'FAIL: exact source-age label is outside the 47-row viewport' >&2; exit 1; }
printf '%s\n' "$viewport" | grep -q '25 unfinished' \
  || { echo 'FAIL: unfinished task count is outside the 47-row viewport' >&2; exit 1; }
task_rows="$(printf '%s\n' "$viewport" | grep -cE '^(QUEUED|RUNNING|OPEN_UNOWNED|BLOCKED|HELD_REJECTED|HELD_EXPIRED)[[:space:]]')"
[ "$task_rows" -ge 20 ] \
  || { echo "FAIL: only $task_rows unfinished task rows fit in the viewport" >&2; exit 1; }
for i in $(seq -w 0 19); do
  printf '%s\n' "$viewport" | grep -q "raw-line-$i" \
    || { echo "FAIL: raw chat line $i is outside the 47-row viewport" >&2; exit 1; }
done
printf 'test-witness-pane-fit: PASS (%s task rows and 20 raw lines visible together)\n' "$task_rows"
