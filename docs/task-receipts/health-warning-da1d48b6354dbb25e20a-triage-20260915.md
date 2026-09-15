# Health warning triage — 2026-09-15

- Exact task: `health-warning/da1d48b6354dbb25e20a/triage`
- Warning source: 2026-09-14 roll-call reported `route:no`, retired `PROPOSE none`, a changed resolver receipt, and a reachability-probe/parent-SSH gap.
- Fresh verification at 2026-09-15T18:55:14Z: `mesh-health` passed `mesh-home`, `imac-rozalia`, and `phaedra`; both LAN targets GL-MT3000 and Redmi 10 were reachable. Six other peer labels remain offline by last-seen age, and the live pane explicitly says local load makes broad reachability probes unreliable.
- `mesh-interruptibility --test` failed one concrete vocabulary guard: `mesh-light` emits `UNKNOWN` but `light_vocab` maps it to `UNREACHABLE`. This is a separate code-quality defect, not evidence that the old route/SSH warning is currently actionable; no substrate change is safe from this triage.
- Disposition: stale/report-only roll-call warning. The remaining offline peers and intermittent probe confidence require their existing owner/authentication or external-event follow-ups; do not infer a routing failure from this observation.
