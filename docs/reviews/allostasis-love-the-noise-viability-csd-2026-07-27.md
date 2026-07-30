# LITERATURE review — allostasis "love the noise": the fluctuation IS the signal (2026-07-27)

**Area:** homeostasis / allostasis / ultrastability (Ashby, Sterling), from the angle of a foundational
idea we **applied too loosely** — that variability is error to be minimized, when allostasis says the
variability is anticipatory *information*.

## The foundational idea, and where we read it too loosely

Sterling's allostasis (Sterling & Eyer; Sterling 2012, *Physiol & Behav*, doi:10.1016/j.physbeh.2011.06.004)
already reframes the set-point: *"a mean value need not imply a set-point but rather the most frequent
demand."* The mesh embodies that mean-shift well — `mesh-algedonic`'s ALLOSTATIC_LOAD sidecar already
integrates the fused pain **level** over time (cumulative burden, the Lee et al. / Hunt von Herbing
2024–2025 transfer). But the **level is only the first moment.** The still-live restatement of allostasis
is blunter: variability itself is not noise around the set-point — it is the leading edge of regulation.

- **Imran Khan, "[Social] Allostasis: Or, How I Learned To Stop Worrying and Love The Noise",
  arXiv:2508.12791 (Aug 2025)** — https://arxiv.org/abs/2508.12791. Thesis: regulatory systems should
  *exploit* stochastic fluctuation as predictive information for pre-emptive adjustment, rather than treat
  it as error to average away. "The system learns to anticipate future demands using information embedded
  in seemingly random fluctuations."
- The mechanism that operationalizes this is the generic early-warning-signal canon: **rising variance
  AND rising lag-1 autocorrelation both precede a critical transition** — Scheffer et al., *Early-warning
  signals for critical transitions*, Nature 461:53 (2009), doi:10.1038/nature08227. This is **critical
  slowing down (CSD)**: as a system nears a bifurcation it recovers more sluggishly from perturbations, so
  its second moment inflates *before* its mean crosses any threshold.

## The gap — CSD is embodied on ONE narrow axis, not on the fused viability signal

We did read the CSD literature — but we scoped it to the single variable of this node's #1 failure mode:
`mesh-therm-watch --csd` computes variance + lag-1 autocorrelation of **temperature** alone, fused by
`mesh-therm-regime` (scripts/mesh-therm-regime:15-19). That is exactly the **subsystem-silo pathology**
`mesh-algedonic` was built to cure: many homeostats, each watching its own variable. The one
cross-subsystem signal the algedonic channel exists to fuse — global viability — was watched only at the
**level** (ALLOSTATIC_LOAD = rolling mean + high-count). Its own fluctuation, the thing "love the noise"
says is the anticipatory signal, was averaged away. Distributed sub-threshold *creep with rising
instability* (the algedonic channel's whole reason to exist) has a second-moment tell that no level
integral can see.

## The concrete application (implemented, read-only)

**File: `scripts/mesh-algedonic`** — added a `viability_csd()` sidecar (+ `CSD_N`/`CSD_MIN_N` knobs) that
reads the fused pain series from its own `algedonic.log`, splits the window, and labels:

- `CSD_PRECURSOR` — variance **and** lag-1 autocorrelation **both rising** (the corroborated Scheffer
  signal): viability is slowing down, an approaching transition, *before* the mean says so.
- `CSD_STABLE` — not both rising.
- `CSD_FLAT` — real variance floor (`var < 1e-4`) so a dead-flat series never trips on numerical noise.
- `CSD_UNKNOWN` — insufficient samples / pain UNKNOWN (honest degradation, no faked calm).

Emitted on every run as `csd=<label> vtr=<var-trend> actr=<ac-trend> csdn=<n>`, right beside the existing
`allostatic=` (level) and `agency=` (empowerment) sidecars. **READ-ONLY, advisory — never escalates**,
matching how CSD stays advisory on the thermal axis and honoring this tool's "measurement before the
actuator" discipline. Level answers *how bad now*; CSD answers *is it about to get worse* — the two are
orthogonal and now sit side by side on the one signal that fuses every subsystem.

Gate: `mesh-algedonic --test` case (8) forges a rising-variance ramp → `CSD_PRECURSOR`, a flat series →
`CSD_FLAT`, UNKNOWN pain → `CSD_UNKNOWN`. RED-first verified: mutating the PRECURSOR condition to `False`
turns the ramp assertion red (`expected CSD_PRECURSOR got CSD_STABLE`), restoring it goes green. Live run
2026-07-27T15:26Z reads `csd=CSD_FLAT vtr=-0.0016` on a calm mesh — correctly not tripping.

## Why not discarded

It would be discardable if the algedonic channel already watched a second moment anywhere, or if CSD were
already fused across subsystems. It is not: CSD lives only on temperature, and the fused-viability read —
the exact place the "distributed creep" argument in this tool's own header points — watched only the
level. The fresh 2025 literature (Khan) names precisely the mis-read ("love the noise"), and the
mechanism (Scheffer CSD) is standard and cheap to compute over a log we already keep.
