#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LABOR="$ROOT/scripts/mesh-labor"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

setup_case(){
  CASE="$TMP/$1"
  mkdir -p "$CASE/home/.mesh" "$CASE/labour"
  : > "$CASE/spend.log"
  date -u -d '6 minutes ago' +%Y-%m-%dT%H:%M:%SZ > "$CASE/labour/.watermark"
}

run_labor(){
  HOME="$CASE/home" \
    MESH_LABOR_DIR="$CASE/labour" \
    MESH_SPEND_LOG="$CASE/spend.log" \
    MESH_CHAT_LOG="$CASE/chat.log" \
    MESH_LEDGER_DIR="$CASE/ledger" \
    "$LABOR" "$@"
}

append_turn(){
  local stamp="$1" window="$2" task="$3"
  printf '%s turn %s codex openai paid unknown event:test task:%s\n' \
    "$stamp" "$window" "$task" >> "$CASE/spend.log"
}

expect_reconciliation_failure(){
  local out="$CASE/check.out" rc=0
  run_labor --check >"$out" 2>&1 || rc=$?
  if [ "$rc" -eq 0 ] || ! grep -q 'source reconciliation: FAIL' "$out"; then
    cat "$out" >&2
    echo "expected source completeness failure, got rc=$rc" >&2
    exit 1
  fi
}

# Concurrent overlapping feeders must serialize at the watermark+journal boundary.
setup_case concurrency
stamp="$(date -u -d '4 minutes ago' +%Y-%m-%dT%H:%M:%SZ)"
append_turn "$stamp" genome coordination/concurrent
run_labor --feed >"$CASE/feed-a.out" 2>&1 & a=$!
run_labor --feed >"$CASE/feed-b.out" 2>&1 & b=$!
wait "$a"
wait "$b"
run_labor --check >"$CASE/check.out"
grep -q 'source reconciliation: OK' "$CASE/check.out"
grep -q 'source TURN=1 journal TURN=1' "$CASE/check.out"
grep -q 'task_attribution: explicit=1/1' "$CASE/check.out"

# Removing a whole balanced transaction used to pass hledger parity and the old journal<=source gate.
setup_case missing
stamp="$(date -u -d '4 minutes ago' +%Y-%m-%dT%H:%M:%SZ)"
append_turn "$stamp" genome coordination/missing-a
append_turn "$stamp" genome coordination/missing-b
run_labor --feed >/dev/null
python3 - "$CASE/labour/2026.journal" <<'PY'
import re, sys
from pathlib import Path
p=Path(sys.argv[1]); text=p.read_text()
blocks=re.split(r'(?m)(?=^\d{4}-\d\d-\d\d\s+\*)', text)
p.write_text(''.join(b for b in blocks if 'labour feed task:coordination/missing-a' not in b))
PY
expect_reconciliation_failure
grep -q 'parity: OK' "$CASE/check.out"

# A duplicated, still-balanced transaction must fail exact task/window comparison.
setup_case duplicate
stamp="$(date -u -d '4 minutes ago' +%Y-%m-%dT%H:%M:%SZ)"
append_turn "$stamp" genome coordination/duplicate
append_turn "$stamp" genome coordination/other
run_labor --feed >/dev/null
python3 - "$CASE/labour/2026.journal" <<'PY'
import re, sys
from pathlib import Path
p=Path(sys.argv[1]); text=p.read_text()
blocks=re.split(r'(?m)(?=^\d{4}-\d\d-\d\d\s+\*)', text)
target=next(b for b in blocks if 'labour feed task:coordination/duplicate' in b)
p.write_text(''.join(b for b in blocks if 'labour feed task:coordination/other' not in b)+target)
PY
expect_reconciliation_failure
grep -q 'parity: OK' "$CASE/check.out"

# A late-arriving completion whose timestamp is already behind the watermark is unexplained, not free.
setup_case delayed
stamp="$(date -u -d '4 minutes ago' +%Y-%m-%dT%H:%M:%SZ)"
append_turn "$stamp" genome coordination/first
run_labor --feed >/dev/null
late="$(date -u -d '3 minutes ago' +%Y-%m-%dT%H:%M:%SZ)"
append_turn "$late" genome coordination/delayed
expect_reconciliation_failure

# Freeze the feed clock at a source event's second. That second is still open
# for appends, so it must remain beyond the committed watermark.
setup_case open_second
fixed_now="$(date -u +%s)"
append_turn "$(date -u -d "@$fixed_now" +%Y-%m-%dT%H:%M:%SZ)" wake coordination/open-second
mkdir -p "$CASE/home/.local/bin"
printf '#!/usr/bin/env bash\nif [ "$*" = "-u +%%s" ]; then echo %s; else exec /usr/bin/date "$@"; fi\n' \
  "$fixed_now" > "$CASE/home/.local/bin/date"
chmod +x "$CASE/home/.local/bin/date"
run_labor --feed >/dev/null
watermark_epoch="$(date -u -d "$(cat "$CASE/labour/.watermark")" +%s)"
test "$watermark_epoch" -lt "$fixed_now"
run_labor --check >"$CASE/check.out"
grep -q 'not_yet_fed=1' "$CASE/check.out"

echo 'test-mesh-labor-reconciliation: PASS (concurrency, balanced missing/duplicate feeds, delayed event)'
