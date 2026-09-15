# Redmi frontier prerequisite audit — 2026-09-14

Task: `unblock/adint/7696b3dcb749cbbd/resolve`
Rejected history: `unblock/discover/0bc9bb716a55f76d/resolve`
Exact active successor: `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`

## Live task and protocol check

At 09:47 UTC, the assigned resolver was open and dispatched to `adint`. The original discover
resolver is rejected, while its exact-owner retry task remains in the ledger as `blocked` on
`event:first-successful-redmi-ssh-port-8022-probe`. This existing discover-owned task is the right
successor for the Redmi Termux frontier; creating another duplicate retry or activating the rejected
step would lose the recorded gate. No BbyWVY comparison gate is satisfied by this Redmi task, so no
comparison was started or registered.

The frozen body protocol requires a real Redmi SSH read before claiming a Termux capability. It also
forbids using another handset as a substitute. The existing `mesh-phone-ip` guard correctly skips an
ADB tunnel when no Redmi serial is explicitly paired; the live attached serial is the Note 3. The
documented retry remains a successful SSH connection to Redmi port 8022, followed by the candidate
command on that endpoint.

## Current evidence

Fresh read-only checks at 09:47:47 UTC confirmed:

- `mesh-health --node Redmi`: Redmi 10 is `OFFLINE`, last seen 10 days ago; the configured
  off-tailnet fallback is unanswered.
- `tailscale status --json`: Redmi `Online=false`, `LastSeen=2026-09-03T09:53:36.1Z`, no current
  endpoint address, and no handshake.
- `adb devices -l`: the only device is serial `4d00553d61ab90b7`, model `SM_N900` (Note 3).
- `ip route get 192.168.8.203`: routes via `100.76.0.1` on `enp42s0`; the candidate Redmi LAN
  address is not on a directly connected Redmi LAN from this node.
- The earlier bounded probe receipt records all three known Redmi `:8022` addresses timing out at
  09:24 UTC. These unchanged conditions do not justify repeating those probes.

The earlier receipt `task-receipts/unblock-discover-redmi-8022-0bc9bb716a55f76d-20260914.md`,
the current state above, and `docs/redmi-termux-ssh-restore-20260910.md` agree: this node has no
available path to wake the Redmi or complete its on-device wireless-debugging pairing. The missing
datum is handset-side state, not a missing mesh registration or a local route/ADB code defect.

## Mesh-owned work and typed blocker

No local change can honestly substitute for the missing handset state. The existing discover retry
task is retained as the single exact-owner successor and remains blocked; no `mesh-task recover`,
duplicate retry, or premature comparison was run. The narrow actionable prerequisite is for the Redmi
to be physically awake/unlocked and on-network with either Tailscale online or Termux `sshd` listening
on port 8022. After that external event, retry the first successful SSH probe to a documented Redmi
endpoint; only then run the remaining Termux frontier candidates and capture their real outputs.

Typed blocker: `external-event`

- Missing datum: a successful SSH connection to the Redmi 10 on port 8022.
- Retry event: `event:first-successful-redmi-ssh-port-8022-probe`.
- Exact active task holding the gate: `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`.

This resolver records the current gate evidence and completes its diagnosis. It does not clear or
resume the discover task. A new comparison task is not eligible until its own required gates are
satisfied.
