#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
control="$root/scripts/mesh-mind-control"

# The resolver may report ABSENT (rc 4), but its caller must turn that into a retryable
# hold. This deterministic wiring assertion prevents adjacent-worker fall-through.
grep -q 'owner-tagged task HELD (owner window absent — not generic-picked' "$control"
grep -q 'return 3' "$control"
if sed -n '/if \[ "\$otrc" = 4 \]/,/fi/p' "$control" | grep -q '_pick_agentic'; then
  echo 'explicit absent owner must not call generic picker' >&2
  exit 1
fi

# Full suites exercise exact owner/key semantics, including ask:<id> citations and
# refusal of adjacent acknowledgements.
bash "$control" --test >/dev/null
bash "$root/scripts/mesh-promises" --test >/dev/null

# Job's outbound contract is concrete-only: the charter and calendar gate require all
# assignment fields, while proposed/incomplete rows cannot become operator work.
grep -q 'confirmed interview needs his presence' "$root/charter/job.md"
grep -q 'participants.*exactly one of' "$root/job/README.md"
grep -q -- '--link' "$root/job/README.md"
grep -q -- '--place' "$root/job/README.md"
grep -q -- '--source' "$root/job/README.md"
grep -q 'proposed.*only an' "$root/job/README.md"
grep -q 'Incomplete records are rejected' "$root/job/README.md"
grep -q 'needs-human.*machine-owned' "$root/charter/job.md"
python3 "$root/job/mesh-job-cal" --test >/dev/null
echo 'job dispatch ownership: explicit absent owner holds; exact-key promise suite passes'
