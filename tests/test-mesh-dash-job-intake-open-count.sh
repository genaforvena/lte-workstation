#!/usr/bin/env bash
# mesh-dash's job role reads the mesh-job-act RUN TAPE by POSITIONAL field cuts. Until 2026-09-23
# the intake line took the "unanswered" count from cut -f4, but f4 is the SETTLED breakdown
# (discharged=..,expired=..) — so a fully-discharged inbox rendered as a deep backlog. Seen live
# 2026-09-23: tape total=192 discharged=170,expired=22 rendered as
# «ВХОДЯЩИЕ БЕЗ ОТВЕТА: discharged=170,expired=22» while the true open count was 0.
# This gate drives the renderer with a fixture tape so the arithmetic is checked, not the inbox.
set -euo pipefail

DASH="$(command -v mesh-dash)"
[ -n "$DASH" ] || { echo "FAIL: mesh-dash not on PATH"; exit 1; }

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh" "$td/.local/bin"

# mesh-dash --once job reaches the tape through $MESH_DIR; a stub funnel keeps the frame cheap and
# hermetic so the assertion is about the tape arithmetic and nothing else.
printf '#!/bin/sh\necho "job fixture"\n' >"$td/.local/bin/mesh-job-funnel"
chmod +x "$td/.local/bin/mesh-job-funnel"

run(){
  HOME="$td" MESH_DIR="$td/.mesh" PATH="$td/.local/bin:$PATH" \
    "$DASH" --once job 2>&1 | grep '^-- ВХОДЯЩИЕ БЕЗ ОТВЕТА'
}

check(){
  desc="$1" want="$2" row="$3"
  printf '%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)	RUN	$row" >"$td/.mesh/job-act.log"
  got="$(run)"
  case "$got" in
    *"ОТВЕТА: $want (всего"*)
      : ;;
    *) echo "FAIL: $desc"; echo "  tape: $row"; echo "  want open count: $want"; echo "  got : $got"; exit 1 ;;
  esac
}
# The regression itself: 10 rows, 7 discharged + 2 expired, so exactly ONE is still open. The old
# cut -f4 reported the settled counts under the "unanswered" label.
check "a mostly-settled inbox reports the one row still open, not the nine it settled" 1 \
  "total=10	discharged=7,expired=2	oldest_over_h=3.5	join_cov=2/8	intake=ok"

# The denominator the pane exists to carry: total and the settled breakdown both reach the line.
check "a fully-settled inbox reports zero open, not the settled count" 0 \
  "total=3	discharged=1,expired=1,sent-unconfirmed=1	oldest_over_h=0.0	join_cov=0/3	intake=ok"

# Nothing settled at all — the count must not collapse to 0 or to the empty-state word.
check "nothing settled reports every row open" 5 \
  "total=5	none	oldest_over_h=0.0	join_cov=0/5	intake=ok"

# A pre-intake-field row (field 7 absent) must still render a count, not a blank or a parse artifact.
check "an old tape row without the intake field still reports its open count" 1 \
  "total=4	discharged=2,expired=1	oldest_over_h=0.0	join_cov=0/4"

# The settled breakdown stays on the line: a reader needs the denominator to trust the 0.
printf '%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)	RUN	total=192	discharged=170,expired=22	oldest_over_h=0.0	join_cov=13/170	intake=ok" \
  >"$td/.mesh/job-act.log"
got="$(run)"
case "$got" in
  *"(всего 192, закрыто discharged=170,expired=22)"*) : ;;
  *) echo "FAIL: the intake line lost its total/settled denominator"; echo "  got: $got"; exit 1 ;;
esac

echo "PASS: the job intake line reports OPEN rows (total − settled), never the settled counts"
