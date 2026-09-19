#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/home/.local/bin" "$td/bin" "$td/mesh" "$td/work/docs" "$td/work/scripts" "$td/work/job"
printf '#!/bin/sh\nexit 0\n' > "$td/bin/mesh-chat"
chmod +x "$td/bin/mesh-chat"
printf '#!/bin/sh\nexit 0\n' > "$td/work/scripts/mesh-fixture"
chmod +x "$td/work/scripts/mesh-fixture"

git init -q --bare --initial-branch=master "$td/origin.git"
git init -q --initial-branch=master "$td/work"
git -C "$td/work" config user.name 'mesh-land internal-doc test'
git -C "$td/work" config user.email 'mesh-land-internal-doc@example.invalid'
printf 'seed\n' > "$td/work/README.md"
printf 'private draft\n' > "$td/work/docs/pub-wifi-crossval-decay-note-20260918.md"
git -C "$td/work" add README.md docs/pub-wifi-crossval-decay-note-20260918.md
git -C "$td/work" commit -qm seed
git -C "$td/work" remote add origin "$td/origin.git"
git -C "$td/work" push -q -u origin master
rm "$td/work/docs/pub-wifi-crossval-decay-note-20260918.md"

HOME="$td/home" PATH="$td/bin:/usr/bin:/bin" \
MESH_REPO="$td/work" MESH_DIR="$td/mesh" \
MESH_LAND_CHAT_LOG="$td/chat.log" MESH_LAND_BRANCH=master \
MESH_LAND_PATHS=docs/pub-wifi-crossval-decay-note-20260918.md \
MESH_LAND_ALLOW_INTERNAL_DELETIONS=1 MESH_LAND_SETTLE=0 \
MESH_MANIFEST_READER="$root/scripts/lib/mesh-manifest-reader.sh" \
MESH_MANIFEST_TOOL="$root/scripts/mesh-manifest" \
bash "$root/scripts/mesh-land" --apply 'Remove preserved internal document from git'

if git --git-dir="$td/origin.git" ls-tree -r --name-only refs/heads/master \
  | grep -Fxq 'docs/pub-wifi-crossval-decay-note-20260918.md'; then
  echo 'FAIL: internal document remains on landed master' >&2
  exit 1
fi
echo 'mesh-land internal-doc removal: PASS'
