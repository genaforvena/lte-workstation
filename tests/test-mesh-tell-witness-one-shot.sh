#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd -P)"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT
cat > "$fixture/tmux" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$MOCK_TMUX_CALLS"
exit 1
EOF
chmod +x "$fixture/tmux"
for mode in direct automatic keyed; do
  args=()
  case "$mode" in
    automatic) args=(--automatic --origin) ;;
    keyed) args=(--idempotency-key fixture-key) ;;
  esac
  rc=0
  PATH="$fixture:$PATH" MOCK_TMUX_CALLS="$fixture/tmux-calls" \
    MESH_TELL_WAL="$fixture/wal" "$root/scripts/mesh-tell" "${args[@]}" witness \
    PRIVATE-fixture-prompt > "$fixture/output" 2>&1 || rc=$?
  [ "$rc" = 3 ] || { echo "FAIL witness $mode fence rc=$rc"; exit 1; }
  grep -q 'witness is one-shot' "$fixture/output" || { echo "FAIL witness $mode verdict"; exit 1; }
  ! grep -q PRIVATE-fixture-prompt "$fixture/output" || { echo "FAIL witness $mode privacy"; exit 1; }
  [ ! -e "$fixture/tmux-calls" ] && [ ! -e "$fixture/wal" ] || {
    echo "FAIL witness $mode touched a pane or sent WAL"; exit 1;
  }
done
echo 'test-mesh-tell-witness-one-shot: PASS (direct, automatic, keyed refused before pane access)'
