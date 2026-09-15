# Health unblock resolver: reliable iMac SSH evidence still pending

Resolver: `unblock/health/2304cc7f1d1880e3/resolve`
Parent: `health-warning/29cc9b04bf711f7d05f9/triage`
Checked: 2026-09-14 09:56 UTC on `mesh-home`.

The resolver was listed by `rtk mesh-task queue --dispatch --owner health`; its exact-owner
dispatch check exited 0, and `MESH_TASK_ACTOR=health rtk mesh-task take` claimed the row. The
one-shot health pane emitted a fresh frame at 09:56:12Z (pane-live 09:56:45Z) with
`PROBE-WARNING: LOCAL LOAD HIGH — reachability probe UNRELIABLE`. It reports local vitals load
`32.16/16` and load-audit `load1=32.79/16c`. This pane state does not establish current SSH
reachability to `100.121.88.110`.

The parent receipt records that the node has no independent LAN fallback configured for this
address, and that recent Tailscale handshake/relay evidence establishes overlay liveness only,
not SSH. Prior resolver receipts for this same parent document that no local change can create
the missing Mac LAN address or owner path. Lowering the probe threshold or attempting ping/SSH
while the current pane says reachability probes are unreliable would weaken the evidence gate,
not satisfy it. No ping, SSH, route, VPN, Tailscale, trust-store, or remote-node change was made.

Disposition: the prerequisite remains unsatisfied; this resolver attempt is diagnosed, and the
parent triage must remain blocked. Do not emit `unblock=cleared` or resume the parent on this
evidence. Exact retry condition: a later `check` pane frame clears the reachability-probe warning,
or a verified independent LAN/owner path appears. Then run a bounded Tailscale ping and read-only
SSH using the temporary known-hosts method recorded in the parent receipt; resume the parent only
if SSH evidence verifies the prerequisite.

Verification: full `mesh-dash --once check` frame; exact-owner dispatch check (exit 0); task
queue and active task status; parent receipt `health-warning-29cc9b04bf711f7d05f9-triage-20260914.md`;
prior same-parent resolver receipts `unblock-health-824532599a8ea867-resolve-20260914.md` and
`unblock-health-d049a3d635775070-resolve-20260914.md`. No substrate or remote-node state changed.
