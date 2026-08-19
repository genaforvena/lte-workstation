# Deleuze & Guattari → RHYTHM IS NOT METER: coupling read at the critical moments, and the grid that was finer than the world

**Date:** 2026-08-19 · **Lane:** genome literature live-review (feed auto-task) · **Organ named and edited:**
`scripts/mesh-leadlag` (uncommitted in the tree) · **Organs implicated:** `scripts/mesh-rhythm`,
`scripts/mesh-rhythm-state`, `scripts/mesh-tempo-context`, `scripts/mesh-activity-tempo`,
`scripts/mesh-cooscillate`, `scripts/mesh-endogeneity`

## Where we already are in this area (checked, not assumed)

D&G is the most worked seam in `docs/reviews/` — 13 prior landings (smooth/striated, deterritorialisation
coefficient, asignifying rupture, transversality, double articulation, order-word, assemblage/relations of
exteriority, disjunctive synthesis, Buchanan's purpose-oriented discharge, machinic phylum, faciality,
rhizome-vs-arborescent, and this morning's conjugation-vs-connection). Plateau 11 is *mentioned* in six of
them. So the ground before landing, by grep over `docs/ scripts/`:

```
ritornello 11 (all prose, 6 review docs + mesh-reflex-health) · refrain 91 (mostly "refrain from")
milieu 1 · transcoding 0 · "event coincidence" 0 · "trigger rate" 0
onset: 52 in scripts/mesh-rhythm — and 0 in BOTH cross-tape instruments (mesh-leadlag, mesh-cooscillate)
```

That last line is the whole finding in one row. **The mesh has onsets. The mesh has cross-tape coupling.
They have never met.**

## The concept, and where I read it

Deleuze & Guattari, *A Thousand Plateaus*, plateau 11 "Of the Refrain", pp. 313–314:

> "rhythm is not meter or cadence, even irregular meter or cadence… Meter, whether regular or not,
> assumes a coded form whose unit of measure may vary, but in a **noncommunicating milieu**, whereas
> rhythm is the Unequal or the Incommensurable that is always undergoing **transcoding**… Rhythm is
> located **between** two milieus, or between two intermilieus… It ties together **critical moments**, or
> ties itself together in passing from one milieu to another. It does not operate in a homogeneous
> space-time, but by heterogeneous blocks. It changes direction."

Live sources read for this (not a fixed reading list — both are current, continuously published venues):

- **Felipe Kong Aránguiz, "The Triple Synthesis of Rhythm", *Deleuze and Guattari Studies* 18(1):36–59
  (2024), doi:10.3366/dlgs.2024.0541** — <https://www.euppublishing.com/doi/10.3366/dlgs.2024.0541>.
  Distributes rhythm over three levels; the *topic* level places rhythm **between chaos and measure**.
  That is the sentence that indicts us: a thing that is neither chaos nor measure cannot be reported by
  an instrument whose only two outputs are "noise" and "a number on a fixed grid".
- **Pascal Michon, "Gilles Deleuze & Félix Guattari and the *Rhuthmoi* of Territory – Part 2",
  rhuthmos.eu art. 2650** — <https://rhuthmos.eu/spip.php?article2650=> (Rhuthmos is a continuously
  published rhythm-studies archive). Michon's own critical point is that commentators routinely collapse
  rhythm into the refrain, i.e. into *periodic territorial marking* — which is exactly the collapse our
  tool names carry.

**The mechanism we did not embody** (the operational half, without which the philosophy is decoration):

- **J.F. Donges, C.-F. Schleussner, J.F. Siegmund & R.V. Donner, "Event coincidence analysis for
  quantifying statistical interrelationships between event time series", *Eur. Phys. J. Special Topics*
  225:471–487 (2016)**, doi:10.1140/epjst/e2015-50233-y, arXiv:1508.03534 —
  <https://arxiv.org/abs/1508.03534>. Directional **precursor / trigger coincidence rates** over
  *unequally spaced* event series, with null hypotheses built from point processes carrying "a prescribed
  inter-event time distribution".
- Ancestor: **R.Q. Quiroga, T. Kreuz & P. Grassberger, "Event synchronization", *Phys. Rev. E* 66, 041904
  (2002)**. Reference implementation: **J. Siegmund et al., "CoinCalc — A new R package for quantifying
  simultaneities of event series", *Computers & Geosciences* 98:64–72 (2017)**,
  doi:10.1016/j.cageo.2016.10.004.

ECA asks D&G's question in a form a shell script can compute: *given the critical moments of milieu A,
what fraction is followed within a tolerance by a critical moment of milieu B — netted against the
reverse?* No shared clock, no equal intervals, no requirement that either milieu be periodic at all.

## What we had applied too loosely

Four organs on this node carry rhythm/tempo in their names — `mesh-rhythm` (Rayleigh time-of-day
concentration of ONE device's appearances), `mesh-rhythm-state`, `mesh-tempo-context`,
`mesh-activity-tempo` (contemporaneous fusion labels). Every one measures periodic repetition **inside one
milieu**, or a label at one instant. Under D&G's own definition that is *meter*, and the name says rhythm.

The two instruments that do reach *between* tapes (`mesh-leadlag`, `mesh-cooscillate`) resample both onto
one homogeneous grid of Δ-values — and the grid deletes precisely the critical moments. `deltas()` keys
`d[b]` on `(b-1)` being present as well, so a channel's **appearance and disappearance — the transcoded
passage itself — contribute nothing at all**.

## Measured, on this node, before touching anything

48h window, live `~/.mesh/presence.log` + `~/.mesh/wifi.log`:

| fact | value |
|---|---|
| channel-bin observations (BLE tape) | 1930 |
| …with no predecessor bin, i.e. discarded by `deltas()` | **1930 (100%)** |
| producer cadence (`mesh-presence`, `mesh-wifiscan`) | median **600 s** (581–618) |
| `LEADLAG_BIN_S` default | **300 s** |
| last 200 cron runs logging "no fresh finding" | **191** |

Two adjacent 5-minute bins cannot both hold a 10-minute scan. **The lead-lag lane was structurally
empty — not thresholded-out, arithmetically impossible — and had been for as long as the cadence held.**
Its `--test` was green throughout, because every fixture plants a sample exactly every 300 s: a grid the
live producers have never once provided. (Fixture-cadence-is-not-producer-cadence; sibling of *a lease
must exceed its producer's cadence*.)

The sibling is not broken the same way, which is the tell: `mesh-cooscillate` pairs two common bins up to
`MAX_GAP_BINS=3` apart for one Δ-step, so it still gets Δ-steps out of a 600 s producer. `mesh-leadlag`
demanded strict adjacency and had no tolerance. (Cooscillate's tolerance has its own cost — Δ-steps of
unequal duration compared as if equal, the same meter/rhythm confusion in another key — untouched here.)

## What was built — `scripts/mesh-leadlag` (uncommitted)

**1. The grid is derived from the tape, not assumed.** `BIN_S` is now the median inter-scan interval of
the *source tapes* (median over tapes; env `LEADLAG_BIN_S` still pins it). Two wrong ways were measured
and rejected on the way: the **union** of two 600 s tapes interleaved ~300 s apart gives 336 s — a cadence
neither tape has; **per channel** gives 2100 s on a device seen every 7th scan, destroying lag resolution
for everyone. What sets the floor is the observer: how often each *tape* produced a line. Every emitted
finding discloses the raise (`grid auto-raised 300s->600s`). On the live tape the delta lane went from **0
adjacent-bin pairs to 2896**, and `--dry` produced a candidate where 191 of the last 200 cron runs had
produced none: `wifi TP-Link_97E0_5G movement PREDICTS wifi Keenetic-8813 ~10 min later (r=0.64, net
0.25, perm p=0.010)` — a candidate for the queue, not yet a fact about the household.

**2. The event lane (ECA).** A *critical moment* is an ONSET: a channel absent for `EV_GAP` consecutive
scans **of its own tape** and present now. Coupling is the trigger coincidence rate of A's onsets followed
by B's within ±`EV_TOL` bins at lag k, netted against the reverse. Guards, each earned:

- **Absence is per tape.** Bins come from three interleaved producers; a wifi AP is not "absent" in a bin
  where only the BLE scanner ran. Read against the union pool, a rock-stable router showed **59 phantom
  onsets** (measured, before the fix).
- **Blackout has two shapes and only one is a hole in the pool.** (a) the scanner stops → a gap;
  (b) *this node's actual failure* — the rtw_8822bu radio wedges, scans keep running **empty**, the tape
  stays perfectly cadenced while every channel reads absent, then all "return" together. Shape (b) leaves
  the pool continuous and the gap rule blind. Census-collapse bins are therefore **removed from the pool**,
  which converts (b) into (a) so one rule covers both; the recovery *window* (not just the first bin) is
  dropped, because an onset claims `EV_GAP` scans of observed absence and after a blackout that evidence
  does not exist.
- **End-censoring.** An A-onset whose whole window lies past the last scan cannot coincide; it leaves the
  denominator instead of deflating the rate.
- **Observer cadence + burstiness in the null.** Surrogates relay each channel's *own* inter-event
  intervals, shuffled, from a random start on its own tape's scan-bin axis. A coincidence that merely
  rides the scan schedule survives into the null and is not reported.
- **Only the corrected maximum is emitted.** The surrogate null corrects one statistic — the global max
  over pairs×lags. Emitting the rest would ship the winner's curse the null exists to remove: on the
  planted fixture the uncorrected list contained *"independent flapper leads Phone at 0.75"*.
- **Resolution is published, not implied.** With a ±1-bin tolerance, k−1, k, k+1 all see a true lag of k,
  so the delay is the **centre of the max-rate plateau** and the finding states its own ±`EV_TOL·BIN_S`
  resolution. (Read as the net-argmax it reported 15 min for a planted 10; as the earliest peak, 5.)

**On the live tape the event lane is honest-empty**: global max net 0.966 (`DIRECT-i8-BRAVIA` →
`TP-Link_97E0_5G`, 4 eligible onsets) at surrogate **p = 0.104** → rejected. An unguarded version would
have posted a 4-event artifact as a household rhythm.

## Gates, and which were seen red

New `--test` legs: planted Door→Phone onset coupling with **unequally spaced** onsets (recovered at
10 min); the same fixture asserted to be **mute in the delta lane**, so the event lane can never be
dismissed as a re-description; an independent flapper and an independent-onset log both rejected; the
wedge trap asserted **both ways** (with `EV_BLACKOUT=0` the false `Fast→Slow` rhythm *is* emitted at
p=0.005 — the fixture needed eleven wedges before the trap could even clear the null, since both channels
inherit the same intervals from the same wedges); and the 600 s tape asserted **dead at a pinned 300 s
grid** and alive at the derived one.

Seen red before being trusted: `LEADLAG_BIN_S=300` → the three grid assertions fail;
`LEADLAG_EV_TOL=3` → the planted-delay assertion fails; `LEADLAG_ALPHA=1` → the independent-onset leg
emits and fails; `EV_BLACKOUT=0` is asserted red-then-green inside the test itself.

**One guard has no red-seen test and the source says so:** `EV_ASYM`, the floor on the net rate. With only
the corrected global max emitted, a fixture isolating that floor cannot be built — a perfectly mutual pair
scores ~0 and dies on the null first, whichever way the floor is set. Direction here is carried by the
*statistic* (a net), not by that floor.

## What this does not claim

n=1 node, one 48 h window. The revived numeric finding (`TP-Link → Keenetic`, p=0.010) is a candidate for
the ideas-queue, not a fact about the household. The event lane has produced **no** live finding yet; its
value today is that a whole class of coupling is now *expressible*, and that the lane says nothing rather
than saying something cheap. `mesh-rhythm` still measures meter and still calls it rhythm — renaming it,
or giving it the between-milieu lane, is the obvious next strand and is **not** done here.
