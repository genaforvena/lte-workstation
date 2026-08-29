# vpn — the egress/tunnel service channel

goal: держать egress и туннели живыми, не подрубая канал, которым их чинят

Engine: opencode. Data pane: `mesh-dash vpn` — server health, the end-to-end tunnel, who is
connected, and the `[vpn-*]` verdicts, all rendered from CACHED reflex artifacts rather than live
probes.

**DIAGNOSE READ-ONLY. Never restart a working VPN.** `mesh-vpn-health --edge` already posts
`[vpn-down]` to the board on a break, so the mesh sees a fault before a user complains; this
window's job is to say WHICH LAYER moved, not to reach for an actuator. The healers that do act
(`mesh-exit-node-lan-heal`, `mesh-tailscaled-heal`, `mesh-revive`'s exit-node arm) are node-local
re-appliers with their own ledgers — read their tapes, do not race them.

**Substrate is single-writer and this window sits on top of it.** Any `ip rule` / `ip route` / DNS
/ nft / WireGuard / exit-node edit is a substrate change: detect other operators, claim on
`mesh-trace`, apply under `mesh-dms`, verify from a vantage the change cannot sever. Never
delegate a substrate write to a subagent, and never live-drive the exit-node DROP from a claude
pane on this node — the rollback rides the channel the change severs.

**The artifact for a path change is the FIB and a real fetch, never the pref.** `ip route get <a
real address in the range>` and the DEVICE that comes back; a public address actually fetched. A
declared preference is not what the kernel will do with your packet.
[[a-declared-pref-is-not-the-fib]]

**A probe that rides the broken link cannot name the far end.** Prove our own side first —
BackendState, the peer present-and-Online in the netmap, uplink age since boot — and render
BLIND/UNKNOWN when we cannot. A verdict about a peer minted from our own blindness is the failure
this lane keeps re-learning. [[a-probe-that-rides-the-broken-link-cannot-name-the-layer]]
[[a-shared-failure-mode-lets-a-probe-blame-the-far-end]]

Owed to the board: `[fyi]` naming the layer that moved, `[task]` for a fault with a one-line
idempotent remedy that has no re-applier yet, and one `[idle]` line stating the current verdict.
