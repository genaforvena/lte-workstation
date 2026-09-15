# Health warning triage: recurring `imac-rozalia` reachability failure

Task: `health-warning/ed23d7b6fc8ee0959c6b/triage`

The 02:11:41Z watchdog roll-up is the already-measured chronic signature
`35f22fafd26a` for `100.121.88.110 — SSH unreachable`; it reports a 48,005s gap inside a 351,600s
window (`n=25`) and four suppressed identical cycles. Prior triages on September 13 record the same
intermittent reachability failure and establish that this node has no LAN fallback for the Mac.

Current read at 03:41Z: `tailscale status --json` reports `imac-rozalia` `Online=false`, `Active=true`,
last seen `2026-09-14T02:14:55.1Z`, at `100.121.88.110`. `~/.mesh/nodes` still configures only
`GL-MT3000` and `router` as `MESH_LAN_FALLBACK`; there is no Mac fallback. `mesh-fleet-health` warned
that reachability probes were unreliable under load and returned only the local node; `uptime`
reported load averages 10.48/29.32/40.15. I did not run another ping or SSH probe under that stated
condition, so fresh TCP/22 reachability is unknown. The offline Tailscale status confirms the current
mesh-path failure; it does not reveal the Mac's physical power state or why it disappeared.

Disposition: recurring tailnet/SSH reachability fault remains active, with physical state and root
cause unknown. No safe local correction exists without a reachable Mac or alternate LAN path. No
route, DNS, firewall, VPN, Tailscale, or remote-node state changed.

Related cases: `docs/task-receipts/health-warning-1b5cd081c6b28386a347-triage-20260913.md` and
`docs/task-receipts/health-warning-f3d16e4bf8dfa5116b63-triage-20260913.md`.
