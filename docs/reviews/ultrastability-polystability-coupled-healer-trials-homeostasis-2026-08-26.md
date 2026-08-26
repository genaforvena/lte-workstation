# LITERATURE review — homeostasis, allostasis & ultrastability (Ashby, Sterling), entered from a known CRITIQUE: **the ensemble does not inherit the single unit's convergence** (2026-08-26)

**Area:** homeostasis, allostasis & ultrastability (Ashby, Sterling).
**Angle (as the task named it):** a known **critique / failure mode** of the area.
**Reviewer:** genome mind · live web review, read today.
**Landing:** `scripts/mesh-homeostasis` — new `--dispersion [--json]` mode, `disp_selftest` with 7
RED-first legs, three mutations driven RED-then-GREEN.

---

## Where the frontier already was (checked BEFORE reading)

`docs/reviews/` holds **19** files in this area. Already taken: ultrastability trials-to-stable-field,
settling-point vs set-point, allostatic load as a specification curve, allostatic overload type 1/2,
rheostasis / defended set-point, habituation & alarm fatigue, predictive-vs-reactive anticipation,
antagonistic controller pairs, gated regulation & cryptic storage, network-physiology time delays,
the outer-loop timescale condition.

Every one of those is about **a regulator**. A `grep -rioE 'polystab|dispersion of the step|partial
connect'` over `docs/` and `scripts/` returns **nothing**. The critique below is about the **ensemble**,
and it is un-landed.

## The critique, cited

Ashby's ultrastability is usually quoted as a convergence result: a two-loop system whose outer loop
re-parameterises on essential-variable breach *will* find a stable field. The standing critique is that
this **does not scale**, and the modern re-simulation is where I read it:

> **Franchi, S., "Homeostats for the 21st Century? Simulating Ashby Simulating the Brain",
> *Constructivist Foundations* 9(1): 93–101 (2013).** The abstract states that "even though Ashby's
> claims about homeostatic adaptivity need to be **slightly weakened**, his overall results are
> confirmed." The simulation's operative finding: **increasing the number of units increases the time
> taken to reach equilibrium, and, conversely, reducing internal connectivity reduces the time taken
> to reach equilibrium.**

The mechanism is mechanical, not statistical: **unit A's step-mechanism TRIAL is, from unit B's side of
the wiring, an environmental DISTURBANCE.** A fully-joined ensemble searches a space that each trial
keeps re-shuffling. Ashby's own cure is **dispersion** — partial connection — and it is a property of
the ensemble that **no single regulator can observe about itself**.

The same failure has an independent, live engineering literature under a different name — interference
between concurrent adaptation loops:

- Vromant, Weyns et al., *"On interacting control loops in self-adaptive systems"* (SEAMS).
- Arcaini, Riccobene & Scandurra, *"Modeling and Analyzing MAPE-K Feedback Loops for Self-Adaptation"*,
  **SEAMS 2015** — proposes *"a verification technique based on meta-properties … to discover unwanted
  interferences between MAPE-K loops at the early stages of the system design."*

Note what that field's answer is: **design-time formal verification of the loop set.** We have no
design-time model of our reflex set and are never going to have one — our healers are independent shell
scripts with their own cadences. What we *do* have is every actuator's own dated ledger. So the
contribution here is to measure the coupling **at runtime, from the tapes**, rather than prove its
absence on paper.

## The failure is REAL on this node, and it was invisible

Measured today from `~/.mesh/link-heal.log` and `~/.mesh/exit-node-lan-heal-applications.log`:

    link-heal -> exit-node-lan-heal   COUPLED    hits=4/7  base=0.0174  p=3.09e-06  overlap=414215s
                                        lags=[117, 117, 120, 121]s — 4 lags inside a 4s band of the 180s window
    exit-node-lan-heal -> link-heal   DISPERSED  hits=0/42 base=0.0026  p=1.0
                                        hits=0 < min-detectable 2 — powered enough to have seen it

**4 of 7** LAN-throw re-applications were preceded within 180s by a `mesh-link-heal` driver reload,
against a base rate of **0.017**. The rate excess alone is p≈3e-6. The stronger evidence is the **lag
concentration**: four lags inside a **4-second** band of a 180-second window. A coincidence has no
reason to be punctual.

And the reverse direction is **DISPERSED with the power to have said otherwise** (0 hits in 42, against
a min-detectable count of 2). So this is a **directed drive**, not a shared cause — which is exactly
what Ashby's picture predicts and what a symmetric excess would have refuted.

The mechanism was already written down in this node's own operator context, and never named as a
coupling: link-heal's driver reload forces a tailscaled netmap reconverge; the reconverge wipes the LAN
throw route out of table 52; `mesh-exit-node-lan-heal` must then re-apply it. **One ultrastable unit's
trial is another ultrastable unit's disturbance.** Both healers are individually correct, individually
tested, and individually green — the pathology exists only at the ensemble level, which is precisely
Franchi's point and precisely the level nothing here was measuring.

## What landed: `mesh-homeostasis --dispersion`

For every ordered pair of actuator ledgers it computes hits within `W` (default 180s), the base rate,
an exact binomial tail, the lag set, and one of four verdicts. **It installs nothing** — matching this
organ's declared instrument-first posture; dispersing a coupled pair (staggering cadences, gating the
downstream healer on the upstream one's quiet) is a substrate decision, not a cron add.

Five things it refuses to do, each of which would have made it a liar:

1. **Underpowered ⇒ UNKNOWN, never DISPERSED.** It publishes the *minimum detectable hit count* at the
   observed base and n. "No coupling found" off 2 events is a statement about power, not about the world
   — the quiet-pool trap this node has been bitten by before.
2. **The base rate is the UNION coverage of A's windows**, never `count × W / span`. With A firing every
   60s under `W=180` the windows overlap three deep and the naive form yields **3.0** — not a probability
   at all. Gated: `0.9 < base ≤ 1.0`.
3. **Spans are the INTERSECTION of the two ledgers' observed spans**, taken from *every* dated row rather
   than from matching rows, and a pair overlapping by less than `W` renders UNKNOWN. A ledger that
   started yesterday cannot speak about last week, and a bare `0/n` there would read as dispersion.
4. **A symmetric excess is BIDIRECTIONAL, not a drive.** A common third disturbance produces exactly
   that signature. (This is computed in two phases — relabelling in the same sweep that reads the
   opposite direction leaves exactly one half of a symmetric pair still asserting a direction, which is
   how the first implementation was wrong and how leg 5 caught it.)
5. **A pattern matching 0 of N dated rows is refused, not counted as zero.** This tool shipped its own
   defaults with `[[:space:]]`, which Python's `re` parses as the character set `{[,:,s,p,a,c,e}` —
   every source read `actuations=0` while looking perfectly configured, and a silently mistyped pattern
   reads *exactly* like a quiet healer. The live run above is what that bug hid.

Also fixed on the way: `math.comb` overflows to `OverflowError` on a ledger with thousands of rows —
i.e. on the pair carrying the **most** evidence, the worst place to lose a verdict. The tail is computed
in log space via `lgamma`.

## Gates — each verdict crossed by construction, three mutations seen RED

`disp_selftest`, 7 legs on synthetic ledgers: deterministic-120s-lag ⇒ COUPLED (lag band 0s) ·
never-in-window with n=60 ⇒ DISPERSED · same geometry with n=2 ⇒ UNKNOWN · always-firing A ⇒ base ≤ 1
and not COUPLED · interleaved ⇒ BIDIRECTIONAL both ways · disjoint spans ⇒ UNKNOWN · the POSIX-class
pattern ⇒ refused.

    mutant: base = count*W/span (naive)       -> FAIL (an ALWAYS-firing A read as COUPLED, or its base rate was not union coverage)
    mutant: underpowered falls through        -> FAIL (n_b=2 reported a verdict instead of UNKNOWN — a null off no power reads as a cure)
    mutant: coupling detector disabled        -> FAIL (a deterministic 120s lag did not read COUPLED — the detector is vacuous)
    restored                                  -> disp-test: ok   ·   smoke-test: ok (whole suite)

One test bug worth recording because it produced *the right colour for the wrong reason*: the first
draft's assertion messages used `{p[\"verdict\"]}` inside an f-string, a `SyntaxError`, so four legs
"failed" without ever evaluating their claim. A red gate that is red for its own syntax proves nothing.

## Bounds, stated

- `n_b = 7` for the coupled pair. The p-value is small and the lag band is the real evidence, but this
  is **one pair on one node over 4.8 days of overlap**; it is not a mesh-wide law.
- `ble-heal` renders UNKNOWN because its ledger has no ISO-dated rows. That is honest and it is also a
  gap: two of the three declared sources are currently unmeasurable against each other.
- **The window `W=180s` is a guess, not a measurement.** It was chosen wide enough to contain the
  observed ~120s lag. A coupling with a longer transport delay is invisible at this setting and the tool
  does not sweep `W` — a real specification-curve over `W` is the obvious next thing and is not here.
- The verdict is association plus a mechanism story, not an intervention. The decisive experiment is a
  deliberate driver reload with the LAN throw watched — the node already has `mesh-route-events` for
  exactly that tape, and it caught this transition once at µs resolution on 2026-08-25.

## Sources

- [Franchi, S., *Homeostats for the 21st Century? Simulating Ashby Simulating the Brain*, Constructivist Foundations 9(1):93–101 (2013)](https://constructivist.info/9/1/093.franchi)
- [Franchi, S., *Homeostats for the 21st century? Lessons Learned from Simulating Ashby Simulating the Brain*](https://www.semanticscholar.org/paper/Homeostats-for-the-21st-Century-Simulating-Ashby-Franchi/9892c775bdce358b66d73a14c380a729aa426626)
- [Vromant, Weyns et al., *On interacting control loops in self-adaptive systems* (SEAMS)](https://www.researchgate.net/publication/221556171_On_interacting_control_loops_in_self-adaptive_systems)
- [Arcaini, Riccobene & Scandurra, *Modeling and Analyzing MAPE-K Feedback Loops for Self-Adaptation*, SEAMS 2015](https://dl.acm.org/doi/abs/10.5555/2821357.2821362)
- [Battle, S., *Ashby's Mobile Homeostat*](https://link.springer.com/chapter/10.1007/978-3-319-18084-7_9)
- [Homeostat — Wikipedia](https://en.wikipedia.org/wiki/Homeostat)
