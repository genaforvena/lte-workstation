# LITERATURE review — wear that MOVES the threshold: the Reactive Scope Model (2026-07-24)

**Area:** homeostasis / allostasis / ultrastability, entered from the angle of a **known critique** —
the objection that *allostatic load* is a cost account that never feeds back into the control law.

## The critique

Allostasis ("stability through change", Sterling & Eyer; Sterling 2012) and its cost term *allostatic
load* (McEwen & Stellar) have a standing complaint against them: they describe chronic wear
conceptually without operationalising it. The stress literature's own answer to that complaint is the
**Reactive Scope Model** (RSM; Romero, Dickens & Cyr, *Horm Behav* 2009), and the live 2025 restatement
is blunt about what was missing:

> "physiological 'wear and tear' accrues when mediators are in the reactive range, and over time, this
> wear and tear can **lower the threshold for homeostatic overload**."
> — Gilmour, Best & Currie, *Using the reactive scope model to redefine the concept of social stress in
> fishes*, J Exp Biol 228(6):jeb249395 (2025).
> The RSM "adds temporal dynamics and threshold mechanics that allostasis describes conceptually but
> doesn't operationalize."

Note the sharper form of "wear and tear" here — it is **not** the slow accumulation of damage with
age. It is the shrinking of the reactive range itself, so that *a future insult of the same magnitude*
tips into overload where an earlier identical one did not.

## The mechanism we did not embody

Formalised in Wright, Buch, Beattie, Gormally, Romero & Fefferman, *A mathematical representation of
the reactive scope model*, J Math Biol (2023), PMC10468437 — **two** boundaries, not one:

    dM/dt = −r₁·θ(y−R)
    dR/dt = −r₂·θ(y−P) + r₃·θ(P−y)·θ(M−R)

- **R(t)** — the current reactive↔overload boundary. Narrows while the mediator `y` sits above the
  predictive threshold `P`; heals back up while it rests below `P`.
- **M(t)** — the **ceiling R may heal back to**. It drops only when overload is genuinely entered,
  and it does not come back.

That second variable is the whole content of the critique. A decaying counter recovers to full; a
reactive scope does not. **After an overload episode, unlimited rest leaves the system with
permanently less headroom.** That is the testable difference between RSM and every "chronic load"
number that merely decays.

**What we had:** `scripts/mesh-stress` already landed allostatic load (review 2026-07-06) — it COUNTS
this node's regulatory-intervention edges over a 6h window and raises a WARM-capped watch flag. The
bands it is judged against (`WARM_C` 90 / `STRESSED_C` 95 / `CRIT_C` 98) are fixed constants. A node
baking at 94°C for six hours is judged by the same 98°C line as one that just arrived. The counter
never moves the line. That is precisely the gap RSM names.

## Application (implemented)

`scripts/mesh-stress` — new **reactive-scope axis**:

- `scope_step R M temp dt` — a pure integrator (tenths of °C, no clock, no files) implementing the two
  equations above. `P = WARM_C`, `R` starts at `CRIT_C`, `M = CRIT_C`.
- `scope_update` — reads/steps/persists `~/.mesh/.stress-scope` (`R M last_ts`), integrating **elapsed
  wall-clock**, so repeated `--status` calls cannot double-count.
- Reported in the reason string: `scope=97.5C`, plus `ceiling=…C(spent)` once an overload episode has
  cost the ceiling, plus `headroom-lost↑`.
- Fusion is **WARM-capped**, exactly like pkg-watts / allostatic-load and for the same reason: `r₁ r₂
  r₃` are uncalibrated for this hardware, so a narrowed `R` is REPORTED and must never be the line the
  verdict is taken against. `R` is additionally floored at `STRESSED_C` — a wear axis may not invent an
  alarm below an already-calibrated band.
- A dead thermal organ (`temp=-1`) **holds** the state instead of integrating as restful cooling — a
  broken sensor must not silently heal the scope back to full (the silent-fallback rule).

Gates (`mesh-stress --test`, all fixture-driven off the pure integrator): 1h above `P` narrows `R` by
exactly `r₂`; rest heals `R` but the heal is capped at `M`; **the signature** — after an overload
episode, ten hours of rest leaves `R` below nominal; `R` floors at the calibrated band; `dt=0` is a
no-op; `temp=-1` holds. Seen RED against the naive reading (heal capped at the nominal ceiling instead
of at `M`): *"RSM signature: after an overload episode, unlimited rest must NOT restore the nominal
boundary — got R=980 M=960 nominal=980"*.

## Honest limits — and a second finding

The axis is live and reporting (`mesh-stress --status` → `scope=98.0C`, state `980 980 …`), but it has
**not yet fired**, and on the current regime it cannot. Replaying this node's own `~/.mesh/therm.log`
(1716 samples, 2026-07-18 → 2026-07-24) through the integrator: **0.0h above P, 0.0h in overload, R
and M never leave 98.0C.**

The reason is not the new axis — it is that **the stress-thermal bands are stale**. They were
calibrated 2026-06-13 against the GPE0x6E storm (p50=90, max=102). The live curve is a different
machine: **p50=64, p75=67, p90=69, p95=70, p99=72, max=76 — 0.000% of samples reach 90°C.** So the
entire thermal axis of `mesh-stress` currently cannot leave CALM on temperature; the WARM it reports
today comes from pkg-watts. That is the same failure this codebase already named for the sound lane
("calibrate a derived axis against the REAL corpus, never an assumed range") showing up in the thermal
lane: a threshold pinned to a regime that has since ended reads as permanent calm.

Follow-up (NOT done here, needs its own calibration pass): re-derive the `stress-thermal` row of
`scripts/uxn/threshold-ledger` from the live `therm.log` percentiles, or express `P` relative to the
running p50 so the axis self-calibrates and cannot silently die when the regime moves again. Until
that happens the reactive-scope axis is correct, gated, and dormant — which is stated here rather than
reported as a win.

**Done, same day** (board `stress-thermal-bands-stale`): the second option, not the first — re-fitting
the numbers to today's corpus would only re-arm the same trap at the next regime change. `WARM` now
takes the stricter of two arms, `min(warm_abs, running_p50 + wd)` (`wd=8` in the ledger row, which
grew a `p50` param and its own fixtures/mutant for the relative arm); on this node that is **72°C
against p50=64, n=1728** — the axis can leave CALM again, and on the storm curve (p50=90) the absolute
arm still binds, so nothing moved where it must not. `STRESSED`/`CRITICAL` stay **absolute** on
purpose: they gate a shed and the board alarm, and scaling them to a cool node's median would post
CRITICAL at 80°C on a node 15°C from any hazard — the mirror failure. The standing detector is
`mesh-stress --test`'s band-reachability gate (RED when the WARM band in force exceeds every
temperature the node's own curve reached in the window; seen red against the pre-fix configuration,
against too wide a `wd`, and against an operator pin above the curve). What stays true: the reactive
scope axis is still dormant — P is now reachable, but nothing has yet spent headroom.

## Sources

- [Gilmour, Best & Currie 2025 — Using the reactive scope model to redefine the concept of social stress in fishes, J Exp Biol 228(6):jeb249395](https://journals.biologists.com/jeb/article/228/6/jeb249395/367509/Using-the-reactive-scope-model-to-redefine-the)
- [Wright et al. 2023 — A mathematical representation of the reactive scope model, J Math Biol (PMC10468437)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468437/)
- [Romero, Dickens & Cyr 2009 — The Reactive Scope Model, Horm Behav](https://www.sciencedirect.com/science/article/abs/pii/S0018506X08003383)
- [Sterling 2012 — Allostasis: A model of predictive regulation, Physiol Behav](https://www.sciencedirect.com/science/article/abs/pii/S0031938411003076)
- [Allostasis — criticism (Carpenter: allostasis reinvents an accurate reading of homeostasis)](https://en.wikipedia.org/wiki/Allostasis)
