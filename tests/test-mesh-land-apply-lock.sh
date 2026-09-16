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
printf '#!/usr/bin/env bash\nexit 0\n' > "$td/repo/scripts/mesh-lock-fixture"
chmod +x "$td/repo/scripts/mesh-lock-fixture"
printf '%s\n' 'mesh_manifest_source_paths(){ printf "%s\n" scripts/mesh-lock-fixture; }' > "$td/manifest-reader.sh"
printf '#!/bin/sh\nexit 0\n' > "$td/bin/mesh-chat"
chmod +x "$td/bin/mesh-chat"

exec 9>"$td/land.lock"
flock 9
set +e
HOME="$td/home" PATH="$td/bin:$PATH" MESH_REPO="$td/repo" \
  MESH_MANIFEST_READER="$td/manifest-reader.sh" MESH_LAND_SETTLE=0 \
  MESH_LAND_RUN_LOCK="$td/land.lock" MESH_LAND_PATHS=scripts/mesh-lock-fixture \
  bash "$repo_root/scripts/mesh-land" --apply 'Protect the landing writer with a single lock' >"$td/out" 2>&1
rc=$?
set -e

[ "$rc" -eq 1 ] || { echo "FAIL: --apply ignored an occupied landing lock (rc=$rc)" >&2; cat "$td/out" >&2; exit 1; }
[ "$(git -C "$td/repo" log -1 --format=%s)" = seed ] || {
  echo 'FAIL: --apply committed while another landing writer held the lock' >&2
  exit 1
}
grep -Fq 'overlap refused' "$td/out" || {
  echo 'FAIL: occupied landing lock did not name the overlap' >&2
  cat "$td/out" >&2
  exit 1
}
echo 'test-mesh-land-apply-lock: PASS'
