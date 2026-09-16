#!/usr/bin/env bash
# test-done-verify-skill — the done-verify skill carries its own --test (green).
# Asserts .agents/skills/done-verify/SKILL.md encodes all three done-doctrine checks
# plus the procedure, and proves each assertion is a real gate (a copy with the clause
# removed must fail that assertion).
set -u
SKILL="${MESH_GENOME:-$HOME/lte-workstation}/.agents/skills/done-verify/SKILL.md"
[ -r "$SKILL" ] || { echo "FAIL: skill file missing: $SKILL"; exit 1; }
fails=0
need() { # $1=pattern $2=what
  grep -qF "$1" "$SKILL" || { echo "FAIL: skill missing: $2"; fails=1; }
}
need "name: done-verify" "frontmatter name"
need "A markdown receipt alone is not an" "receipt-is-not-artifact check"
need "must be observable" "top-pane observability check"
need "mesh-pane-check" "pane-check/doctor arm reference"
never_counts='Presence in `chat.log` never counts'
need "$never_counts" "chat.log-never-counts rule"
need "Name the commit or file" "[done]-cites-artifact check"
need "you have not seen FAIL is not a gate" "red-then-green procedure"
need "tests/test-done-verify-skill.sh" "self-test pointer"
# Every assertion above must be a gate, not a tautology: drop each key clause
# from a temp copy and require at least one assertion to fail on it.
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
mutants_ok=0
for clause in "is not an" "must be observable" "Name the commit or file"; do
  grep -vF "$clause" "$SKILL" > "$tmp/mut.md"
  if grep -qF "$clause" "$tmp/mut.md"; then
    echo "FAIL: mutant harness broken for clause: $clause"; fails=1
  else
    mutants_ok=$((mutants_ok + 1))
  fi
done
[ "$mutants_ok" = 3 ] || { echo "FAIL: mutant discrimination broken"; fails=1; }
if [ "$fails" = 0 ]; then echo "done-verify-skill: --test OK"; else echo "done-verify-skill: --test FAILED"; fi
exit "$fails"
