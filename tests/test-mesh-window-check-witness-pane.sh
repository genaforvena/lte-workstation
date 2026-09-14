#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/home/.mesh"

cat >"$td/bin/tmux" <<'EOF'
#!/usr/bin/env bash
case "$1" in
  list-windows) printf 'witness\n' ;;
  list-panes) printf '0\n' ;;
  display-message)
    case "$*" in *pane_height*) printf '%s\n' "${WINDOW_HEIGHT:-24}" ;; *) printf '0\n' ;; esac
    ;;
  display) printf '0\n' ;;
  capture-pane) cat "$WINDOW_CAPTURE" ;;
  *) echo "unexpected tmux call: $*" >&2; exit 2 ;;
esac
EOF
chmod +x "$td/bin/tmux"

for n in $(seq 1 22); do
  printf 'QUEUED\tgenome\tfixture-chain/task-%02d\tdispatch=sent\n' "$n"
done >"$td/home/.mesh/tasks.journal"
for n in $(seq -w 1 20); do
  printf '2026-09-14T01:00:%02dZ  fixture@mesh-home  :: [fyi] raw-line-%s\n' "$((10#$n))" "$n"
done >"$td/home/.mesh/chat.log"

{
  printf '%s\n' 'WITNESS TASKS — structured unfinished work'
  printf '%s\n' 'materialized view: /tmp/tasks.journal · source age=7s · authority=explicit task-state events'
  printf '%s\n' 'tasks: 22 total · 22 unfinished · 0 rejected · 0 done'
  for n in $(seq -w 1 20); do
    printf 'QUEUED\tgenome\tfixture-chain/task-%s\tdispatch=sent\n' "$n"
  done
  printf '%s\n' 'chat.log: showing 20/20 raw lines (unfiltered tail)'
  cat "$td/home/.mesh/chat.log"
} >"$td/valid-pane"

check() {
  HOME="$td/home" PATH="$td/bin:$PATH" WINDOW_CAPTURE="$1" WINDOW_HEIGHT="${2:-24}" \
    "$ROOT/scripts/mesh-window-check"
}

expect_issue() {
  local pane="$1" expected="$2" out rc=0
  out="$(check "$pane")" || rc=$?
  [ "$rc" -eq 1 ] || { echo "FAIL: incomplete pane exit=$rc, expected 1" >&2; exit 1; }
  printf '%s\n' "$out" | grep -Fq "witness pane $expected" || {
    echo "FAIL: missing witness-pane diagnostic '$expected'" >&2
    printf '%s\n' "$out" >&2
    exit 1
  }
}

if out="$(check "$td/valid-pane")"; then
  printf '%s\n' "$out" | grep -qE '^  witness[[:space:]]+✓ ok$' || {
    echo 'FAIL: complete witness pane was not reported OK' >&2; exit 1;
  }
else
  echo 'FAIL: complete witness pane was reported as an issue' >&2
  printf '%s\n' "$out" >&2
  exit 1
fi

# At 80x11 the renderer publishes an honest compact contract: source age and exact counts, a
# bounded task sample with its omission count, and the newest two unfiltered raw board lines.
{
  printf '%s\n' 'WITNESS TASKS — structured unfinished work'
  printf '%s\n' 'materialized view: /tmp/tasks.journal · source age=7s · authority=explicit task-state events'
  printf '%s\n' 'tasks: 22 total · 22 unfinished · 0 rejected · 0 done'
  for n in 1 2; do
    printf 'QUEUED\tgenome\tfixture-chain/task-%02d\tdispatch=sent\n' "$n"
  done
  printf '%s\n' '… +20 more unfinished (not shown; counts above)'
  printf '%s\n' 'chat.log: showing 2/20 raw lines (unfiltered tail; compact)'
  tail -n 2 "$td/home/.mesh/chat.log"
} >"$td/compact-pane"
if out="$(check "$td/compact-pane" 11)"; then
  printf '%s\n' "$out" | grep -qE '^  witness[[:space:]]+✓ ok$' || {
    echo 'FAIL: compact 80x11 witness pane was not reported OK' >&2; exit 1;
  }
else
  echo 'FAIL: compact 80x11 witness pane was reported as an issue' >&2
  printf '%s\n' "$out" >&2
  exit 1
fi

cp "$td/home/.mesh/tasks.journal" "$td/tasks-full"
head -n 4 "$td/home/.mesh/tasks.journal" >"$td/home/.mesh/tasks.journal.small"
mv "$td/home/.mesh/tasks.journal.small" "$td/home/.mesh/tasks.journal"
{
  printf '%s\n' 'WITNESS TASKS — structured unfinished work'
  printf '%s\n' 'materialized view: /tmp/tasks.journal · source age=7s · authority=explicit task-state events'
  printf '%s\n' 'tasks: 4 total · 4 unfinished · 0 rejected · 0 done'
  for n in $(seq -w 1 4); do
    printf 'QUEUED\tgenome\tfixture-chain/task-%s\tdispatch=sent\n' "$n"
  done
  printf '%s\n' 'chat.log: showing 20/20 raw lines (unfiltered tail)'
  cat "$td/home/.mesh/chat.log"
} >"$td/small-backlog-pane"
if out="$(check "$td/small-backlog-pane")"; then
  printf '%s\n' "$out" | grep -qE '^  witness[[:space:]]+✓ ok$' || {
    echo 'FAIL: pane with fewer than 20 available tasks was not reported OK' >&2; exit 1;
  }
else
  echo 'FAIL: pane with fewer than 20 available tasks was reported as an issue' >&2
  printf '%s\n' "$out" >&2
  exit 1
fi

cp "$td/tasks-full" "$td/home/.mesh/tasks.journal"
expect_issue "$td/small-backlog-pane" 'missing unfinished task count'

sed '/source age=/d' "$td/valid-pane" >"$td/no-age"
expect_issue "$td/no-age" 'missing labelled source age'

sed '/fixture-chain\/task-20/d' "$td/valid-pane" >"$td/short-tasks"
expect_issue "$td/short-tasks" 'only 19/20 unfinished task rows visible'

sed '/raw-line-20/d' "$td/valid-pane" >"$td/short-tail"
expect_issue "$td/short-tail" 'only 19/20 raw chat.log tail lines visible'

echo 'test-mesh-window-check-witness-pane: PASS (visible witness frame contract and failure diagnostics)'
