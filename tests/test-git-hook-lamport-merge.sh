#!/usr/bin/env bash
set -euo pipefail

hook="$(cd "$(dirname "$0")/.." && pwd)/scripts/git-hooks/commit-msg-lamport"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

git_configure() {
  local repo=$1 name=$2 node=$3
  git -C "$repo" config user.name "$name"
  git -C "$repo" config user.email "$node@example.invalid"
  git -C "$repo" config mesh.node-id "$node"
  install -m 755 "$hook" "$repo/.git/hooks/commit-msg"
}

git -C "$td" init -q seed
git_configure "$td/seed" seed seed
printf 'base\n' > "$td/seed/base"
git -C "$td/seed" add base
GIT_AUTHOR_DATE='2026-09-19T00:00:00Z' GIT_COMMITTER_DATE='2026-09-19T00:00:00Z' \
  git -C "$td/seed" commit -q --no-verify -m 'base'

git clone -q "$td/seed" "$td/alpha"
git clone -q "$td/seed" "$td/beta"
git_configure "$td/alpha" alpha alpha
git_configure "$td/beta" beta beta
git -C "$td/alpha" switch -C alpha >/dev/null 2>&1
git -C "$td/beta" switch -C beta >/dev/null 2>&1

printf 'alpha\n' > "$td/alpha/alpha-stream"
git -C "$td/alpha" add alpha-stream
GIT_AUTHOR_DATE='2026-09-19T00:01:00Z' GIT_COMMITTER_DATE='2026-09-19T00:01:00Z' \
  git -C "$td/alpha" commit -q -m 'alpha concurrent stream'

printf 'beta\n' > "$td/beta/beta-stream"
git -C "$td/beta" add beta-stream
GIT_AUTHOR_DATE='2026-09-19T00:02:00Z' GIT_COMMITTER_DATE='2026-09-19T00:02:00Z' \
  git -C "$td/beta" commit -q -m 'beta concurrent stream'

alpha_commit="$(git -C "$td/alpha" rev-parse HEAD)"
beta_commit="$(git -C "$td/beta" rev-parse HEAD)"
alpha_trailer="$(git -C "$td/alpha" show -s --format='%(trailers:key=Mesh-Lamport,valueonly)' HEAD)"
beta_trailer="$(git -C "$td/beta" show -s --format='%(trailers:key=Mesh-Lamport,valueonly)' HEAD)"
test "$alpha_trailer" = '1@alpha'
test "$beta_trailer" = '1@beta'
test "$alpha_commit" != "$beta_commit"

git -C "$td/alpha" remote add beta "$td/beta"
git -C "$td/alpha" fetch -q beta beta
GIT_AUTHOR_DATE='2026-09-19T00:03:00Z' GIT_COMMITTER_DATE='2026-09-19T00:03:00Z' \
  git -C "$td/alpha" merge --no-edit --no-ff beta/beta >/dev/null

git -C "$td/alpha" cat-file -e "$alpha_commit^{commit}"
git -C "$td/alpha" cat-file -e "$beta_commit^{commit}"
test "$(git -C "$td/alpha" show -s --format='%(trailers:key=Mesh-Lamport,valueonly)' "$alpha_commit")" = "$alpha_trailer"
test "$(git -C "$td/alpha" show -s --format='%(trailers:key=Mesh-Lamport,valueonly)' "$beta_commit")" = "$beta_trailer"

tie_break_key='numeric counter ascending, then node ID ascending (counter@node)'
expected_order="$(printf '%s\n' "$alpha_trailer" "$beta_trailer" | LC_ALL=C sort -t@ -k1,1n -k2,2)"
test "$expected_order" = $'1@alpha\n1@beta'

receipt_path="${MESH_RECEIPT_PATH:-}"
if test -n "$receipt_path"; then
  mkdir -p "$(dirname "$receipt_path")"
  {
    printf '%s\n' '# CRDT Lamport merge fixture receipt'
    printf 'command: %s\n' "${MESH_TEST_COMMAND:-bash tests/test-git-hook-lamport-merge.sh}"
    printf 'alpha_commit: %s\n' "$alpha_commit"
    printf 'alpha_trailer: %s\n' "$alpha_trailer"
    printf 'beta_commit: %s\n' "$beta_commit"
    printf 'beta_trailer: %s\n' "$beta_trailer"
    printf 'tie_break_key: %s\n' "$tie_break_key"
    printf 'merged_repository: %s\n' "$td/alpha"
    printf 'result: PASS\n'
  } > "$receipt_path"
fi

printf 'ok: concurrent Lamport trailers survive merge; equal-counter order=%s\n' "$expected_order"
