#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

export HOME="$TMP/home"
export MESH="$TMP/mesh"
export MESH_DIR="$MESH"
export MESH_TASK_DIR="$MESH/chains"
export MESH_OBSERVER_NOW=2026-09-08T12:00:00Z
mkdir -p "$HOME" "$MESH"

cat > "$MESH/chat.log" <<'EOF'
2026-09-08T10:01:00Z  health@node  ::  [health] first
2026-09-08T10:01:00Z  health@node  ::  [health] first
2026-09-08T11:30:00Z  health@node  ::  [health] second
2026-09-08T13:30:00Z health@node :: [health] third
EOF
cat > "$MESH/witness.log" <<'EOF'
2026-09-08T10:02:00Z witness first
2026-09-08T11:31:00Z witness second
2026-09-08T13:31:00Z witness third
EOF
cat > "$MESH/sensors.log" <<'EOF'
2026-09-08T10:03:00Z node sense first
2026-09-08T11:32:00Z node sense second
2026-09-08T11:59:00Z sensor|<script>alert(1)</script>
2026-09-08T13:32:00Z node sense third
EOF
cat > "$MESH/hw-fault.log" <<'EOF'
2026-09-08T11:59:59,999999+00:00 Out of memory: Killed process 123 (llama-server)
2026-09-08T11:59:59,999999+00:00 Out of memory: Killed process 123 (llama-server)
2026-09-08T14:00:00,000000+02:00 Out of memory: Killed process 124 (mesh-voice-clon)
EOF

export MESH_TASK_CHAT_CMD="$TMP/observer-chat"
cat > "$MESH_TASK_CHAT_CMD" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$1" >> "$TEST_BOARD"
EOF
chmod +x "$MESH_TASK_CHAT_CMD"
export TEST_BOARD="$TMP/board"

"$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/first.out"
grep -q 'unique_events=8' "$TMP/first.out"
test -f "$MESH/autopoiesis-observation/analysis/20260908T100000Z-120000Z.md"
grep -q 'deduplicated_events=2' "$MESH/autopoiesis-observation/analysis/20260908T100000Z-120000Z.md"
REPORT="$MESH/autopoiesis-observation/analysis/20260908T100000Z-120000Z.md"
test "$(awk '/^## Event evidence$/{section=1;next} section && /^\|/{n++} END{print n+0}' "$REPORT")" -eq 10
test "$(grep -Fxc '| chat.log | <code>2026-09-08T10:01:00Z health@node :: [health] first</code> |' "$REPORT")" -eq 1
grep -Fqx '| chat.log | <code>2026-09-08T11:30:00Z health@node :: [health] second</code> |' "$REPORT"
grep -Fqx '| witness.log | <code>2026-09-08T10:02:00Z witness first</code> |' "$REPORT"
grep -Fqx '| sensors.log | <code>2026-09-08T10:03:00Z node sense first</code> |' "$REPORT"
grep -Fqx '| sensors.log | <code>2026-09-08T11:59:00Z sensor&#124;&lt;script&gt;alert(1)&lt;/script&gt;</code> |' "$REPORT"
grep -q '^source_rows=10$' "$REPORT"
grep -Fqx '| hw-fault.log | 2 | 1 |' "$REPORT"
test "$(grep -Fxc '| hw-fault.log | <code>2026-09-08T11:59:59,999999+00:00 Out of memory: Killed process 123 (llama-server)</code> |' "$REPORT")" -eq 1
! grep -Fq 'Killed process 124' "$REPORT"
grep -q 'observation-window:20260908T100000Z-120000Z' "$MESH_TASK_DIR/20260908T100000Z-120000Z.json"

if "$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/second.out" 2>&1; then
  :
fi
grep -q 'already exists' "$TMP/second.out"
test -f "$MESH_TASK_DIR/20260908T100000Z-120000Z.json"

cat > "$MESH/hw-fault.log" <<'EOF'
2026-09-08T16:00:00,000000+02:00 Out of memory: Killed process 124 (mesh-voice-clon)
EOF
MESH_OBSERVER_NOW=2026-09-08T14:00:00Z "$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/quiet-fault.out"
grep -q 'unique_events=3' "$TMP/quiet-fault.out"
grep -q '^admitted source=observation-window:20260908T120000Z-140000Z' "$TMP/quiet-fault.out"
QUIET_REPORT="$MESH/autopoiesis-observation/analysis/20260908T120000Z-140000Z.md"
grep -q '^evidence_complete=yes$' "$QUIET_REPORT"
grep -q '^source_rows=3$' "$QUIET_REPORT"
grep -Fqx '| hw-fault.log | 0 | 0 |' "$QUIET_REPORT"
test -f "$MESH_TASK_DIR/20260908T120000Z-140000Z.json"

rm "$MESH/hw-fault.log"
if "$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/incomplete.out"; then
  :
fi
grep -q 'deferred: incomplete admission evidence' "$TMP/incomplete.out"
grep -Fqx -- '- hw-fault.log: unreadable or missing' "$REPORT"

echo 'test-autopoiesis-observer: ok'
