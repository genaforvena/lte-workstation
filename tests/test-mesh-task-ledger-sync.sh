#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/mesh/chains"
printf 'alpha\twork\tproduce a verified artifact\n' >"$td/plan.tsv"
printf 'evidence\n' >"$td/artifact.md"

base_env=(
  MESH_DIR="$td/mesh"
  MESH_TASK_DIR="$td/mesh/chains"
  MESH_TASK_HANDOFF_CMD=/bin/true
  MESH_TASK_ACTOR=alpha
)

env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/true \
  python3 "$repo/scripts/mesh-task" create demo "$td/plan.tsv" ask:demo >/dev/null

if env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/false \
    python3 "$repo/scripts/mesh-task" take demo work >"$td/take.out" 2>"$td/take.err"; then
  echo 'FAIL: take succeeded although its ledger-visible [taking] event was refused' >&2
  exit 1
fi
python3 - "$td/mesh/chains/demo.json" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["status"] == "open", data
assert data["steps"][0]["status"] == "open", data
PY

env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/true \
  python3 "$repo/scripts/mesh-task" take demo work >/dev/null
if env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/false \
    python3 "$repo/scripts/mesh-task" done demo work "$td/artifact.md" verified \
    >"$td/done.out" 2>"$td/done.err"; then
  echo 'FAIL: done succeeded although its ledger-visible [done] event was refused' >&2
  exit 1
fi
python3 - "$td/mesh/chains/demo.json" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
step = data["steps"][0]
assert data["status"] == "active", data
assert step["status"] == "active", data
assert "artifact" not in step, data
PY

if env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/false \
    python3 "$repo/scripts/mesh-task" progress demo work "$td/artifact.md" continue tomorrow \
    >"$td/progress.out" 2>"$td/progress.err"; then
  echo 'FAIL: progress succeeded although its ledger-visible event was refused' >&2
  exit 1
fi
if env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/false \
    python3 "$repo/scripts/mesh-task" block demo work dependency upstream event:upstream \
    >"$td/block.out" 2>"$td/block.err"; then
  echo 'FAIL: block succeeded although its ledger-visible event was refused' >&2
  exit 1
fi
python3 - "$td/mesh/chains/demo.json" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
step = data["steps"][0]
assert data["status"] == "active", data
assert step["status"] == "active", data
assert "progress_artifact" not in step, data
assert "blocker_type" not in step, data
PY

env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/true \
  python3 "$repo/scripts/mesh-task" block demo work dependency upstream event:upstream >/dev/null
if env "${base_env[@]}" MESH_TASK_CHAT_CMD=/bin/false \
    python3 "$repo/scripts/mesh-task" resume demo work upstream-arrived \
    >"$td/resume.out" 2>"$td/resume.err"; then
  echo 'FAIL: resume succeeded although its ledger-visible event was refused' >&2
  exit 1
fi
python3 - "$td/mesh/chains/demo.json" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
step = data["steps"][0]
assert data["status"] == "blocked", data
assert step["status"] == "blocked", data
PY

grep -q 'board event failed' "$td/take.err"
grep -q 'board event failed' "$td/done.err"
grep -q 'board event failed' "$td/progress.err"
grep -q 'board event failed' "$td/block.err"
grep -q 'board event failed' "$td/resume.err"
echo 'test-mesh-task-ledger-sync: PASS'
