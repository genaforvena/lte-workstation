# Clear-on-claim lifecycle audit — 2026-09-12

Audited `docs/superpowers/specs/2026-07-24-clear-on-claim-lifecycle-design.md` against
`scripts/mesh-mind-compact` and its embedded `--test` fixtures. This records source parity; it does
not change the clear behavior.

## Live behavior

`clear_reason()` has one trigger: `clear_has_completion()` returns `post-claim` when the window has
posted a recognized explicit task boundary since its last clear. The recognized boundaries include
completion markers, explicit `[idle]`/`[heartbeat]` yields, and the roll-call digest attributed to its
runner window. The last-clear cutoff prevents replay. The reflex only targets already-idle windows and
keeps the handoff and background-work gates on both send paths. The script declares a ten-minute
reflex cadence.

The implementation intentionally does not clear on arbitrary elapsed idle time or context percentage.
Its comments explain the safety rule: those triggers could clear mid-task. The “before the next claim”
behavior is achieved by clearing after the previous unit closes, leaving the window fresh for the next
`[taking]` event.

## Spec drift

The July 24 proposal is not as-built in three material ways:

- `clear_has_claim_start()` is absent; a `[taking]` record alone is not a clear trigger.
- `hold-leak` and `turn-ceiling` are absent; `MESH_COMPACT_INTERVAL` remains only in the stuck-pane
  liveness path, not as a clear trigger.
- The proposed test cases for claim-start and ledger-derived reasons are not present. Embedded tests
  instead assert that elapsed-idle and context-percentage clears stay absent, and that explicit task
  boundaries trigger once.

The source spec now carries a status note identifying it as a historical proposal and pointing to this
audit. It remains useful as design history, not as current behavior documentation.

## Lifecycle question left open

The live interpretation treats clearing after a completed unit as satisfying “fresh before the next
claim.” It does not establish freshness for a first claim made after a long idle period when no explicit
boundary has been recorded since the last clear. Adding a claim-start trigger would be a behavior change
and is not justified by the current implementation or tests. The current evidence supports recording
this as an explicit boundary of the design, rather than silently claiming that claim-start is covered.

## Verification

- `mesh-dash --once wake`: no distillation run in flight at 2026-09-12 02:10 UTC.
- `mesh-task queue --dispatch --owner wake`: returned the exact `spec-clear-on-claim` row; its dispatch
  check exited 0 and the owner-authored take succeeded.
- `mesh-mind-compact --test`: passed, including the post-claim event trigger, single-trigger decision,
  interval/context-clear rejection, and the handoff/background gates.
- Source inspection confirmed the reflex cadence declaration and both clear call paths.

No runtime behavior was changed. The first-claim-after-idle case remains the only lifecycle decision
not settled by this audit.
