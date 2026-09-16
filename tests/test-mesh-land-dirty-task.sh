#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/repo/scripts" "$td/home/.mesh" "$td/bin"
git -C "$td/repo" init -q
git -C "$td/repo" config user.email test@example.invalid
git -C "$td/repo" config user.name test
printf 'seed\n' > "$td/repo/README.md"
git -C "$td/repo" add README.md
git -C "$td/repo" commit -qm seed
git -C "$td/repo" branch -M main
printf 'changed\n' >> "$td/repo/README.md"
printf '#!/usr/bin/env bash\nexit 0\n' > "$td/repo/scripts/mesh-dirty-fixture"
chmod +x "$td/repo/scripts/mesh-dirty-fixture"
printf '%s\n' 'mesh_manifest_source_paths(){ printf "%s\n" scripts/mesh-dirty-fixture; }' > "$td/manifest-reader.sh"
printf '#!/usr/bin/env bash\nexit 0\n' > "$td/bin/mesh-task"
chmod +x "$td/bin/mesh-task"
printf '#!/bin/sh\nexit 0\n' > "$td/bin/mesh-chat"
chmod +x "$td/bin/mesh-chat"

HOME="$td/home" PATH="$td/bin:$PATH" \
  MESH_REPO="$td/repo" MESH_DIR="$td/home/.mesh" \
  MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_SETTLE=0 \
  MESH_LAND_TASK_CMD="$td/bin/mesh-task" \
  MESH_LAND_CHECK_BULK_THRESHOLD=0 MESH_LAND_DIRTY_TASK_STATE="$td/dirty.state" \
  MESH_LAND_DIRTY_TASK_LOG="$td/task-called" MESH_LAND_DIRTY_REPORT="$td/dirty.tsv" \
  bash "$repo_root/scripts/mesh-land" --check > "$td/out" 2>&1 || rc=$?
rc=${rc:-0}
[ "$rc" -eq 1 ] || { echo "FAIL: dirty --check returned rc=$rc" >&2; cat "$td/out" >&2; exit 1; }
grep -q $'\tland-dirty-' "$td/task-called" || {
  echo 'FAIL: dirty --check did not create a landing incident task' >&2; cat "$td/out" >&2; exit 1;
}
grep -q 'dirty-worktree incident=' "$td/out" || { echo 'FAIL: incident was not reported' >&2; exit 1; }
[ -s "$td/dirty.tsv" ] || { echo 'FAIL: dirty report artifact was not written' >&2; exit 1; }

rm -f "$td/task-called"
HOME="$td/home" PATH="$td/bin:$PATH" \
  MESH_REPO="$td/repo" MESH_DIR="$td/home/.mesh" \
  MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_SETTLE=0 \
  MESH_LAND_TASK_CMD="$td/bin/mesh-task" \
  MESH_LAND_CHECK_BULK_THRESHOLD=0 MESH_LAND_DIRTY_TASK_STATE="$td/dirty.state" \
  MESH_LAND_DIRTY_TASK_LOG="$td/task-called-2" MESH_LAND_DIRTY_REPORT="$td/dirty.tsv" \
  bash "$repo_root/scripts/mesh-land" --check > /dev/null 2>&1 || true
[ ! -e "$td/task-called-2" ] || { echo 'FAIL: unchanged dirty state created a duplicate incident task' >&2; exit 1; }
echo 'test-mesh-land-dirty-task: PASS'
