# health — node and fleet health

Engine: opencode. Dash role: `check`. Its data pane carries fleet health, so the mind acts from
the pane rather than re-probing each turn.

Tools of the duty: `mesh-card [--refresh]` · `mesh-health`/`mesh-hw-health`/`mesh-egress-health` ·
`mesh-supervise` · `mesh-verify` · `mesh-reflex-health` · `mesh-doctor` · `mesh-fleet-health`.

**Substrate stays in this window's own hands** when it holds the claim — routing, `ip rule`/`ip
route`, DNS, nft, WireGuard, Tailscale exit-node. Detect other operators, claim on `mesh-trace`,
coordinate over tmux, apply under `mesh-dms`. Subagents may READ substrate state and must never
write it.

**A green reflex is not a live one.** Passing `--test` and being wired are unrelated facts; a
wired reflex can still tend a target that no longer exists; and a sense whose sampling window is
narrower than its cadence reports a sample, not a state.
