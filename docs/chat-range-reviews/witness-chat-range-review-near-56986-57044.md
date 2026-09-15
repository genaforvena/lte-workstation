# Witness near chat-range review — 2026-09-15

## Scope

Reviewed `~/.mesh/chat.log` physical lines 56986–57044 with the production
`MESSAGE_RE` and `is_source_message` predicate in
`scripts/mesh-chat-range-review`. The interval contains exactly 50 source
messages: first source line 56986 and last source line 57044. Structural
`[task-ledger]` rows were excluded; no malformed row or this reflex's own
`witness-chat-range-review-` row changed the count.

## Findings and disposition

1. Lines 57006–57010 show `health-warning/25c94fbe1c2ffda0455a/triage`
   reaching DONE with a receipt while its ledger retains `dispatch=failed`.
   The current replay confirms the exact task is terminal `complete/health`,
   with artifact
   `docs/task-receipts/health-warning-25c94fbe1c2ffda0455a-triage-20260912.md`.
   Its recorded SHA-256 `230ae3d90c8dd6dce5c33371a3792c8a15450e707e1c3b09649d4b7cb0e289ae`
   matches the file. The generated autoland request at line 57009 is the
   existing owner-routed follow-up; no duplicate triage was created.

2. Lines 57020–57021 and 57034 show a separate health warning with repeated
   dispatch failure, but current replay records
   `health-warning/21b83e4337b01ec10b67/triage` as DONE/health with its receipt
   and `dispatch=sent`. Its receipt hash was independently recomputed as
   `e95ce5ae02456c0dd76dd331983e1bfe02837b139be68909e22353598c887e9d`.
   This is not a duplicate of the prior warning.

3. Lines 57026–57042 show the witness-created CGNAT repair chain dispatched,
   then taken by VPN with an owner-authored `[taking]` transition. Current
   replay shows the chain terminally rejected, so the historical dispatch and
   claim are not an orphan or premature closure.

4. The remaining task, handoff, idle, FYI, sensor, and dispatch lines have no
   safe duplicate or forgotten exact-owner task after checking current replay.
   Repeated idle/handoff prose is historical coordination output, not closure
   evidence.

## Verification

- `mesh-dash --once witness` consumed the live unfiltered pane.
- Read `/home/mesh-home/.mesh/tasks.journal` and the raw chat tail.
- `mesh-task check dispatch witness-chat-range-review-near-56986-57044/review witness`
  was rerun after the owner claim; it returned 2 because the step was already
  active, while the live board contains the owner-authored `[taking]` and the
  ledger records `status=active`, owner `witness`, and a live lease.
- Production predicate recomputation returned `COUNT 50 FIRST 56986 LAST 57044`.
- `mesh-task audit` returned 0.

## Disposition

The exact range is reviewed. The dispatch-failure persistence is preserved as
evidence for the existing autoland/routing work; no new corrective task was
opened. This receipt is the completion artifact for
`witness-chat-range-review-near-56986-57044/review`.
