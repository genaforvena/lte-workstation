# Health-warning triage: `health-warning/391ad277f062ccf7c921/triage`

- Checked: 2026-09-12 14:30–14:33 UTC on `mesh-home`.
- The exact-owner dispatch check exited 0; `health` claimed the task.
- Read-only triage. No route, DNS, firewall, WireGuard, or Tailscale settings changed.

## Findings

- `mesh-dash --once check` produced no visible output and did not finish within 30 seconds in this session; it was stopped. The pane did not yield a readable payload here.
- `mesh-card --refresh` refreshed at 14:30:54Z and exited 2. It reports default egress via `tailscale0`, exit node `phaedra`, and a swallowed LAN gateway: `100.76.0.1` routes through Tailscale table 52. The card proposes `throw 100.76.0.0/16 table 52`, but that range overlaps Tailscale CGNAT space; no peer-route collision proof or coordinated substrate window exists in this triage, so the route change was not safe to apply.
- Independent `ip route get` reads confirm both `100.76.0.1` and public destination `1.1.1.1` select `tailscale0 table 52`. `mesh-lan-presence --nodes` exits 1 with `router unreachable — UNKNOWN` and no local `192.168.8.0/24` address. This is a real loss of LAN visibility, not proof the router is down.
- The current `mesh-doctor` output still shows the two reported egress FAILs (egress over `tailscale0`; exit-node SPOF) and `mic DEFAULT device broken/busy`. It also passes actual microphone capture on `plughw:1,0`. The broad doctor run was interrupted during its later smoke-test section, so no overall exit status is claimed.
- `tailscale status` shows `imac-rozalia` active via relay `hel` and `phaedra` active/direct as the exit node. The historical imac offline observation has recovered at the tailnet layer; the current `mesh-health` probe still skips it because SSH authentication is refused. `GL-MT3000` remains offline by last-seen age while retaining relay metadata.
- `mesh-health` passes local `mesh-home` and `phaedra`, skips the imac on SSH authentication, and reports the other sampled peers offline by last-seen age. `mesh-fleet-health` warns that local load makes peer reachability probes unreliable; its PATH sample at 14:29:01Z is `DEGRADED OK`, 8 peers, 1 direct, 1 relay, 6 offline. Treat those offline labels as bounded/uncertain reachability observations.
- Recent trace entries show `mesh-exit-node-lan-heal` repeatedly refusing the `100.76.0.0/16` exclusion because it is outside its RFC1918-only eligibility rule. That is an identified automation blind, not recovery.

## Disposition

The check-stream delta is partly stale: `imac-rozalia` is active via relay now. The two egress failures, default-mic warning, and LAN/router UNKNOWN remain current. The LAN route remains swallowed by table 52, and the fleet reachability sample is load-limited. Keep the route issue as a known alarm; a repair needs a separate current `mesh-trace` claim, operator coordination, collision checks against Tailscale peer routes, and rollback-first `mesh-dms` handling. No substrate change was made here.

## Verification

- `mesh-task check dispatch health-warning/391ad277f062ccf7c921/triage health` — exit 0.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/391ad277f062ccf7c921 triage` — claimed by `health`.
- `mesh-card --refresh` — live refresh; exit 2 with swallowed-route invariant.
- `ip route get 100.76.0.1` and `ip route get 1.1.1.1` — both select `tailscale0 table 52`.
- `mesh-lan-presence --nodes` — exit 1, router/LAN state UNKNOWN.
- `mesh-doctor` — current egress FAILs and mic-default WARN observed; broad run interrupted during smoke tests, so the run is incomplete.
- `mesh-health`, `tailscale status`, `mesh-fleet-health`, `mesh-trace --tail 20`, and `mesh-dms --list` — observations above; no live dead-man switch was armed.
