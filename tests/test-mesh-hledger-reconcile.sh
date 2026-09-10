#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/scripts/mesh-hledger-reconcile"
T="$(mktemp -d -t mesh-hledger-reconcile-test.XXXXXX)"
trap 'rm -rf "$T"' EXIT

mkdir -p "$T/home/.mesh" "$T/repo/docs/task-receipts" "$T/bin"
cat > "$T/home/.mesh/chat.log" <<'EOF'
2026-09-09T00:00:01Z  genome@node :: [task] task-one
EOF
cat > "$T/bin/mesh-task" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' '{"tasks":[{"id":"task-one"}]}'
EOF
cat > "$T/bin/mesh-promises" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'promise-check=PASS'
EOF
cat > "$T/bin/mesh-ledger" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'ledger-check=PASS'
EOF
cat > "$T/bin/mesh-labor" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'labor-check=PASS'
EOF
chmod +x "$T/bin"/*
printf 'receipt\n' > "$T/repo/docs/task-receipts/one.md"
touch -d 2026-09-08T00:00:00Z "$T/repo/docs/task-receipts/one.md"
git -C "$T/repo" init -q
git -C "$T/repo" config user.email test@example.invalid
git -C "$T/repo" config user.name test
git -C "$T/repo" add docs/task-receipts/one.md
git -C "$T/repo" commit -qm fixture

out="$T/report"
set +e
HOME="$T/home" PATH="$T/bin:$PATH" MESH_RECON_REPO="$T/repo" \
  "$BIN" --cutoff 2026-09-09T00:01:00Z --output "$out"
rc=$?
set -e

test "$rc" -eq 0
grep -q '^cutoff=2026-09-09T00:01:00Z$' "$out"
grep -q '^cadence=hourly$' "$out"
grep -q '^source=board status=KNOWN' "$out"
grep -q '^source=task status=KNOWN' "$out"
grep -q '^source=artifacts status=KNOWN' "$out"
grep -q '^difference_class=' "$out"
grep -q '^adjustment_policy=PROPOSE_ONLY' "$out"

# A deployed copy is outside the genome checkout. With only the standard MESH_REPO contract,
# it must still resolve task receipts and the repository instead of silently reading ~/.local.
deployed_out="$T/deployed-report"
MESH_REPO="$T/repo" HOME="$T/home" PATH="$T/bin:$PATH" \
  env -u MESH_RECON_REPO "$BIN" --cutoff 2026-09-09T00:01:00Z --output "$deployed_out"
grep -q '^source=artifacts status=KNOWN count=1 ' "$deployed_out"
grep -q '^source=git status=KNOWN ' "$deployed_out"

echo 'test-mesh-hledger-reconcile: PASS'
