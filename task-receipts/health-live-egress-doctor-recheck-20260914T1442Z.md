# Health live egress and doctor recheck — 2026-09-14

## Action and result

Consumed `mesh-dash --once check`, then ran `/home/mesh-home/.local/bin/mesh-doctor --quiet`
after confirming its `flock` was free. The doctor completed with exit 0: `0 FAIL, 34 WARN`;
serial-confirm reached 1/162, with 17 `FAIL(stale)`, 160 stale-verdict, and 1 never-assessed.
Its live output named the configured exit node as an intentional consumer dependency. The old
dashboard/doctor cache still shows the pre-change `FAIL=3 WARN=33` from 13:32Z, and
`~/.mesh/doctor.log` still ends at 13:23Z; the quiet run did not refresh those artifacts.

## Live FIB evidence

- `ip -4 route get 1.1.1.1` → `dev tailscale0 table 52 src 100.81.222.19`.
- `mesh-card --exit-node-lan` → `state: ok`, exit-node `phaedra`, active prefix
  `100.76.0.0/16`, target `100.76.0.1`, `dev enp42s0`, verdict `ok`.
- `ip -4 route get 192.168.8.1` → `via 100.76.0.1 dev enp42s0 src 100.76.82.121`.

This matches the declared consumer policy: public egress through the configured Tailscale exit node,
while the active LAN prefix stays on the LAN device. No route, rule, DNS, VPN, or exit-node state was
changed.

## Pane prediction and next wake

Refreshed `mesh-wake-expect health` with four narrow patterns covering only expected churn in the
self `/clear` age, fleet sample age, OK feed/evolve ages, and render counter. The cached doctor line
is deliberately not predicted, so its age, headline, or policy verdict changing will wake the mind.

At the next real health wake, run `mesh-dash --once check` and see whether the scheduled doctor
writer replaced the cached 13:32Z failure with a fresh policy-aware report. If it has not, inspect
the cron-state/log writer path; do not treat the quiet run's live result as a cache refresh.
