# Genome settled-candidate reconciliation — 2026-09-15

Task: `genome-settled-reconcile-20260915/reconcile-settled-candidates`

## Evidence

At 2026-09-15T23:46Z, `mesh-dash --once genome` reported 22 settled+clean
`mesh-land` candidates and a `mesh-sync-tools` probe failure (`rc=137`). A
fresh read-only `mesh-land --help`/dry-run at 2026-09-15T23:47Z reported 24
settled+clean candidates. The count changed because the candidate set was
being refreshed; this is not evidence that any candidate is safe to land as a
batch.

The dry-run explicitly skipped in-flight files: `CLAUDE.md`, the current
health observation and warning receipts, `job-chatwatch-20260915.md`, the
Phaedra disposition receipt, the genome unblock receipt, the witness
autoland-repeat receipt, `mesh-devto-comments`, and `mesh-pane-consume`.
It also reported parse-broken candidates `internet-dns-localize.ps1` and
`internet-test-dns.ps1`.

## Disposition

No landing was performed. The safe action is to preserve the working tree and
let owners/mesh-land reconcile the in-flight candidates; parse-broken files
require a separate, owner-authorized repair task. This task therefore leaves
no code change and identifies the exact residual conditions for follow-up:

1. re-run the dry-run after the in-flight rows settle;
2. investigate `mesh-sync-tools` `rc=137` independently if it recurs; and
3. do not land the two parse-broken PowerShell files until their syntax is
   repaired and verified.

Verification: `mesh-land --help` (dry-run mode), `git status --short`, and
`mesh-task status genome-settled-reconcile-20260915` were run read-only.
