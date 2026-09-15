#!/usr/bin/env bash
set -u

repo=$(cd "$(dirname "$0")/.." && pwd)
cd "$repo"

out=$(mktemp)
trap 'rm -f "$out"' EXIT
reply_before=$(sha256sum "$HOME/.mesh/job/reply-state.json" 2>/dev/null || true)
cal_before=$(sha256sum "$HOME/.mesh/job/cal-state.json" 2>/dev/null || true)

# The fixture drives the whole parser path without contending for the shared HH browser.
MESH_JOB_REPLY_TEST_OFFLINE=1 ./job/mesh-job-reply --test >"$out" 2>&1 || {
  cat "$out" >&2
  exit 1
}
grep -Fq 'mesh-job-reply --test: ok' "$out" || {
  cat "$out" >&2
  exit 1
}
test "$reply_before" = "$(sha256sum "$HOME/.mesh/job/reply-state.json" 2>/dev/null || true)" || {
  echo 'FAIL: parser regression mutated reply state' >&2
  exit 1
}
test "$cal_before" = "$(sha256sum "$HOME/.mesh/job/cal-state.json" 2>/dev/null || true)" || {
  echo 'FAIL: parser regression mutated calendar state' >&2
  exit 1
}

# Wiring proof: the scheduled reflex is still the owner-facing job reflex, and the exact
# dispatched ledger row is durable and owned by job.
grep -Fq 'mesh-job-reply --tg' "$HOME/.mesh/reflexes.cron" || {
  echo 'FAIL: scheduled HH reply reflex is not wired' >&2
  exit 1
}
# The source task is terminal after an owner-authored close. Accept both the
# pre-close leased state and that durable terminal state, but match the exact
# status row so an unrelated description or child task cannot satisfy ownership.
mesh-task status witness-live-unattended-followup-20260908 |
  awk '$2 == "witness-live-unattended-followup-20260908/repair-hh-parser-selector" &&
       $3 ~ /^\[(active|done)\]$/ && $4 == "owner=job" { found=1 }
       END { exit(found ? 0 : 1) }' || {
    echo 'FAIL: HH parser task is not durably owned/taken by job' >&2
    mesh-task status witness-live-unattended-followup-20260908 >&2
    exit 1
  }

echo 'test-job-reply-parser: PASS'
