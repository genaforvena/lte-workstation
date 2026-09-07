# Live promise balance clearance — `tg-operator-intake-owner`

Observed at `2026-09-07T15:10:22Z` after a fresh `mesh-promises --feed`.

## Settlement path

`mesh-promises --feed` materializes the generated journal from the board; the journal is not
hand-edited. The implementation in `scripts/mesh-promises` writes one `+1 PROMISE` opening and,
when the keyed closure is matched, one `-1 PROMISE` keep to the same account. The feed refuses to
commit if `hledger check` fails.

## Direct journal evidence

Source: `~/.mesh/promises/promises.journal`, current lines 3774–3780:

```text
2026-09-07 * promise opened: tg-operator-intake-owner  ; promise:tg-operator-intake-owner owner:step opened:2026-09-07T14:44:20Z
    liabilities:promises:unrouted:tg-operator-intake-owner  1 PROMISE
    equity:promises  -1 PROMISE

2026-09-07 * promise kept: tg-operator-intake-owner  ; promise:tg-operator-intake-owner kept:2026-09-07T15:00:44Z lag:0.3h
    liabilities:promises:unrouted:tg-operator-intake-owner  -1 PROMISE
    equity:promises  1 PROMISE
```

The target account therefore nets `+1 - 1 = 0`. A direct hledger balance query for
`liabilities:promises:unrouted:tg-operator-intake-owner` returned no row.

## Independent verification

```text
mesh-promises --feed
  open=1 leak=0 ... unrouted=0 kept=478

mesh-promises --balance
  target key absent; remaining promise:
  liabilities:promises:tg:tg-scripts-layout-audit-20260907-frame-s

mesh-promises --check
  parity: PASS
  over-discharge: none
  agreement: PASS (replay=1 == hledger=1)
  roster: clean
```

The one remaining open promise is unrelated to `tg-operator-intake-owner`; this artifact claims
target-key clearance, not an empty promise ledger.
