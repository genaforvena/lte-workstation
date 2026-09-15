# Correlation investigation: `body_power=CHARGING` ↔ `presence=MANY`

**Date:** 2026-09-08  
**Verdict:** **SPURIOUS / discard.** No fused sense or reflex.

## Re-measurement against the live tape

The queued snapshot (32 episodes / 8 occasions / 539 rows, era beginning
`2026-08-15T18:40:01Z`) is not reproducible verbatim because the tape has advanced and its
effective window has changed. Re-reading the current real
`~/.mesh/sensor-tape.tsv` from that same era start gives 2,259 rows through
`2026-09-08T20:20:01Z` (577.7 hours). Excluding honest missing/fault tokens leaves 516
rows where both axes have a real token:

| measure | current era |
|---|---:|
| aligned usable rows | 516 |
| `body_power=CHARGING` | 131 |
| `presence=MANY` | 162 |
| joint rows | 82 |
| raw aligned lift | **1.99** |
| joint occasions, gap <1h merged | 11 |

This reproduces an association above the 1.8 mining floor, but not a causal or operationally
useful signal. The queued invariance result is decisive: **0 of 4 environments** clears the
floor (env18 1.64, env20 0.66, env21 1.51, env25 1.00). It is in the Markov blanket only,
not the stable blanket, so it cannot be generalized or seeded into a reflex.

## Reality check

`body_power` is a real battery status read when it is available. Its timestamped ledger,
`~/.mesh/body-power-readings.log`, confirms actual CHARGING readings, including a later
2026-09-02 charging run. That does not validate the paired presence observations: the raw
BLE `~/.mesh/presence.log` stopped at **2026-08-30T07:10:10Z** and has mtime
2026-08-30 07:10:12Z. The current tape therefore renders the later presence field `STALE`;
there are only two jointly usable rows after that boundary and no later usable CHARGING/MANY
pair. The apparent relationship is consequently concentrated in the old BLE observation era.

Before the presence freshness boundary, the tape has 514 jointly usable rows, 131 charging
rows, and all 82 observed CHARGING/MANY joints. `MANY` is a coarse count bucket for nearby
Bluetooth devices (more than eight), not a person-presence ground truth; it includes
appliances and ambiguous devices. The source itself therefore cannot establish that charging
causes human presence, and its later silence prevents a live check of the proposed fusion.

## Decision

**Discard in one line:** `CHARGING` is a genuine phone-battery state, but `MANY` is a stale,
coarse BLE device-count proxy whose apparent overlap is environment-specific (0/4 stable
environments), so fusing them would turn an old availability/household-regime coincidence
into a false presence reflex.

## Verification

- `bash scripts/mesh-correlate --dry` and `--stable` completed successfully; this pair is not
  emitted by the current miner and the stable report preserves the queued `UNSTABLE` result.
- Independent read-only parsing of `~/.mesh/sensor-tape.tsv` reproduced the counts above.
- `bash scripts/mesh-body-power --test` and `bash scripts/mesh-presence --test` were not used
  to manufacture a green live claim; the live artifacts are explicitly stale/unavailable.
- No source tool was edited and no commit was made.
