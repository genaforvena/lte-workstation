# Correlation investigation: `light=MODERATE` → `psi=BUSY`

**Disposition:** spurious; discard. No fused sense or reflex.

The queued finding (the 2026-08-25 real-tape window) reported hour-stratified
lift `2.80` over `11` episodes / `8` occasions, after a light-hour shadow that
scored `0.82`; the full-window lift `2.0` was explicitly the confounded number.
The independent environment check was negative in all three qualifying
environments: `env17=0.64`, `env20=1.25`, `env21=1.20`, all below the `1.8`
floor. It is therefore an unstable Markov-blanket hypothesis, not a relation
that can be generalized.

## Reality check

The pair is a window-regime artifact. `psi=BUSY` had only 11 of 234 readings
before the 2026-08-15 regime boundary, while 97.4% of BUSY readings and all 22
light/BUSY co-occurrences were in the recent tail. The earlier regime occupied
2,418 rows (69% of the window), included 50 `light=MODERATE` rows, and had zero
co-occurrences. Restricting the calculation to the regime in which BUSY was
actually present gives lift `1.29`, below the floor. The environment-specific
values above bracket that same result.

This is not rescued by the hourly control: hour matching corrects position
within a day, while the confound is a rate change across the observation
window. Nor is it evidence of a physical light/load mechanism. `psi` is a
kernel pressure classification (BUSY at CPU/IO/memory pressure thresholds),
whereas the candidate's support is concentrated in the period when the node's
BUSY state became common.

There is a separate measurement defect worth preserving, but it is not evidence
for this correlation: before the light vocabulary repair, `MODERATE` also
encoded which light organ answered (phone/beacon versus webcam). That can create
availability confounding, but the regime-shift falsifier alone is sufficient to
discard this pair.

## Action

Do not create a light/PSI fusion or reflex. Keep the regime-onset correction in
`scripts/mesh-correlate`; it is the appropriate general defense for this class
of false finding. The correlation seed remains withheld.

## Verification evidence

- Historical board record: `~/.mesh/board-weekly/board-week-2026-08-31.txt`,
  entry 639, records the raw-tape recomputation, the regime-restricted `1.29`,
  the three failed environment lifts, and the mass-quantile regime-gate fix.
- Current raw tape spot-check (`~/.mesh/sensor-tape.tsv`, 2026-09-06) still
  shows the same shape: the joint rows occur in bursty recent runs rather than
  a stable cross-environment relation. The live tape is now longer, so its
  totals are not substituted for the queued window's figures.
- `scripts/mesh-correlate --dry` currently exits through an existing live-tape
  `IndexError` in its analyzer after printing other gate diagnostics; this is
  recorded as an unresolved regression, not called a passing verification.

