# Health warning triage — b97e85120d4614c026b9 — 2026-09-14

Source event: `mesh-home/mesh-witness-task-autono@mesh-home` reported two
`active-task-stalled` errors at 10:55:49Z. I checked the repository, canonical task
ledger, and live witness pane before disposition.

## Finding

The TinyFleet row
`tinyfleet-confirmatory-v1-comparison-20260914/execute-confirmatory-v1-generative-matrix`
is Haunt-owned and was active. Its contemporaneous progress receipt at 10:55:51Z says
PID 3942700 was still generating the complete registered matrix and gives the exact
next action. The ledger recorded owner progress at 10:56:21Z and renewed the lease to
11:26:21Z. The 10:55:49Z stall alarm raced with an in-progress update; this row is not
currently abandoned. Its dispatch check returns 2 because the exact row is active,
which is the correct refusal. No duplicate prerequisite or recovery task was needed.

The witness checker row
`chat-review/witness-pane-charter-contract-20260914/make-checker-enforce-charter`
is Genome-owned and still active, but its last recorded progress is 10:16:39Z and its
lease ended at 10:46:39Z. Its dispatch check also returns 2 because the row remains
active. The 10:59Z witness pane still lists it unfinished. This is a genuine stale
owner-held task; only Genome can safely resume or close that work. The exact active
task already exists, so no substitute prerequisite or duplicate row was created and
health did not alter Genome's task.

## Evidence

- `/home/mesh-home/.mesh/witness-task-autonomy.log`: 10:55:14Z FAIL with both stall
  errors; no later run had appeared at inspection time.
- `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-confirmatory-v1-generative-matrix-progress-20260914.md`:
  PID 3942700, frozen input hashes, and exact wait/validate/scoring next action at
  10:55:51Z.
- Canonical `mesh-task replay --json`: TinyFleet row active, Haunt-owned, last progress
  10:56:21Z, lease through 11:26:21Z; witness row active, Genome-owned, last progress
  10:16:39Z, lease through 10:46:39Z.
- `mesh-task check dispatch` for each exact owner row returned exit 2, consistent with
  both already-active ledger entries.
- `mesh-dash --once witness` at 10:59Z: task journal source age 31s; the witness row
  remained visible among unfinished work.

Disposition: one transient stall alert caused by a concurrent progress update, plus
one real owner-held stall awaiting Genome's handling. No task owned by another mind
was claimed or changed. No routing, DNS, firewall, VPN, Tailscale, or other substrate
state changed.
