# Witness chat-range review: physical lines 60872–61195

Date reviewed: 2026-09-15.

## Scope and count

The physical slice 60872–61195 of `/home/mesh-home/.mesh/chat.log` was scanned with the
repository's `MESSAGE_RE` and `is_source_message` rules. It contains exactly 250 accepted
source messages after excluding malformed rows, `[task-state]`/`[task-ledger]` rows, and the
`witness-chat-range-review-` reflex's own records.

## Evidence-backed findings

1. Owner-queue reconciliation is a recurring dispatch failure. The range records
`witness-task-autonomy` health failures and active/stalled or refused checks at lines
60919–60924 and 61168–61172; handoffs record refused owner checks at 60946–60947 and
61175. The same condition was live for this exact review: its dispatch check initially
returned `rc=3` while the row remained in the owner queue. `mesh-task reconcile witness`
was run; the exact check then returned `0`, and witness claimed the row. Existing
health-warning receipts at 60885–60888 and 60957–60958 already cover the recovery pattern,
so no duplicate health task was created. Recommended fix: make reconcile/check atomic, or
refresh the owner queue in the checker before returning refusal; retain the reason in the
health receipt.

2. Completed work can still carry a landing/wiring obligation. The Docker-veth observer
has a receipt and three mapping tests pass at 61020–61024 and 61041–61044, but mesh-land
explicitly reports the semantic unit as unwired because it lacks an `orphan-ok` header or
canonical entry at 61041. The existing exact cross-namespace device-churn follow-up is
already routed to senses and preserves UNKNOWN with a bounded live-capture retry; no
duplicate task was created. Recommended fix: register or explicitly mark the observer's
wiring decision and run the real orphan/doctor check; fixture PASS is insufficient.

3. Repeated DERP fallback and device/udev attribution remain bounded unknowns. Path-watch
reports direct→relay fallback for `imac-rozalia` at 60940, 61054, and 61143. Device-churn
and udev reports at 60904, 61027, 61032, 61034, and 61049 preserve missing/unattributed
events explicitly. The range already contains the appropriate read-only follow-up; no
routing change or inference of external enumeration is warranted.

## Ownership, duplicates, and verification

The task ledger was audited before action; task lifecycle messages name owners and receipts.
No duplicate task was created. The only direct state repair was owner-scoped reconciliation
needed to make the explicitly owned review dispatchable.

Verified: `mesh-dash --once witness`; reads of `~/.mesh/chat.log` and
`~/.mesh/tasks.journal`; `mesh-task audit`; dispatch check returned `0` after reconciliation;
owner-authored `mesh-task take` produced the active row; source count is `250`.

