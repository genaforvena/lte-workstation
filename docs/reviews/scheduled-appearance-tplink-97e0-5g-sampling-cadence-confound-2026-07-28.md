# Scheduled appearance: TP-Link_97E0_5G — SPURIOUS (sampling-cadence confound)

**Date:** 2026-07-28 · **Mind:** genome@mesh-home (loop-baton) · **Source:** mesh-rhythm idea-queue finding
("wifi TP-Link_97E0_5G appears ~17:24 UTC ±3.9h, 12 appearances/72h, Rayleigh p=0.0289 Bonferroni over 2").

## Verdict: SPURIOUS — an always-present neighbour AP, not a schedule

What recurs is **one dual-band neighbour router** — BSSID `b0:a7:b9:d8:97:e0` (`TP-Link_97E0`, 2.4GHz/2462)
and `…:97:e2` (`TP-Link_97E0_5G`, 5GHz/5200). Measured over the full 12.9-day wifiscan log (1405 scans):

- 2.4G band present in **41.6%** of scans (a near-fixture); 5G band in only **8.7%**, and **86.9% of the
  5G sightings also show the 2.4G partner** → same physical device, weak second band.
- 5G RSSI 37-42 vs the 2.4G partner's 39-82 — the 5GHz sits **near the scan detection floor**, so it
  drops in and out on RF/propagation noise, not on the device arriving or leaving.
- Over the full log the 5G appearances span the **whole 24h** (circular mean ~13:00, R=0.32). The
  "17:24 ±3.9h" is a 72h small-sample artifact; ±3.9h circular spread is nearly uniform.
- **Per-hour detection RATE is flat** (χ²=33.3, df=23, p≈0.077) and is **0.051 at the claimed 17:00 —
  below the 0.087 baseline.** The raw-count clustering is inherited from the scan cadence itself (55% of
  scans fall 06-18h; appearances 67% daytime).

So: a weak, always-present 5GHz band flickering across the scan floor, whose apparent "17:24 rhythm" is
the observer's own daytime-heavy sampling. Not a routine, commute, or beacon.

## The real gap this exposed → fixed in `scripts/mesh-rhythm` (uncommitted, steward lands)

mesh-rhythm's Rayleigh test assumed appearances are drawn from a **uniform clock** (`p=exp(-n·R²)`). But a
device is only sightable when a **scan runs**, and the scan cadence is itself non-uniform over time-of-day
— so **every** device's onsets inherit the daytime lean and the uniform null flags a "schedule" with zero
intrinsic rhythm. The winner's-curse Bonferroni guard corrects for *multiple devices* but not for the
*non-uniform sampling baseline*. Sibling of mesh-correlate's clock-gate confound.

**Fix (SAMPLING-CADENCE GUARD):** the null is now the **observation-time distribution itself** — a
deterministic (fixed-seed) Monte-Carlo test asking *"are these onsets clustered BEYOND the scan cadence?"*
(draw n angles from the actual per-tape scan pool, p = P(R_null ≥ R_obs)). A device that merely rides the
cadence gets p≈0.5 and is rejected; only clustering tighter than the sampling survives. Falls back to the
uniform p (never faked) when scans are too few (<30) to build a null.

**Verified:**
- RED-first `--test`: a synthetic with scans confined to 10-16h and a device at spread daytime hours
  (no intrinsic rhythm) **surfaces under the uniform null** (RED — proves the confound is real) and is
  **rejected by the sampling-corrected null** (GREEN). Toggled via `RHYTHM_MC_MIN_POOL`, deterministic.
- Live data: the corrected tool returns **honest-empty** on the real logs; forcing the uniform path
  (`RHYTHM_MC_MIN_POOL=999999`) reproduces the **exact** task finding (17:24, ±3.9h, 12/72h, p=0.0289) —
  so the correction, not a data change, is what rejects it.

## Cite

- Live wifiscan data: `~/.mesh/wifiscan.log` (2026-07-15..28), `~/.mesh/wifi.log` (mesh-rhythm's tape).
- Confound class: observer/sampling non-uniformity vs a uniform-circle Rayleigh null; cf.
  `docs/reviews/…` clock-gate control in mesh-correlate.
