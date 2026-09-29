#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
repo="$td/repo"
home="$td/home"
mesh="$home/.mesh"
bin="$td/bin"
mkdir -p "$repo/scripts/lib" "$repo/docs" "$home" "$mesh" "$bin"
git init -q --bare "$td/origin.git"
git init -q "$repo"
git -C "$repo" config user.email test@example.invalid
git -C "$repo" config user.name test

git -C "$repo" remote add origin "$td/origin.git"
cp "$repo_root/scripts/mesh-land" "$repo/scripts/mesh-land"
cp "$repo_root/scripts/mesh-docs-currentness" "$repo/scripts/mesh-docs-currentness"
cp "$repo_root/scripts/mesh-task" "$repo/scripts/mesh-task"
cp "$repo_root/scripts/mesh_task_log.py" "$repo/scripts/mesh_task_log.py"
cp "$repo_root/scripts/mesh-log-scrub" "$repo/scripts/mesh-log-scrub"
chmod +x "$repo/scripts/mesh-land" "$repo/scripts/mesh-docs-currentness" "$repo/scripts/mesh-task" "$repo/scripts/mesh-log-scrub"

cat > "$repo/scripts/mesh-fixture" <<'EOF'
#!/usr/bin/env bash
[ "${1:-}" = --test ] && { echo 'mesh-fixture --test: PASS'; exit 0; }
exit 0
EOF
chmod +x "$repo/scripts/mesh-fixture"
printf '# Fixture living document\n' > "$repo/docs/mesh-fixture.md"
printf 'scripts/mesh-fixture\tdocs/mesh-fixture.md\tmesh-land-hook\tA committed source change creates one exact-owner docs review.\tscripts/mesh-fixture --test\n' > "$repo/scripts/mesh-docs-currentness.map"
cat > "$td/manifest-reader.sh" <<'EOF'
mesh_manifest_source_paths() { printf '%s\n' scripts/mesh-fixture; }
EOF
cat > "$bin/mesh-chat" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${MESH_LAND_CHAT_LOG:?}"
EOF
cat > "$bin/mesh-autowire" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$bin/mesh-task-chat" <<'EOF'
#!/usr/bin/env bash
if [ "${1:-}" = --task-state ]; then
  exec python3 "$TASK_MODULE" append "$MESH_DIR" mesh-land-hook-test "$2"
fi
printf '%s\n' "${1:-}" >> "${MESH_TASK_CHAT_LOG:?}"
EOF
cat > "$bin/mesh-handoff" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$bin/mesh-chat" "$bin/mesh-autowire" "$bin/mesh-task-chat" "$bin/mesh-handoff"

printf 'seed\n' > "$repo/README.md"
git -C "$repo" add README.md docs/mesh-fixture.md scripts
git -C "$repo" commit -qm seed
git -C "$repo" branch -M main
git -C "$repo" push -q -u origin main
printf '\n# landed source-contract fixture change\n' >> "$repo/scripts/mesh-fixture"
printf '1\n' > "$mesh/docs-currentness.enabled"

export HOME="$home"
export PATH="$bin:$repo/scripts:/usr/bin:/bin"
export MESH_REPO="$repo"
export MESH_DIR="$mesh"
export MESH_LAND_CHAT_LOG="$mesh/chat.log"
export MESH_LAND_PATHS=scripts/mesh-fixture
export MESH_LAND_SETTLE=0
export MESH_LAND_PUSH_TIMEOUT=10
export MESH_MANIFEST_READER="$td/manifest-reader.sh"
export MESH_MANIFEST_TOOL="$td/unused-manifest-tool"
export MESH_DOCS_PILOT_FLAG="$mesh/docs-currentness.enabled"
export MESH_DOCS_CURRENTNESS_MAP="$repo/scripts/mesh-docs-currentness.map"
export MESH_TASK_DIR="$mesh/task-chains"
export MESH_CHAT_LOG="$mesh/chat.log"
export MESH_TASK_CHAT_LOG="$td/task-chat.log"
export MESH_TASK_CHAT_CMD="$bin/mesh-task-chat"
export MESH_TASK_HANDOFF_CMD="$bin/mesh-handoff"
export MESH_TASK_LIVE_OWNERS='docs genome'
export MESH_TASK_MINDSTATE_CMD=
export MESH_TASK_ACTOR=genome
export MESH_EVIDENCE_ROOT="$mesh/evidence"
export MESH_PLANS_DIR="$mesh/plans"
export TASK_MODULE="$repo/scripts/mesh_task_log.py"

if ! bash "$repo/scripts/mesh-land" --apply 'mesh-land: update scripts/mesh-fixture: exercise the post-commit docs-currentness event' > "$td/apply.log" 2>&1; then
  echo 'test-mesh-land-docs-currentness-hook: FAIL (isolated --apply failed)' >&2
  cat "$td/apply.log" >&2
  exit 1
fi
commit="$(git -C "$repo" rev-parse HEAD)"
remote="$(git --git-dir="$td/origin.git" rev-parse refs/heads/main)"
[ "$commit" = "$remote" ] || { echo 'test-mesh-land-docs-currentness-hook: FAIL (isolated commit did not reach its local bare origin)' >&2; cat "$td/apply.log" >&2; exit 1; }
event="$mesh/docs-currentness/$commit.json"
[ -f "$event" ] || { echo 'test-mesh-land-docs-currentness-hook: FAIL (post-commit hook did not write the source event)' >&2; cat "$td/apply.log" >&2; exit 1; }
python3 - "$mesh" "$event" "$commit" <<'PY'
import json
import pathlib
import sys

mesh = pathlib.Path(sys.argv[1])
event_path = pathlib.Path(sys.argv[2])
commit = sys.argv[3]
event = json.loads(event_path.read_text(encoding="utf-8"))
if event.get("revision") != commit or event.get("state") not in (None, "GREEN"):
    raise SystemExit(f"event revision/state mismatch: {event}")
candidates = event.get("candidates", [])
if len(candidates) != 1:
    raise SystemExit(f"expected one mapped docs candidate, got {candidates}")
candidate = candidates[0]
if (candidate.get("source"), candidate.get("document"), candidate.get("contract"), candidate.get("disposition")) != (
    "scripts/mesh-fixture", "docs/mesh-fixture.md", "mesh-land-hook", "created"
):
    raise SystemExit(f"unexpected post-commit candidate: {candidate}")
chain_path = mesh / "task-chains" / f"{candidate['chain']}.json"
chain = json.loads(chain_path.read_text(encoding="utf-8"))
step = chain["steps"][0]
if step.get("owner") != "docs" or step.get("status") != "open" or chain.get("origin", {}).get("kind") != "docs-currentness":
    raise SystemExit(f"post-commit task is not exact-owner/open/docs-currentness: {chain}")
chains = list((mesh / "task-chains").glob("docs-currentness-*.json"))
if len(chains) != 1:
    raise SystemExit(f"expected exactly one docs-currentness task, found {len(chains)}")
PY
printf '%s\n' "$(<"$td/apply.log")" | grep -q 'docs-currentness: created docs-currentness-' || {
  echo 'test-mesh-land-docs-currentness-hook: FAIL (apply output lacks created event)' >&2
  cat "$td/apply.log" >&2
  exit 1
}
echo 'test-mesh-land-docs-currentness-hook: PASS (isolated commit invokes the real event producer and creates one exact docs-owned review task)'