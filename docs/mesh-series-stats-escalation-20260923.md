# mesh-series-stats escalation re-check — 2026-09-23

Decision: **(a) already done — deficit stays cleared; no new repair, no decay, no mute.**
The 2026-09-08 disposition diagnosed the right fix class (stale decay-candidate cache, not
the statistics organ) and it holds on the live tape. Re-running any repair would be the
exact error the task forbids.

## Live evidence (2026-09-23, read-only, genome source)

- `scripts/mesh-series-stats --test`: rc=0 — full gate green (17 truth-table rows,
  rom==source, 5 source-mutants RED, domain pinned both sides, 8 random series vs 64-bit
  twin, double-word carries red, --claims gate GREEN/RED/MIXTURE/UNKNOWN-never-HOLDS).
- `scripts/mesh-reflex-decay --candidates`: rc=0, no candidates — the stale-candidate
  cache fix (classifier-hash stamp + foreign/unstamped rejection + post-report subject
  change drop) still suppresses the 4× re-filed cue.
- `mesh-needs --check`: no ACTIVE deficit on mesh-series-stats (only two MUTED loop-closure
  rulings on unrelated `.cooscillate-state`/`.correlate-state`, both ruled by genome with
  expiry + stated reason).
- Deployment parity: `scripts/mesh-series-stats` ≡ `~/.local/bin/mesh-series-stats`
  (symlink, byte-identical by construction).
- Wiring (decay rejected): consumers exist — `scripts/mesh-sound-reflex:1063`
  (`--claims`/`--prior` quoted live), `scripts/mesh-fitness`, `scripts/mesh-convexity`
  reference it; the 4 decay-review rows (1463/1469/1471/1473) are `[x]` done.

## Why the deficit never cleared before the fix

Per the 2026-09-08 disposition (docs/mesh-series-stats-escalation-20260908.md, still
accurate): the cue was the decay lane's age-accepted cached report outliving its scanner
and subject — four filings 05:00–07:15Z 2026-08-21, cue-pinned escalation 07:30Z. The fix
class was cache invalidation (report stamping + subject-change drop), not organ repair.

No tool edited; receipt left uncommitted for steward landing.
