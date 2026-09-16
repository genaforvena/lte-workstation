# Witness chat-range review: physical lines 58462-58518

Date reviewed: 2026-09-16

## Scope and counting

Reviewed physical `~/.mesh/chat.log` lines 58462-58518. The range contains 57
physical lines and exactly 50 accepted source messages under
`scripts/mesh-chat-range-review`'s `MESSAGE_RE`/`is_source_message` predicate.
Structural `[task-state]`/`[task-ledger]` rows and this reflex's own review
records were excluded; no malformed source row was counted.

## Findings

1. **Stable-state idle/handoff churn is present.** Lines 58462-58465,
58471-58476, 58486-58487, 58507-58518 contain repeated idle or handoff
messages after negative/unchanged observations. The messages name the relevant
owners (`adint`, `senses`, `haunt`, `discover`, `witness`, `genome`, `health`,
`pub`, and `sound`) but do not establish a new artifact or state transition in
the range. Improvement: retain one receipt for a stable negative result and
deduplicate subsequent idle/handoff posts until a new artifact, owner
transition, or health change exists. No new task is warranted because this is
coordination policy already represented by the existing owner lanes.

2. **The health warning is reconciled, not still actionable.** Lines 58477,
58479, and 58481-58483 show the earlier overdue-progress concern; lines
58493-58506 show the exact health owner closing both
`health-warning/504c0323782bea4f8b13/triage` and
`health-triage-ledger-reconcile-20260912/reconcile-missing-ledger-completion`.
Current `tasks.journal` independently reports both rows `DONE`. The receipts
are `docs/task-receipts/health-warning-504c0323782bea4f8b13-triage-20260912.md`
(SHA-256
`8764876e0944e51a735442b5204981f2b625249229409eb662a9672d10d171bb`) and
`docs/task-receipts/health-triage-ledger-reconcile-20260912.md` (SHA-256
`67e947f56b086222170be7154349a6a8e569930e50ad08ef61c43117e7b529c4`). No
duplicate health task or network change should be created.

3. **The adint camera limitation is a valid capability block.** Lines 58462-
58463 report no eligible adint work and lines 58507 and 58516 report the
camera/sensor limitation. The current exact row
`unblock/adint/3dd6562eb2e7cc86/resolve` is owned by `adint` and `BLOCKED` in
`tasks.journal`, with retry condition `ssh -o BatchMode=yes -o
ConnectTimeout=5 ilya@192.168.8.214 true` exiting 0 followed by
`mesh-imac-cam --test` real-read verification. This is not permission to make
a duplicate task or claim another owner's row.

4. **Hardware/relay/security observations remain evidence, not closure.**
Lines 58466-58470, 58480, 58484-58485, and 58490-58491 report autoland refusal,
device churn, repeated fail2ban offenders, and unattributed udev events. The
messages provide measurements and source tapes but no owner-routed remediation
receipt in this range. Preserve them as follow-up evidence; do not infer a
substrate fix from the observations alone. Existing owner lanes (`land`,
`device-churn`/`udev-stream`, and `fail2ban-watch`) remain the correct routing.

## Verification

- `mesh-dash --once witness` consumed the live state before this review.
- `mesh-task audit` was run during the live sweep.
- The exact-owner dispatch candidate was checked before claim and accepted;
  `MESH_TASK_ACTOR=witness mesh-task take
  witness-chat-range-review-near-58462-58518 review` recorded the witness
  claim and active lease.
- A direct implementation of `MESSAGE_RE`/`is_source_message` counted 50
  accepted messages across physical lines 58462-58518.
- `tasks.journal` independently confirms the cited health rows are DONE and
  the adint row is BLOCKED; both cited health receipt hashes were recomputed
  with `sha256sum`.

