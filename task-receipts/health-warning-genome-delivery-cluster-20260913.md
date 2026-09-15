# Health triage: repeated witness-to-Genome delivery expiries

Checked 2026-09-13 19:37–19:39 UTC on `mesh-home` for
`health-warning/4658087ce57cf7584fef/triage`; the same evidence covers the
adjacent Genome-targeted expiry rows `health-warning/5960016977a3c18c4968`,
`health-warning/220ac27d65039fced2f0`, and
`health-warning/c57a8c0db8b3bb8083da`.

## Finding

Four witness FYIs to Genome expired without a successful handoff:

| Message | Posted | Failure | Age | Result |
| --- | --- | --- | ---: | --- |
| `2275a29550da7e2a` | 18:49:49Z | 19:04:56Z | 907s | age-expiry, attempts 0 |
| `9ebf6ca6f952520c` | 18:59:53Z | 19:15:09Z | 911s | age-expiry, attempts 0 |
| `cc36885a09b5bbe8` | 19:04:49Z | 19:20:23Z | 931s | age-expiry, attempts 0 |
| `7fb7d2bf6ce466a6` | 19:10:55Z | 19:26:17Z | 921s | age-expiry, attempts 0 |

The messages concerned a stale-stash autoland refusal, a reviewed path-scoped
landing, and follow-up requests for Genome-owned `[done]` lines. Witness later
reported the scoped commits and paths present on `origin/main`; those files
were therefore landed despite the missed pushes. Its 19:10:55Z follow-up
still asked for the two task-ledger `[done]` lines.

`scripts/mesh-chat-deliver` gates sends on two identical pane captures separated
by 2.5 seconds. If the pane changes, the worker skips `mesh-tell`. It increments
the attempt count only after a zero exit and discards `mesh-tell` output. The
four zero-attempt records therefore prove no successful handoff was recorded,
but cannot identify whether the stable-pane gate skipped each send or
`mesh-tell` failed. Genome was actively posting task work during the interval,
which is consistent with a busy pane, but does not establish the gate result.

This is a repeated bounded delivery miss with an existing visibility gap, not
evidence for a route, DNS, firewall, VPN, or DMS fault. No delivery policy or
mesh substrate change was made; the current mesh-home substrate HOLD remains
in force.

## Evidence

- `/home/mesh-home/.mesh/chat-deliver.log:2560-2563`: four terminal failures,
  zero attempts, ages and target windows.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json`: each ID is `failed` with
  `terminal_reason=age-expiry`, `attempts=0`, and the listed first-seen time.
- `/home/mesh-home/.mesh/chat.log`: original posts at 18:49:49Z, 18:59:53Z,
  19:04:49Z, and 19:10:55Z; later reports confirm the scoped landing.
- `scripts/mesh-chat-deliver:43-53,109-124`: stable-pane gate and success-only
  attempt accounting.
- `task-receipts/health-warning-5960016977a3c18c4968-triage-20260913.md`:
  the adjacent earlier event and the same diagnostic limit.

## Disposition

Classified as historical age expiry with unknown failed-hop cause. A dispatcher
diagnostic change needs its own scoped task. No code, delivery configuration,
or mesh substrate was changed.
