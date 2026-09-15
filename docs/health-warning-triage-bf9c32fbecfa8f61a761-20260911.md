# Health-warning triage: `health-warning/bf9c32fbecfa8f61a761`

Date: 2026-09-11
Owner: health / mesh-home

## Canonical task state

The task was live before work: `mesh-task status health-warning/bf9c32fbecfa8f61a761`
reported one open step, `triage`, owner `health`, priority 70. It was claimed with:

```text
MESH_TASK_ACTOR=health mesh-task take health-warning/bf9c32fbecfa8f61a761 triage
```

The exact source warning is present in `~/.mesh/chat.log` at `2026-09-11T18:41:25Z`.

## Evidence and diagnosis

The failed message is `7ecce4f51c94a2e8`, sent by `vpn` to `haunt`:

- source record: `2026-09-11T18:25:15Z`, `[@haunt] [task] D02 corrective prerequisite...`
- delivery log: one successful handoff attempt at `2026-09-11T18:28:25Z`
- terminal warning: `2026-09-11T18:41:25Z`, `attempts=1`, `age=947s`, `reason=age-expiry`
- ledger entry: status `failed`, `terminal_reason=age-expiry`, `failure_window=5963840`
- configured bound in current source: `MAX_AGE=900`, `MAX_ATTEMPTS=3`

The target is not an absent name: `mesh-chat --targets` includes `haunt`, and the
`mesh-home:haunt` tmux window exists. The current pane is occupied by an active Codex
session, so target existence does not imply an idle delivery opportunity.

Current source and deployed wrapper are identical:

```text
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  scripts/mesh-chat-deliver
d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd  ~/.local/bin/mesh-chat-deliver
```

The implementation deliberately makes delivery bounded and idempotent: it only calls
`mesh-tell` when the target pane is idle, records the one attempt, and emits a terminal
`age-expiry` failure when the 900-second age bound is crossed. `mesh-chat-deliver --test`
passes, but that is only the implementation smoke test; the live ledger and delivery log
above are the runtime evidence.

## Disposition

This is a settled historical delivery failure, not evidence of a current missing target
or a source/deployment mismatch. No code or substrate change is warranted. Retrying the
same expired message would falsify the bounded-delivery contract and could duplicate the
operator-directed work; the sender retains the original failure and can re-issue a fresh
message if the prerequisite is still needed.

Verification performed:

```text
mesh-task status health-warning/bf9c32fbecfa8f61a761        PASS (live before claim)
mesh-task take ... triage                                    PASS
mesh-chat --targets                                          PASS (haunt listed)
tmux list-windows                                             PASS (haunt exists)
mesh-chat-deliver --test                                      PASS
```
