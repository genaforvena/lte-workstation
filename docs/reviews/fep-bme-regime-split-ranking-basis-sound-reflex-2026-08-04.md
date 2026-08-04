# FEP / active inference — embodiment 2026-08-04

## The BME finding, written into the organ that the finding was about: `mesh-sound-reflex --regime`

**Lane:** genome (the write half of the metabolic loop).
**Source find:** `docs/reviews/fep-bayesian-model-expansion-structure-learning-precision-2026-08-04.md`
(landed as `mesh-precision --bme`, commit `ad58f8e`).
**This edit:** `scripts/mesh-sound-reflex` — new report-only `--regime`.

---

## 1. What the source find left open

The BME review landed the estimator and pointed it at one live tape:

> LIVE: `dyn` over `~/.mesh/records.log` reads **EXPAND** (n=471 lnK=4.52 split@205) — the corpus
> `mesh-sound-reflex` ranks against is two regimes pooled as one (confounded w/ a scape/drop mix
> shift 13.7→9.0%).

Two things were owed. The finding names an organ (`mesh-sound-reflex`) that could not ask the
question of itself — the verdict lived in another tool's one-off invocation, which is the
"a subagent's finding does not exist until it is landed" shape at tool scale. And the finding's own
stated weakest joint — the mix-shift confound — was never resolved, so the claim as it stood was
*"either the corpus changed regime, or the organs' proportions changed"*, which are different faults
with different remedies.

## 2. The three questions about one ranking corpus

`corpus_pct` ranks every record against the live ledger. Two properties of that basis were already
measured in this file; the third had no reader:

| mode | question | axis |
|---|---|---|
| `--ergodicity` (2026-07-24) | WHICH population does this record belong to? | organ — a **spatial** split |
| `--basis-drift` (2026-08-03) | WHEN may the ruler move? | turnover — the ruler's **velocity** |
| `--regime` (this edit) | is there ONE population in time **at all**? | a **temporal** split |

The gap is structural, not an oversight: every structure-learning move in the mesh had been a
REMOVAL — `--bmr` prunes, `sensorium --balance` prices redundancy, `reflex-decay` retires. Nothing
could ask whether the data warrant an EXTRA state, so a corpus that really *is* two regimes is
pooled into one and every percentile drawn from it ranks a record against a mixture of a
distribution that ended and one that started.

## 3. The mix-shift confound, resolved

`--regime` reads each axis **both ways**, and this is the whole content of the report rather than a
second opinion:

- **POOLED sequence** — file order across organs. `records.log` is a per-organ sliding window, so a
  shift in the *mixing proportions alone* can read EXPAND with neither organ's own distribution
  having moved.
- **PER-ORGAN** — each organ's own tape, which a mixing shift cannot move.

Only a per-organ EXPAND restricts anything. Live, the confound **does not explain the finding**:

```
REGIME dyn -> s  pooled=EXPAND  per-organ[drop:EXPAND@181(lnK=1.33) tail=238 mean 0.4327->0.3668
                                          scape:PARSIMONIOUS(n=52)]  n=20 med|dp|=0.128 slot_flips=14
```

`drop`'s own dyn tape (n=419) is two regimes on its own evidence. The source find's alternative
explanation is falsified, not merely restated — and the split is **discriminating**, not a blanket
verdict: every other axis (`act` MARGINAL, `rich`/`move`/`cent` PARSIMONIOUS) and `scape` on every
axis leave the basis alone.

## 4. What the restriction would buy

`dyn` drives `s` — the TRACK SPEED, the rhythm axis. Re-ranking the last 20 records against the
current regime instead of the whole history moves **14 of 20 into a different `s` slot**
(med |Δp| 0.128, max 0.692). That is the number the steward is being asked about; it is not small.

## 5. Report-only, deliberately

Restricting the basis changes what gets ground. The `--basis-drift` block one screen above says the
same thing about freezing and holds for the same reason, and this stays consistent with it: `--regime`
prices the restriction and adopts nothing. The one place it would be easy to be dishonest — a real
split whose current regime is too short to rank against — renders `NOT-ADOPTED` with the tail size
shown, because a basis below the noise floor is a *different* fault, not an improvement over a mixed
one (`corpus_pct`'s own `<8` rule is the same instinct).

## 6. The estimator is not re-implemented

`bme_read()` shells to `mesh-precision --json --bme`. The closed form is ~15 lines and copying it
would have been cheaper — and would have given this file a second estimator that can rot apart from
the gated one. `BME_CORE`'s "defined ONCE" discipline is held **across the tool boundary**, and the
`--test` legs drive the real binary, never a stub (the whisper.cpp trap: a wrapper's test that never
invokes the thing it wraps asserts nothing about it).

Every failure mode — binary absent, non-zero exit, timeout, unparseable output — gets its own `n/a`
verdict string. A reader cannot tell "one regime" from "could not ask", so neither may quietly become
the other; a dead `mesh-precision` must not read as a healthy single-regime corpus.

## 7. Gates

`--test` block **2g**, five legs, all driving the real estimator through the real report path:

| leg | fixture | asserts |
|---|---|---|
| (i) two regimes | 30 records `move~0.1x` then 30 `move~0.6x`, one organ | `drop:EXPAND@` found **and** slot_flips > 0 — a split with no priced consequence is not worth reporting |
| (ii) control | 60 records cycling the same 15 `move` values | `PARSIMONIOUS` + `basis unchanged` + total flips **0** — the report cannot manufacture a split from sample noise |
| (iii) mix shift | two organs, each stationary, proportions flipped halfway | `pooled=EXPAND` with **every** organ PARSIMONIOUS and the basis refused |
| (iv) thin tail | 40 records then 8 | `EXPAND@40 … tail=8<12 NOT-ADOPTED`, basis unchanged |
| (v) estimator absent | `SR_BME_BIN=/nonexistent/...` on the (i) ledger | `n/a(estimator unreachable…)`, and **explicitly fails** on PARSIMONIOUS or EXPAND |

(i) and (ii) are each other's red by construction. Five mutants run from a scratch copy, each red for
its own leg and green everywhere else:

| mutant | edit | dies at |
|---|---|---|
| M1 | unreachable estimator returns `PARSIMONIOUS` | (v) |
| M2 | `len(_tail) < REGIME_MIN` floor removed | (iv) |
| M3 | per-organ read replaced by the pooled tape | (iii) |
| M4 | `bme_read` never forks — no split ever claimed | (i)+(ii'... all five) |
| M5 | regime slot-flip counter pinned to 0 | (i) |

Control green. Suite 16.5s (was ~15s), well inside the runner's 30s.

Note on M5: the naive edit (`if _i[0] != _i[1]` → `if False`) matches **two** sites — the
`--basis-drift` counter shares the idiom — and killed that neighbouring gate too. Re-run scoped to
the last occurrence, it kills the `--regime` leg alone. Both readings are reported; a mutant that
goes red because it broke a *different* gate has not tested the one you meant.

## 8. Held

- **Adoption.** Restricting `dyn`'s basis to the current regime flips 14/20 `s` slots. That is a
  change to what the operator hears; the steward/operator decides, not this lane.
- **A regime-aware `corpus_pct`.** The composition is already worked out (regime restriction first —
  WHEN — then the existing organ logic — WHO) and is deliberately not wired.
- **Cadence.** `--regime` is on-demand like `--basis-drift`, not in `--status`: 0.39s and 5 forks is
  too much to pay on a pane that refreshes.

## 9. Weakest joint, stated

The split index is an index into the ledger's *retained* order, and `records.log` is pruned every
sweep. A regime boundary that ages out of the window stops being findable — the report will
eventually call a two-regime corpus one-regime not because it healed but because the older regime was
evicted. `--regime` reports `n=` per organ so the reader can see the window it is reasoning inside,
but it cannot see past it, and no figure here is reproducible against a future ledger
(`records-log-is-a-sliding-window`).
