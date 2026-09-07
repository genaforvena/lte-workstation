# Promise-ledger clearance — `tg-operator-intake-owner`

## Result

At 2026-09-07T15:06Z, the live generated promise journal contains a balanced
open/keep pair for the exact key `tg-operator-intake-owner`. The stale liability
`liabilities:promises:unrouted:tg-operator-intake-owner` is absent from the live
`mesh-promises --balance` output.

## Direct ledger evidence

Source: `~/.mesh/promises/promises.journal`, lines 3774–3780 at verification:

```text
2026-09-07 * promise opened: tg-operator-intake-owner  ; promise:tg-operator-intake-owner owner:step opened:2026-09-07T14:44:20Z
    liabilities:promises:unrouted:tg-operator-intake-owner  1 PROMISE
    equity:promises  -1 PROMISE

2026-09-07 * promise kept: tg-operator-intake-owner  ; promise:tg-operator-intake-owner kept:2026-09-07T15:00:44Z lag:0.3h
    liabilities:promises:unrouted:tg-operator-intake-owner  -1 PROMISE
    equity:promises  1 PROMISE
```

The `+1` and matching `-1` net to zero; no journal hand-edit was performed.
The generated journal was materialized through `mesh-promises --feed`.

## Live verification

```text
mesh-promises --balance
  target key absent; the only open promise is unrelated:
  liabilities:promises:tg:tg-scripts-layout-audit-20260907-frame-s

mesh-promises --check
  parity: PASS
  agreement: PASS (replay=1 == hledger=1)
  no negative liability; roster: clean

mesh-promises --feed
  open=1 leak=0 unrouted=0 kept=478
```

The remaining `open=1` is the unrelated `tg-scripts-layout-audit-20260907-frame-s`
promise; it is not the dispatched stale key. This is therefore target-key
clearance, not a claim that the entire promise ledger is empty.

