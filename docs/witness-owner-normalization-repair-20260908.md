# Witness owner-normalization repair — 2026-09-08

## Live audit

The repair chain `witness-owner-normalization-repair-20260908` was open and
dispatch-eligible. The existing witness owner-correction chain was also open,
with its step recorded as `owner=mesh-land/genome`.

Before the repair, `scripts/mesh-task` reduced `MESH_TASK_ACTOR=mesh-land/genome`
to `genome` but compared it with the unnormalized stored owner, so the supported
take was refused. The existing disposition artifact was already valid:
`docs/witness-live-unattended-followup-owner-correction-20260908.md`.

## Repair

`scripts/mesh-task` now canonicalizes slash-qualified service/window owners to
their post-slash window at plan creation and at every loaded mutation boundary.
`scripts/mesh_task_log.py` applies the same normalization to eligibility checks.
Thus creation, `take`, terminal mutation, and dispatch checks use one identity.

The live malformed row was then settled through supported transitions:

```text
MESH_TASK_ACTOR=genome mesh-task take witness-live-unattended-followup-20260908-owner-correction-20260908 repair-parked-autostash-strand
MESH_TASK_ACTOR=genome mesh-task reject witness-live-unattended-followup-20260908-owner-correction-20260908 repair-parked-autostash-strand <existing disposition reason>
```

The resulting canonical state is `rejected`, owner `genome`, with the existing
evidence cited in the rejection reason. No replacement task, generic owner, or
ledger bypass was used.

## Verification

- `python3 tests/test-mesh-task-owner-normalization.py` — PASS.
- `python3 -m unittest tests/test-mesh-task-log.py tests/test-mesh-task-import.py tests/test-mesh-task-no-expiry.py tests/test-mesh-task-optional-owner.py` — PASS.
- `bash tests/test-mesh-task-source-coverage.sh` — PASS.
- `bash tests/test-mesh-task-dispatch-receipt.sh` — PASS.
- `bash tests/test-mesh-task-restart-continuity.sh` — PASS.
- `mesh-task --test` — PASS.
- `git diff --check` — PASS.
- Live `mesh-task status witness-live-unattended-followup-owner-correction-20260908` — `[rejected]`, step owner `genome`.
