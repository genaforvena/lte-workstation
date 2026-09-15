#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
test -x "$repo/scripts/mesh-task-journal" || {
  echo 'FAIL: task journal materializer is missing' >&2
  exit 1
}
test ! -e "$repo/scripts/mesh-witness-promises" || {
  echo 'FAIL: retired promise-named materializer still exists' >&2
  exit 1
}
if grep -Eq 'mesh-(promises|claim)|promise ledger|active claims' \
  "$repo/scripts/mesh-task-journal" "$repo/charter/witness.md"; then
  echo 'FAIL: witness contract still references legacy promise/claim coordination' >&2
  exit 1
fi
if grep -q 'witness-coordination\.summary' "$repo/scripts/mesh-task-journal" "$repo/charter/witness.md"; then
  echo 'FAIL: witness contract still names the retired coordination summary' >&2
  exit 1
fi
grep -q 'tasks\.journal' "$repo/scripts/mesh-task-journal"
witness_nudge="$(grep '^[[:space:]]*witness)' "$repo/scripts/mesh-tick")"
if grep -Eqi '\b(promises?|claims?|holds?)\b' <<<"$witness_nudge"; then
  echo 'FAIL: witness tick still instructs legacy promise/claim/hold work' >&2
  exit 1
fi
grep -q 'mesh-task audit' <<<"$witness_nudge"
for retired in scripts/mesh-promises scripts/mesh-promises-watch scripts/mesh-claim scripts/mesh-claim-verify scripts/uxn/mesh-claims-tick; do
  grep -q '^# reflex-cadence: off' "$repo/$retired" || {
    echo "FAIL: legacy coordination reflex remains schedulable: $retired" >&2
    exit 1
  }
done
echo 'PASS: witness contract and tick are task-only'
