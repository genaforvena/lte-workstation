# Measurement–Control Complementarity (the epistemic cut), applied to `mesh-link-heal`

**Area:** autopoiesis & the biology of cognition (Maturana/Varela lineage → Pattee → relational biology)
**Date:** 2026-08-18 · **Window:** genome · **Status:** implemented, uncommitted in tree

---

## 1. Where the literature actually is right now

The live front of this area is not Maturana and Varela's 1972/1980 texts — it is the attempt to turn
their organizational claims into *measurable signatures*. Two current sources, both checked this
session:

- **ALIFE 2026 tutorial, "Autopoiesis & Structural Coupling"** (Waterloo, August 2026) —
  <https://autopoiesistutorial.netlify.app/>. Read in full. Its thesis is that **structural coupling**,
  not autopoiesis, is the fundamental phenomenon; it surveys (M,R) systems, Chemoton, RAF sets, COT,
  and the ouroboros `f(f) = f`. **It proposes no quantitative measure at all** — it is conceptual and
  historical. Recording that here so the next review does not re-fetch it hoping for one. (Its RAF leg
  we already landed: `alife-raf-catalytic-closure-food-set-vitality-2026-08-18.md`.)

- **López-Díaz, A. J. & Gershenson, C., "A Matter of Time: Towards a General Theory of Agency"**,
  arXiv:2606.23122, submitted 22 June 2026, revised 30 July 2026 (cs.AI, q-bio.OT).
  <https://arxiv.org/abs/2606.23122> · full text read at
  <https://arxiv.org/html/2606.23122v2>. This one *does* propose operational signatures — six of them:
  semantic closure index, **measurement–control complementarity (MCC)**, anticipatory modulation index,
  affordance reconstruction rate, syntactic open-endedness, and viability-corrected skill acquisition.

Of the six, we have already landed **semantic closure**
(`autopoiesis-semantic-closure-interpreter-provenance-closure-semantic-2026-08-16.md`). **MCC we have
never touched.**

## 2. The mechanism: measurement–control complementarity

The paper's definition, verbatim in its key clause: the *epistemic cut* is the "necessary descriptive
distinction between relatively **rate-independent symbolic structures** and **rate-dependent physical
dynamics**." MCC is the operational signature of that cut inside one closed organization. Its
measurement procedure: *"Identify distinct timescales: one for signal detection/interpretation and
another for response/constraint maintenance."* Its falsifiable prediction: *"Disrupting the slower
(maintenance) timescale should preserve measurement capacity initially but degrade control fidelity;
disrupting faster (sensing) timescale should immediately reduce adaptive response."*

The operational content, stripped of biology: **a symbol does not carry a rate.** A counter is
rate-independent — it says "3", not "3 minutes". Physical dynamics are rate-dependent — a wedged radio
is dark for seconds whether or not anyone counted. A system that crosses the cut **without an explicit
converter** silently asserts that its symbol *is* the duration. It is right only while every scheduled
observation lands.

This is genuinely new ground for us. Our closest doctrine — *"a sense's coverage is its sampling window
over its cadence"* (`mesh-psi`, fe35dd9) — is about the **sensing** side: a narrow window under a wide
cadence reports a sample, not a state. MCC is about the **acting** side and the **conversion**: what a
count of observations means as a duration, and what an actuator's own settling time does to the
evidence the next observation collects.

## 3. Where it bites: `scripts/mesh-link-heal`

`mesh-link-heal` is the node's only actuator on its only uplink (a wedging USB `rtw_8822bu`). It climbs
a ladder — observe · reassociate · bounce · driver reload · USB re-enumerate · shout for a human — and
the rung is chosen by `down_checks`, a count of consecutive runs that saw the link down. Its own header
said it plainly: *"one rung per consecutive down-check; cadence is 1/min so a rung ≈ a minute."*

That ≈ is the uncrossed cut, and it does not hold here.

**Artifact 1 — the ticks do not all land.** `~/.mesh/link-heal.cron.log`, one line per run, birth
2026-08-16T15:08:01Z, measured 2026-08-18T03:24Z: **1727 lines in a 2177-minute window = 79.3%.** One
scheduled check in five never happened.

**Artifact 2 — the counter froze while the fault ran.** From `~/.mesh/link-heal.log`:

```
2026-08-17T01:10:07Z  ACTION reassociate ... down_checks=2
2026-08-17T01:18:01Z  RECOVERED ... after 2 down-check(s)      <- 7m54s, ZERO increments
2026-08-17T15:09:07Z  ACTION reassociate ... down_checks=2
2026-08-17T15:14:01Z  RECOVERED ... after 3 down-check(s)      <- 4m54s, ONE increment
```

Honest about the cause: both episodes predate 5a04e4f, and their freeze came from the disarm bug it
fixed (a wedge deletes the default route, `find_iface` derived the interface from that route, the run
exited n/a before touching the counter). But the disarm was **one** of the paths that freeze it. Every
`exit 2` still returns before `write_state`, and the 20.7% of missing ticks are unexplained by it.
Nothing in the tool ever converted ticks to seconds; that was never fixed because it was never named.

**Artifact 3 — the consequence, in the one line that matters.** The top rung posted to the board:

```
"... still $state_word after ${DOWN_N} min — ... the node needs hands or a reboot"
```

`DOWN_N` is a run count. At the measured 79.3% delivery, `SHOUT_AFTER=14` is ~17.7 minutes, and at the
freeze rate seen above it is far more. The message that summons a human to a 55-minute outage was
built to announce it as a 14-minute one. **A rate-independent symbol printed with a rate-dependent
unit** — MCC's failure mode, in a string.

**The control half, same cut.** `do_reload` returns after `modprobe` + 8s, `do_replug` after 13s of
`authorized` toggling; the link is not back at either moment — USB re-probe, supplicant re-attach and
DHCP still have to run. The next tick measured "still down" and scored it as further evidence of the
**fault** when it was evidence of the **cure**, and the ladder stacked the next rung on it. This is
exactly the paper's prediction that disrupting the slower maintenance timescale degrades control
fidelity while measurement still looks fine.

## 4. What was implemented

All in `scripts/mesh-link-heal` (genome source; the deployed `~/.local/bin/` copy is untouched).

1. **The converter, and it names its winner.** `effective_n <ticks> <secs>` → `"<n> clock|ticks|agree"`.
   The ladder escalates on `max(down_checks, down_secs / TICK)`. A frozen counter can no longer stall
   the climb because wall-clock carries it; a burst of extra runs cannot outrun the clock either. Both
   axes are printed on every verdict line and in `--json`; neither is ever collapsed into the other.
2. **The episode clock.** State gains `first_down_epoch` — set on the first down observation of an
   episode, never restarted by a later one, cleared only by recovery.
3. **The settle window** — the rate-dependent half made explicit. `settle_secs` per rung
   (reassociate 15s · bounce 25s · reload 60s · replug 75s), measured from when the action *returned*.
   A check inside that window is a new verdict word, **`settling`**: it observes, it prints, it keeps
   the episode clock running, it advances `down_checks` by nothing and it acts on nothing. Because the
   clock axis keeps running through it, a settle window can delay a rung but can never cancel the
   escalation.
4. **The alert stops lying.** It now reports wall-clock (`after 15m0s wall-clock`) *beside* the
   counted axis (`14 down-checks; escalation carried by=clock`), never instead of it.
5. **State is append-only, 5 → 7 fields.** A file written by the pre-cut copy reads with the new
   fields at 0 = "no episode open" — never epoch 0, which would date the fault to 1970 and fire the
   top rung on the first down check.

## 5. Gates, and each one seen red

Added to `--test`; the whole suite is green on this node. Every new gate was mutated and watched fail
**for its own reason** (mutants run from a scratch copy, exec bit set):

| mutant | gate that caught it |
|---|---|
| M1 clock axis deleted from `choose_rung` | 5 rows: frozen counter + N×cadence elapsed → `none` instead of the rung |
| M2 settle suppression deleted | `down=10 after reload with 1s left chose 'replug'` |
| M3 alert reverted to `${DOWN_N} min` | 3 rows, incl. "spells the tick count as a duration again" |
| M4 `settle_secs reload` zeroed | "that rung's transient is unmodelled" (per-rung rows, so one can rot alone) |
| M5 state read truncated to 5 fields | round-trip row + the alert losing its wall-clock |
| M6 `effective_n` winner mislabelled | "wanted '9 ticks', got '9 clock'" |

The unit gate is worth naming separately. Its **first draft greped `$0` for the old string and failed
on its own comment quoting it** — the self-matching-grep trap, live. It was replaced with an
artifact-driven gate: drive the real shout branch with a fixture whose two axes **disagree on purpose**
(14 down-checks, 900s elapsed), capture what `mesh-chat` was actually handed, and require the alert to
carry the 15 minutes that elapsed rather than the 14 that were counted. Source text is never behaviour.

## 6. One honest note on the deploy window

While the genome copy writes 7 fields and the deployed copy still reads 5, a `read -r` with five
variables lands the trailing `<first_down> <acted_at>` inside `KNOWN_GW`. Observed live: running
`--status` from the tree produced `gw="192.168.8.1 0 0"` in the state, and the deployed copy's next
cron tick (≤60s) overwrote it back to five clean fields. The window is one tick, it self-heals, and
`KNOWN_GW` is only a fallback ping target — but it is a real transient, so do not hand-run the tree
copy against the live state before `mesh-sync-tools` deploys it.

## 7. What was left on the table

The other four signatures from the same paper, unlanded and each a candidate for a later review:
anticipatory modulation index (`P(future | internal constraint)` vs `P(future | perturbation alone)`),
affordance reconstruction rate (novel functional couplings per unit time — aims at `mesh-sense-evolve` /
`mesh-needs`), syntactic open-endedness, viability-corrected skill acquisition. The ALIFE 2026 tutorial
is conceptual only; do not re-fetch it for measures.

**Sources**

- [ALIFE 2026 Tutorial: Autopoiesis & Structural Coupling](https://autopoiesistutorial.netlify.app/)
- [López-Díaz & Gershenson, *A Matter of Time: Towards a General Theory of Agency*, arXiv:2606.23122 (Jun–Jul 2026)](https://arxiv.org/abs/2606.23122)
