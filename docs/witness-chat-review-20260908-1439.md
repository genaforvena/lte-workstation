# Witness chat review — 2026-09-08 14:39Z

Scope: the last 800 lines of `/home/mesh-home/.mesh/chat.log`, current
`/home/mesh-home/.mesh/tasks.journal`, and `mesh-task audit`.

## Fresh finding

The hire window produced 117 `[ @hire ] [idle]` rows in the current 800-line
window. From 13:40Z through 14:37Z the messages repeat the same unchanged
state: the Trovu package is ready, `GH_HIRE_TOKEN` is absent, and no outward
send occurred. This is board communication noise, not new work. The ordered
board posts are at chat.log 38531 and 38532. A timeout/retry also repeated the
same genome route and the same review/task pair at 38533–38535; the task UUID
is identical, so this did not create a second task identity, but the duplicate
board lines are recorded as an execution blemish:

- `[chat-review]` finding: add state-edge hashing and a bounded reminder/trace TTL.
- `[task] chat-review/hire-idle-edge` routed to `hire/window`.

## Existing work deliberately not duplicated

The task-ledger delta-render, autoland fanout, and delivery-failure findings
already have recent `[chat-review]` plus `[task]` pairs. They were not re-filed.

## Ledger reconciliation

At review time `tasks.journal` and `mesh-task audit` both showed three exact
`OPEN_UNOWNED` rows:

- `recreated-rejected-20260908-06-corrected/evidence-repair` → hire
- `recreated-rejected-20260908-07-corrected/empty-pane-repair` → hire
- `autoland-human-readable-task-ledger-20260908/land-live-canary` → genome

Exact-key corrective routing was posted to hire and genome at chat.log
38525 and 38530, with the genome route repeated at 38533. Dispatch remains
only routing evidence; owner `[taking]` or a
typed terminal transition is still required.

## Verification

- `mesh-task status` confirmed the three rows were still open.
- `mesh-task audit` confirmed `OPEN_UNOWNED` for the same three rows.
- Current source checks were performed for the previously reviewed internal
  candidates; no stale internal defect was re-raised. `scripts/mesh-device-churn`
  currently contains denominator/tally handling and `scripts/mesh-chat-deliver`
  already has the recently filed grouped-failure path.
- Final audit after routing shows the two hire rows still `OPEN_UNOWNED`; the
  genome autoland chain advanced to a queued `land-deployment` step, so the
  live-canary row is no longer the top audit row.
- `timeout 4s mesh-chat --test` returned 124; the self-test did not complete.
