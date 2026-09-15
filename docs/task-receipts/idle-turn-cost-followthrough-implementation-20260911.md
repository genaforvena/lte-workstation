# Idle-turn cost follow-through implementation — 2026-09-11

## Live audit

- The board task was live at revision 2: `idle-turn-cost-followthrough-20260911/implement-task-aware-idle-gate`, owner `genome`, status `open`.
- The current implementation had a prompt-only `mesh-task queue --dispatch` instruction in `wake_msg`; `gate_decision` could still emit `WAKE:deaf` without consulting exact-owner task eligibility.
- Source and deployed copies were byte-identical before the change (`be5f3c…837eec`), so the audited code path was live.

## Change

`scripts/mesh-pane-consume` now:

- validates the first `mesh-task queue --dispatch` row against `mesh-task check dispatch <task-id> <exact-owner>` and surfaces that exact candidate;
- includes the canonical chain/step and `MESH_TASK_ACTOR=<owner> mesh-task take <chain> <step>` requirement in the wake message;
- suppresses a deaf-guard wake as `HOLD:no-eligible` when no exact-owner candidate exists, while retaining plain and surprise fail-toward-waking;
- hashes eligible exact-owner task state alongside the pane signature, so an eligibility change wakes even when the pane itself is unchanged.

## Red-first and verification

- Red-first regression: `tests/test-mesh-pane-consume-task-aware-idle-gate.sh` initially failed with `mesh-pane-consume: unknown arg 'genome'` before the new interfaces existed.
- Green regression: `tests/test-mesh-pane-consume-task-aware-idle-gate.sh` passed, covering exact-owner candidate validation, owner-authored take text, no-eligible deaf suppression, and an unpredicted change wake.
- Existing consumer regression: `scripts/mesh-pane-consume --test` passed.
- Syntax: `bash -n scripts/mesh-pane-consume tests/test-mesh-pane-consume-task-aware-idle-gate.sh` passed.
- Live deployment: `mesh-sync-tools --apply` returned 0; source and `/home/mesh-home/.local/bin/mesh-pane-consume` now match at SHA-256 `c43262f3835832bca7e714c22f3db5869496653876590863eb0e109b46b5713e`.

## Remaining landing obligation

`mesh-land --apply` must be run after the normal 600-second settle window; the live landing check currently leaves this freshly edited file `in-flight` rather than forcing a premature land.
