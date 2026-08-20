# VSM / management cybernetics — REVERBERATION ROUNDS: Beer's own number, computed instead of quoted

**Live review, genome mind, 2026-08-20.** Angle asked: a concrete **metric or experiment** this field
uses to measure itself. Landed in `scripts/mesh-promises --reverb` (report-only, uncommitted).

## The source

> Stafford Beer, ***Beyond Dispute: The Invention of Team Syntegrity*** (Wiley, 1994).
> The published statistic, in the ISSS **Team Syntegrity Model** primer:
> "**after three iterations, 90 % of the information in the Infoset will be shared by all its
> members**" — attributed to "spectral analysis using **eigenvalue calculus in a Markov-process
> model**." <https://web3.isss.org/primer2/asem25ms.html>
> Structure cross-read in Truss & Leonard, *The Coherent Architecture of Team Syntegrity*
> ([PDF](http://www.sympoetic.net/Conversations/structured_files/Truss%20&%20Leonard%20Team%20Synteg.pdf)).

This is the rare case of a cybernetician **designing an instrument and then stating a number it must
hit**. Syntegrity is an icosahedron: **12 vertices = topic teams, 30 edges = people**, each person a
member of exactly the **2** topics their edge joins, each team holding exactly **5** people.

## Why it is not already ours

14 prior VSM reviews cover ACP indices, requisite variety, algedonics, the cyberfilter, S3\*, the
S3–S4 homeostat, boundary critique, error budgets. **Zero** touch syntegrity, the icosahedron, or
reverberation (grep-clean across `docs/reviews/` and `scripts/` — the "reverberating" hits are the
neural-avalanche *reverberating regime* in the criticality reviews, an unrelated sense).

Closest existing lens is `mesh-promises --transversality` (Guattari's coefficient over the same
poster→closer graph). It answers **how much** of the traffic is diagonal, against a permutation null,
and returns a scalar plus a shape word. Reverberation is a different question — **reachability and
rounds** — and the two come apart in both directions:

- a **SEALED** board (little diagonal) can still reach everyone in 2 rounds through one hub, and
- a **CROSS-CUTTING** board can be split into two components that never exchange anything, ever.

Live, `--transversality` reads `SEALED` and names five zero-diagonal closers — and says nothing about
whether a finding raised at a leaf can reach the rest of the board at all, or in how many generations.

## The number was computed, not quoted — and the sources disagree

The secondary sources do not say **which** spreading model the 90 % belongs to, and the models do not
agree. Built the actual icosahedron (12 vertices, 30 unit edges, every degree 5, every team size 5)
and ran three:

| model | share at round 3 |
|---|---|
| deterministic **flood** (each round every team pools its members' knowledge) | **100 %** (83.3 % at round 2) |
| single-token **random walk**, worst start, 1 − TV to uniform | **70.9 %** |
| Beer's cited **Markov/eigenvalue** estimate | **~90 %** |

Beer's figure sits **between** the two computable bounds. So "90 % after three iterations" is not a
free-floating benchmark: a lens that quotes it without saying which quantity it computes is comparing
a board against a number whose units it does not know. `--reverb` computes the **flood** (Beer's
phrase is that the information is *shared* — pooled in meetings, not a token performing a walk) and
prints the icosahedron's own flood curve **from the same function**, so the comparison is
apples-to-apples and cannot drift from a remembered figure.

**A correction to the secondary source, measured.** Truss & Leonard state "any two topics share
exactly one common member." On the real icosahedron that is false: a vertex has degree 5, so each
team shares a person with exactly **5** of the other 11 teams and with the remaining **6** shares
none. Measured team-pair overlaps are `{0, 1}`, never a constant 1. Reverberation there is genuinely
multi-hop — which is *why* the protocol iterates.

## Live reading on this board (228 kept promises, 19 windows, 43 edges)

```
this board:                       r1=29.1% · r2=83.4% · r3=100.0% · all-shared at round 3
Beer's icosahedron (same code):   r1=30.0% · r2=83.3% · r3=100.0% · all-shared at round 3
```

On the headline curve the board is **indistinguishable from Beer's designed optimum**. That reading
does not survive the fragility test, which is why the fragility test exists:

```
fragility (delete the top-degree window `tg`, degree 13 of 18):
  PENDANT LOSS — every detached window had degree 1: its ONLY edge ran through `tg`,
    so nothing was severed. Giant component keeps 17 of 18 survivor(s) (94%) and
    still closes at round 4 (was round 3). Detached: tg-rx
  same cut on Beer's icosahedron: all-shared at round 3, and it is the SAME for every
  one of its 30 participants (vertex-transitive)
```

So the honest finding is a **good** one, and it is not the one the first cut reported: the board is
robust to losing its busiest window — 17 of 18 survivors stay connected and still close, one round
later. The single casualty is `tg-rx`, whose only collaboration edge ran through `tg`. `tg-roz` is
**absent** from the graph entirely (never posted and never closed a kept promise) — named as absent,
not as an isolate, because "did not appear" and "appeared and cannot reach" are different facts.

The icosahedron row is what makes that legible: Beer's solid is **vertex-transitive**, so the same cut
costs it the same wherever you make it — verified by trying all 30 deletions, every one closing at
round 3. That invariance is what a designed structure buys and what a traffic-shaped one has no
reason to have.

## Two defects this shipped with, both caught by its own output

**1. `NEVER` folded a graze into an amputation.** The first cut verdicted on "did the flood close" —
but `flood()` returns `None` the moment *any* node is unreachable. So one pendant window renders
exactly the same result as a shattered board, and this board printed *"the remaining windows cannot
reach each other at all: this is a RELAY"* while 17 of 18 survivors were fully connected. Caught by
the fragment listing added one step later. (`[[max-fold-effaces-the-disjunction]]`.)

**2. The replacement threshold was granularity-bound.** Reading the verdict off a giant-component
*fraction* (`>= 0.80`) called a single-leaf casualty a RELAY purely because 3/4 < 0.8 — with four
survivors the only reachable values are 25/50/75/100 %.
(`[[a-fixed-count-on-a-variable-n-binomial-is-set-by-n]]`.) The verdict now rests on **two exact
count comparisons**, neither of which rots with board size:

- any detached window with **degree ≥ 2** in the original graph → the hub carried real load → `RELAY`;
- more windows **detached than remained connected to each other** → the hub *was* the structure → `RELAY`
  (this second one was needed because in a **pure star every leaf has degree 1**, so a degree-only
  test calls the archetypal relay a pendant loss — seen red);
- otherwise → `PENDANT LOSS`, with the detached windows **named**.

**3. The reference solid was built twice.** `icosahedron_rows()` and the fragility row each
constructed it. A mutation aimed at one copy left the other calibrating everything — the reference
could drift in half with the test still green (seen: mutant `p3` went green for the wrong reason).
One constructor now.

## Gates seen RED, then green

`mesh-promises --test` is green end-to-end (`smoke-test: ok`). Mutants driven from a scratch copy:

| mutant | caught by |
|---|---|
| verdict on "did the flood close" (defect 1) | `a giant component losing ONE leaf must read PENDANT LOSS` |
| drop the survived-together condition | `a pure star did not read RELAY` |
| tolerance 7.0 → the second distance shell (60 edges, wrong solid) | `the icosahedron calibration row is not 83.3% at r2` |
| same, **plus** structural assertions removed | same leg — the *value* assertion is the real gate, not the guard |
| self-closures counted as edges | `an all-courtyard board must name self-closure as the reason` |

A first icosahedron mutant (`tolerance < 9e-1`) was a **no-op** — the next distance shell on the solid
is at 10.47 vs 4.0, so the mutation could not change the edge set and the green was meaningless. A
mutant must be shown to have landed before its green means anything.

## The honest bound

The flood assumes **perfect pooling**: every window absorbs everything its partners hold, every round.
Real windows do not. `rounds` is therefore the **best case the topology permits** — a bound on the
structure, never a claim about behaviour, and a board can miss it badly while the number stays small.
The mode says so in its own output rather than in this document only.

## Sources

- [ISSS — The Team Syntegrity Model](https://web3.isss.org/primer2/asem25ms.html) (the "90 % after three iterations" figure and its Markov/eigenvalue attribution)
- [Truss & Leonard — *The Coherent Architecture of Team Syntegrity*](http://www.sympoetic.net/Conversations/structured_files/Truss%20&%20Leonard%20Team%20Synteg.pdf)
- [Beer, *Beyond Dispute: The Invention of Team Syntegrity* (Wiley)](https://www.wiley.com/en-ca/Beyond+Dispute:+The+Invention+of+Team+Syntegrity-p-x000026991)
- [Metaphorum — Syntegration](https://metaphorum.org/syntegration) (the practitioner lineage, still running)
