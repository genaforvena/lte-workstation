#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/mesh/chains" "$td/target-repo/artifacts" "$td/default-repo/artifacts" "$td/bin"
printf 'target evidence\n' >"$td/target-repo/artifacts/progress.md"
printf 'wrong repository evidence\n' >"$td/default-repo/artifacts/progress.md"
cat >"$td/plan.tsv" <<EOF
# repository=$td/target-repo
# scope=publishable Tiny Fleet closeout
# artifact_root=$td/target-repo/artifacts
# revision=811bd8d
# next_command=cd $td/target-repo && make verify
EOF
printf 'haunt\tclose\tassemble the targeted repository closeout\n' >>"$td/plan.tsv"

cat >"$td/bin/mesh-chat" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >>"$TEST_BOARD"
EOF
chmod +x "$td/bin/mesh-chat"

base=(
  MESH_DIR="$td/mesh"
  MESH_TASK_DIR="$td/mesh/chains"
  MESH_TASK_CHAT_CMD="$td/bin/mesh-chat"
  TEST_BOARD="$td/board"
  MESH_TASK_ACTOR=haunt
)

env "${base[@]}" python3 "$repo/scripts/mesh-task" create scoped "$td/plan.tsv" >/dev/null
env "${base[@]}" python3 "$repo/scripts/mesh-task" take scoped close >/dev/null

context="$td/mesh/task-context/haunt.json"
python3 - "$context" "$td/target-repo" <<'PY'
import json, sys
row = json.load(open(sys.argv[1], encoding="utf-8"))[0]
assert row["repository"] == sys.argv[2], row
assert row["scope"] == "publishable Tiny Fleet closeout", row
assert row["artifact_root"] == sys.argv[2] + "/artifacts", row
assert row["revision"] == "811bd8d", row
assert row["next_command"].endswith("make verify"), row
PY

if (cd "$td/default-repo" && env "${base[@]}" python3 "$repo/scripts/mesh-task" \
    progress scoped close "$td/default-repo/artifacts/progress.md" \
    'wrong repository receipt' '2026-09-08T05:00:00Z' \
    >"$td/wrong.out" 2>&1); then
  echo 'workspace scope: FAIL (wrong-repository receipt was accepted)' >&2
  exit 1
fi
grep -Fq 'outside expected repository' "$td/wrong.out"

(cd "$td/default-repo" && env "${base[@]}" python3 "$repo/scripts/mesh-task" \
  progress scoped close "$td/target-repo/artifacts/progress.md" \
  'correct repository receipt' '2026-09-08T05:00:00Z' >/dev/null)

grep -Fq "repository=$td/target-repo" "$td/board"
grep -Fq 'scope=publishable Tiny Fleet closeout' "$td/board"
grep -Fq 'artifact-root=' "$td/board"
grep -Fq 'revision=811bd8d' "$td/board"
grep -Fq 'next-command=' "$td/board"

echo 'test-mesh-task-workspace-scope: PASS (explicit repository beats default cwd; wrong-repo receipt rejected; context and board carry scope metadata)'
