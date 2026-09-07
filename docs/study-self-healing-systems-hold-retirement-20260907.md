# Retired hold: `STUDY(self-healing systems)`

- **Hold:** leaked 25-hour board task `msg:1c7719bfbe231629`, supervision.
- **Owner:** `discover`.
- **Decision:** retire the duplicate study; do not add code.
- **Reason:** the existing study artifact already maps OTP supervision to the live mesh:
  supervisor/child registry, one-for-one restart, restart-intensity circuit breaker,
  wedged-child detection, and process restart in the existing pane. The proposed
  `kill-session` shape is both not a tmux supervision primitive and conflicts with the
  mesh's append-only scrollback invariant.

## Artifact chain

The substantive prior artifact is:

`/home/mesh-home/.mesh/knowledge/study-fault-tolerance-otp-supervision-already-embodied-2026-06-21.md`

It is the evidence for retirement, not merely a reachability claim. The repo-side receipt
is this file; its SHA-256 is recorded on the board with the verification result.

## Verification run

On 2026-09-07, inspected the cited live implementations and ran:

```text
bash -n scripts/mesh-supervise scripts/mesh-mind-keepalive scripts/mesh-channel-keepalive
```

The syntax check passed. `mesh-supervise --test` was also driven; its hermetic child
exercise reached the intentional killed-child path (the command emitted `Killed`), so it
was not counted as a clean exit claim. The artifact's cited implementation remains the
basis for the retirement, with no wiring or substrate change made.
