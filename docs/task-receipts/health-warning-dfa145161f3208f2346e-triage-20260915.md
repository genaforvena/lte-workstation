# Path-watch warning triage — 2026-09-15

- Exact task: `health-warning/dfa145161f3208f2346e/triage`
- Source warning: `path-watch@phaedra` at 2026-09-14T10:39:04Z reported DERP latency 17.7 ms versus an 8.4 ms rolling baseline.
- Fresh `mesh-dash --once check` at 2026-09-15T19:02:23Z reports egress `OK`, 0% loss, average 1.147 ms on `enp42s0`; `mesh-health` is not indicating a current egress outage. The VPN panel remains degraded/observe-only with stale WG handshakes, so this does not authorize routing or VPN mutation.
- Current caveat: local load is high and the pane marks broad reachability probes unreliable; this single recovered latency alert cannot establish a persistent path fault.
- Disposition: historical/recovered path-quality warning. Retain the VPN degraded condition as a known observation and await a fresh repeated path-watch signal or correlated egress failure before escalation.
