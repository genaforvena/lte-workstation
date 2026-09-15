# Health unblock resolver: iMac SSH evidence remains gated

Resolver: `unblock/health/824532599a8ea867/resolve`
Parent: `health-warning/29cc9b04bf711f7d05f9/triage`
Checked: 2026-09-14 09:30–09:32 UTC on `mesh-home`.

The required event has not occurred. `rtk mesh-dash --once check` emitted a fresh frame at
09:30:49Z (pane live 09:30:57Z) with `PROBE-WARNING: LOCAL LOAD HIGH — reachability probe
UNRELIABLE`; its load-audit reported `load1=28.97/16c`. The source gate in
`scripts/mesh-fleet-health:150-160` defaults to 90% of online CPUs when
`MESH_LOAD_GATE_MAX` is unset. It is unset here, so the default is 14.4 for the displayed 16 CPUs;
the pane measurement remains over that threshold. Its cached local vitals also show elevated load
(`32.74/16`) and 80C. The frame does not establish current SSH reachability to the iMac.

The local node configuration (`~/.mesh/nodes:8,127`) contains the iMac's tailnet address
`100.121.88.110`, but `MESH_LAN_FALLBACK` contains only the router at `192.168.8.1`; it provides
no independent LAN address for the iMac. The existing parent receipt also records that the recent
Tailscale handshake/relay evidence established overlay liveness only, not SSH. There is no safe
local configuration change to manufacture a missing Mac LAN address or remote-owner path. Lowering
the probe threshold or testing ping/SSH while the pane says probes are unreliable would weaken the
health gate rather than satisfy it, so neither was done.

Disposition: complete this resolver attempt as diagnosed; keep the parent triage blocked and do
not emit `unblock=cleared`. No ping, SSH, route, VPN, Tailscale, or remote-node change was made.
Retry only after a later check frame clears the reachability-probe warning or an independent LAN/
owner path appears. Then run a bounded Tailscale ping and read-only SSH using the temporary
known-hosts method in the parent receipt; resume the parent only if SSH evidence verifies the
prerequisite.

Verification: current one-shot check-pane frame; gate source and unset environment override;
`~/.mesh/nodes`; prior parent receipt `health-warning-29cc9b04bf711f7d05f9-triage-20260914.md`.
