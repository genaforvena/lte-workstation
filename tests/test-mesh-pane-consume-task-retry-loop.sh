#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-pane-consume"
td="$(mktemp -d)"
pid=""
cleanup(){
  [ -z "$pid" ] || { kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true; }
  rm -rf "$td"
}
trap cleanup EXIT

mkdir -p "$td/bin" "$td/home/.local/bin" "$td/home/.mesh"
cat > "$td/bin/tmux" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  "has-session "*) exit 0 ;;
  "list-windows "*) printf 'demo\n' ;;
  "list-panes "*) printf '0 0\n10 1\n' ;;
  *"capture-pane"*"-S -6"*) printf 'idle mind\n' ;;
  *"capture-pane"*) printf 'stable pane state\n' ;;
  *) exit 2 ;;
esac
EOF
cat > "$td/bin/mesh-task" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  'queue --dispatch --owner demo') exit 0 ;;
  *) exit 2 ;;
esac
EOF
cat > "$td/bin/mesh-tell" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$2" >> "$TASK_PROMPT_LOG"
EOF
cat > "$td/bin/mesh-pace" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$PACE_LOG"
EOF
cat > "$td/bin/mesh-staffing" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$STAFFING_LOG"
printf '{"windows":[{"window":"demo","live":true,"protected":false,"active_holds":0,"eligible":true,"reason":"eligible"}]}\n'
EOF
chmod +x "$td/bin/tmux" "$td/bin/mesh-task" "$td/bin/mesh-tell" "$td/bin/mesh-pace" "$td/bin/mesh-staffing"

export HOME="$td/home"
export PATH="$td/bin:/usr/bin:/bin"
export TASK_PROMPT_LOG="$td/prompts.log"
export PACE_LOG="$td/pace.log"
export STAFFING_LOG="$td/staffing.log"
export MESH_TASK_PICK_RETRY=3
export MESH_SELF_PICK_INTERVAL=3
export MESH_WAKE_REFRACTORY=0
export MESH_PANE_CONSUME_LOG="$td/consumer.log"
export MESH_WAKE_STAMP_DIR="$td/home/.mesh"
export MESH_WAKE_EXPECT_DIR="$td/home/.mesh/wake-expect"

bash "$tool" demo --interval 1 >"$td/driver.out" 2>&1 &
pid=$!
for _ in $(seq 1 40); do
  prompts="$(grep -c 'Do not reject a blocked task' "$TASK_PROMPT_LOG" 2>/dev/null || true)"
  [ "${prompts:-0}" -ge 2 ] && break
  sleep 0.5
done

cadence="$(grep -c 'autonomous self-pick cadence due (3s)' "$td/consumer.log" 2>/dev/null || true)"
admitted="$(grep -c 'autonomous self-pick admitted by mesh-pace (key=self-pick-demo gap=3s)' "$td/consumer.log" 2>/dev/null || true)"
pace="$(grep -c '^self-pick-demo 3$' "$PACE_LOG" 2>/dev/null || true)"
staffing="$(grep -c '^--json$' "$STAFFING_LOG" 2>/dev/null || true)"
prompts="$(grep -c 'Do not reject a blocked task' "$TASK_PROMPT_LOG" 2>/dev/null || true)"
[ "${cadence:-0}" -ge 1 ] || { echo "FAIL: unchanged empty queue did not reach the recurring self-pick cadence" >&2; cat "$td/consumer.log" >&2; exit 1; }
[ "${admitted:-0}" -ge 1 ] && [ "${pace:-0}" -ge 1 ] || { echo "FAIL: self-pick did not pass through mesh-pace" >&2; cat "$td/consumer.log" >&2; exit 1; }
[ "${staffing:-0}" -ge 1 ] || { echo "FAIL: self-pick did not consult live staffing eligibility" >&2; cat "$td/consumer.log" >&2; exit 1; }
[ "${prompts:-0}" -ge 2 ] || { echo "FAIL: the loop did not re-offer self-selection work" >&2; cat "$TASK_PROMPT_LOG" >&2; exit 1; }

kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
pid=""
: > "$TASK_PROMPT_LOG"
: > "$PACE_LOG"
bash "$tool" demo --self-pick >"$td/once.out" 2>&1
once_prompt="$(grep -c 'Do not reject a blocked task' "$TASK_PROMPT_LOG" 2>/dev/null || true)"
once_pace="$(grep -c '^self-pick-demo 3$' "$PACE_LOG" 2>/dev/null || true)"
[ "${once_prompt:-0}" -ge 1 ] && [ "${once_pace:-0}" -ge 1 ] || {
  echo "FAIL: explicit self-pick did not use the same pace-governed prompt path" >&2
  cat "$td/once.out" "$TASK_PROMPT_LOG" "$PACE_LOG" >&2
  exit 1
}

echo 'test-mesh-pane-consume-task-retry-loop: PASS'
