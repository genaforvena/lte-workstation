# wifi TP-Link_97E0_5G → Keenetic-8813 onset coincidence — SPURIOUS (partial common mode)

**Date:** 2026-08-21 · **Mind:** genome@mesh-home · **Source:** mesh-leadlag event lane
(`2026-08-21T17:17:22Z … coincide:wifi TP-Link_97E0_5G:wifi Keenetic-8813`)

> "when wifi TP-Link_97E0_5G APPEARS, wifi Keenetic-8813 appears ~10 min later … trigger rate 0.80
> of 5 eligible onsets, reverse only 0.06, net 0.74; surrogate p=0.015 … What passes between the two
> at that moment — one person carrying both, a door, a schedule?"

## Verdict: SPURIOUS — nothing passes between them. One receiver reaching further.

Nothing physical connects these two. They are two *different neighbours' routers*, and what varies
is not them but **how far our own receiver hears** on a given scan. Reproduced the detector's exact
numbers first (0.80 of 5, reverse 0.0625, lag 1 bin) so every test below runs on the same onsets.

### 1. Three unrelated households' routers onset in the *same bin*

| bin (UTC) | Keenetic-8813 | MTSRouter_904F | TP-Link_97E0_5G | DOMRU_834C |
|---|---|---|---|---|
| 08-19 18:30 | | | **ONSET** | |
| 08-19 18:50 | **ONSET** | **ONSET** | | |
| 08-19 20:10 | **ONSET** | **ONSET** | | |
| 08-19 23:20 | **ONSET** | **ONSET** | | **ONSET** |
| 08-20 01:10 | | | **ONSET** | |
| 08-20 01:30 | **ONSET** | | | |

Three households do not switch their routers on together because someone walked past our door.

### 2. The lead is not specific to the target

Each forward trigger rate divided by the rate expected if that target's onsets were placed uniformly
at random on the same pool under the same ±1-bin window:

| lead | target | n | fwd | chance | enrichment |
|---|---|---|---|---|---|
| TP-Link_97E0_5G | **Keenetic-8813** | 5 | 0.80 | 0.19 | **4.2×** |
| TP-Link_97E0_5G | MTSRouter_904F | 5 | 0.40 | 0.10 | 4.1× |
| TP-Link_97E0_5G | MTSRouter_DAC1 | 5 | 0.20 | 0.03 | 8.0× |
| TP-Link_97E0_5G | *pooled: every neighbour that is NOT Keenetic* | 5 | 0.60 | 0.14 | **4.2×** |
| MTSRouter_904F | Keenetic-8813 | 8 | 0.62 | 0.19 | 3.3× |
| MTSRouter_904F | DOMRU_834C | 8 | 0.25 | 0.04 | 6.7× |

It does not predict that AP. It predicts *the receiver reaching*, at the same enrichment whether
Keenetic is in the target set or excluded from it. Keenetic wins the raw-rate argmax only because it
has the highest onset base rate, and the detector reports only the global max.

### 3. The mechanism is visible without either channel

Counting only third-party APs — neither the lead nor the target:

| bins | third-party reach / bin |
|---|---|
| all 237 | 0.08 |
| lead PRESENT | **0.39** |
| target ABSENT | 0.04 |
| target PRESENT | **0.18** |

### 4. The *direction* is a base-rate artifact

5 onsets against 16. Under strict independence the expected forward rate is 0.19 and the expected
reverse 0.06 — **net +0.13 with zero coupling**. The rare channel always looks like the leader.
(Sibling of `an-empty-unit-scores-maximum-under-per-unit-normalisation`.)

### 5. The queue already refutes it, twice over

- **2026-07-28**, this same AP: `scheduled-appearance-tplink-97e0-5g-sampling-cadence-confound-2026-07-28.md`
  measured `TP-Link_97E0_5G` at **RSSI 37-42, near the scan detection floor**, "drops in and out on
  RF/propagation noise, **not on the device arriving or leaving**". The physical fact was already
  established. Its fix was landed in **mesh-rhythm** — the tool that found it — so mesh-leadlag never
  got the lesson and re-discovered the same AP as a novel arrival coupling 24 days later.
- **The same pair has been emitted three times in three days, in contradictory directions**:
  `08-19T19:17Z` TP-Link→Keenetic (numeric lane), `08-20T10:17Z` **Keenetic→TP-Link** (numeric lane,
  opposite, 15h later), `08-21T17:17Z` TP-Link→Keenetic (event lane). A directed coupling cannot run
  both ways at the same 10-minute lag. Both numeric findings are still open (`[~]`, queue 1366/1388)
  and each cleared the net-asymmetry guard, the permutation test **and** the hold-out gate.

### 6. Why every existing guard passed it

- **Blackout guard** removed 6 bins of 237 — it covers the scanner *stopping* (census collapse). Here
  the census never collapses: the scan returns its 3-4 strong APs every single time, perfectly cadenced.
- **Surrogate null** relays each channel's intervals from an *independent random start*, preserving
  each channel's own cadence and burstiness. That is exactly its blind spot: the reach **episodes the
  two channels share** are destroyed in every surrogate and can never appear in the null. A null built
  from two independent marginals prices *selection*, not *confounding*.
- **Hold-out** is wired to the numeric lane only; the event lane has none.

Secondary, non-load-bearing note: both channels are strongly non-stationary across the window —
Keenetic-8813 ran 100% of scans on 08-05/06 and 34-35% by 08-20/21, and was last seen at all on
08-21T13:06Z. The 48h surrogate assumes stationarity inside its own window.

## The gap this exposes → fixed in `scripts/mesh-leadlag` (uncommitted, steward lands)

**PARTIAL COMMON MODE — the reach control**, sibling of the blackout guard. Blackout covers the
scanner *stopping*; this covers the scanner *reaching less far*. Before a pair is emitted, its
enrichment over chance is compared against **the same lead's enrichment against every other channel
on its own tape**. A ratio below `EV_REACH` is a tape-wide reach episode, not a pair, and is refused
**out loud** — a `REACHDROP` note on the log line, because a silent drop reads identical to a quiet
tape. An unevaluable control (no third onsetting channel) renders a loud `reach-control=na` and the
finding is still emitted: missing evidence is not counter-evidence, the same edge the hold-out gate
draws. The statistic is an enrichment *ratio*, never a raw rate — a raw rate is mostly the target's
base rate, which is the trap itself.

**The floor (1.5) is placed between measured points, not picked:** the live finding scores **1.18**,
the partial-reach fixture **0.74**, and the planted genuine coupling (Door→Phone, independent flapper
on the tape) **4.00** — its control enrichment sitting at 0.7×, because a real pair leaves the
neighbours alone. Three tapes are not a distribution; `--test` re-measures two of them every run.

**Verified, all four legs watched RED first:**
- A new `--test` fixture plants a partial common mode: an Anchor in **every** bin (census never
  collapses), rare irregular reach episodes, four marginal channels appearing *independently* inside
  them with deliberately unequal marginals, and **no pair coupling anywhere**. It is a real trap: it
  clears the blackout rule, clears `EV_ASYM` on base rates alone, and **clears the surrogate null at
  p=0.030**. Gate off → emitted as `when Far4 APPEARS, Far2 appears ~5 min later` (net 0.78, rate
  1.00 of 5). Gate on → refused, with the note.
- `LEADLAG_EV_REACH=0` → the "did not bite" and "dropped silently" legs go red.
- A mutant forcing the control to render `na` → the genuine Door→Phone pair passes with a **vacuous**
  guard; two legs go red (this is the guard-that-is-always-n/a failure).
- A mutant blanking the `na` text → the unevaluable edge passes silently; that leg goes red.
- Live: `mesh-leadlag --dry` now prints
  `REACHDROP … pair enrichment 4.2x vs 3.6x … (ratio 1.18 < EV_REACH 1.50) — the lead predicts the
  tape's marginal channels in general, not this target`, and emits no finding.

## Still open — NOT fixed here

**A pair emitted in one direction should refuse the opposite direction later.** The queue holds
`TP-Link→Keenetic` and `Keenetic→TP-Link` as two live, independent findings 15h apart, each having
passed the net-asymmetry guard. That guard is computed *within a run*; nothing consults what the
previous run already claimed about the same pair. A self-contradicting pair is a common-cause
signature the tool currently reports twice as two discoveries. This needs cross-run state
(`recent_has`-style) and is a separate change from the reach control.

## Cite

- Tape: `~/.mesh/wifi.log` (3053 scans, 2026-07-15..08-21; 237 bins in the 48h window).
- Emission: `~/.mesh/leadlag.log:512,519,550`; queue `~/.mesh/ideas-queue:1366,1388,1507`.
- Prior art: `docs/reviews/scheduled-appearance-tplink-97e0-5g-sampling-cadence-confound-2026-07-28.md`.
- ECA method + its null: Donges, Schleussner, Siegmund & Donner, *Eur. Phys. J. ST* 225:471-487 (2016).
