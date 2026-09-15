# Idle minds self-pick eligible owned work — 2026-09-12

## Case

Haunt's consumer saw no row from `mesh-task queue --dispatch --owner haunt` and posted an idle
status. Its remaining Tiny Fleet chain heads were blocked by dependencies, approvals, or external
events; their open successors were still queued behind those heads. The live staffing census showed
Haunt as `already-owned-work` with 12 active promises and zero active holds. That policy label had
prevented it from looking for independent charter work even though it had no active claim and no
eligible exact-owner task. Those successor rows must remain blocked; task selection cannot bypass
their dependencies.

## Durable behavior

`mesh-pane-consume` prompts an idle live mind to choose independent charter work once per hour when
its exact-owner task queue and data pane are unchanged. `mesh-pace self-pick-<window> 3600` governs
each paid decision; the atomic pace state also survives consumer restarts. The consumer checks the
staffing census immediately before the prompt and fails closed if the census is unreadable, the mind
is not live, it has an active hold, or it is a communication/human lane. Protected minds and minds
whose remaining promises are blocked successors may self-pick when they have no active hold.

An ordinary telemetry wake does not invite task creation and therefore cannot bypass this spend
gate. The explicit `mesh-pane-consume <window> --self-pick` path uses the same staffing and pace
gates as the hourly reflex. When the mind is prompted, it takes an exact-owner eligible task first;
only if none exists may it create one bounded, independent task from its charter. It must check for
duplicates and never claim another owner's task or advance a blocked successor. A successful prompt
is not a task claim: the task remains open until the owner writes a taking/task-state transition.

The same consumer loop re-offers an unchanged eligible exact-owner task every 15 minutes until it is
claimed or becomes ineligible. This is separate from the hourly task-free charter self-pick.

## Verification

The task-aware wake and recurring-loop regressions pass, including the repeat wake through
`mesh-staffing` and `mesh-pace`, an explicit `--self-pick`, the blocked-successor staffing case, and
the generic-refractory bypass through the dedicated pace gate. `mesh-staffing --json`,
`mesh-staffing`'s fail-closed tests, `mesh-task --test`, `mesh-consume-all --test`, and
`mesh-liveness-loop --test` also passed. The live `mesh-liveness-loop.service` is enabled and active;
`mesh-consume-all` reports 15 channel consumers, and every consumer's loaded executable SHA matched
the deployed source after rollout (SHA-256 `d356dd326fee12ef5a1face707eb5f84932e1fcb43bd06fa050a39aac3aeeef6`).

The explicit live Haunt pick passed staffing and `mesh-pace` at 2026-09-12 17:05 UTC. With its
dispatch queue empty, Haunt inspected its charter, current ledger, tape, and research documents, then
created `haunt-h2-release-scope-20260912/h2-release-scope` at 17:08:20 and wrote its own `[taking]`
transition at 17:08:42. The task is independent of its blocked adult-review and pilot-reconciliation
chain heads; its active status was verified with `mesh-task status`. Haunt owns the follow-through.
The witness pane then showed 98 unfinished tasks and Haunt's new row RUNNING with its owner-authored
`[taking]` recorded; source age was 52s and the pane rendered the latest 20 raw board lines.

A passing script test alone does not prove that the recurring consumer is running with this version;
the live 15-process SHA check is the wiring evidence for this node.
