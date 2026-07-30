# Live review — second-order cybernetics: von Foerster's **eigenform / eigenbehavior**, applied to `mesh-situation`

**Date:** 2026-07-28 · **Area:** second-order cybernetics (von Foerster, Pask, Beer) · **Angle:** cross-domain
transfer to a distributed sensor mesh · **Landed:** report-only `eigen_classify()` sidecar in
`scripts/mesh-situation` (does NOT touch POSTURE or the `.situation.state` consumer contract).

## The concept (named + cited)

**Eigenform / eigenbehavior** (Heinz von Foerster; formalized by Louis H. Kauffman). Von Foerster's claim:
an **"object" is not a pre-given thing — it is a *token* for an eigenbehavior**, i.e. the **fixed point** a
recursive operation converges to. Writing the recursion as an operator `F`, an object `Obj` satisfies

    Obj = F(Obj)

The object is *what the recursion stabilizes into*. Kauffman's formalization ("EigenForm", *Kybernetes*
34(1/2), 2005; and "A concise approach to eigenform and reflexivity") makes the operational point sharp:
the eigenform has **no existence outside the recursive interaction** — it is the observed stability, not a
thing behind it. Corollary that matters for a sensor: **if the recursion does not converge, a reported
"object" is a reification of a transient** — you are naming a stable thing where there is only churn.

**Where I found it (live, currently-published lineage):**
- Louis H. Kauffman, *EigenForm*, constructivist.info/Kybernetes — <https://constructivist.info/special/second-order/material/kauffman-2005-eigenform.pdf>
- Paul Pangaro, *An Invitation to Recursioning: Heinz von Foerster and Cybernetic Praxis* — <https://www.pangaro.com/Heinz-von-Foerster/Pangaro-Invitation-to-Recursioning-Heinz-von-Foerster.pdf>
- *Eigenbehavior at the intersection of second-order cybernetics and ecosystem management*, **Kybernetes**, Emerald, 2024 — <https://doi.org/10.1108/K-03-2023-0482> (a **currently-published** application, confirming this is live literature, not a fixed 1970s list)
- Von Foerster, "Objects: Tokens for (Eigen-)Behaviors" (the primary source Kauffman formalizes).

**Why this is NEW for us.** Our second-order-cyb coverage map already embodies von Foerster's *trivial vs
non-trivial machine* (`nontrivial-machine-*`) and his *observer-coverage* ("the observer is part of the
observed" — already a comment inside `mesh-situation` counting `axes_unseen`). **Eigenform is a distinct
von Foerster concept and was uncovered** (`grep -rl 'eigenform\|eigenbehav' scripts/` → 0 before this).
Observer-coverage is about *spatial* blindness (which eyes are open right now); eigenform is about
**temporal convergence** — whether the reported object is a fixed point at all.

## The cross-domain transfer (code-grounded)

`mesh-situation` folds three axis-fusions into one committed **posture** (NOMINAL/WATCH/ALERT), and — to
kill cry-wolf flapping — it **debounces**: the committed posture `ann` in `.situation.state` only changes
when a new raw posture is *sustained* `SIT_N` reads (`situation_decide()`).

Read `situation_decide()` as von Foerster's recursion:

    committed_{t+1} = F(committed_t, raw_observation_t)

- The committed posture `ann` **IS the eigenform** — the stable object the recursion holds.
- The branch `if [ "$posture" = "$ann" ]` (raw agrees → state unchanged) is **literally `F(x) = x`**.

**The gap the transfer exposes.** The `SIT_N` debounce *suppresses* oscillation but **never measures
whether an eigenform exists at all**. A raw axis that flaps `ALERT ↔ NOMINAL` every read has **no fixed
point** — there is no stable "situation" object — yet the debounce **launders that churn into a serene
committed NOMINAL**. That is exactly von Foerster's warning: an object reported *before the recursion
converged*. It is also the mesh's own recurring failure family — the silent-fallback / cry-wolf shape — in
a new dress: the calm label looks like a settled fact while, underneath, the observation never settled.

This is the failure the *debounce cannot see because the debounce is what causes it*: the more aggressively
you damp oscillation to stop cry-wolf, the more completely you hide that the underlying axis has no object.

## What I landed (report-only, additive)

A pure, clock-free classifier `eigen_classify RING COMMITTED` measuring the **eigen-residual**: over a short
ring of **raw** postures (the `*/15` edge cadence appends one per run; `--json`/fold **read** the tape,
never grow it), what fraction *differ* from the committed object, and how often do they *flip*:

- **`settled`** — residual 0: every recent raw read reconfirmed the committed object → **the eigenform is
  reached, the object is real.**
- **`converging`** — residual > 0 but one-sided drift toward a new value, not yet committed.
- **`churning`** — flips ≥ half the adjacent pairs: **no fixed point exists**; the calm committed label is a
  **debounce artifact** masking an unstable observation. *This is the reification the sidecar exists to expose.*
- **`cold`** — ring not yet filled (first runs).

Surfaced as `eigen_state` / `eigen_residual` in `--json` (dash consumers can now **refuse to trust a calm
posture whose object is churning**) and an `EIGENFORM[...]` line in the human fold. **Additive & verdict-
preserving:** it does not touch POSTURE or `.situation.state`, so — like the inclusive-disjunction sidecar
already in this file and unlike the held causal-emergence synergy rule — it needs no operator sign-off; it
only *describes* the temporal stability of the object the fold already commits.

**Test (RED-first, per doctrine — "a gate you have not seen FAIL is not a gate"):** four falsifiable
`eigen_classify` cases (settled / churning / converging / cold) plus an end-to-end assertion that `--edge`
**grows** the ring while `--json` **reads it without growing** (no double-count on dash refresh). Verified
the churning gate goes **RED** when its flips-≥-half branch is disabled (an alternating tape then misreads
as `converging`), GREEN when restored.

## Honest scope / non-claims

- The ring is **cold** until the `*/15` edge reflex fills it (`~2h` window at `SIT_EIGEN_K=8`) — the sidecar
  reports `cold`, not a faked `settled`. It becomes load-bearing only once the tape exists.
- It measures convergence of the **committed** posture's recursion, not of the underlying continuous axes
  (thermal, egress) — those have their own smoothing. This is deliberately the *object-level* eigenform.
- It is a **detector, not a fix**: a `churning` verdict says "this calm label has no stable object behind
  it", inviting a look at *why* the raw axis won't settle (a hollow/oscillating input — the family
  `mesh-stress` thermal flap already lives in). It does not change the debounce.

## Related coverage

`[[second-order-cybernetics-coverage]]` · sibling sidecars in the same organ: causal-emergence (held) and
D&G inclusive-disjunction (`concordance`/`spread`) · failure-family kin: the silent-fallback / cry-wolf
doctrine and `[[a-sub-axis-is-not-the-verdict]]`.
