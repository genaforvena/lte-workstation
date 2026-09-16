# Health warning triage: phaedra DERP latency

- Task: `health-warning/aa534b9b765097a6df65/triage`
- Warning source: `path-watch@phaedra`, 2026-09-15T21:39:04Z; DERP latency 22.5 ms versus 8.35 ms rolling baseline.
- Fresh observation: `mesh-dash --once check` at 2026-09-16T10:06:19Z reported egress `OK`, 0% loss, average 1.090 ms, mdev 0.042 ms (sample age 16s). The warning is not reproduced by the current egress sample.
- Concurrent health caveat: the same dashboard reported `LOCAL LOAD HIGH` and reachability probes unreliable (load1 48.28/16, later 51.08/16). This makes non-answers and latency samples less trustworthy; it is a known blindness, not evidence of a current phaedra path failure.
- Independent local check: `mesh-health` at 2026-09-16T10:09:28Z showed this node PASS and phaedra PASS. `mesh-egress-health` produced no failure output.

## Disposition

Report-only recovery: no routing, VPN, DNS, firewall, or substrate change is justified by the fresh healthy sample. Keep the alert as a transient/recovered episode. Retry only on a fresh path-watch warning or a fresh egress degradation sample; if local load remains high, re-sample after load settles because reachability probes are unreliable in that state.

Delegation record: a read-only `health-load-audit` worker was launched to independently inspect the load cause. It produced no report before the bounded stop request; therefore no worker claim is used as evidence. The evidence above was inspected directly from live command output and the task source in `~/.mesh/chat.log`.
