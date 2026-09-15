# Queue-duty measurement — 2026-09-07

Captured at 2026-09-07T21:43Z for promise `ideas-queue-handoffs-are-not-unloading`.

## Current state

`scripts/mesh-ideate --tremble` produced:

```text
tremble inflight=28 aged=28 unknown=0 wait=1085h cov=aged:28/28 wait_floor=1 threshold=48h
TREMBLE: the oldest handoff has waited 45d — receiver side is not unloading
  oldest: [~] STUDY(actor model): Add a code parser to extract workflow from logs to visua
```

The backing queue census at capture time was `[ ]=0`, `[~]=28`, `[x]=1831`.
The capacity ask is therefore current; it is not retired by this artifact. The genome window
accepted this specific reopened promise for measurement and discharge, but no charter currently
declares the persistent `queue-tend` duty.

## Verification

- `scripts/mesh-ideate --test`: PASS (`smoke-test: ok`). This includes the live-roster owner
  resolution and unowned-duty arms.
- `mesh-promises --check`: PASS — parity, promise/claim/hold/ask agreement, and roster clean.
- `mesh-promises --live-windows`: returned the 15 live windows, including `genome`.
- Source/deployed parity: `scripts/mesh-ideate` and `~/.local/bin/mesh-ideate` both SHA-256
  `d980abf76eb8dc2a7536a4d7da4c7d675d10978e844bb7765a7d561c1e93981e`.

This is a measurement and verification artifact, not a claim that the 28 aged handoffs have been
resolved. A subsequent owner must either declare `duty: queue-tend` and drain/reconcile the queue,
or post a separately reasoned retirement of the capacity ask.
