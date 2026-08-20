# CORRELATION investigation — `body_power=CHARGING` ↔ `ambient=QUIET`: **SPURIOUS** (clock), 2026-08-20

**Emitted claim:** "when body_power reads CHARGING, ambient tends to read QUIET — lift 2.26 (20 episodes),
re-measured inside body_power=CHARGING's own era (since 2026-08-15T06:30:01Z, 14.3% of the window) …
2.26 vs the 1.8 floor is the whole margin this finding has; 8 distinct occasions / 20 episodes of 212,
window 877.2h."

**Verdict: spurious — the diurnal profile of `ambient`'s own label alphabet.** A shadow antecedent with
`CHARGING`'s exact hour-of-day histogram and *no relation to ambient whatsoever* already scores **1.62** of
the observed 2.22 crude lift. Hour-stratified, the finding is **1.37** — under this lane's own 1.8 floor.

## The mechanism, in the producer's own source

`scripts/mesh-ambient-clock:1019`:

```sh
if [ "$label" = "QUIET" ] && { [ "$HOUR" -ge 23 ] || [ "$HOUR" -le 5 ]; }; then
  label="NIGHT-QUIET"
fi
```

A quiet room between 23:00 and 05:00 is **renamed**. So `P(ambient=QUIET | deep night) = 0 by construction`
— measured on the live tape (era rows since 2026-08-15T06:30Z): **3 of 185** deep-night rows read QUIET, all
at the 23:00 boundary (node TZ is `Etc/UTC`, so tape hour = ambient's hour). And `CHARGING` is a
morning/evening behaviour: **3 of 38** rows in the deep night, against 27.7% of the era.

The hole is only the largest piece. `P(QUIET | hour)` over the era:

| hour | 00–05 | 06 | 07 | 08 | 09 | 10 | 11 | 12–15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|------|------:|---:|---:|---:|---:|---:|---:|------:|---:|---:|---:|---:|---:|---:|---:|---:|
| P    |  0.00 |0.86|1.00|0.77|0.79|0.63|0.60| .40–.44|0.23|0.20|0.20|0.30|0.37|0.57|0.60|0.10|

`CHARGING` piles into 06–09 (17 of 38) and 18–22 (14 of 38) — the two high-`QUIET` shoulders.

## Why the existing clock gate never ran

`mesh-correlate`'s clock gate fires only when a token is **confined** to a contiguous band
≤ `CLOCK_BAND_MAX`=12h. At the live `CLOCK_BAND_COVER`=0.9:

| token | 0.9-cover band | gated? |
|---|---|---|
| `ambient=NIGHT-QUIET` | 23:00–06:00 (**7h**) | yes — dropped, as designed |
| `ambient=QUIET` | 06:00–22:00 (**16h**) | **no** |
| `body_power=CHARGING` | 06:00–23:00 (**17h**) | **no** |

The gate is a **band** test; this confound is a **hole**. It is the exact mirror of
`light=DARK ↔ ambient=NIGHT-QUIET`, which this lane discarded on 2026-07-25 — same producer, same line of
source, complementary shape, and the existing control is structurally blind to it. A test for confinement
cannot see a complement.

## Numbers (live tape, era since 2026-08-15T06:30:01Z, n=667 rows)

| | value |
|---|---|
| `P(QUIET)` over era | 0.367 |
| `P(QUIET \| CHARGING)`, n=38 | 0.816 |
| crude era lift | **2.22** (tool reports 2.26 on its episode-collapsed basis) |
| lift an **hour-matched shadow** would report | **1.62** |
| QUIET observed among CHARGING rows | 31 |
| QUIET expected under the hour-matched null | 22.66 |
| **hour-stratified lift** | **1.37** (floor 1.80) |

**Discriminating control — it is not "the phone was readable at all":** the same computation per
`body_power` token shows `DISCHARGING` moves the *other* way (stratified 0.66), `UNREACHABLE` 0.77,
`LOW` 0.00. If the driver were "the phone answered", every readable token would lift together. They do not.

**The residual is not zero, it is under the floor.** A block permutation preserving both the start hour and
the run length (25 contiguous CHARGING runs) puts the observed 31 against a null mean of 23.4, p=0.0045. So
something non-clock is plausibly there — a plugged-in phone is a stationary phone, and both senses ride the
same household rhythm. But 1.37 does not clear 1.80, and this lane's job is to emit findings that clear it.
**Discarded as a finding; the gate below is what the investigation produced instead.**

## The change (uncommitted — `scripts/mesh-correlate`)

`hour_shadow(rs, A, B, x, y)` + a third gate after the clock and regime gates: for every `A=x` row, credit
a shadow with `P(B=y | that row's hour)` computed over the whole tape and sum. `obs/exp` is the
hour-stratified lift — what survives after the hour has been paid what it is owed. Below `MIN_LIFT` → drop
**loudly** on stderr, naming how much the shadow alone scored.

- **Drop-only.** It can remove a candidate or *lower* the published lift (`corr` carries the minimum),
  never mint or raise one. That is also why the sample-level/episode-level unit mismatch is safe here and
  only here: autocorrelation inflates `obs`, which makes the gate more permissive, never more aggressive.
- **Fails OPEN and loudly** when the control cannot be estimated (`CORRELATE_HOUR_SHADOW_MIN_N`=8 usable
  antecedent rows, `CORRELATE_HOUR_SHADOW_MIN_H`=3 rows per hour bucket) — a suppression gate that mutes on
  thin data deletes findings for a reason nobody can see.
- Knobs: `CORRELATE_HOUR_SHADOW` (1; 0 for the red half), `_MIN_N`, `_MIN_H`.

**Live effect** (`mesh-correlate --dry` on the real tape):

```
hour-shadow: DROPPED body_power=CHARGING <-> ambient=QUIET (lift 2.21, 20 episodes) — a shadow with
body_power=CHARGING's exact hour-of-day histogram and NO relation to ambient already scores 1.27 of the
observed 1.67 (n=38); hour-stratified lift is 1.32 < 1.8 — time-of-day profile, not structure
```

It caught a **second** live confound in the same run that no existing gate reached:

```
hour-shadow: DROPPED tempo=RESTING <-> light=LIT (lift 1.86, 10 episodes) — … hour-stratified lift is 0.89
```

## Gate seen RED, then green

Two fixtures in `mesh-correlate --test`, one row per 6h block so both tokens span a 13h band and the
**clock gate cannot fire**:

- `tape-hourhole.tsv` — the whole association carried by the hour (03:00 `DISCHARGING`/`NIGHT-QUIET`,
  08:00 `CHARGING`/`QUIET`, 14:00 `DISCHARGING`/`MODERATE`, 20:00 `CHARGING`/`QUIET` odd days else
  `MODERATE`). Episode-lift 30·80/(40·30)=**2.0** > floor; hour-stratified **1.00** → must drop.
  **(a)** load-bearing red half: with `CORRELATE_HOUR_SHADOW=0` it really does emit. **(b)** with the
  control on it is gone. **(c)** and it went loudly.
- `tape-hourreal.tsv` — **no wolf**: same hour profile, but the antecedent varies *within* its own hours
  and the consequent tracks it. Hour-stratified 20/10 = **2.0** → must survive.

Mutation check: replacing the drop condition with `if False:` turned fixture (b) RED, and the emitted line
printed the fixture's arithmetic back verbatim — *"lift 1.00 (30 episodes) … a shadow with … own
hour-of-day histogram (which alone scores 2.00) — the full-window lift is 2.0"*. Restored → full
`mesh-correlate --test` green.

## What is NOT claimed

The gate drops the **finding**, not the residual. It does not assert that charging and a quiet room are
unrelated; it asserts that the reported 2.26 was mostly the clock and what is left is under the floor. And
`P(QUIET|hour)` is estimated from this tape, so a tape whose hours are unevenly sampled gives a noisier
control — which is what `_MIN_H` exists for, and why the gate fails open rather than guessing.
