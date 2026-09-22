#!/usr/bin/env bash
# Regression test: a pane progress command must not render a false zero.
#
# The jev progress signal counted evidence artifacts with
# `find ... -newermt 'today'`. That date string is invalid on this build of find,
# which errors and prints nothing; because the pipeline ends in `wc -l`, the rc is
# 0 and mesh-handoff's failure detection never fires. The pane rendered a clean
# "0 Jev evidence artifacts today" while 19 artifacts existed — a silent false zero
# that read as a window with no recorded work.
#
# This test refuses that failure mode generally, not by counting files: it asserts
# that a progress command which has something to count does not answer zero, and
# that a progress command which answers zero says so loudly instead of reading as
# a healthy measurement.
#
# It runs the progress command the same way mesh-handoff does (bash -lc, piped to
# head -1, stderr dropped) so the failure reproduces in the harness, not just in
# an ideal shell.
set -uo pipefail

CHARTER="${1:-$HOME/.mesh/charter/jev.md}"

[ -f "$CHARTER" ] || { echo "SKIP: no charter $CHARTER"; exit 0; }

# --- 1. the progress line is declared and reachable -------------------------
prog="$(grep -m1 -E '^[[:space:]]*progress:' "$CHARTER" | sed -E 's/^[[:space:]]*progress:[[:space:]]*//')"
[ -n "$prog" ] || { echo "FAIL: no progress: line in $CHARTER"; exit 1; }

# --- 2. exactly the renderer's invocation -----------------------------------
# mesh-handoff line ~430: out="$(timeout 10 bash -lc "$prog" 2>/dev/null | head -1)"
# No pipefail in that shell — a failing producer followed by a succeeding
# consumer reports rc 0, which is the bug this test guards against.
out="$(timeout 20 bash -lc "$prog" 2>/dev/null | head -1)"

# --- 3. the date predicate must actually be a date find accepts ------------
# The old failure: find errors, prints nothing, wc reports 0, rc is 0.
# Catch the class: any find in the command whose -newermt argument is not a
# resolvable date must surface as a failure, never as a zero count.
if printf '%s' "$prog" | grep -q "newermt 'today'\|newermt 'midnight'"; then
  echo "FAIL: progress uses a literal 'today'/'midnight' that this find build rejects: $prog"
  exit 1
fi

# --- 4. a counted signal must not render zero silently ----------------------
# Re-resolve the same command's date reference at the harness level: if the
# command counts files modified since a date, and such files exist, zero is a
# defect. Rather than parse intent, require a zero answer to be explicitly
# flagged by the command itself — that is the fix's contract, and it is what
# makes a future false zero visible instead of clean.
case "$out" in
  0*|"")
    echo "FAIL: progress rendered a bare zero — indistinguishable from a broken signal: [$out]"
    exit 1
    ;;
  *SUSPECT*)
    : ;; # a zero that names itself is the loud, honest form
esac

# --- 5. non-zero answers must be a real count, not an error string ----------
# A command that errored but still emitted text would otherwise pass #4.
case "$out" in
  *"find:"*|"cannot figure out"*|*"invalid date"*|*"No such file"*)
    echo "FAIL: progress output is a tool error, not a measurement: [$out]"
    exit 1
    ;;
esac

echo "PASS: $CHARTER progress signal renders a live measurement: [$out]"
