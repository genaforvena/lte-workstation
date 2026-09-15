# Promise lifecycle plan audit — 2026-09-12

## Scope and tracking evidence

Audited `docs/superpowers/plans/2026-07-24-promise-lifecycle-and-clear-triggers.md`
(SHA-256 `7a741480286893dfa6b09279856cc503412531e9f89c64b8744fe0b7f22f858e`)
against `scripts/mesh-promises` (SHA-256
`2df906059f3920340381702a1dcb4a99cf2842645241a510fc73c09c322f26f3`) and
`scripts/mesh-mind-compact` (SHA-256
`2b268de6045375279dfae64f8fffa108532c22cee72c8d0e4230f02bcafdb60d`). The plan has
96 unchecked and 0 checked boxes; those boxes were not maintained and do not describe
implementation state. The six task sections below were checked against current code and tests.

## Six-task disposition

| Plan task | Outcome | Current evidence and remaining work |
|---|---|---|
| 1. `mesh-promises` writeoff/reroute primitives | PARTIAL; not the planned interface | Current code has a time-based writeoff only for structurally unpayable `reflex-broadcast` claims when `MESH_CLAIM_WRITEOFF_H > 0`; it books to `expenses:claims:uncollectible`. There is no `--writeoff` or `--reroute` CLI, no general promise/claim/hold admin-close event, and no distinct equity legs. The later spec audit must decide whether to implement the planned operator-posted primitive or revise the design around the existing narrow automatic writeoff. No live writeoff was issued. |
| 2. Uniform unrouted accounting | PARTIAL | Promise rows expose `unrouted`; current claim and hold JSON rows do not. Current `counts` has only `unrouted`, and `--check`'s roster section enumerates promises only. Add the claim/hold counts, fields, report glyphs and roster evidence if this component remains required. |
| 3. Suggested-owner hint | NOT IMPLEMENTED | No `suggest_owner`/suggestion field or corresponding open-item rendering exists in `mesh-promises`. |
| 4. Confidence-gated auto-reaction | NOT IMPLEMENTED | No `MESH_PROMISE_AUTOREACT`, `_auto_react`, `automute_candidates`, or reroute CLI path exists. The live auto-reaction smoke test was not run and no automatic board mutation was enabled. |
| 5. Claim-start clear trigger | SUPERSEDED by operator direction | Commit `d4daa92e` (2026-07-24, “clear: drop every conditional clear — task boundary only”) records the operator direction: “clear before and after claiming a task from the board. no other conditions, no llm checks.” It deliberately removed conditional triggers. Current `clear_reason` only fires on the task-boundary event; `clear_has_claim_start()` is absent. The July 24 plan/spec should be marked superseded here rather than reimplemented. |
| 6. Hold-leak / turn-ceiling clear tiers | SUPERSEDED by the same operator direction | Current `clear_reason` has no hledger `hold-leak` or `turn-ceiling` tier. `MESH_COMPACT_INTERVAL` remains for the manual-target cooldown, not as an idle-clear trigger. Tests explicitly assert that interval and context-percentage clears stay gone. Update the stale July 24 plan/spec to record this later decision. |

There is one queued related task in the task ledger, `design-spec-task-sweep-20260907/spec-promise-writeoff`;
it is queued behind `spec-sound-collage`. No implementation task for the remaining Components A–D
appears in `tasks.journal`. Use that later spec-audit step to decide and materialize only the still
desired implementation work, avoiding duplicate tasks while the design audit is pending.

## Verification

- `rtk bash scripts/mesh-promises --test`: PASS, exit 0.
- `rtk bash scripts/mesh-mind-compact --test`: PASS, exit 0. Its final summary names only the
  post-claim event trigger and explicitly says interval/context-percentage clears are gone; it does
  not claim coverage of `claim-start`, `hold-leak`, or `turn-ceiling`.
- `mesh-promises --check` in a private `MESH_PROMISES_DIR`: PASS for parity and independent open
  balances across promises, claims, holds and asks. A check on the default shared materialization
  path did not remain consistent: one run found replay/hledger agreement for the first three
  families but failed on asks (`replay=66`, `hledger=0`); inspection then found the default
  `promises.journal` empty. This is a separate promise-ledger materialization issue, not a
  `tasks.journal` verdict. No cause or fix is claimed here; retain it as an open verification item.

## Operator-directed task-ledger check with witness

The operator clarified that the relevant task record is `tasks.journal`, and asked for a witness
check. `mesh-dash --once witness` reported the materialized view at
`/home/mesh-home/.mesh/tasks.journal`, with task source authority from explicit task-state events.
At the captured snapshot, the file header reported `task_source=PASS`, 52,400 source/replayed
events, 0 source errors, and 776 task rows (214 unfinished, 109 rejected, 453 done). Its source
SHA-256 was `12b31736da93325c2776aeaa655b58223512e338f5136a9b7685a55768a67b99`; the materialized
file SHA-256 was `f254a36ce830e21c084d7e8592e820639869c1db0cdbd5543ebe32b67d1e03f1`.

The same snapshot contained `RUNNING tg design-audit-task-sweep-20260907/plans-promise-lifecycle`
and `QUEUED tg design-spec-task-sweep-20260907/spec-promise-writeoff`. The prior
`design-spec-task-sweep-20260907/spec-sound-pane-records` row was `DONE`. These are task-ledger
facts; the promises materialized hledger journal is a distinct data product.

## Remaining obligations

1. In the queued `spec-promise-writeoff` audit, reconcile the manual writeoff/reroute and unrouted
   components with the existing implementation; create implementation tasks only for requirements
   that remain in force.
2. Amend the July 24 clear-on-claim plan/spec to cite `d4daa92e` and remove the superseded
   claim-start/hold-leak/turn-ceiling requirements.
3. Diagnose the default-path `promises.journal` inconsistency before treating live
   `mesh-promises --check` as verified. Do not confuse that result with witness's `tasks.journal`
   validation.
