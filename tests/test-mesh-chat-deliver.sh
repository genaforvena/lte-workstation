#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="${DELIVER_TOOL:-$repo/scripts/mesh-chat-deliver}"
td="$(mktemp -d)"; trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"
cat >"$td/bin/tmux" <<'EOF'
#!/bin/sh
case "$1" in
  list-panes) printf '0 1\n' ;;
  capture-pane) printf 'idle prompt\n' ;;
esac
EOF
cat >"$td/bin/mesh-tell" <<'EOF'
#!/bin/sh
exec "$TEST_CHAOS_EMU" --id chat-deliver --fail-first 2 --rc 75 -- "$TEST_REAL_TELL" "$@"
EOF
cat >"$td/bin/mesh-tell-real" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$TEST_PUSHES"
EOF
cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
if [ "$1" = --targets ]; then printf 'witness\n'; exit; fi
printf '%s  sender@test  ::  [@%s] %s\n' "$(date -u +%FT%TZ)" "$2" "$3" >> "$MESH_CHAT_LOG"
EOF
chmod +x "$td/bin/"*
export PATH="$td/bin:$PATH" MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/mesh/chat.log"
export MESH_CHAT_DELIVER_LEDGER="$td/mesh/ledger.json" MESH_CHAT_DELIVER_LOG="$td/mesh/delivery.log"
export TEST_CHAOS_EMU="$repo/scripts/mesh-chaos-emu" TEST_REAL_TELL="$td/bin/mesh-tell-real"
export MESH_CHAOS_EMU_DIR="$td/chaos-emu"
export MESH_CHAT_DELIVER_IDLE_DELAY=0 MESH_CHAT_DELIVER_MAX_AGE=999999 TEST_PUSHES="$td/pushes"
now="$(date -u +%FT%TZ)"
printf '%s  vpn@test  ::  [@witness] historical pre-ledger fact\n' '2000-01-01T00:00:00Z' >"$MESH_CHAT_LOG"
printf '%s  vpn@test  ::  [@witness] first fact\n' "$now" >>"$MESH_CHAT_LOG"
for _ in 1 2 3 4 5 6 7; do "$tool" --once witness; done
[[ "$(wc -l <"$TEST_PUSHES")" -eq 3 ]]
[[ "$(grep -c '\[delivery-failed\]' "$MESH_CHAT_LOG")" -eq 1 ]]
grep -Eq 'attempts:[0-9a-f]{16}=3' "$MESH_CHAT_LOG"
grep -Eq 'reason:[0-9a-f]{16}=attempt-limit' "$MESH_CHAT_LOG"
first_id="$(sed -n 's/.*msg:\([0-9a-f]\{16\}\).*/\1/p' "$TEST_PUSHES" | head -1)"
[[ -n "$first_id" ]]
printf '%s  witness@test  ::  [@vpn] [ack] ack:%s\n' "$now" "$first_id" >>"$MESH_CHAT_LOG"
before="$(wc -l <"$TEST_PUSHES")"; "$tool" --once witness
[[ "$(wc -l <"$TEST_PUSHES")" -eq "$before" ]]
printf '%s  vpn@test  ::  [@witness] distinct fact\n' "$now" >>"$MESH_CHAT_LOG"
"$tool" --once witness
[[ "$(wc -l <"$TEST_PUSHES")" -eq $((before + 1)) ]]
spaced_id="$(sed -n 's/.*msg:\([0-9a-f]\{16\}\).*/\1/p' "$TEST_PUSHES" | tail -1)"
printf '%s  witness@test  ::  [@vpn] [ack] ack: %s\n' "$now" "$spaced_id" >>"$MESH_CHAT_LOG"
spaced_before="$(wc -l <"$TEST_PUSHES")"; "$tool" --once witness
[[ "$(wc -l <"$TEST_PUSHES")" -eq "$spaced_before" ]]
python3 - "$MESH_CHAT_DELIVER_LEDGER" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))['messages']
assert sorted(x['status'] for x in d.values()) == ['acked','acked','expired-preledger']
assert max(x['attempts'] for x in d.values()) == 3
PY
[ "$($TEST_CHAOS_EMU --count chat-deliver)" -eq 6 ]
printf 'test-mesh-chat-deliver: chaos emulator forced 2 transient mesh-tell failures before recovery\n'
printf 'test-mesh-chat-deliver: PASS (3 attempts, one failure edge, terminal ack, spaced terminal ack, duplicate suppression, fresh id reopen)\n'
