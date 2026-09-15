# Health roll-call triage: historical CGNAT gateway route

Task: `health-warning/260821f9e5d5b7063fc2/triage`  
Source warning: 2026-09-12T15:02:18Z roll-call

## Live evidence at 2026-09-14 20:06Z

- The warning refers to the former `100.76.0.0/16` address and the old healer refusal when that
  prefix was not the connected LAN. The current refreshed exit-node-LAN card derives this node's
  actual network as `100.74.186.131/16`, target `100.74.0.1`, and interface `enp42s0`, with verdict
  `ok`.
- Live `ip -4 route get 100.76.0.1` now follows the current gateway via `100.74.0.1 dev enp42s0`;
  `ip -4 route show table 52` contains throws for both `100.74.0.0/16` and the former
  `100.76.0.0/16`, plus the existing Tailscale peer routes. The current gateway is not swallowed
  by the exit-node table.
- The existing `exit-node-lan-cgnat-live-repair-20260914.md` records the successful live route
  verification and the healer's connected-prefix guard. It distinguishes the retired `100.76`
  sample from the later current connected prefix; no real route write was needed during that
  verification.

## Disposition

This is a stale duplicate of the completed route-repair verification. The LAN prefix has changed
since the warning; the current card-derived target and FIB both pass. Reject this row without
editing routing state. Reopen only if the card's current gateway resolves through `tailscale0`,
the exit-node-LAN card reports non-OK, or the healer refuses a prefix that is actually connected
and owned by the current LAN interface. Inward router presence remains a separate known unknown.

## Verification

- `mesh-card --exit-node-lan`: state `ok`, current target `100.74.0.1`, `dev enp42s0`.
- `ip -4 route get 100.76.0.1`: `via 100.74.0.1 dev enp42s0`.
- `ip -4 route show table 52`: throws for active `100.74.0.0/16` and former `100.76.0.0/16`;
  Tailscale peer routes remain present.
- Read `task-receipts/exit-node-lan-cgnat-live-repair-20260914.md`; its route verification is
  complete and is consistent with current live state.
