#!/usr/bin/env bash
# REGRESSION TEST (added by discover STUDY(write-ahead log) 2026-09-23):
# _gate_scrub must recover EVERY intact txn from a crash-shaped journal and never let one
# fragment eat the txn that follows it. The old `getline p1; getline p2` arm recovered 1 of 2.
#
# This drives the REAL _gate_scrub (sourced from scripts/mesh-pace with the gate-log redirected),
# so a regression in the awk body fails here rather than only in a comment.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../scripts/mesh-pace"

T="$(mktemp -d)" || exit 2
trap 'rm -rf "$T"' EXIT
PACE_GATE_LOG="$T/gate.journal"
export PACE_GATE_LOG
export MESH_PACE_BUDGET_OVERRIDE=under          # keep book_gate quiet; we only want _gate_scrub

# craft a journal in the three crash shapes mesh-pace documents plus two intact txns:
#   good | NUL span | severed header (no NUL) | good | severed at posting 1 | good
python3 - "$PACE_GATE_LOG" <<'PYEOF'
import sys
def txn(d, dec, calls):
    return f"{d} * gate d\n    gate:decision:{dec:<12}   1 GATE\n    gate:calls   {calls} GATE\n".encode()
with open(sys.argv[1], "wb") as f:
    f.write(txn("2026-09-23", "keep", 3))
    f.write(b"2026-09-22 * gate d\n\x00\x00\x00\x00\x00\n    gate:calls   9 GATE\n")   # NUL span
    f.write(b"2026-09-21 * gate d\n    gate:de")                                        # severed mid-posting
    f.write(txn("2026-09-20", "drop", 1))
    f.write(b"2026-09-19 * gate d\n    gate:decision:hold")                             # severed at posting 1
    f.write(txn("2026-09-18", "nocap", 2))
PYEOF

# extract the REAL _gate_scrub body: from "_gate_scrub() {" to the first line that is exactly "}"
# (its awk is multi-line, so the stop is the closing brace alone, not any "}")
sed -n '/^_gate_scrub() {/,/^}$/p' "$SRC" > "$T/scrub.sh" 2>/dev/null
# shellcheck source=/dev/null
. "$T/scrub.sh" >/dev/null 2>&1
_gate_scrub >/dev/null 2>&1

out="$PACE_GATE_LOG"
n="$(grep -c '^2026' "$out" 2>/dev/null || echo 0)"

echo "intact txns recovered: $n (expected 3)"
echo "--- recovered ---"
sed -n '1,12p' "$out"
fail=0
[ "$n" -eq 3 ] || { echo "FAIL: expected 3 intact txns, recovered $n"; fail=1; }
# every recovered date must be one of the intact ones — the severed headers must NOT reappear
for d in 2026-09-23 2026-09-20 2026-09-18; do
  grep -q "^$d \* gate" "$out" || { echo "FAIL: intact txn $d was lost"; fail=1; }
done
for d in 2026-09-22 2026-09-21 2026-09-19; do
  grep -q "^$d \* gate" "$out" && { echo "FAIL: crash fragment $d survived as a header"; fail=1; }
done
# the repair must leave its audit trace, and must be idempotent
grep -q '; scrub' "$out" || { echo "FAIL: no ; scrub audit comment left"; fail=1; }
_gate_scrub >/dev/null 2>&1
n2="$(grep -c '^2026' "$out" 2>/dev/null || echo 0)"
[ "$n2" -eq 3 ] || { echo "FAIL: not idempotent — second scrub moved $n -> $n2"; fail=1; }

[ "$fail" -eq 0 ] && echo "PASS: crash-recovery keeps every intact txn, drops every fragment, idempotent"
exit "$fail"
