# Homeostatic coupling vs mere partner-state access — `mesh-load-gate --coupling`

**Date:** 2026-08-04 · **Area:** homeostasis / allostasis / ultrastability, cross-domain transfer to a
distributed sensor mesh · **Landed:** read-only diagnostic in `scripts/mesh-load-gate` (actuator HELD)

## The source (live literature, found this session)

**Aishik Sanyal, *Prosociality by Coupling, Not Mere Observation: Homeostatic Sharing in an Inspectable
Recurrent Artificial Life Agent*, arXiv:2604.10760v2, submitted 2026-04-12.** Found by searching
current arXiv cs.MA / ALife for homeostatic regulation across agents; abstract read via the arXiv API
(`export.arxiv.org/api/query?id_list=2604.10760` — the web page is unreachable from this node's egress).

The paper isolates a narrow route to helping behaviour. Building on ReCoN-Ipsundrum, it adds a scalar
homeostat and a *social coupling channel* while keeping action selection strictly self-directed — the
planner scores **only the actor's own predicted internal state**, with no partner-welfare reward. Two
results matter here:

1. **Access is inert; coupling is not.** In SocialCorridorWorld, *"partner-state access without coupling
   leaves behavior unchanged, whereas coupled agents fetch, carry, and pass food to the partner."*
   Sham lesions preserve helping; coupling-off and shuffled-partner lesions abolish it. The paper's own
   summary: *"partner-state access is behaviorally inert unless partner distress is routed into
   self-regulation."* (In the one-step FoodShareToy an exact solver puts the EAT→PASS switch at
   λ\*≈0.91.)
2. **Coupling does not guarantee rescue.** A coupling/load sweep shows coupling creates a **low-load
   helping regime** but *"does not guarantee rescue under higher metabolic load"* — a saturated actor
   cannot help however well coupled.

Not a claim about empathy or moral status, and not imported as one. It is a **control-topology** result:
what an input has to be wired *into* before it can change behaviour.

## Why this is new ground for us

The homeostasis area is heavily covered here (allostatic load, Mahalanobis joint dysregulation, CDP,
CSD, reactive scope, requisite variety, ultrastability trials-to-stable-field, settling-vs-set-point,
antagonistic controller pairs, rheostasis, enantiostasis, control-burden hysteresis). **Every one of
them reads a single regulator's own variables.** Even the two-controller landing (`mesh-pace
--control-mode`, 2026-08-04) is two controllers *inside one node* on *one* controlled variable.

The open-gap note carried "social allostasis / co-regulation via peers — the set-point-reconfiguration-
via-other-agents half is not embodied" as a standing gap from Khan arXiv:2508.12791. Sanyal sharpens
that gap into something **testable on artifacts we already write**: it is not enough to ask whether a
node *can see* its peers; you have to ask whether seeing them changes what it *does*, and the
discriminator is a lesion, not an intuition.

## The mesh is the inert-access case

`mesh-load-gate` is the mesh's shed regulator: heavy reflexes are prepended with it and skip their tick
when the box is loaded. `decide()` takes exactly three inputs — **this box's** load1, **this box's**
free disk, the wall clock. Its essential variables are strictly local.

But the reflexes it gates are not local. `mesh-node-care` SSHes **every declared node every 5 minutes**;
`mesh-fleet-health` / `mesh-fleet-states` walk the fleet; `mesh-tell` drives peer windows. And peer
distress is not merely *accessible* — this node has already **measured it and written it to its own
disk**: `~/.mesh/node-care.log` carries per-node `load=/temp=/disk=/mem=` every sweep, 11k lines of it.

The gate has never read that file. Verified by grep: `mesh-load-gate`, `mesh-resource-guard`,
`mesh-pace`, `mesh-mind-control`, `mesh-algedonic` — **zero** references to any fleet/peer state source.
So mesh-home reads its own load1, PROCEEDs, and lands another sweep onto a peer that is itself drowning.
Access without coupling, exactly the configuration Sanyal shows is behaviourally inert.

That the peer really is drowning is not hypothetical: phaedra is a **2-core** box whose 7-day mean load
is **4.91** (max 20.94) — chronically over 2× saturated — while mesh-home (16 cores) idles at ~1.2.

## What landed: `mesh-load-gate --coupling [hours]` (read-only)

The **measurement** half. The actuator — a peer term in `decide()` — is **HELD**: shedding a local
reflex on a *remote* reading changes behaviour on the operator's hand-tuned ceiling, and a peer sense
that goes hollow would silently disable every heavy reflex forever, against this file's own explicit
false-skip asymmetry ("a false skip silently disables a reflex forever, so uncertainty proceeds").

It runs the paper's question against real artifacts:

| | |
|---|---|
| **output** | this gate's **real** shed events (`~/.mesh/load-gate.log`) — actual behaviour, not a replay |
| **partner** | each peer's `load=` in `~/.mesh/node-care.log`, aligned into 5-min buckets |
| **effect** | `P(shed \| peer distressed) − P(shed \| peer calm)` |
| **distress** | self-calibrated at the `CS_Q`-th percentile of **that peer's own** loads — a 2-core peer at load 5 is not a 16-core peer at load 5 |
| **null** | `max \|effect\|` over K **circular shifts** of the peer series |

**Shift, not shuffle.** The paper's lesion is a shuffled partner; loads are strongly autocorrelated, and
an i.i.d. permutation null is anticonservative on an autocorrelated series (our own `mesh-cooscillate`
finding). A circular shift destroys the alignment while preserving each series' own structure — the
same lesion, done correctly for time series.

Verdicts: `INERT-ACCESS` · `ASSOCIATED-UNROUTED` · `NO-OUTPUT-VARIANCE` · `NO-DISTURBANCE` ·
`INSUFFICIENT` · `NO-ACCESS`, plus the paper's load sweep as `rescue=HEADROOM|NO-RESCUE|MIXED|UNKNOWN`.

Two of those deserve their names spelled out:

- **`ASSOCIATED-UNROUTED`, not `COUPLED`.** A statistic cannot distinguish *routed* from *co-located*.
  If shed behaviour covaries with peer distress beyond the null, the honest reading is **common cause**
  (one operator burst loading both boxes), because no code path routes peer state into `decide()` — and
  here the lesion that settles it is trivial to run: read `decide()`. This keeps the tool from
  laundering a correlation into a claim about mechanism.
- **`NO-OUTPUT-VARIANCE`.** If the gate never shed (or always shed) in the window, its behaviour did not
  move, so its dependence on *anything* is untestable. An honest refusal, not a pass — the shape that
  would otherwise have read as a confident "not coupled".

## Live result (mesh-home, 2026-08-04)

```
COUPLING span=168h self=mesh-home thr=11 (modal, from shed log) buckets=764 shed-buckets=200
  EDGE:          INSUFFICIENT         eff=+0/1000 null=±0/1000 n=1 high=0 (load>2.67, spread 2.67..2.67)
  phaedra        INERT-ACCESS         eff=+40/1000 null=±83/1000 n=763 high=153 (load>7.36, spread 2.39..20.94) rescue=HEADROOM
      effect 40m within circular-shift null ±83m
      rescue: 96% of the peer's distressed buckets had local headroom
COUPLING-STATE: INERT-ACCESS
```

Two facts, both measured:

1. **The coupling is absent, and now demonstrated absent rather than assumed.** Across 763 aligned
   5-min buckets with 200 real shed events and 153 phaedra-distress buckets, mesh-home's shed behaviour
   is statistically independent of phaedra's distress (effect +0.040, inside the ±0.083 shift null).
   24h read agrees (−0.048 inside ±0.144).
2. **The helping regime is available here** — the paper's second result comes out the *favourable* way
   on this fleet. In **96%** of phaedra's distressed buckets mesh-home had headroom under its own
   threshold. Sanyal's animats failed to rescue because the actor was saturated too; mesh-home is not.
   So wiring the coupling would not be theatre — it is the case where coupling can actually pay.

That second number is the argument for the HELD actuator, and it is the number to re-derive before
anyone proposes it (it is the current answer of a live claim, not a constant — the fleet's load
correlation can change).

## Test (RED-first; 9 mutants seen fail, from scratch copies)

25 coupling cases: 13 on the pure classifiers (`cs_classify`/`cs_rescue`) + 6 end-to-end fixtures
driving `cs_report` through the two real artifact formats. Full suite 0.7s, `rc=0`.

Four mutants **survived the first version of the suite** — the gates were vacuous and had to be rebuilt:

| Mutant | Why it survived | The leg that now kills it |
|---|---|---|
| null-band veto deleted | the null-veto fixture's effect was *also* under the practical floor, so the floor caught it either way | fixture with effect **above** the floor but **inside** the null (and its mirror for the floor) |
| circular-shift null → 0 | no end-to-end case where a **real** effect must be vetoed | **periodic fixture**: peer-high and shed share one 2h period → raw effect **+1.000**, reproduced by every whole-period shift → must read `INERT-ACCESS` |
| per-peer quantile → fixed absolute cut | every fixture had one peer on one scale | **two-scale fixture**: a 2-core-like peer (0.2/1.8) and a 16-core-like peer (2.0/18.0), both coupled — a shared absolute cut finds only one |
| unresolvable-threshold guard removed | rescue-UNKNOWN was only tested on the pure function | fixture whose shed lines carry no `threshold=` (disk-floor skips) → `rescue=UNKNOWN`, never a faked `NO-RESCUE` |

Also caught and fixed while building, each a real defect rather than a test artifact:

- **`NR==FNR` on an empty first file.** With no shed events — precisely the `NO-OUTPUT-VARIANCE` state
  this tool exists to report — `NR==FNR` stays true into the *second* file and the care log is parsed
  as the shed log. Now keyed on `FILENAME`. (Seen red before the fix.)
- **Bucket key was an ordinal.** `"10"` sorts before `"9"`, scrambling the time order the shift null
  depends on. The key is now a real 5-min-floored timestamp, sortable by construction and legible in
  the output; a dumped-artifact assertion (`MESH_COUPLING_DUMP`) gates the format and the ordering.
- **First-wins verdict precedence.** A single-sample `EDGE` row (n=1, `INSUFFICIENT`) sorted ahead of
  phaedra and turned a 763-sample `INERT-ACCESS` read into `COUPLING-STATE: INSUFFICIENT` — one noise
  peer masking the whole answer. Precedence is now by informativeness.
- **Quantile inside the plateau.** A peer whose high band is wider than `(100−CS_Q)%` puts the cut
  *inside* it, and `> hi` yields zero distressed buckets. Honest `INSUFFICIENT`, documented at the
  fixture that hit it.

Span is a parameter for the reason `mesh-pace --control-mode` learned: a 24h read answers about a
window, not about the mesh. Default 168h.

## Files

- `scripts/mesh-load-gate` — header note, `cs_classify` / `cs_rescue` / `cs_report`, `--coupling`
  dispatch, 25 test cases. No change to `decide()`, to any exit code, or to any shed behaviour.
- Consumed (read-only, unmodified): `~/.mesh/node-care.log`, `~/.mesh/load-gate.log`.

## Held / open

- **The actuator** — a peer-distress term in `decide()` (Sanyal's coupling channel; λ\* is the mesh
  analogue of "how much peer load counts as local load"). Operator's call: it changes shed behaviour.
  The `rescue=HEADROOM 96%` reading is the evidence that it would do something.
- **Direction.** This measures association, not who loads whom. A directed read (does mesh-home's sweep
  *cause* phaedra's load?) needs the transfer-entropy machinery in `mesh-cooscillate`, and would answer
  the sharper question: is the steward's own care reflex a load source on the node it is caring for?
