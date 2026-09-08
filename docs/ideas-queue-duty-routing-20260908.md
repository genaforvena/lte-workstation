# Ideas-queue duty routing — 2026-09-08

Owner: `mesh-land/genome` / duty `queue-tend`

The live queue census before the owner sweep was `floor=0 [ ]`, `inflight=27 [~]`.
The genome charter now declares `duty: queue-tend`; the deployed charter at
`~/.mesh/charter/genome.md` carries the same declaration. `mesh-promises --live-windows`
includes `genome`, so the declaration resolves to a live owner rather than a retired name.

## Reconciliation

`mesh-queue-tend --reopen-aged` was run with `MESH_REAP_WINDOW=0` and an empty board fixture.
This is an explicit owner sweep: it re-opens aged work to the visible `[ ]` floor, never
blind-closes it, and still parks `BLOCKED` external dependencies. The first pass re-floored
13 items; the second pass re-floored the remaining 14 history-matched items. Final live census:

```text
floor=27 [ ]  inflight=0 [~]  done=1833
```

The queue is therefore visible to the floor gate again; no aged handoff remains hidden in `[~]`.

## Regression and reflex proof

`scripts/mesh-queue-tend --test` passes. Its fixture asserts both sides of the visibility
invariant: an empty floor with three in-flight items is printed as `floor=0, inflight=3`, and
after safe reaping it prints `floor=1, inflight=2` while the blocked and actively claimed items
remain `[~]`. The new `--reopen-aged` fixture proves matched historical evidence can be re-floored
without re-flooring a phone-offline item.

The runtime now prints `queue visibility` before every pass and `queue visibility after apply`
after mutation. `mesh-ideate --test` also passes, including the tremble reflex's live-roster
owner resolution and floor-vs-inflight backpressure proof.
