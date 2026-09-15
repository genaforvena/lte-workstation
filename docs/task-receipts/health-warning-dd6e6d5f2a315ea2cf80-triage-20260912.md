# Health-warning triage: `health-warning/dd6e6d5f2a315ea2cf80`

- Checked: `2026-09-12T05:14Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/dd6e6d5f2a315ea2cf80/triage`
- Source: `health@mesh-home`, `2026-09-09T00:01:30Z`: `route:no | PROPOSE none (retired 2026-09-07T08:59:10Z) | CHANGED egress wiring and chaos finding recorded | GAP known fleet degradation`.

## Finding

The roll-call line is a historical status summary, and its fleet-degradation warning remains accurate. The live pane at `2026-09-12T05:12:36Z` still shows cached doctor failures for egress over `tailscale0` and the configured exit-node SPOF, a degraded fleet (10 nodes, 2 SSH, 0 LAN, 8 down), and current egress reachability. A fresh `mesh-health` read at `05:14:52Z` passed `mesh-home` and `phaedra`; it reports the other peers offline or SSH-authentication-refused.

The current routing evidence confirms that the unresolved egress topology is real: `enp42s0` has `100.74.232.82/16` and the main table has a default via `100.74.0.1`, but policy rule 5270 selects table 52 first. `ip route get 1.1.1.1` and `ip route get 100.74.0.1` both select `tailscale0` in table 52. A source-pinned ping to `100.74.0.1` on `enp42s0` received 0/3 replies. Thus public egress being reachable does not establish the local gateway or LAN path.

The recorded chaos result is the isolated `mesh-chaos-emu` sample: two injected rc=75 retries followed by recovery on attempt three. Its acceptance note explicitly says this proves a reusable local emulator path, not live-service wiring; the witness receipt confirms no cron wiring was added. This is not evidence that egress recovered.

No safe route change was made. The existing coordination receipt says a local route exception needs a current `mesh-trace` claim, peer-route collision checks, and independent before/after reachability, because table 52 also carries Tailscale peers. The related health-owned check-stream triage `health-warning/5a1fd4103ba0b7f8ee4f/triage` remains open; this receipt does not replace it or create a duplicate route-repair task. `mesh-egress-health` returned rc=0 with no output, which does not override the explicit route and ping observations.

## Disposition

Reconcile this historical roll-call warning as a status report: the known fleet degradation remains current, while the egress/LAN topology remains unresolved and has no safe local route proposal in this triage. Keep substrate unchanged. Retry route work only through the health charter's single-writer sequence after obtaining the required `mesh-trace` claim and verifiable collision/reachability evidence.

## Verification

- `mesh-dash --once check` — exit 0; live pane consumed.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/dd6e6d5f2a315ea2cf80/triage health` — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/dd6e6d5f2a315ea2cf80 triage` — claimed by the exact owner.
- `mesh-health` — live result at `2026-09-12T05:14:52Z` recorded above.
- Read-only `ip -br addr`, `ip route show table main`, `ip route show table 52`, `ip rule`, and `ip route get` checks support the current routing finding.
- `ping -I enp42s0 -c 3 -W 1 100.74.0.1` — 3 transmitted, 0 received.
- `mesh-task status health-warning/5a1fd4103ba0b7f8ee4f` — the related health check-stream triage remains open.
- Chaos outcome/acceptance and witness consumer verification reviewed; no live service wiring or cron activation claimed.
