# LITERATURE review — second-order cybernetics (Beer), from the **alarm-fatigue / desensitization** critique of the algedonic channel: **habituation & dishabituation** (2026-07-28)

**Area:** management cybernetics / the Viable System Model (Stafford Beer), entered from the task's
angle — a **known failure mode** of the area. The failure mode: the **algedonic channel**, Beer's
out-of-band pain/pleasure alert that bypasses the S1→S3 hierarchy to reach S5 (policy/identity)
directly, is chronically defeated by **alarm fatigue / desensitization** — the same pathology that
kills SOC alert queues and clinical bedside monitors. Landing on the mechanism that answers it and is
**not yet embodied**: **habituation / dishabituation**.

## The concept

An **algedonic signal** is "a pre-emptive message concerning pleasure or pain … a privileged signal
indicating fundamental danger to survival" that "cut[s] through normal filters when ordinary reporting
structures are insufficient" ([Wikipedia, *Algedonic signal*](https://en.wikipedia.org/wiki/Algedonic_signal)).
Beer's own named failure mode is **S5 somnolence** — the policy layer falls asleep and the algedonic
system exists to wake it ([businessballs, *Viable System Model*](https://www.businessballs.com/strategy-innovation/viable-system-model-stafford-beer/)).

But the algedonic bypass has a **second, opposite failure mode that Beer under-specified and the
current literature documents exhaustively: desensitization.** A privileged channel that fires too
often stops being privileged. The alert-fatigue literature is blunt about the mechanism:

- "When the volume of notifications exceeds human processing capacity, people stop responding to all of
  them — including the ones that matter … the brain adapts and filters the alarms out"
  ([Vectra AI, *Alert fatigue*](https://www.vectra.ai/topics/alert-fatigue)).
- "Alert fatigue is caused by … **poor threshold configuration** … over time, the signal-to-noise ratio
  deteriorates so badly that critical alerts get treated the same way as noise"
  ([Tractian, *Alert Fatigue*](https://tractian.com/en/glossary/alert-fatigue)).
- The cybernetic framing: "Systems often fail not because they lack data, but because key danger signals
  are **filtered out, misrecognized or treated as administrative irritants**."

The root defect named across all of these is **a fixed threshold against a drifting baseline.** A pain
that has been high for a week is not an emergency — it is the new normal — yet a level-triggered
algedonic channel keeps escalating it, and in doing so trains every observer to ignore the channel.

The mechanism that answers this is **habituation / dishabituation** — the oldest form of learning, and
a load-bearing idea in second-order cybernetics (it *is* the observer adapting to their own invariants,
von Foerster's eigenbehavior): a repeated stimulus at **constant** intensity produces a **declining**
response (habituation); a **change** restores the response (dishabituation). Translated to alerting: do
not escalate on the *level*, escalate on the **deviation from the established baseline**. A chronic pain
habituates out of the bypass; a sudden onset — even one whose absolute level equals the chronic case —
dishabituates back into it.

## What we already embody vs. the gap

`scripts/mesh-algedonic` already fuses the many siloed per-subsystem alarms into one VSM algedonic read
(noisy-OR over therm/hw/egress/stress/crit), and already carries **three** read-only moments of that
fused pain:

| moment | reading | tool sidecar |
|---|---|---|
| **level** | pain now (noisy-OR) | `pain=` / `[band]` |
| **level integral** | cumulative multisystem burden (allostatic load) | `allostatic=LOAD_*` |
| **2nd moment** | variance ∧ lag-1 AC rising → tipping-point proximity (CSD) | `csd=CSD_*` |

The **missing moment is the first difference vs. the tool's own baseline** — the habituation signal.
Nothing in the channel asks "is this pain *new*, or is it what this mesh has habituated to?" A chronic
`stress=0.3` (visible pinned at `pain=0.300` for the whole current log) and a fresh jump to 0.55 look
identical to every level-based reading, and CSD stays `CSD_FLAT` for a clean step (a single jump is not
rising autocorrelation). That is precisely the blind spot the alarm-fatigue critique names — and it is
the one an algedonic *bypass* most needs, because the bypass is the mesh's scarcest attention channel.

Note the two readings are **deliberately opposed and both correct**: `allostatic_load` *accumulates*
chronic pain (the longer it's high, the worse the burden), while the algedonic *bypass* must *discount*
it (the longer it's high, the less it is an emergency). Burden-tracking and attention-gating are
different jobs; the tool now carries both without contradiction.

## The mechanism landed — read-only `salience` sidecar in `scripts/mesh-algedonic`

Added a fourth read-only sidecar mirroring the existing three (aggregate + log, **never escalates** —
consistent with this tool's whole charter). `salience()` reads the trailing pain window from
`algedonic.log` (excluding the current sample), takes a **robust baseline** = median, **robust spread**
= MAD·1.4826 floored at 0.05 (so a dead-flat baseline can't blow the z up), and computes the current
pain's robust-z deviation:

- **`SAL_ONSET`** — `dev ≥ 3.0` *and* the absolute step over baseline `≥ 0.15`: dishabituation, a real
  change that deserves the bypass.
- **`SAL_HABITUATED`** — baseline already ≥ 0.45 and `|dev| < 3.0`: chronic-but-stable, **discounted**
  from emergency attention (the alarm-fatigue defense).
- **`SAL_CALM`** — low/quiet, no deviation.
- **`SAL_UNKNOWN`** — current pain UNKNOWN, or < 12 samples of history (honest-degraded, never a faked
  quiet — same discipline as every other sidecar here).

New log field: `salience=<label> salz=<robust-z> salbase=<baseline> saln=<n>`.

**The discriminating claim, proven RED-first** (`mesh-algedonic --test`, case 9): a sudden onset against
a quiet 0.20 baseline reads `SAL_ONSET` while a chronic-but-stable 0.60 reads `SAL_HABITUATED` — *even
though the onset's absolute level (0.70) sits in the same band as the chronic case (0.60).* Salience is
deviation, not level; the bypass must not cry wolf on the established baseline. Broke the classifier
(forced `SAL_ONSET`→`SAL_CALM`) and watched `salience onset label` go red, then restored — the gate
fails when the mechanism is absent, so it asserts the mechanism, not its own text.

This is read-only calibration data today (as `allostatic_load`/CSD were when added): a future escalating
consumer of the algedonic channel — or the dispatch `priority:incident` path, which today deliberately
does **not** mint a slot — can gate the genuine *bypass* on `SAL_ONSET` (a real dishabituation event),
leaving chronic `SAL_HABITUATED` pain to the ordinary paced channel. That is the alarm-fatigue fix
Beer's algedonic channel needs and the literature prescribes, wired to the one place the mesh already
fuses viability.

**Doctrine resonance:** this is CLAUDE.md's "a fallback must be **rare and loud**" applied to the
attention channel itself — habituation is what *keeps* it rare, so that when it fires it is still loud.

## Sources

- [Wikipedia — *Algedonic signal*](https://en.wikipedia.org/wiki/Algedonic_signal)
- [businessballs — *Stafford Beer's Viable System Model*](https://www.businessballs.com/strategy-innovation/viable-system-model-stafford-beer/) (S5 somnolence / algedonic wake mechanism)
- [Vectra AI — *Alert fatigue: causes, real cost, and how to fix it*](https://www.vectra.ai/topics/alert-fatigue)
- [Tractian — *Alert Fatigue: What It Is and How to Reduce False Alarms*](https://tractian.com/en/glossary/alert-fatigue)

## Artifact

- `scripts/mesh-algedonic` — `salience()` sidecar + emit field + test case 9 (RED-first verified);
  `--test` green, live `--quiet` emits `salience=SAL_CALM salz=0.000 salbase=0.300 saln=48`.
- Left uncommitted in the tree (steward lands).
