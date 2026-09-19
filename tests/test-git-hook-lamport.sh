#!/usr/bin/env bash
set -euo pipefail

hook="$(cd "$(dirname "$0")/.." && pwd)/scripts/git-hooks/commit-msg-lamport"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

git -C "$td" init -q
git -C "$td" config user.name test
git -C "$td" config user.email test@example.invalid
printf 'first\n' > "$td/msg"

(cd "$td" && "$hook" msg)
grep -q '^Mesh-Lamport: 1@' "$td/msg"
grep -q '^1@' "$td/.git/mesh-lamport.log"

before="$(cat "$td/msg")"
(cd "$td" && "$hook" msg)
test "$(cat "$td/msg")" = "$before"
test "$(wc -l < "$td/.git/mesh-lamport.log")" -eq 1

printf 'second\n' > "$td/msg2"
(cd "$td" && "$hook" msg2)
grep -q '^Mesh-Lamport: 2@' "$td/msg2"
grep -q '^2@' "$td/.git/mesh-lamport.log"

echo 'ok: commit-msg hook adds one monotonic Mesh-Lamport trailer and log entry'
