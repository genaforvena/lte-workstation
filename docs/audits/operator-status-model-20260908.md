# Typed human-gate audit — 2026-09-08

**Observed:** 2026-09-08T19:27:33Z UTC. The assigned chain was live and claimed at 19:25:46Z (lease through 19:55:46Z). Source snapshot: `/home/mesh-home/.mesh/task-chains/*.json`; exhaustive snapshot hash: `3e85c3b4af6501c19761c04b4e6449b077e80d470d9edce1c3611340b744daf7` (the TSV in this directory, before the operator row was appended).

## Model

- `autonomous-open`: the next action is executable by the named mesh owner; uncertainty, review, missing evidence, or a dependency is not a human gate.
- `autonomous-blocked`: progress is blocked by a machine/dependency/evidence condition; it has a concrete retry or owner path.
- `human-gated`: an objectively external operator act/choice/secret/physical action is required. The gate names the exact act; “needs-human” alone is invalid.
- `stale-ledger`: a disposition note, not a workflow status. It is recorded here as `autonomous-blocked` only when the machine ledger must be reconciled.

## Current mapping

The exhaustive mapping is [operator-status-model-20260908.tsv](operator-status-model-20260908.tsv), one row per remaining structured task plus the one board-only operator task. It also retains the just-closed audit row as `active-at-observation` for an auditable 151-row receipt; that row is excluded from the current counts below.

| classification | count | meaning |
|---|---:|---|
| autonomous-open | 126 | machine-owner work can proceed |
| autonomous-blocked | 22 | machine/dependency/evidence blocker; no operator action implied |
| human-gated | 1 | operator must repair phone SSH authorized_keys or confirm PHONE_USER drift |
| stale-ledger overlay | 1 | SpaceAI child is ledger-open after Job's completed result; reconcile the row, do not ask operator |

The counts above cover 149 remaining structured task-chain steps (127 open, 21 blocked), with the stale SpaceAI row moved to the machine-blocked class, plus the board-only operator row. The 151-row receipt additionally contains the audit row active at observation time; it is closed by this artifact.

## Findings

1. The generic status must not be used. A task is human-gated only when its evidence names external authority, a personal decision, a secret, a physical action, or an irreducibly subjective acceptance criterion.
2. SpaceAI is **not** human-gated. Job's 18:08:58Z done says ordinary incoming work remains machine-owned and only invitations with date/time/contact reach TG; 18:08:57Z says the Security Researcher contact was not sent because Chrome is absent, and Go developer already answered. 18:13:58Z records the corrected draft. The open child `tg-operator-spaceai-needs-human-20260908/spaceai-needs-human-routing` is therefore a stale machine-owned ledger row.
3. The only objective human gate in the current inventory is `operator/phone-authorized-keys-recheck`: the board record explicitly requires hands-on-phone re-adding `authorized_keys` or confirming `PHONE_USER` drift. It must not be routed as a generic status.
4. The sound rows mentioning rendering/listening, and audit rows mentioning operator gates, remain autonomous: they request evidence or a named decision artifact; no current row proves that the operator must act before the owner can produce the next artifact.

## Durable routing rule

Use typed fields `gate_type`, `gate_owner`, `gate_action`, `gate_evidence` when a human gate exists. Allowed `gate_type` values here are `external-authority`, `operator-decision`, `operator-secret`, `physical-action`, and `subjective-acceptance`. If none applies, keep normal workflow state `open` or `blocked` and record the machine retry/next action. FYI remains an event, not a task.

Verification: task-chain status, live board dispatch, and cited chat/job artifacts were read; the exhaustive TSV was generated from the current chain files and manually checked for the SpaceAI and phone exceptions. No workflow code or task state was changed.
