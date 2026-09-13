#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

HOME_DIR="$TMP/home"
MESH_DIR="$TMP/mesh"
TASK_DIR="$MESH_DIR/chains"
mkdir -p "$HOME_DIR" "$MESH_DIR"

cat > "$MESH_DIR/chat.log" <<'EOF'
2026-09-13T15:01:00Z health@node :: first observation
EOF
cat > "$MESH_DIR/witness.log" <<'EOF'
2026-09-13T15:02:00Z witness first observation
EOF
cat > "$MESH_DIR/sensors.log" <<'EOF'
2026-09-13T15:03:00Z node sense first observation
EOF

cat > "$TMP/board" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$TMP/board"

env -i \
  PATH=/usr/bin:/bin \
  HOME="$HOME_DIR" \
  MESH="$MESH_DIR" \
  MESH_DIR="$MESH_DIR" \
  MESH_TASK_DIR="$TASK_DIR" \
  MESH_OBSERVER_NOW=2026-09-13T17:00:00Z \
  MESH_TASK_CHAT_CMD="$TMP/board" \
  MESH_TASK_ACTOR=observer-test \
  "$ROOT/scripts/mesh-autopoiesis-observer" --run > "$TMP/observer.out"

grep -q 'admitted source=observation-window:20260913T150000Z-170000Z' "$TMP/observer.out"
CHAIN="$TASK_DIR/20260913T150000Z-170000Z.json"
test -s "$CHAIN"
test -f "$MESH_DIR/chat.log"
grep -q '\[task-ledger\]' "$MESH_DIR/chat.log"
python3 - "$CHAIN" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    chain = json.load(stream)
assert chain["chain"] == "20260913T150000Z-170000Z"
assert chain["origin"]["source"] == "observation-window:20260913T150000Z-170000Z"
assert chain["steps"][0]["id"] == "20260913T150000Z-170000Z/analyze-observation"
assert chain["dispatch"] == "sent"
PY

cat > "$TMP/incomplete.tsv" <<'EOF'
#origin.kind=need
#origin.source=incomplete-test
health	analyze	incomplete plan
EOF
if env -i \
  PATH=/usr/bin:/bin \
  HOME="$HOME_DIR" \
  MESH="$MESH_DIR" \
  MESH_DIR="$MESH_DIR" \
  MESH_TASK_DIR="$TASK_DIR" \
  MESH_TASK_CHAT_CMD="$TMP/board" \
  "$ROOT/scripts/mesh-autopoiesis" admit --plan "$TMP/incomplete.tsv" > "$TMP/incomplete.out" 2>&1; then
  echo 'incomplete admission unexpectedly succeeded' >&2
  exit 1
fi
grep -q 'incomplete admission envelope: missing hypothesis, question, acceptance, feedback' "$TMP/incomplete.out"

cat > "$TMP/unavailable.tsv" <<'EOF'
#origin.kind=need
#origin.source=unavailable-test
#origin.hypothesis=the task command is selected explicitly
#origin.question=does the adapter report a missing command cleanly?
#origin.acceptance=the adapter exits 127 with an actionable error
#origin.feedback=keep the failure visible
health	check-command	verify command resolution
EOF
if env -i \
  PATH=/usr/bin:/bin \
  HOME="$HOME_DIR" \
  MESH="$MESH_DIR" \
  MESH_DIR="$MESH_DIR" \
  MESH_TASK_DIR="$TASK_DIR" \
  MESH_TASK_BIN="$TMP/missing-mesh-task" \
  "$ROOT/scripts/mesh-autopoiesis" admit --plan "$TMP/unavailable.tsv" > "$TMP/unavailable.out" 2>&1; then
  echo 'missing task command unexpectedly succeeded' >&2
  exit 1
else
  rc=$?
  test "$rc" -eq 127
fi
grep -q "cannot execute mesh-task command '$TMP/missing-mesh-task'" "$TMP/unavailable.out"
if grep -q 'Traceback' "$TMP/unavailable.out"; then
  echo 'missing task command produced a Python traceback' >&2
  exit 1
fi

echo 'test-autopoiesis-admission-cron-path: ok'
