#!/usr/bin/env bash
# An isolated lifecycle birth must recover the canonical task pointer before its
# first post-restart progress.  Nothing here addresses a production pane or tape.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh/chains"
printf 'alpha\twork\tproduce a durable artifact\n' >"$td/plan.tsv"
printf 'alpha\tsecond\tqueued second task\n' >"$td/second.tsv"
printf 'restart fixture artifact\n' >"$td/artifact.md"

cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >>"$TEST_BOARD"
EOF
cat >"$td/bin/mesh-handoff" <<'EOF'
#!/bin/sh
exit 0
EOF
cat >"$td/bin/mesh-task" <<'EOF'
#!/bin/sh
exec python3 "$TEST_REPO/scripts/mesh-task" "$@"
EOF
chmod +x "$td/bin/mesh-chat" "$td/bin/mesh-handoff" "$td/bin/mesh-task"

base=(MESH_DIR="$td/mesh" MESH_TASK_DIR="$td/mesh/chains" MESH_TASK_CHAT_CMD="$td/bin/mesh-chat" MESH_TASK_HANDOFF_CMD="$td/bin/mesh-handoff" TEST_BOARD="$td/board" TEST_REPO="$repo" PATH="$td/bin:$PATH")
env "${base[@]}" MESH_TASK_ACTOR=alpha mesh-task create demo "$td/plan.tsv" >/dev/null
env "${base[@]}" MESH_TASK_ACTOR=alpha mesh-task take demo work >/dev/null
env "${base[@]}" MESH_TASK_ACTOR=alpha mesh-task create second "$td/second.tsv" >/dev/null

# This is the interrupted take -> restart boundary: the canonical chain is
# active, while the cache has the historical stale pointer from another task.
mkdir -p "$td/mesh/task-context"
printf '%s\n' '[{"chain":"stale","step":"lost","task":"stale/lost","owner":"alpha","status":"active"}]' >"$td/mesh/task-context/alpha.json"
printf '%s\n' '[{"chain":"demo","step":"work","task":"demo/work","owner":"beta","status":"active"}]' >"$td/mesh/task-context/beta.json"

env "${base[@]}" python3 - <<'PY'
import os
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec

loader = SourceFileLoader("lifecycle", str(Path(os.environ["TEST_REPO"]) / "scripts/mesh-codex-lifecycle"))
spec = spec_from_loader(loader.name, loader)
module = module_from_spec(spec)
spec.loader.exec_module(module)
module.birth("alpha", "restart-alpha")
assert module.active_task("alpha") == "demo/work"
module.birth("beta", "restart-beta")
assert module.active_task("beta") == ""
PY

# No second owner claim can start across the restart, and a foreign owner cannot
# manufacture the first progress receipt for alpha's recovered obligation.
if env "${base[@]}" MESH_TASK_ACTOR=alpha mesh-task take second second >"$td/concurrent.out" 2>&1; then
  echo 'restart continuity: FAIL (second alpha task was claimed)' >&2; exit 1
fi
grep -Fq 'already has active task demo/work' "$td/concurrent.out"
if env "${base[@]}" MESH_TASK_ACTOR=beta mesh-task progress demo work "$td/artifact.md" 'wrong owner' '2026-09-08T03:00:00Z' >"$td/wrong-owner.out" 2>&1; then
  echo 'restart continuity: FAIL (wrong owner fabricated progress)' >&2; exit 1
fi
grep -Fq 'exact owner required' "$td/wrong-owner.out"
env "${base[@]}" MESH_TASK_ACTOR=alpha mesh-task progress demo work "$td/artifact.md" 'run focused verification' '2026-09-08T03:00:00Z' >/dev/null
grep -Fq '[progress] demo/work:' "$td/board"
grep -Fq 'next=run focused verification' "$td/board"

echo 'test-mesh-task-restart-continuity: PASS (restart take->progress, canonical owner, stale/wrong-owner, bounded concurrency)'
