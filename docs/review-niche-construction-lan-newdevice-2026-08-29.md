# Literature review — niche construction & the extended phenotype, landed on `scripts/mesh-lan-newdevice`

**Arm:** treated (assigned)
**Date:** 2026-08-29
**Target organ:** `scripts/mesh-lan-newdevice` — assigned by coin at p=0.20, drawn uniformly from the
561 never-reviewed tools in the lane's denominator. Not chosen; not retargeted.
**Area:** niche construction / extended phenotype, from the angle of a concrete metric.

## The concept we did not embody

**μ — the persistence coefficient of the constructed resource, and its cumulative weight
M₁ = Σ_{τ=1..n} μ^τ.**

From Fogarty, L. & Wade, M.J., *"Niche construction in quantitative traits: heritability and response
to selection"*, **Proc. R. Soc. B 289:20220401 (2022)**, equation 3.1:

    z₁(t) = a₁(t) + e₁(t) + Ψ Σᵢ Σ_{τ=0..n} μ^τ · z₂ᵢ(t−τ)

μ discounts how far into the future a modification the organism made to its own environment keeps
acting on it. The paper's central result is not the equation but its consequence: **when the
constructed environment is itself heritable, the definitions of heritability that are numerically
identical without niche construction come apart** — their h₁², h₂², h₃² — and only h₃² carries the
ecological-inheritance term M₁. You must say *which* definition you mean, because they no longer
agree.

Read via PMC (open access): https://pmc.ncbi.nlm.nih.gov/articles/PMC9156914/

The paired experimental tradition for the same idea is the two-phase **plant–soil feedback**
conditioning design and Bever's interaction coefficient Iₛ (home soil vs away soil) — a live,
continuously-published literature; see the 2025 temporal-dimension work in *J. Ecology*
(https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/1365-2745.14435). It supplied the
framing (measure an organism against the substrate *it itself conditioned*) but μ is the part that
transplants cleanly, so μ is what landed.

## Why it applies to this organ specifically

`mesh-lan-newdevice` is an intrusion sense that **builds its own perceptual environment**: the MAC
baseline `~/.mesh/.lan-known-macs`, plus `.lan-known-pairs`. That file is ecological inheritance in
the literal sense — each run inherits what previous runs decided to trust, and what it inherits
determines what it can still perceive.

**In this organ μ = 1 exactly, and it is structural, not measured.** Verified by reading every write
path: `--allow` appends, a `PROMOTE` in `track_unconfirmed` appends, `heal_torn_promote` touches only
the tracking file, `torn_promotes` reads only. **No code path removes a single entry from the
baseline.** `--forget` deletes the whole file, which is an operator decision, not decay.

So M₁ grows without bound. The trusted set is a one-way ratchet that can only converge on the whole
LAN — and this is an **edge-triggered alarm**, so the terminal state of that convergence is silence,
which is exactly what "no intrusion" looks like.

The file already documents this failure on the **space** axis: a VM proxied behind a baselined MAC
was *"structurally un-alertable, forever."* μ=1 re-creates the identical failure on the **time**
axis — a device seen 30 times in April is still trusted in August with nothing corroborating it — and
before this review nothing in the tool measured it.

What the literature adds beyond our own doctrine: CLAUDE.md already says *a saturated LEVEL is not a
state — publish the two opposing RATES*. Fogarty & Wade add the part that rule does not contain —
that under a heritable constructed environment the **definitions themselves diverge**. "Known device"
has three non-equivalent readings here, and every decision in the file used only the first:

| reading | meaning | used by the code? |
|---|---|---|
| **baselined** | present in `$KNOWN` | yes — every trust decision |
| **present** | baselined *and* in the current read | no |
| **corroborated** | baselined *and* actually seen inside a window | no |

## What landed

`scripts/mesh-lan-newdevice` (uncommitted, in-tree):

- **`--niche`** — the constructed-niche reading, publishing all three definitions plus `na`,
  coverage, and the structural constants: `mu=1.000 v_dec=0/day residence=unbounded`. `v_dec` is
  stated with its reason so it can never be misread as a measured quiet interval.
- **`record_seen`** — a last-seen ledger (`~/.mesh/.lan-lastseen`), stamped from the same observation
  the alarm path uses. It feeds `--niche` and nothing else, so a corrupt or absent ledger cannot
  change whether a device alerts.
- **`niche_measure`** — pure, so every branch is asserted.

Three honesty properties, each gated:

1. **A young ledger abstains.** Coverage is `partial:<age>/<window>` until the ledger has run a full
   window, and the verdict is `UNKNOWN` — the ledger's silence is amnesia, not a device's absence.
2. **`na` is typed apart from `inherited`.** A baselined MAC the ledger has never seen is *unknown*,
   never *observed-absent*, and never folded into the accusing bucket.
3. **`present=na` when no observation was supplied.** `--niche` is a pure local read; `present=0`
   there would claim no baselined device is on the LAN — a strong claim minted from an absent
   measurement.

Four words, four remedies: `UNKNOWN` (wait) · `RATCHETED` (review those entries) ·
`UNDER-OBSERVED` (nothing accounts for an entry yet) · `CORROBORATED`.

**Gate: 15 new assertions, 10 mutants driven red, control green** — including folding `na` into
`inherited`, dropping the coverage abstention, re-minting the birth stamp every run (which would
make coverage permanently immature while looking well-behaved), refreshing MACs the run did not
observe (self-granted corroboration), and letting `na` wear the clean word.

## A defect this review introduced, and caught

Adding a state file to a tool put it **outside the override set the existing `--test` harness already
carried**. `run_status()` sandboxed `KNOWN`, `PAIRS`, `UNCONFIRMED` and `BEAT` — but not `LASTSEEN`,
because `LASTSEEN` did not exist when that list was written. Nothing announced the omission. The
suite's fixture MACs are **real LAN MACs reused as fixtures** (`7c:c3:a1:a5:20:d7`,
`80:56:f2:a7:90:61`), so running `--test` wrote them into the live ledger at 00:39:07Z, where
`--niche` would have read them back as genuine corroboration of devices nothing had observed — the
measurement forging its own evidence, in the tool built to detect trust with nothing behind it.

Fixed three ways: `LASTSEEN` added to the harness overrides; the polluted ledger deleted; and a guard
arm that snapshots the real path and fails if the suite moved it. **The guard was wrong first** — put
with the niche arms it sat *downstream* of the `run_status()` arms that cause the leak, so it measured
only its own section and passed green while the mutant demonstrably leaked. It is now taken at the top
of the suite, before any arm runs, and driven red from there.
[[a-new-state-file-is-outside-the-suites-sandbox-env]]

## The live reading on this node

    niche: state=UNKNOWN baselined=13 present=na corroborated=0 inherited=0 na=13
           coverage=unknown(no-ledger) window=14d mu=1.000 v_dec=0/day residence=unbounded

13 baselined MACs and **not one is corroborated by anything**, correctly rendered `na=13` /
`UNKNOWN` rather than as 13 ghosts — the ledger does not exist yet, so its silence is amnesia, not
absence. The reading becomes answerable 14 days after the steward lands and deploys this, which is
the finding's own discipline applied to itself.

What the number will say when it matures is not predicted here. The claim of this review is only
that **the quantity was previously unmeasurable**, and that μ=1 with `v_dec=0` is a structural fact
of the code, read off every write path, not an estimate.

## Not done on purpose

Nothing **demotes**. The file's own `torn_promotes` comment argues that pulling a MAC out of the
baseline re-arms an alarm on an unidentified device and is a human decision, not a cleanup side
effect. That argument holds exactly as well for a stale entry, so this review adds the
**measurement** and no actuator. Giving μ a value below 1 — an actual decay — is a security posture
change and belongs to the operator, not to a literature review.
