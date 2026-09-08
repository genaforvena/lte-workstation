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
EOF
cat > "$MESH/witness.log" <<'EOF'
2026-09-08T10:02:00Z witness first
2026-09-08T11:31:00Z witness second
EOF
cat > "$MESH/sensors.log" <<'EOF'
2026-09-08T10:03:00Z node sense first
2026-09-08T11:32:00Z node sense second
EOF

export MESH_TASK_CHAT_CMD="$TMP/observer-chat"
cat > "$MESH_TASK_CHAT_CMD" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$1" >> "$TEST_BOARD"
EOF
chmod +x "$MESH_TASK_CHAT_CMD"
export TEST_BOARD="$TMP/board"

"$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/first.out"
grep -q 'admitted source=observation-window:20260908T100000Z-120000Z' "$TMP/first.out"
grep -q 'unique_events=6' "$TMP/first.out"
test -f "$MESH/autopoiesis-observation/analysis/20260908T100000Z-120000Z.md"
grep -q 'deduplicated_events=1' "$MESH/autopoiesis-observation/analysis/20260908T100000Z-120000Z.md"
grep -q 'observation-window:20260908T100000Z-120000Z' "$MESH_TASK_DIR/20260908T100000Z-120000Z.json"

if "$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/second.out" 2>&1; then
  :
fi
grep -q 'already exists' "$TMP/second.out"
test -f "$MESH_TASK_DIR/20260908T100000Z-120000Z.json"

rm "$MESH/witness.log"
if "$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/incomplete.out"; then
  :
fi
grep -q 'deferred: incomplete admission evidence' "$TMP/incomplete.out"

echo 'test-autopoiesis-observer: ok'
