#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/home/.local/bin" "$tmp/bin" "$tmp/mesh"
cat > "$tmp/bin/mesh-autowire" <<'EOF'
#!/bin/sh
echo 'mesh-autowire: skipped by branch override test'
EOF
cat > "$tmp/bin/mesh-chat" <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x "$tmp/bin/mesh-autowire" "$tmp/bin/mesh-chat"

git init -q --bare --initial-branch=master "$tmp/origin.git"
git init -q --initial-branch=master "$tmp/work"
git -C "$tmp/work" config user.name 'mesh-land test'
git -C "$tmp/work" config user.email 'mesh-land-test@example.invalid'
git -C "$tmp/work" remote add origin "$tmp/origin.git"
git -C "$tmp/work" config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
printf '# seed\n' > "$tmp/work/README.md"
git -C "$tmp/work" add README.md
git -C "$tmp/work" commit -qm seed
git -C "$tmp/work" push -q -u origin master
git -C "$tmp/work" fetch -q origin master

receipt='docs/reviews/branch-override-2026-09-12.md'
mkdir -p "$tmp/work/docs/reviews"
printf '# branch override fixture\n' > "$tmp/work/$receipt"

HOME="$tmp/home" PATH="$tmp/bin:/usr/bin:/bin" \
MESH_REPO="$tmp/work" MESH_DIR="$tmp/mesh" \
MESH_LAND_CHAT_LOG="$tmp/chat.log" MESH_LAND_BRANCH=master \
MESH_LAND_PATHS="$receipt" MESH_LAND_SETTLE=0 \
bash "$root/scripts/mesh-land" --apply 'Land receipt on master'

local_head="$(git -C "$tmp/work" rev-parse HEAD)"
remote_head="$(git --git-dir="$tmp/origin.git" rev-parse refs/heads/master)"
[[ "$remote_head" == "$local_head" ]] || {
  echo "FAIL: master remote is $remote_head, local landing is $local_head" >&2
  exit 1
}
git --git-dir="$tmp/origin.git" show "refs/heads/master:$receipt" | grep -qx '# branch override fixture'
echo 'mesh-land branch override: PASS'
