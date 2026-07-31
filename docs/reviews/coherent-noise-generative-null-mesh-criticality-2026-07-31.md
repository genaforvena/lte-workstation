# Coherent-noise: the generative NULL to SOC (a sensor-mesh cross-domain transfer)

**Landed:** 2026-07-31 · **Tool:** `scripts/mesh-criticality` (read-only sidecar `--coherent`) · **Mode:** LIVE literature review

## The concept

**Coherent-noise model** (M. E. J. Newman & K. Sneppen, *"Avalanches, scaling, and coherent noise"*,
Phys. Rev. E **54**, 6226 (1996)). A population of agents each carries a random threshold. A single
**global external stress** — "coherent noise" — is drawn each step; every agent whose threshold falls
below it topples and is reassigned a new threshold. The model **contains no direct interaction between
agents and therefore has no dynamical critical point**, yet it produces a **power-law event-size
distribution over many decades**. It is the competing *generative* explanation for a heavy tail: not
internal self-organization near a critical point, but one **common-mode stressor sweeping heterogeneous
thresholds** all at once.

Its one distinguishing fingerprint — the thing conservative SOC *lacks* — is an **Omori aftershock
train**: after a large event, the rate of follow-on events decays as a power law `t^−τ`.

> "the probability to find a large event at time *t* after an initial major event decreases as *t^−τ*
> … with the exponent τ ranging from 0 to values well above 1."
> — C. Wilke, S. Altmeyer, T. Martinetz, *"Aftershocks in Coherent-Noise Models"*, Physica D **120**
> (1998) 401, [arXiv:physics/9710023](https://arxiv.org/abs/physics/9710023) (fetched & read 2026-07-31).

Conservative SOC (the sandpile lineage) is **memoryless between avalanches** — avalanches are
Poisson-timed and temporally uncorrelated, so there are **no aftershocks and no foreshocks**. That
asymmetry is the discriminator.

## Why it is NEW (not any covered sidecar)

Every proximity sidecar already in `mesh-criticality` — branching ratio m̂, susceptibility χ, avalanche
shape, crackling exponent, CSD, Widom/drive, dynamic range, SOB, dragon-kings — **presumes the power law
comes from internal cascade coupling near a critical point** and only asks *how close* the system sits.
None of them can distinguish that hypothesis from the coherent-noise null, in which an **identical**
power-law tail is produced with **zero coupling and no critical point**. It is a *mechanism* question, not
a proximity metric. The closest neighbour, `--widom`, measures the **global** silence fraction φ under
drive; this is the **conditional** post-mainshock rate — a temporal-clustering signature `--widom` and
CSD do not compute.

## The sensor-mesh transfer (the application)

`mesh-criticality` already frames itself as a cross-domain transfer of neural-avalanche SOC onto a
distributed sensor/coordination mesh; the board event stream **is** the sensor mesh's own event tape. The
coherent-noise null asks the operationally sharp question: **is the mesh's near-critical m̂ genuine
self-organization, or one shared stressor hitting many reflexes at once?** — e.g. a Wi-Fi channel storm,
this node's logged **14-minute deauth cycle**, or a thermal/power dip driving many organs to fire together
and *manufacturing* a heavy tail with no coordination at all. The same discriminator transfers verbatim to
dropout/report cascades in `mesh-lan-health` / `mesh-sense-monitor` (the runner-up target).

**Landed** as a read-only sidecar `coherent_regime()` + `--coherent`:

- Extract avalanches from the binned activity tape `A`. Mainshock = size ≥ the `CRIT_COHERENT_HIQ` (0.90)
  quantile.
- **Near-field** = the `CRIT_COHERENT_WIN` (5) bins after each mainshock's end (the Omori window).
  **Far-field** = every other bin *not* inside a mainshock's own span (the background rate).
- **Aftershock excess** `R = mean(near)/mean(far)`, self-calibrated (no hardcoded rate). `R ≥ 1+band`
  (`CRIT_COHERENT_BAND`=0.5) → **COHERENT-NOISE** (the near-critical reading may be an exogenous
  common-mode artifact); otherwise **SOC-CONSISTENT** (avalanches temporally uncorrelated, as conservative
  SOC requires); thin data → **INSUFFICIENT**.
- Reports the Omori exponent τ descriptively (log rate vs log lag) when ≥3 lags are populated.
- **Never touches m̂ / regime / alarm.** No board post. Read-only honesty flag, exactly like the other
  sidecars.

**RED-first `--test`:** a tape whose mainshocks are followed by a decaying aftershock train (3,2,1) must
read COHERENT-NOISE; the *same* mainshocks followed by silence must read SOC-CONSISTENT (label tracks the
excess, is not a constant); <10 avalanches → INSUFFICIENT. Verified the constant-label mutation
(`if False:`) goes RED and the restore goes green.

**Live (real board tape, 2026-07-31):** `SOC-CONSISTENT` — mainshocks=3, aftershock-excess R=0.84,
Omori τ=−0.14, avalanches=25. Honest negative: no post-mainshock rate excess today, so the board's
near-critical readings are **not** an obvious exogenous common-mode artifact at this moment.

## Runner-up (not picked)

**Highly Optimized Tolerance** (Carlson & Doyle, Phys. Rev. E **60**, 1412, 1999;
[arXiv:cond-mat/9812127](https://arxiv.org/abs/cond-mat/9812127)) — power laws from *design/optimization*
under resource constraints ("robust-yet-fragile"). Passed over because its hub-hypersensitivity partially
overlaps the existing hub-driven dragon-king / redispatch-concentration alarm, whereas coherent-noise is
cleanly orthogonal to the whole covered set.

## Unwired next

Per-window join of R (or the aftershock excess) to the m̂ tape: **does the COHERENT-NOISE verdict
coincide with a known external stressor window** (the deauth cycle, a thermal spike)? That would upgrade
the flag from "aftershocks present" to "aftershocks *explained by* a named common-mode source" — the
strong form of the coherent-noise claim. Twin of the edge-optimality / dynrange / susceptibility
tape-joins already noted as open.
