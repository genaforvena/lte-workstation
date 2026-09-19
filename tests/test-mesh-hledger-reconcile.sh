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
[ "${MESH_PROMISE_AUTOREACT:-}" = 0 ] || exit 21
case "${MESH_PROMISES_DIR:-}" in /tmp/mesh-hledger-reconcile.*/promises) ;; *) exit 22;; esac
mkdir -p "$MESH_PROMISES_DIR"
printf 'temporary derived journal\n' > "$MESH_PROMISES_DIR/promises.journal"
printf '%s\n' 'promise-check=PASS'
EOF
cat > "$T/bin/mesh-ledger" <<'EOF'
#!/usr/bin/env bash
[ "${TEST_CHECK_RC:-0}" = 0 ] || exit "$TEST_CHECK_RC"
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
HOME="$T/home" MESH_DIR="$T/home/.mesh" MESH_EVIDENCE_ROOT="$T/home/.mesh/evidence" PATH="$T/bin:$PATH" MESH_RECON_REPO="$T/repo" \
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
grep -q '^source=promises status=KNOWN verdict=PASS$' "$out"

# A deployed copy is outside the genome checkout. With only the standard MESH_REPO contract,
# it must still resolve task receipts and the repository instead of silently reading ~/.local.
deployed_out="$T/deployed-report"
MESH_REPO="$T/repo" MESH_DIR="$T/home/.mesh" MESH_EVIDENCE_ROOT="$T/home/.mesh/evidence" HOME="$T/home" PATH="$T/bin:$PATH" \
  env -u MESH_RECON_REPO "$BIN" --cutoff 2026-09-09T00:01:00Z --output "$deployed_out"
grep -q '^source=artifacts status=KNOWN count=1 ' "$deployed_out"
grep -q '^source=git status=KNOWN ' "$deployed_out"

# Cron invokes an absolute tool path with only the system PATH. Installed sibling
# tools must still be discovered; otherwise every accounting source reads UNKNOWN.
mkdir -p "$T/home/.local/bin"
cp "$T/bin/mesh-task" "$T/bin/mesh-promises" "$T/bin/mesh-ledger" "$T/bin/mesh-labor" "$T/home/.local/bin/"
cron_out="$T/cron-report"
HOME="$T/home" MESH_DIR="$T/home/.mesh" MESH_EVIDENCE_ROOT="$T/home/.mesh/evidence" PATH=/usr/bin:/bin MESH_RECON_REPO="$T/repo" \
  "$BIN" --cutoff 2026-09-09T00:01:00Z --output "$cron_out"
grep -q '^source=task status=KNOWN ' "$cron_out"
for source in promises ledger labor; do
  grep -q "^source=$source status=KNOWN verdict=PASS$" "$cron_out"
done

# Forced deadline termination is UNKNOWN, never a verified accounting failure.
HOME="$T/home" MESH_DIR="$T/home/.mesh" MESH_EVIDENCE_ROOT="$T/home/.mesh/evidence" PATH="$T/bin:$PATH" MESH_RECON_REPO="$T/repo" TEST_CHECK_RC=137 \
  "$BIN" --cutoff 2026-09-09T00:01:00Z --output "$T/killed-report"
grep -q '^source=ledger status=UNKNOWN reason=timeout$' "$T/killed-report"

echo 'test-mesh-hledger-reconcile: PASS'
