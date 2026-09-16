# Audit follow-through enforcement — 2026-09-16

Task: `audit-followthrough-enforcement-20260916/enforce-audit-followthrough`

## Result

Audit/review settlement is now mechanically guarded instead of relying on prompt prose.
Tasks explicitly tagged `audit-followthrough` require an adjacent
`<artifact>.findings.json` manifest. Every finding must either map to a canonical exact-owner
`chain/step` task or carry a non-actionable reason. `mesh-task done` validates the mapping,
owner, dispatch/state, and terminal evidence; `mesh-task reject` cannot bypass the guard.
The dispatch text tells owners about the manifest and non-bypassable settlement contract.

The shared `mesh-window-turn` procedure now requires the explicit tag and sidecar for audits,
reviews, reconciliations, and any other task that promises downstream task creation. New witness
chat-range reviews and operator-intake reconciliation tasks emit that tag and describe the sidecar
schema. This is metadata-driven; task names and receipt prose are not used as enforcement inputs.

Standalone scheduled audits were also checked. `mesh-edge-gate-audit` and `mesh-lease-audit`
previously exited red after writing only logs. Confirmed red findings now post `[health-fail]` and
immediately invoke the existing `mesh-health-warning-task` admission path. Doctor FAIL rows,
clear-audit FLAG rows, and health-owned `[verify]` failures are now admitted by that converter.

Historical sound-audit backfill is durably assigned as
`sound-audit-taskification-20260916/audit-receipts-to-corrective-tasks`, owner `sound`, status
QUEUED with `dispatch=sent`. Its acceptance requires receipt-to-task mappings, exact owners,
reuse-or-create decisions, retry edges, and an independently checkable receipt.

## Independent audit and inspection

- Subagent `audit_completion_paths` identified `mesh-task done/reject` as the shared settlement
  boundary and found the standalone edge-gate/lease/doctor/clear-audit admission gaps. I inspected
  the cited code in `scripts/mesh-task`, `scripts/mesh-chat-range-review`,
  `scripts/mesh-health-warning-task`, `scripts/mesh-edge-gate-audit`, and
  `scripts/uxn/mesh-lease-audit` before using the findings.
- Subagent `audit_contract_tests` found that the existing witness regression asserted prompt text
  only and recommended explicit tag metadata plus a canonical-replay sidecar validator. I inspected
  the cited tests and the live ledger before implementing it.

## Red/green evidence

- `tests/test-mesh-task-audit-followthrough.py` first failed because a tagged audit completed with
  no manifest; it now passes missing-manifest, missing-task, wrong-owner, valid routed finding,
  reasoned non-action, reject-bypass, and ordinary-task compatibility arms.
- `tests/test-mesh-chat-range-review.py` first failed because generated plans lacked the tag; all
  eight tests now pass.
- `tests/test-mesh-operator-intake-lifecycle.py` first failed because intake reconciliation lacked
  the tag; all twelve tests now pass.
- `tests/test-mesh-health-warning-task.py` first failed on doctor/clear-audit/verify admission; it
  now passes.
- `scripts/mesh-edge-gate-audit --test` first failed because the confirmed fixture finding never
  reached a redirected admission sink; it now passes without touching the production board.
- `scripts/uxn/mesh-lease-audit --test` first failed for the same reason; it now passes its broken
  multiplier RED arm and live-genome clean arm with redirected admission.

## Wiring inspected

The live cron contains `mesh-lease-audit` at line 187, `mesh-edge-gate-audit` at line 241,
`mesh-health-warning-task` every minute at line 321, and `mesh-chat-range-review` every fifteen
minutes at line 347. Operator intake was installed and enabled but had failed with
`Too many open files`: the node had exhausted `fs.inotify.max_user_instances=128` across its
long-lived agent processes. Unrelated processes were left untouched. The node now has the durable
`/etc/sysctl.d/90-mesh-inotify.conf` setting `fs.inotify.max_user_instances=512`; `sysctl --system`
applied it and `mesh-operator-intake.path` restarted successfully. A subsequent event pass timed out
after creating `operator-intake/85bad20df34521d4154f620c/reconcile`; canonical replay contains that
exact tagged task, the pass reported `missing=0`, and the service's configured `Restart=on-failure`
with `RestartSec=60` preserved retry. This distinguishes a retried post-create timeout from a lost ask.
