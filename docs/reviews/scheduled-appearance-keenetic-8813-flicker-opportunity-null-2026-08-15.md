# Scheduled appearance "wifi Keenetic-8813 @ 14:46 UTC" — DISCARDED, and the two guards it exposed

**Date:** 2026-08-15 · **Window:** genome · **Tool:** `scripts/mesh-rhythm` · **Tape:** `~/.mesh/wifi.log`

## The claim

> SCHEDULED APPEARANCE (auto, real data): wifi Keenetic-8813 tends to appear around 14:46 UTC
> (±1.8h, 5 appearances over 72h, clustered beyond scan cadence, sampling-corrected Rayleigh
> p=0.032 Bonferroni-corrected over 2 devices)

Live and reproducible at review time (`mesh-rhythm --dry` → same finding, p=0.036).

## Verdict: spurious

Nothing recurs at 14:46. Keenetic-8813 is a neighbour AP that is **in range 80% of all scans** (1828 of
2296 over 31 days). It does not arrive and it does not leave — it **crosses the scan detection floor**
when its signal is weak, and each crossing back is counted as an "appearance".

### The mechanism, measured

`P(device absent at the next scan | its signal quality now)`, adjacent scans only (no blind gap),
full 31-day tape:

| quality | n | dropouts | P(drop) |
|---|---|---|---|
| 0–9 | 3 | 1 | 0.333 |
| 10–19 | 24 | 10 | 0.417 |
| 20–29 | 418 | 108 | 0.258 |
| 30–39 | 332 | 34 | 0.102 |
| 40–49 | 126 | 20 | 0.159 |
| 50–59 | 229 | 7 | 0.031 |
| 60–69 | 345 | 2 | **0.006** |
| 70–79 | 323 | 1 | **0.003** |

A 140× swing driven by signal strength. Confirming it from the other side: **onsets happen at median
quality 27, steady presence sits at median 50** — an "appearance" is by construction a weak-signal event.

The 72h window that produced the finding contained exactly one weak spell (08-12 afternoon, q 9–27,
three onsets) and one recovery (08-14 13:46 → 15:16, two onsets), after which the AP sat **continuously
present for 19 hours** at q 42–77 and produced no onsets at all. Five "appearances" = two physical
episodes of RF marginality, both in the afternoon by coincidence.

### The full tape says the same

| | onsets | mean | R | sampling-corrected p |
|---|---|---|---|---|
| 72h window (the finding) | 5 | 14:46 | — | 0.036 → **surfaced** |
| full 31d tape | 67 | 13:59 | 0.232 | **0.465** |
| full tape, resume-onsets dropped | 51 | 14:44 | 0.196 | **0.646** |

13× more data and the effect evaporates. The mean hour stays ~14:00 not because anything recurs but
because that is the middle of the observation distribution.

## Two guards the detector was missing

The 2026-07-28 TP-Link_97E0_5G review diagnosed the same failure in two halves — "an always-present
neighbour AP whose weak band **flickers near the scan floor**" *and* the daytime-heavy scan cadence.
Only the cadence half got a guard. This is the flicker half arriving thirteen days later under a
different SSID.

### 1. Opportunity-set null (the flicker guard)

The cadence null asks *"when could a **scan** have happened?"*. But an onset can only occur at a scan
where the device was **absent at the previous scan** — while it sits continuously present, an onset is
structurally impossible there. On this node ~2/3 of the window's scans were "already present" and thus
onset-impossible, yet the null drew from all of them. That understates how clustered chance alone is.

Fix: the per-device null pool is now the scans at which an onset was **possible**. Same principle as the
cadence guard, one level deeper — condition on when the *event* could occur, not merely on when
*observation* could. A device that is genuinely away most of the day (a commuter phone) has an
opportunity pool spread across the clock and is unaffected; a floor-flicker AP has one confined to its
weak spells and dies.

Ladder, each labelled in the emitted finding so it names the null it actually survived:
opportunity-set → scan-cadence (thin pool) → uniform clock (too few scans).

### 2. Blind-gap guard (the scanner-resume artifact)

When the vantage goes down and comes back, **every device still in range registers a fresh onset at the
resume time**. This is systematic, not random: it lands at whatever hour the node tends to wake. The
tape has **22 outages >30 min in 31 days** (including 61.2h, 66.3h and 42.7h gaps), resuming
overwhelmingly late-morning to early-afternoon — manufacturing exactly the cluster the Rayleigh test
hunts for. 16 of the 67 full-tape onsets are resumes.

No null over scan *times* can reject this, because the resumes really are that clustered. The onsets
themselves must be dropped. Sibling of `reflex-stale-can-be-honest-blindness`: a missing sighting across
an outage is blindness — and so is the sighting that ends it.

## Changes (`scripts/mesh-rhythm`, uncommitted)

- `opp_pool()` — per-device onset-opportunity pool; correction ladder with `null_name` threaded through
  to both consumers (findings lane + absence lane), so neither reports in the other's words.
- `onsets()` now takes the tape's observation times and drops any onset whose immediately preceding
  observation is >`GAP_S` away, or which has no prior observation (arrival undatable).
- Emitted text: "5 **appearances** … clustered beyond **scan cadence**" → "5 **arrivals** … clustered
  beyond **<the null actually used>**".
- Two RED-first `--test` fixtures, each seen failing before passing:
  - `Flicker` — present every scan except 45-min dropouts inside a 13:00–17:00 weak spell. Surfaces
    under `RHYTHM_SKIP_OPP_NULL=1`, rejected by default.
  - `NeverLeaves` — never absent, vantage awake only 14:00–20:00. Surfaces under
    `RHYTHM_SKIP_BLINDGAP_GUARD=1` as a perfect R=1 "14:00 schedule", rejected by default.

## Artifact

`mesh-rhythm --test` green with both new gates; on live data the deployed copy still emits the Keenetic
finding while the genome copy returns honest-empty:

```
=== DEPLOYED (old) ===
2.1735  RHYTHM  rhythm:wifi Keenetic-8813  SCHEDULED APPEARANCE ... around 14:47 UTC (±1.7h, 5 appearances ...)
=== GENOME (fixed) ===
mesh-rhythm: no device appears on a clear schedule above the corrected significance floor (honest empty)
```

## Side note (latent, not live)

`~/.mesh/wifiscan.log` is missing the newline before each scan header: 2401 `=== mesh-wifiscan` headers
exist but only 109 start a line. Nothing reads that file but its writer, so no live consumer is wrong
today — but any future reader anchoring on `^===` would silently see 4.5% of the tape. Not fixed here.
