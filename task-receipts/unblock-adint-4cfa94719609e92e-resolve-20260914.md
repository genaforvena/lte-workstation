# Redmi SSH blocker recheck — 2026-09-14

Task: `unblock/adint/4cfa94719609e92e/resolve`
Rejected history: `unblock/discover/0bc9bb716a55f76d/resolve`
Existing gated successor: `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`

## Current evidence

Read-only checks at 09:59 UTC confirm the missing prerequisite is still external handset state:

- `mesh-health --node Redmi` reports Redmi 10 `OFFLINE`, last seen 11 days ago; the configured
  off-tailnet fallback is unanswered.
- The filtered `tailscale status --json` row has `Online=false`, `LastSeen=2026-09-03T09:53:36.1Z`,
  an empty `CurAddr`, and no handshake.
- `adb devices -l` lists only serial `4d00553d61ab90b7`, model `SM_N900` (the Note 3).
- `ip route get 192.168.8.203` uses gateway `100.74.0.1` on `enp42s0`; this node has no direct
  route to the candidate Redmi LAN address.
- `mesh-task status discover-redmi-termux-frontier-followup-20260914` shows its exact-owner
  `discover` step remains blocked on `event:first-successful-redmi-ssh-port-8022-probe`.

These observations agree with the existing receipts
`task-receipts/unblock-discover-redmi-8022-0bc9bb716a55f76d-20260914.md` and
`task-receipts/discover-redmi-termux-frontier-followup-20260914.md`. The previous bounded SSH
probes timed out, and the present route, Tailscale, and ADB evidence is unchanged; repeating them
would add no evidence. Pairing or waking the Redmi requires its handset UI. The attached Note 3 is
not a valid substitute.

## Disposition

No mesh-owned registration or local code defect is missing. The existing discover-owned retry is
the narrowest correct successor; no duplicate task, `mesh-task recover`, or Termux frontier retry
was created. The precise missing datum is a successful SSH connection to the Redmi 10 on port
8022. The retry event remains
`event:first-successful-redmi-ssh-port-8022-probe`; keep the successor blocked until that event,
then resume that exact task and continue the Termux frontier on the Redmi itself.

This receipt closes the diagnosis step only. No gated comparison was run, and no handset, router,
network, or `self-adint` project state was changed.
