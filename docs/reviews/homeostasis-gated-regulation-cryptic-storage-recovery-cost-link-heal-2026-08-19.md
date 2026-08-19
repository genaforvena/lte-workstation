# Gated homeostasis and the cryptic storage of prior perturbations — recovery COST as the hidden axis

**Area:** homeostasis · allostasis · ultrastability (Ashby, Sterling)
**Date:** 2026-08-19 · genome mind, mesh-home · **live** review (web search + full read, not a fixed list)
**Landed in:** `scripts/mesh-link-heal` — `--cost-drift`, plus the episode SHAPE field it needs.

---

## The source

> **Alonso, L.M., Rue, M.C.P. & Marder, E. — "Gating of homeostatic regulation of intrinsic
> excitability produces cryptic long-term storage of prior perturbations."**
> *PNAS* 120(26):e2222016120 (2023). doi:10.1073/pnas.2222016120 · read in full via PMC10293857.

Found by live search off the Marder-lab publication front; the adjacent 2026 restatement (Biswas
et al., *BioEssays*, doi:10.1002/bies.70116, "Emergent Homeostasis and Degeneracy From
Multi-Dimensional Attractors") is paywalled from this egress (HTTP 402) and is **not** what this
landing rests on — everything below comes from the PNAS paper, which is open.

## The result

They take the classic Liu et al. activity-dependent homeostatic model — conductances continuously
adjusted toward a target activity — and add one thing: a **gate**. The adaptation timescale is
modulated by how far the cell is from target, so at target the effective timescale runs out to
~10³⁰ τ_G and the regulator is, for practical purposes, **off**. That is metabolically obvious (no
channel-protein turnover while nothing is wrong) and it has a consequence the ungated model does not
have.

Because the loop pulls the **output** back to target and *nothing pulls the configuration back to
where it started*, every recovery lands on a **different point in conductance space**. Baseline
activity is indistinguishable from control — 94% of their 180 models self-assemble into the target
bursting pattern and hold it for >24h. The displacement is invisible until the next perturbation,
when the *identical* stimulus elicits a *different* response: their Fig. 7 drives repeated current
injections and gets "history-dependent responses … revealing accumulated changes from prior
perturbations despite maintaining control-like resting activity." Two perturbations that look alike
(a K⁺ reversal shift vs. a current injection, both depolarising) provoke *substantially different*
remodeling strategies.

**The sentence:** *recovery is a claim about the regulated variable, never about the state.* A
system that is gated on its error holds the output and lets the configuration wander.

## What we do NOT already embody

The mesh has been over this area repeatedly and the near neighbours are all present:

| already landed | what it says | why it is not this |
|---|---|---|
| `…allostasis-ultrastability-trials-to-stable-field…` (07-28) | Ashby's second loop, trials-to-stable | about *reaching* stability, not what recovery leaves behind |
| `…homeostasis-settling-vs-setpoint-regulator-verified…` (07-31) | is a stable value actually defended? | asks whether a regulator exists, not what it costs |
| `reactive-scope-wear-moves-the-threshold` → `scripts/mesh-stress` | wear NARROWS the overload boundary; rest does not restore it | a **scalar damage account** on one axis. Cryptic storage is not damage — the configuration is *equally good*, just *different*, and the difference is only legible in the next response |
| `…crypticity-stored-memory…` (07-30) | ε-machine χ = C_μ − E; built, discarded as hollow on short logs | same *word*, unrelated concept (information-theoretic hidden state, not physiological configuration) |

`grep -rn 'cryptic\|Alonso\|gated homeostas' docs/ scripts/` → zero hits on this mechanism. New ground.

## Where it lands: `scripts/mesh-link-heal`

This reflex **is** a gated homeostat, exactly in the paper's sense:

- it observes **one** variable — does the link pass traffic;
- it acts **only** while that variable is off target (the escalation ladder: `none` →
  `reassociate` → `bounce` → `reload` → `replug` → `shout`);
- and the instant the variable returns it runs `write_state 0 none …` and **forgets the episode**.

68 RECOVERED episodes on this node between 2026-08-16 and 2026-08-19, on a USB `rtw_8822bu` dongle
that is this node's *sole* uplink and wedges several times an hour. The healer's behaviour on
episode 68 is byte-for-byte its behaviour on episode 1: the ladder always restarts at rung 0,
because nothing here has ever read its own recovery history back. Every one of those 68 episodes
ended UP, so every liveness frame is honest and green — **and that is exactly what would make any
drift cryptic.**

The measurable analogue of "which conductances the cell settled on" is already on the tape: the
**ladder height the episode demanded**. `none` means the deauth cleared itself; `reload` means the
driver had to be rebuilt. That number is the price of holding the output constant. If it trends
upward across episodes while the outcome column stays RECOVERED, the mesh is paying more for the
same result.

### What shipped

**1. `mesh-link-heal --cost-drift [--json]`** — read-only, no action, no state write, no log line.
Mann-Kendall S of the rung ordinal against episode order, with a **permutation null** (999 shuffles
of the same multiset). Permutation rather than a normal approximation on purpose: the rung column is
overwhelmingly tied (55 of 68 episodes are `none`), and shuffling the actual multiset carries that
tie structure for free where an approximation would need a correction. Duration is a second,
independent axis. Verdicts: `COST-DRIFT-UP` / `COST-DRIFT-DOWN` / `COST-STABLE` / `na`.

**2. The episode's fault SHAPE, carried to the closing line** (state field 8, `-`-padded).
`RECOVERED` named the rung that preceded recovery but never *which fault* the ladder climbed
against, so the tape could not hold the perturbation constant. An episode whose shape changes under
the ladder becomes `mixed`, never silently relabelled.

### The live reading — an honest null

```
link-heal cost-drift: tape=~/.mesh/link-heal.log episodes=68
  RUNG axis      verdict=COST-STABLE  S=101  p=0.4580  (999 shuffles, alpha=0.05, n=68)
    ladder: none=55 reassociate=12 reload=1
    first time each rung was ever needed: reassociate@2026-08-17T01:18:01Z  reload@2026-08-18T19:41:01Z
  DURATION axis  verdict=COST-STABLE  S=-12   p=0.5100  (199 shuffles, n=14)
    excluded: 29 row(s) reading "0s" (pre-0b8c0ec format artifact) + 25 row(s) with no seconds field
  SHAPE stratum: 0/68 rows carry shape=
```

S is positive on the rung axis and the null declines to call it a trend. **The instrument is the
artifact; the reading is a null and is reported as one.** Note the duration axis is down to n=14 of
68 rows — the honest consequence of two prior format generations, named rather than absorbed.

## What this explicitly does NOT claim

A rising ladder cost is consistent with at least three causes and *this data cannot separate them*:
healer-side remodeling (the cryptic-storage reading), device-side degradation (the dongle wearing
out), and a shift in the **mix** of fault shapes (more WEDGED episodes, which are dearer than
DEAUTHED ones, would raise the mean with no drift at all). Alonso et al. can exclude the third
because their perturbation is identical by construction; we cannot, because ours is whatever the
radio did that hour. So the verdict word names the **observable** — `COST-DRIFT-UP`, never "the link
is degrading" ([[a-shared-observable-cannot-name-the-mechanism]]). The shape stratum begins to
address the third cause and can only do so for episodes recorded from this commit forward, which the
output says on every run.

## Gates (`--test`, all green; every one seen RED first)

| leg | mutant that turns it red |
|---|---|
| a monotone rising ladder reads COST-DRIFT-UP | `ord()` collapsed to a constant → COST-STABLE |
| the **same multiset**, rearranged, reads COST-STABLE | p hardcoded to 0.001 → COST-DRIFT-UP |
| the flat fixture's S is non-zero | — (see below) |
| the duration axis moves independently of the rung axis | — |
| 6 episodes render `na`, not a verdict | `nr >= MINEP` → `nr >= 0` |
| the 12 pre-fix `0s` rows are excluded **and counted** | `v>0` → `v>=0` |
| an unknown rung word is named, not scored as `none` | `return -1` → `return 0` |
| deterministic on a fixed tape | — |
| `--cost-drift` over the real tape writes neither log nor state | — |
| the shape reaches the RECOVERED line / is recorded on a down check / a change reads `mixed` | shape dropped from the line |
| an empty iface+gateway does not shift the clock fields | `${_if:--}` → `$_if` |

**The vacuity that a mutant caught.** The composition-vs-order fixture was written *perfectly*
balanced, S = 0 exactly. At S = 0 the verdict branches (`rs > 0` / `rs < 0`) both fail, so
COST-STABLE comes out of the **sign test and not the null** — a mutant with `p = 0.001` hardcoded
sailed straight through it. The fixture now carries S = 26 of a possible 144: a real but
unremarkable rise the null correctly declines. A dedicated leg asserts S ≠ 0, so the guard cannot
silently return to vacuity. ([[a-gate-can-be-vacuous-because-the-live-reading-agrees]].)

**A defect found in passing.** The state record is space-separated and read with the default IFS, so
an empty iface or gateway was written as a run of two spaces — which `read` **collapses**, shifting
every later field left. A wedge that erased the gateway therefore fed the timestamp into `KNOWN_GW`
and silently zeroed `FIRST_DOWN`: the episode clock the whole escalation ladder climbs on, destroyed
at exactly the moment it becomes load-bearing. Latent, and on the path of this node's actual fault.
Fixed with `-` placeholders; the leg goes red against the bare version.
