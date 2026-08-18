# Live literature review — swarm intelligence & stigmergy

**Area:** swarm intelligence / collective decision-making · **Angle:** a known **CRITIQUE / failure
mode** — the swarm's inability to tell a stuck source from a real second witness
**Date:** 2026-08-18 · **Channel:** genome · **Organ:** `scripts/mesh-operator-home`
**Status:** uncommitted in tree, steward lands

---

## The critique we did not embody

**Asocial dynamics collapse three distinct corruptions into ONE indistinguishable term — so
agreement is not corroboration.**

> "we unify these seemingly distinct forms of asocial dynamics within a single mathematical
> formulation" — stubborn agents (zealots), self-sourced discovery, and man-in-the-middle
> communication corruption all enter the opinion-update equation as the same probability `η`,
> split into `η_a`/`η_b` by which option they favour.

**Citation (LIVE — revised two months ago):**
Raina Zakir, Timoteo Carletti, Marco Dorigo, Andreagiovanni Reina, *"Bio-inspired decision making in
robot swarms under biases"*, **arXiv:2509.07561** — submitted 2025-09-09, **v2 revised 2026-06-14**
(cs.MA). <https://arxiv.org/abs/2509.07561> · full text read at
<https://arxiv.org/html/2509.07561v2>. Found via live web review 2026-08-18 (search →
arxiv/researchportal.unamur.be; lineage: Reina et al., *"Robot swarm democracy: the importance of
informed individuals against zealots"*, Swarm Intelligence).

The two mechanisms they compare, as difference equations over committed fractions `a`,`b` and
uncommitted `u = 1−a−b`:

```
direct-switch      da/dt = ab(1−η)(q_a − q_b)      + η(b·η_a − a·η_b)
cross-inhibition   da/dt = a(1−η)(q_a·u − q_b·b)   + η(u·η_a − a·η_b)
                   db/dt = b(1−η)(q_b·u − q_a·a)   + η(u·η_b − b·η_a)
```

Findings that matter to us:

- **Direct-switch deadlocks under WEAK bias** — `η ≤ 0.05–0.1` is enough to stall it when the two
  options are close in quality (`q ≈ 1`). A 5 % corrupted minority is sufficient.
- **Cross-inhibition is antifragile to bias** — "moderate levels of asocial dynamics can improve the
  accuracy of cross-inhibition by eliminating the suboptimal attractor"; a bifurcation at `η*` turns
  bistability into monostability at maximal accuracy.
- The unification is the sting: **from the dynamics alone, the swarm cannot tell WHICH of the three
  it is suffering.** A zealot beacon and an honest independent witness deposit the same term.

### Why this is somewhere we have NOT been

The genome carries fourteen prior swarm landings. Cross-inhibition itself is **already embodied**
(`swarm-cross-inhibition-value-sensitive-dispatch-2026-07-28`, landed in `mesh-dispatch`), and
density/evaporation/quorum/repellent/ant-mill/fundamental-diagram are all taken. What none of them
touched is the **`η` term on the other side of the equation** — the *asocial* input, and the claim
that a stubborn source is mathematically indistinguishable from a second witness.

## The failure it names in a live organ

`scripts/mesh-operator-home` carries a **social-confidence calibration sidecar** (added 2026-07 from
Miehling et al., arXiv:2503.00237 §3.3) that counts how many **independent modality groups**
(phone / ble / att / cam) vote HOME and reports `corroborated` at `≥2`, `lone` at `1`.

Its own header states the motivation:

> "the HAND-CODED Bose exclusion … 'stationary desk speaker broadcasts BLE 24/7 … excluded': a BLE
> source that confidently voted HOME against the true consensus, caught only because a human noticed
> and hardcoded it out. This sidecar **GENERALISES that fix** — so a future silent broadcaster
> surfaces as `support=lone` instead of needing another manual exclusion."

**It does not generalise it.** The Bose speaker is a textbook **zealot**: `η = 1`, always votes HOME.
A zealot beacon plus one live phone read gives `n = 2` → **`corroborated`** — the *strongest*
confidence label the sidecar can emit, awarded to **one witness counted twice**. The generalisation
claim is false in exactly the case it names, and measured on this node right now the live verdict is
`corroborated (2/4)` on `phone + ble` — the very pair.

`mesh-operator-home` also runs a **direct-switch** rule (`_verdict`: LAN→HOME else BLE→HOME else …),
which is the mechanism the paper shows deadlocking at `η ≤ 0.05–0.1`. Its `UNCERTAIN` state is
already the uncommitted `u`, so the organ is one term short of cross-inhibition — but the *support*
count is the load-bearing gap, because that is what a downstream reader trusts.

## The change (uncommitted, in tree)

**File: `scripts/mesh-operator-home`.** A zealot is not detectable from **agreement**; it is
detectable from **responsiveness**. Three additions:

1. **`AXES_TAPE` (`~/.mesh/op-home-axes.log`)** — one line per eval, **written unconditionally**
   (`<epoch> phone= ble= att= cam= status=`). Never gated on a change: a tape written only when the
   value moves has zero entropy in the very axis it exists to measure (CLAUDE.md, the room-sense
   `confidence=high` 253/253 shape). The tool is the tape's sole writer, so it owns the trim
   (`AX_KEEP`, ~7 d at the `*/5` cadence).
2. **`_asocial <tape> [min_n] [window]` → `"<stuck-csv|-> <n>/<min_n> <varied>"`** — an axis is
   `stuck` (`η ≈ 1`) iff it voted positive on **every** record in the window, `n ≥ min_n`, **and the
   fused verdict took ≥2 distinct values in that window**. That last guard is load-bearing and is the
   doctrine's own *value-frozen is honest calm* (`mesh-psi`): if the operator simply never left,
   every axis is constant and constancy is TRUE. Constancy is evidence of asociality only against a
   world that moved. A thin window or a frozen world renders `-` — degrading to the old count, never
   to a fabricated accusation — and the **coverage `n/min_n` is published beside the verdict**, so
   "no stuck axis" can never be read as "checked and clean".
3. **`_calibration` gains a 6th arg** and **discounts** stuck axes out of the support count. New
   verdict class **`asocial`**: positive evidence exists but *every* source of it is non-responsive —
   the Bose shape, which used to read `corroborated`. Still strictly **report-only**: the sidecar
   annotates, it never changes `status`.

Swept every reader of the changed format: the `read -r` at the call site, the `--json` line (three
additive fields `discounted` / `asocial_coverage` / `world_varied`), the human report block, and all
six pre-existing `_calibration` asserts.

### Verification (artifacts, not claims)

`--test`: **+9 new assertions** (the banner tally goes 31 → 40), green. Six new tape cases, driven from a `mktemp -d` fixture so the
test never writes the durable tape it exists to check (test-forgery rule): thin window · frozen world
· the zealot · end-to-end `corroborated → lone:phone` degradation · a responsive axis · an absent tape.

**Seen RED before green** — four mutants, run from a scratch copy:

| mutant | result |
|---|---|
| drop the world-varied guard | RED — `frozen world (varied=0) must NOT call a constant axis stuck: phone,ble 30/24 0` |
| drop the coverage floor | RED — `thin tape (5<24) must render '-' …: ble 5/24 1` |
| ignore the discount entirely | RED — 3 asserts incl. `zealot-BLE + live phone must degrade corroborated → lone:phone` |
| count 0-votes as positive | RED — `a responsive axis must never be called stuck: phone,ble,att,cam 30/24 1` |

**Live path exercised** (not just the pure functions): 3 real runs + `--json` + `--edge`, tape
override to scratch. Tape written, coverage counted up `1/24 → 2/24 → 3/24`, `--edge` rc=0 with
`.op-home.state` unchanged, and the real `~/.mesh/op-home-axes.log` **not** created (override
honoured). Deployed `~/.local/bin/` copy untouched — steward lands from the tree.

## What is deliberately NOT done

Converting `_verdict` from direct-switch to a true cross-inhibition update (a conflicting axis drives
the verdict to `UNCERTAIN` rather than flipping it) is the paper's second, larger claim. It changes
the **verdict** of a reflex six other tools read (`mesh-perimeter`, `mesh-burn-window`,
`mesh-cell-info`, `mesh-motion-attribution`, `mesh-household-state`, `mesh-operator-state`) and is a
separate task with its own before/after artifact — filed, not smuggled in behind a report-only
sidecar.
