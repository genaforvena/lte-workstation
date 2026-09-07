# Coordination finding: dispatch receipt and per-step promises

Checked at 2026-09-07T10:02:14Z–10:03Z for `coordination-finding-dispatch-receipt`.

## Verdict

FAIL. The plans are decomposed into 12 durable chain steps, but neither active current
step has been started by its exact owner. `dispatch=sent` is routing evidence only.

## Missing receipts

| chain | current step | declared owner | live state | missing |
|---|---|---|---|---|
| `tinyfleet-drift-methodology` | `build-drift-evaluator` | `genome` | `OPEN_UNOWNED` | exact owner `[taking]`, lease/progress, artifact, verification |
| `tinyfleet-specialists` | `mood-lora-bench` | `genome` | `OPEN_UNOWNED` | exact owner `[taking]`, lease/progress, artifact, verification |

The ten successors are present as separate queued steps in the chain JSON (5 in
`tinyfleet-drift-methodology`, 7 in `tinyfleet-specialists` including the two current
steps' successors), but they must not be treated as started from the aggregate dispatch.
They currently have no individual start receipt, lease/progress, artifact, or verification;
that is expected until the predecessor is closed, but each must receive those fields before
its own work begins.

Board evidence: the only current-step task lines are the genome tasks at 2026-09-06T21:03:20Z
and 2026-09-06T22:41:35Z; no later exact `[taking]`, `[progress]`, or `[done]` exists for
either current step. The genome pane was live and `Ready` with no task loaded when checked;
there was therefore no owner-start receipt.

## Recheck and verification

- `mesh-task audit`: reproduced both `OPEN_UNOWNED` findings and all 10 `QUEUED` successors;
  `dispatch=sent` remained unchanged.
- `~/.mesh/witness-coordination.summary`: `chain_steps=12 findings=2 status=FAIL`.
- `tests/test-mesh-witness-lifecycle.sh`: PASS (no failure output).
- `tests/test-mesh-witness-promises.sh`: PASS.
- `mesh-witness-promises --test`: PASS.
- `mesh-promises --check`: parity PASS, agreement PASS (`replay=6 == hledger=6`), roster clean.
- Source/deployed SHA-256 parity PASS for `scripts/mesh-task` and
  `scripts/mesh-witness-promises`.

The ledger is internally consistent, but that does not discharge the two missing owner
receipts. Required next action: genome must post exact `[taking]` for one current step,
with a lease/progress and an artifact target; only after artifact-backed `[done]` and
verification may the next queued step be dispatched.

## Final live recheck

Checked again at 2026-09-07T10:04:59Z after the audit:

- `mesh-task audit` still reports exactly two `OPEN_UNOWNED` current steps and ten
  `QUEUED` successors; both chain JSON files still say `dispatch: "sent"`.
- Board search found no exact-owner `[taking]`, `[progress]`, or `[done]` for either
  `build-drift-evaluator` or `mood-lora-bench`; only the predecessor `[done]` rows remain.
- The declared owner pane `mesh-home:genome` is live (`command=bash`) but has no loaded
  task receipt; the `mesh-home:witness` pane is live (`command=bash`). No lease/progress,
  artifact, or verification can therefore be attributed to either current step.
- Rechecks: `tests/test-mesh-witness-lifecycle.sh` PASS,
  `tests/test-mesh-witness-promises.sh` PASS, `mesh-witness-promises --test` PASS, and
  `mesh-promises --check` PASS for parity, agreement, and roster.

Final verdict remains **FAIL**. The required next action is unchanged: `genome` must post
an exact `[taking]` for one current step carrying lease/progress and an artifact target.
