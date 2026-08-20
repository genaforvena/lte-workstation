# The lead that only exists inside the window that found it

**2026-08-20 · genome · task: LEAD-LAG "wifi Keenetic-8813 predicts wifi TP-Link_97E0_5G ~10 min later"**

## Verdict

**Spurious.** The hidden process is not in the world — it is **this node's own dongle deciding how
deep to sweep**. Two threshold-censored APs climbing off one shared scan dropout, one scan apart,
is what "A predicts B by 10 minutes" is made of.

And the finding is not one bad pair: it is a **class** that mesh-leadlag was structurally unable to
reject, because every guard it had was computed inside the 48 hours that selected the winner.

## What reproduces

Independently re-derived from `~/.mesh/wifi.log` (36 days, 2876 scans), 600 s grid, 48 h window:

| | |
|---|---|
| fwd r (k=1) | **+0.735** on 19 aligned Δ-steps |
| reverse | −0.168 |
| perm p / circular-shift p | 0.035 / 0.005 |

Every gate cleared. Then:

| test | result |
|---|---|
| **hold-out: the 34 days BEFORE the window** | **r = +0.073 on n = 61** |
| pooled over the whole tape | +0.293 (n=80 — just the 19 window points dragging 80) |
| Spearman in-window | +0.421 (vs Pearson 0.735 → leverage) |
| drop the single dominant episode | 0.735 → **0.388** |
| 19 "independent" Δ-steps | are **9 contiguous episodes** |
| rolling 48 h windows stepping back | 0.735 → 0.644 → 0.199 → 0.322 → 0.249 |

It did not weaken with more data. **It was never there.**

## The mechanism, named

Both channels are **threshold-censored by the same receiver**. Keenetic-8813 appears in 97/241 bins
(median 22, near this dongle's floor); TP-Link_97E0_5G in 118/241. Both vanish when the RTL8822BU
truncates its sweep, both re-enter from below when it completes one.

The single episode carrying half the effect, raw from the tape:

```
12:16  n=5  GL=87 BRAVIA=77 GL5G=67 TPLink=67 Keenetic=0     <- TP-Link_5G ABSENT
12:26  n=5  GL=89 BRAVIA=77 GL5G=70 TPLink=62 Keenetic=9     <- TP-Link_5G ABSENT
12:36  n=7  GL=89 BRAVIA=80 GL5G=69 TPLink=44 TPLink5G=40 Keenetic=40 MTS=15   <- deep sweep, both back
12:46  n=6  GL=87 BRAVIA=74 GL5G=69 TPLink=67 TPLink5G=47 Keenetic=22
```

Keenetic re-entered one scan earlier than TP-Link_5G. On the 600 s grid that is `dA=+31` in bin *t*
and `dB=+7` in bin *t+1*. **One event, two censored channels, one bin of rounding = a 10-minute lead.**

### The tell that names the class, and it is free

Keenetic's "lead" reaches **only** the other censored channel:

| target | Δ-steps | r at k=1 |
|---|---|---|
| GL-MT3000-765 | 233 | −0.227 |
| GL-MT3000-765-5G | 233 | −0.074 |
| **TP-Link_97E0** (the *same physical router*, 2.4 GHz radio, same box) | 229 | **+0.084** |
| DIRECT-i8-BRAVIA | 183 | −0.156 |
| **TP-Link_97E0_5G** (censored) | 75 | **+0.735** |

A propagating physical process cannot select one radio of a two-radio box and skip the other.
A censoring artifact selects exactly the channels that get censored.

### Why the circular-shift null could not catch it

Its comment is correct that it preserves each channel's own sparsity. But the bias does not live in
either marginal — **it lives in the coupling between the two presence patterns**, and sliding one
series relative to the other destroys precisely that. The file already says "a surrogate that breaks
the structure a bias feeds on clears that bias every time" about the value-shuffle null it replaced;
the same sentence convicts the replacement.

## The fix (genome source: `scripts/mesh-leadlag`)

The winner is re-measured on the tape **outside** the selection window — data already parsed, that
the window filter was throwing away.

- **collapsed** (`|r_out| < 0.5·|r_in|`, or the sign flips) → **dropped**.
- **not evaluable** (fresh tape / new channel) → emitted as `holdout=na (n, UNREPLICATED)`.
  Missing evidence is not counter-evidence; a genuinely new process has no past to replicate in.
- **always published** in the line, plus each channel's **presence coverage** — the censoring tell.
- `LEADLAG_HOLDOUT=0` disables it (what `--test` uses to drive the leg red on purpose).

### Live effect, measured

With the gate off, the **top two** candidates on the real tape today:

```
#1  Keenetic-8813 -> [TV] Samsung 5 Series, ~80 min, r=0.60, n=38
    perm p=0.035  circular-shift p=0.004   coverage 39%/95%
    OUT-OF-WINDOW HOLD-OUT: r=+0.03 on 1150 steps
#2  Keenetic-8813 -> TP-Link_97E0_5G, ~10 min, r=0.73, n=19   (the reported task)
    perm p=0.035  circular-shift p=0.005   coverage 39%/48%
    OUT-OF-WINDOW HOLD-OUT: r=+0.07 on 61 steps
```

`#1` looks *stronger* than the reported finding on every in-window number, and is refuted by 1150
out-of-window steps. With the gate on the tool renders honest-empty. That is the correct output.

## Gates seen RED before being trusted

| mutation (scratch copy) | leg that went red |
|---|---|
| gate condition → `if False` | "hold-out gate passed a lead its own tape refutes" |
| gate condition → always drop | "hold-out gate suppressed a lead that replicates out of window" |
| coverage clause renamed (arg count preserved) | "emitted line omits the presence-coverage clause" |
| `na` loses its `UNREPLICATED` word | "no-past tape did not render the honest UNREPLICATED na" |

Plus the two-step red leg inside the suite itself: the un-replicated fixture must **surface** with
the gate off before its absence with the gate on counts as a drop — *nothing to drop is not a drop*.

## The rule

> **A null computed inside the window that selected the winner is not a hold-out.**
> No amount of care in the surrogate fixes it: the surrogate is calibrated on the same sample the
> selection ran on. If the tape holds more history than the window, the hold-out is free — and a
> finding that cannot be re-measured on the tape's own past should not be minted, because emitting
> it spends a mind's whole turn.

## Siblings — reported, not silently fixed

`mesh-cooscillate` and `mesh-rhythm` both truncate to a window (`WINDOW_H*3600`) and neither has a
hold-out. Same shape, not audited here.
