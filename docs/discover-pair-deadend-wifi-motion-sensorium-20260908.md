# Connection dead end: `mesh-wifi-motion` × `mesh-sensorium`

Date: 2026-09-08

## Verdict

Dead end. The proposed new edge was a one-shot attribution read: combine the WiFi passive-radar
verdict with the rest of the cached sensorium and report whether motion is corroborated by other
fresh senses. It does not create a new sense here.

## Price before reachability

The intended consumer acceptance predicate was:

```text
wifi JSON verdict is assessable (exit 0), AND sensorium --cached contains wifi-motion without STALE
```

Live sample at 2026-09-08T19:52:10Z: **0/1 accepted (0%)**.

Evidence:

- `mesh-wifi-motion --json` → `{"verdict":"UNCERTAIN","reason":"tape_stale","age_s":821769,"stale_limit_s":1800}`; exit 2.
- `mesh-sensorium --cached` already emitted `wifi-motion=UNCERTAIN (STALE)`.
- `mesh-sensorium --test` passed, including its existing `ROOM wifi-motion` cache acceptance
  check; this validates wiring, not live material value.

The pairing therefore duplicates an existing sensorium row and would turn stale/absent inputs into
a second derived label. No prototype or source edit was warranted. Durable dead-end trace:
`mesh-trace gen-pair-deadend mesh-wifi-motion×mesh-sensorium: sensorium already exposes the cached wifi-motion verdict, and the live consumer predicate accepted 0/1 samples because the source tape was stale; a fusion would duplicate stale evidence rather than add a new sense.`
