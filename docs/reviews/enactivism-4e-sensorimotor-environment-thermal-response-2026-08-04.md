# Enactivism / 4E — the sensorimotor ENVIRONMENT (s = g(m)) as a mesh axis

**Date:** 2026-08-04 · **Lane:** genome, live literature review · **Landed in:** `scripts/mesh-therm --response`

## The mechanism

**Buhrmann, T., Di Paolo, E. A., & Barandiaran, X. (2013). "A dynamical systems account of
sensorimotor contingencies." *Frontiers in Psychology* 4:285. doi:10.3389/fpsyg.2013.00285**
(open access, PMC3664438 — read live 2026-08-04). Live restatement in the current sensorimotor
literature: **arXiv:2510.14227**, "Sensorimotor Contingencies and The Sensorimotor Approach to
Cognition" (2025); 2026 framing of action–perception inseparability as an AI design constraint:
**Rafiee & Sutton, arXiv:2605.24238, "Toward Enactive Artificial Intelligence"** (2026-05-22).

The paper's contribution is not philosophy — it is the **operational disambiguation** of four things
that "sensorimotor contingency" talk conflates. Two of them are the ones with teeth:

| kind | definition (verbatim) |
|---|---|
| **SM environment** | *"the set of sensory states as a function of motor variations independently of the agent's internal (e.g., neural) dynamics"* — the loop **opened**, motor treated as the independent variable: `s = g(m)` |
| **SM habitat** | *"the set of possible sensorimotor trajectories traveled by a closed-loop agent for a range of values of relevant parameters"* |
| SM coordination | *"individual trajectories within the SM habitat that occur reliably and contribute functionally to a goal"* |
| SM strategy | coordinations organised by a normative preference |

The methodological claim: **the habitat is not the environment.** An agent that observes only its own
closed loop never recovers `g`. Any claim about what its body can do must be evidenced from outside
the trajectory the standing policy happens to travel.

## What we already embody (checked, not assumed)

Four candidate readings of this were **discarded because the mesh already has them**, each verified
against the genome before writing a line of code:

- *"exercise the un-taken branch"* — `mesh-relay --chaos-drill` already force-fails pools to drive
  the fallover chain; `mesh-say --test:103` already gates the piper fallback.
- *"a reliable pattern with no functional role"* (SM **coordination**, the `and contribute
  functionally` half) — `mesh-doctor`'s **umwelt-check** already flags a state producer with no
  reader, `# umwelt-ok:` self-declares intentional-manual-only.
- *"a sense that never moves"* — `mesh-lease` **FLATLINE** (byte-identical evidence across renewals)
  and `mesh-precision` **FROZEN** (variance-collapse, precision capped so a flatline is never
  up-weighted) both already exist.
- *"did the reflex produce at all"* — `mesh-reflex-health` (wired-but-dead / stale artifact).
- SM **strategy** (normative selection among coordinations) — `mesh-fitness`.

## The gap that survived

**Every one of those is UNIVARIATE on `s`.** They ask *is the sensor alive*, *how hot is it*, *does
anyone read it*, *did it refresh*. **None asks the bivariate question the SM-environment concept
names: does this sensor move with the work this node does.**

A sensor can be alive, jittering, precision-weighted, read by eight consumers — and still be
**decoupled from the agent's own action**. The guard then thresholds on a channel its own compute
cannot move. This is one level up from the failure `mesh-therm`'s own header records (`max=0` — a
plausible reading nothing downstream could reject): not a fake value, **a real value on the wrong
channel**.

The mesh measures sense↔sense coupling (`mesh-cooscillate`, APPLIANCE×APPLIANCE) and sense liveness.
It has **no action↔sense coupling axis anywhere** — the only prior instance is
`mesh-audio-active --confirm`, which is binary (heard | unheard) for one self-issued emission.

## The landing: `mesh-therm --response`

`~/.mesh/therm.log` already carries the motor variable and every sensory variable **on the same
line** (`load=` and `zones=[...]`, both written by `mesh-therm` itself). The pairing is free — no new
probe, no state written, no reflex touched, report-only, exit 0.

Per sensor: OLS slope (°C per unit loadavg), Pearson r, n — plus the same for the `max=` channel,
which is what every downstream thermal consumer thresholds on.

### The live result on mesh-home (n=1561 rows, load support 0.46..30.88)

```
  1:nvme/Composite         slope= -0.047 °C/load  r=-0.055  n=1561
  2:nvme/Sensor 1          slope= -0.116 °C/load  r=-0.034  n=1561
  3:nvme/Sensor 2          slope= -0.200 °C/load  r=-0.055  n=1561
  ...
  8:k10temp/Tctl           slope= +1.048 °C/load  r=+0.525  n=1561
  9:k10temp/Tccd1          slope= +0.440 °C/load  r=+0.304  n=1561
  10:gpu                   slope= +0.272 °C/load  r=+0.394  n=1561
  max (guarded)            slope= +0.088 °C/load  r=+0.073  n=1561
  6:nvme/Sensor 2          n=436   FLAT — never moved (value=56.8)
best-coupled sensor: 8:k10temp/Tctl (|r|=0.525, +1.048 °C per unit loadavg)
WARN guarded channel DECOUPLED: max |r|=0.073 vs best |r|=0.525 (ratio 0.14 < 0.50)
```

**`max=` — the single number the whole thermal-homeostasis lane thresholds on
(`mesh-therm-watch`, `mesh-stress`, `mesh-therm-regime`, `mesh-therm-ambient`, `mesh-cpu-throttle`,
`mesh-patterns.sh`, `mesh-mind-keepalive`) — is pinned by NVMe sensors whose slope is ≈0 or
NEGATIVE.** `nvme/Sensor 1` reaches 75.8 °C where `k10temp/Tctl` tops out at 69.5, so the hottest-
sensor rule hands `max` to a channel with r=0.07 against this node's own compute, while the channel
that actually responds (+1.05 °C per unit loadavg, r=0.53) is discarded by the max-fold. Compute-
driven heating is largely invisible to the guards. Nothing in the mesh could see this, because
nothing crossed the action ledger with the sensory one. (Sibling of
[[max-fold-effaces-the-disjunction]], measured rather than argued.)

This is **reported, not acted on** — changing what `max` means touches eight consumers and is the
steward's call. `--response` is the measurement that makes the choice arguable.

### Design decisions

- **UNIDENTIFIED, never a coefficient fitted to a constant regressor.** The log is closed-loop —
  `load` is what the mesh *happened* to do, not a commanded sweep — so this estimates `g` only over
  the habitat actually traveled. When the load support span in the window is below `MIN_SPAN`, the
  tool says so and prints **no slope at all**. The paper's central claim made structural: a
  regression over a constant motor variable is the very blindness this axis removes, wearing a
  coefficient. (Leg r2; mutant M1 RED.)
- **FLAT decided on exact `min==max` of the raw readings, never on a computed variance.** The
  streaming form `SYY−SY²/n` cancels catastrophically for a constant sensor — `nvme/Sensor 2` sat at
  56.9 °C for 436 rows and first came out as `slope=+0.000 r=+0.000`, i.e. *a well-measured zero
  response* where the truth is *this sensor never moved*. A degenerate channel must be **named**.
  (Caught during implementation, against live data.)
- **The DECOUPLED flag is a ratio WITHIN THIS DATA, not an invented absolute r.** It asks whether
  the guarded channel tracks the node's work as well as the best channel available on the same node
  in the same window. Self-calibrating, so it cannot rot into a dead constant
  ([[a-constant-outlives-its-reader]], [[stress-thermal-bands-calibrated-to-a-dead-regime]]).
- Missing history ⇒ **exit 2** (honest n/a), never a fabricated response.
- Env: `MESH_THERM_LOG`, `MESH_THERM_RESPONSE_MIN_N` (24), `MESH_THERM_RESPONSE_MIN_SPAN` (1.0),
  `MESH_THERM_RESPONSE_DECOUPLED_RATIO` (0.5).

### Test (RED-first, functional not arithmetic)

Five legs, all driving `"$0" --response` end-to-end against fixture logs — a pure-arithmetic leg
asserts the regression and not the wiring (the `mesh-load-gate` E9 lesson):

| leg | asserts |
|---|---|
| r1 | fixture `cpu = 50 + 2·load` exactly → **slope +2.000, r +1.000**; constant `disk` → FLAT; best-coupled = cpu; **no** false DECOUPLED alarm |
| r2 | constant `load` → `UNIDENTIFIED — load support span`, and **no `slope=` anywhere in the output** |
| r3 | 5-sample window → UNIDENTIFIED |
| r4 | missing log → rc=2 |
| r5 | max pinned by a load-blind hot sensor → **WARN DECOUPLED** fires (the alarm arm — a gate whose alarm arm is never exercised is not a gate) |

Six mutants run from a scratch copy, each RED on a **distinct** leg, plus a no-op control green:

```
M1 drop support gate         FAIL (--response fitted a slope to a CONSTANT load …)
M2 slope=sxy/syy             FAIL (--response missed the KNOWN slope +2.000/r+1.000 …)
M3 drop FLAT branch          FAIL (… must be NAMED, not rendered as slope 0 …)
M4 mute DECOUPLED warn       FAIL (--response missed a guarded channel decoupled …)
M5 drop min-n gate           FAIL (--response did not refuse a 5-sample window)
M6 missing log rc=0          FAIL (--response on a missing log → want rc=2, got rc=0)
M7 no-op control             ok
```

`mesh-therm --test` 0.33 s (was ~0.2 s); bare and `--verbose` snapshot paths byte-identical.

## Follow-on this opens (not claimed here)

`g(m)` is the **precondition for the still-open allostasis gap** (Candia-Rivera, arXiv:2604.24527 —
homeostatic / allostatic / enactive interoception; every mesh guard thresholds on *current* state,
none pre-adjusts on *predicted* demand). You cannot anticipate what a queued grind will do to
temperature without knowing what load does to temperature. That is now measured.

Second follow-on: the same axis generalises — the mesh logs its actions (spend, grind params, cron
runs, board posts) and its senses in separate ledgers that are **never crossed**. `--response` is the
first crossing.
