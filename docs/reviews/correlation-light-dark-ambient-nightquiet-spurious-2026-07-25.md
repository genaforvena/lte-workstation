# CORRELATION investigation: `light=DARK ↔ ambient=NIGHT-QUIET` — SPURIOUS (clock confound)

**Date:** 2026-07-25 · **Mind:** genome@mesh-home · **Source:** ideas-queue, `mesh-correlate` LIFT lane
**Claim under test:** *when `light` reads DARK, `ambient` tends to read NIGHT-QUIET (lift 2.2, 8 distinct
episodes of 79, window 242.7h; autocorrelation-collapsed).*

**Verdict: SPURIOUS.** One line: `mesh-ambient-clock` computes NIGHT-QUIET as `QUIET ∧ (23:00–05:00)`,
so the label cannot exist outside 7 of 24 hours — and the light sensor reads DARK in those hours
because of the sun. Conditioned on that window the lift is **exactly 1.000**.

---

## 1. The finding is arithmetically real

Reproduced independently from `~/.mesh/sensor-tape.tsv` (1266 rows, 2026-07-14T22:40Z →
2026-07-25T01:40Z), same episode-collapsing the tool uses:

| measure | value |
|---|---|
| lift(`light`=DARK, `ambient`=NIGHT-QUIET) | **2.179** (8 of 79 episodes) |

So this is not an arithmetic error. It is a *correct measurement of the wrong thing*.

## 2. It is the clock, read from the producer's own source

`scripts/mesh-ambient-clock:1009`:

```bash
if [ "$label" = "QUIET" ] && { [ "$HOUR" -ge 23 ] || [ "$HOUR" -le 5 ]; }; then
  label="NIGHT-QUIET"
```

NIGHT-QUIET **is** QUIET ∧ off-hours. The tape agrees: of 241 NIGHT-QUIET rows, 235 fall in 23:00–05:00
and 728 of 734 QUIET rows fall outside it (the ~6+6 leakage is edge skew — the row's `ts` is when the
tape sampled, minutes after the label was computed).

This is not a *statistical* confound to be argued about. The label carries a wall-clock predicate in its
definition, so `NIGHT-QUIET` vs `QUIET` is the same appliance state split by the hour.

## 3. The decisive measurement

Restrict to the only hours the label can occur in (23:00–05:00, n=320 rows):

| | lift | episodes |
|---|---|---|
| pooled (what the miner reported) | 2.179 | 8 of 79 |
| **restricted to 23:00–05:00** | **1.000** | 8 of 15 |
| the bare clock: lift(DARK, off-hours) | 2.045 | 9 of 75 |

Partial lift **1.000** = DARK carries *zero* information about NIGHT-QUIET once you know the hour. And
the bare clock predicate reproduces almost the whole pooled association on its own (2.05 vs 2.18).

**Not causal, not useful anyway.** There is no fused sense or reflex to propose: a "DARK ⇒ NIGHT-QUIET"
rule is a sunset detector with extra steps, and both organs already read the clock more cheaply.

## 4. The part worth fixing: the generator, not the finding

This was the LIFT lane's **first and only emitted finding** over the full extent of
`~/.mesh/correlate.log` — 424 runs, 2026-07-14 → 2026-07-25 (the log opens with "no tape yet", i.e. it
covers the lane's entire life on this node). One finding, and it is the clock. Nothing in
`mesh-correlate` controlled for time of day; its only tautology guard is the `FAMILY` dict, and
`light`(PHONE) / `ambient`(NODE) are cross-family, so the pair was never a candidate for exclusion.

Three confound classes were already documented in-source (collapse-inflation, high-base-rate token,
regime-shift), each with its fix **HELD** — "could suppress genuine findings; validate vs the seed
history first". This is the fourth, and the history *is* the validation: there are no genuine findings
to suppress.

### What shipped (`scripts/mesh-correlate`, uncommitted — steward lands)

**LIFT — clock-gate control.** For a winning pair, compute each token's *occupancy band*: the narrowest
contiguous circular hour window covering ≥90% of its readings. If either token is confined to ≤12h,
recompute **the same episode-lift restricted to that band**. No association there ⇒ the finding was the
clock ⇒ drop it, loudly, to the log.

- The band is read from the **data**, not guessed. A negative result forced this: stratifying by fixed
  6h blocks leaves the partial lift at **1.32** — still "surviving" — because the producer's 23–05 gate
  *straddles* two blocks. A guessed strata width is only as good as its alignment with a gate it does
  not know about. Self-calibrating, nothing to rot.
- **It cannot cry wolf by construction:** inside the band is the only place a gated token can occur, so
  a real association must show there. Outside it, the "co-occurrence" is both tokens being absent
  together — which is the clock.
- The drop prints to the log, never silently: a discarded candidate must not be indistinguishable from
  "nothing found today" on a lane that emits at most one finding per half-hour.

**PRED — clock baseline.** Found by the new fixture, not by inspection: with the LIFT gate on, the same
clock-confounded tape still emitted *"light at t predicts ambient at t+1 — 100% vs 53% baseline, perm-p
0.001"*. Perfectly significant, and still just the clock — significance cannot catch it, because the
link **is** real; it is the clock wearing a sensor's name. So the hour now competes as a third baseline
alongside majority-class and persistence: `base = max(maj, pers, clock)`. Deliberately conservative (24
buckets can out-resolve a 2-token predictor, so it errs toward silence — this file's stated default),
priced against a lane whose entire record is one confound. `CORRELATE_PRED_CLOCKBASE=0` restores the
old behaviour.

### Gates (all seen RED, each on its own assertion)

| mutation | fails |
|---|---|
| LIFT control disabled at source | clock-confounded pair emitted as a finding |
| drop made silent | candidate dropped SILENTLY — no notice in the output |
| control drops everything | suppressed a link that HOLDS INSIDE the gated token's own band |
| PRED clock baseline disabled | clock-confounded PREDICTION emitted |

Both new fixtures carry their **own** RED half in the suite (`CORRELATE_CLOCK_GATE=0` /
`CORRELATE_PRED_CLOCKBASE=0` must still emit the confound), so a fixture that silently stopped tripping
the miner fails loudly instead of turning the gate vacuous.

**One of these gates was vacuous when first written and the mutation caught it.** The original no-wolf
check reused the all-hours `tempo↔psi` fixture — but `BUSTLE` spans a 15h band, over `CLOCK_BAND_MAX`,
so the control never ran on it and the assertion held *no matter what the drop decided*. Mutating the
drop to fire unconditionally left it GREEN. Replaced with a fixture that puts the gated token inside a
narrow band and keeps a real association there (NIGHT-QUIET only at 01:00/02:00, DARK tracking it while
LIT tracks MODERATE → in-band lift 2.0, must survive). That fixture needed 20 days, not 8: the
alternation collapses across the midnight boundary, so 8 days fell under MIN_SUPPORT and the fixture
would have read "no finding" for a reason unrelated to the control.

### Live A/B on the real tape

```
controls OFF: 17.434  LIFT  lift:light:ambient  CORRELATION ... lift 2.2, 8 distinct episodes of 79
controls ON : clock-gate: DROPPED light=DARK <-> ambient=NIGHT-QUIET (lift 2.18, 8 episodes)
              — ambient=NIGHT-QUIET is confined to 23:00-06:00 (7h); inside that band lift is 1.00
                (8 episodes) < 1.8 — time-of-day confound, not structure
              no correlation/prediction meets thresholds (need more data — honest empty, not a failure)
```

The only thing the controls remove on live data is the confound. `--test` 0.35s (well inside
`mesh-autowire`'s `timeout 30`); deployed == genome.

## 5. Why this mattered beyond one bad idea

`.correlate-state` is capped at `RECENT_MAX=40`, so the suppression of an already-emitted key **ages
out** — without this control the same clock confound returns and costs another mind another paid turn,
indefinitely. A miner whose lifetime output is one tautology is not a quiet miner; it is a miner aimed
at the wrong thing.
