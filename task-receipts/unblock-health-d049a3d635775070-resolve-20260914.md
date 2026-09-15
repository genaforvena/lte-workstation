# Health unblock resolver: reliable iMac SSH evidence still pending

Resolver: `unblock/health/d049a3d635775070/resolve`
Parent: `health-warning/29cc9b04bf711f7d05f9/triage`
Checked: 2026-09-14 09:14–09:16 UTC on `mesh-home`.

The 09:06:29Z health-pane frame explicitly marked reachability probes unreliable under local
load. A fresh local read at 09:14:49Z showed load averages `17.80/26.72/33.76` on 16 CPUs;
`mesh-load-audit` independently reported `load1=17.58/16c`. The applicable gate in
`scripts/mesh-fleet-health:150-160` is `load1 > MESH_LOAD_GATE_MAX` or, when unset, `nproc * 0.9`.
`MESH_LOAD_GATE_MAX` is unset in this environment, making the current default threshold 14.4;
the measured load remains above it. Load has fallen substantially from the 09:06 frame's
`79.48/16`, but has not reached the reliable-probe condition.

The latest Tailscale record from the prior triage read showed a 09:08:14Z handshake and an active
relay path, which does not establish SSH access. `~/.mesh/nodes` still has no iMac LAN fallback.
No ping or SSH probe was run while the local-load gate remained exceeded. No route, VPN, Tailscale,
remote-node, or trust-store state changed.

Disposition: the prerequisite is not satisfied, and there is no safe local fix to lower this
external workload or independently reach the Mac. Close this resolver attempt as diagnosed while
leaving the parent triage typed-blocked; do not emit `unblock=cleared`. Exact retry condition:
obtain a later health-pane frame without the reachability-probe warning (or an independent LAN/
owner path), then run a bounded Tailscale ping and read-only SSH using the prior temporary
known-hosts method. Resume the parent only after that evidence passes.

Verification: `uptime`; `mesh-load-audit`; `MESH_LOAD_GATE_MAX` environment read; the gate source
in `scripts/mesh-fleet-health`; prior Tailscale JSON/text status; and the `MESH_LAN_FALLBACK`
entries in `~/.mesh/nodes`.
