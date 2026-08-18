# Live-literature review — biosemiotics: the DIALOGUE OF CONSTRAINTS, and the paradigm of choice `mesh-organ` destroyed

Date: 2026-08-18 · lane: genome (idea-queue LITERATURE task) · status: proposal, **uncommitted** (steward lands)

## Area & angle

Biosemiotics — sign and meaning in living systems — taken, as the task demands, through an
**operational mechanism**, not a philosophy. Searched the live journals rather than a fixed list:
Springer *Biosemiotics* (via the OpenAlex work index, 44 items since 2025-06, through 2026-08-14)
and *Sign Systems Studies* 53 (2025).

## What was already ours, and why it forced the search wider

Eleven biosemiotics landings exist here. The obvious 2026 candidates were **already spent**, and
saying so is part of the review:

- **"Measuring Meaning of Molecular Motifs"**, *Biosemiotics* (2026-02-24),
  https://doi.org/10.1007/s12304-026-09637-1 — Schneider's `Rsequence ≈ Rfrequency`. Landed
  2026-07-27 on the wake recognizer (`docs/reviews/biosemiotics-information-balance-wake-recognizer-2026-07-27.md`),
  same paper, same metric.
- **Pattee's epistemic cut / rate-independent symbolic constraint** — reached today from the other
  side (`docs/reviews/autopoiesis-measurement-control-complementarity-link-heal-2026-08-18.md`),
  which is also what closes out Lacková Bennett's "Toward a biosemiotics framework for AI:
  Folding and the dynamics of meaning", *Sign Systems Studies* 53(3/4): 444–463 (read in full).
- **Umwelt degeneracy** — ours since 2026-07-27, and the fresh
  https://doi.org/10.1007/s12304-026-09646-0 (pink salmon) is the same concept applied, not a new one.

Two genuinely fresh Springer items were **discarded for source quality, not content**:
"When Matter Loses Its Habit" (2026-06-19, territorial semiosis; *"regeneration should not be
understood as the recovery of a previous material state, but as the recomposition of the
conditions that enable coordinated interpretation and response"*) and "Neurophenomenological
Rehabilitation" (2026-08-14, recovery as **expansion** of the autopoietic system rather than
restoration of function). Both are paywalled behind Springer's bot challenge from this egress —
`link.springer.com` answers curl and WebFetch with a JS `Client Challenge` / 303, proxied and
direct alike — so I have **abstracts only**. Same rule the algedonic pass applied to MDPI 403 two
commits ago: an abstract is not a read. Both are logged here as **open leads**, not landed.

## The concept landed — the DIALOGUE OF CONSTRAINTS

**Source (open access, read in full, 24 pp.):** Rędzioch-Korkuz, Anna, **"(Re)conceptualizing
translation as a dynamic dialogue of constraints"**, *Sign Systems Studies* 53(3/4), 2025, 333–356.
https://doi.org/10.12697/SSS.2025.53.3-4.03 · PDF
https://ojs.utlib.ee/index.php/sss/article/download/26385/20075

Its lineage is squarely biosemiotic — Deacon's semiotic constraints (1997, 2011) and Marais's
absential (2023) — and its contribution is that it makes them **classificatory** rather than
gestural. Three claims are operational:

1. **A typology, and all of it applies at once.** Nine constraint types, one per element of the
   event (Table 1: meta-translational, ST-specific, system-based, medium-specific, translation
   problems, context-specific, ideology-based, audience-related, psychological/cognitive). The
   binding sentence: *"Irrespective of their actual potency, all the constraints operate in each
   translation event"* and *"if we want to understand a particular translation event, we should
   most likely attempt at reconstructing the **whole framework of constraints**, rather than focus
   on a detailed analysis of single aspects."*
2. **A constraint is a reduction of the option set.** Via Levý: constraints *"define the paradigm
   of choice and instructions, thus reducing the number of possibilities."*
3. **The absential half.** Via Deacon/Marais: constraints are *"both what is given and what could
   have been given"*, *"both 'what is not' and what 'could have been'"*. So the meaning of an
   outcome is the chosen option **together with** the options eliminated and what eliminated them.

Distinct from our prior biosemiotics work: code-duality is about fidelity across a channel;
interpretant is about the third term; index-vs-icon is about mode of reference. **None of them is
about the option set a sign-event selected from.**

## Why it is not already embodied

The nearest thing we have is the doctrine line *"fold with a max that NAMES its winner"*
(CLAUDE.md, and memory `max-fold-effaces-the-disjunction`). That is claim 2 half-done: name the
winner. **Claim 3 — name the losers and the constraint that killed each — is nowhere in the
genome.** Every router, picker and fuser here publishes its choice and discards its paradigm.

## The organ: `scripts/mesh-organ` (the capability router)

Routing a capability *is* a translation event in this paper's sense: a request crosses a semiotic
border (name → instance, here → there), and what survives is decided by several constraints acting
at once. `mesh-organ` already declares two constraint **types** — `cap-scope` (WHERE: bound vs
fungible) and `cap-allow` (WHO: which channel may invoke) — and adds a third implicitly (REACH: an
address in `~/.mesh/nodes`). It consulted them **one at a time and reported none of them**. The
whole record of a decision was one line:

```
[mesh-organ] tv → mesh-home (mesh-home@100.74.178.97)
```

Read that in a log a day later and there is no way to tell whether one node offered `tv` or four
did and three lost — nor which constraint lost them.

### What reconstructing the framework immediately exposed

Writing the mode surfaced a **live latent defect** that a single-aspect router could not show.
`cap_scope()` and `cap_allow()` declared `local … v` and then assigned it only inside
`is_cap_local "$nm" && v=…`. For every node with **no `~/.mesh/caps/<name>` file** — i.e. every
legacy `mesh-<tool>` organ, which is most of them — `v` stayed **unset**, and under this script's
`set -u` the expansion killed the command substitution outright. The caller read `""` and treated
it as `bound` / `unrestricted`. Measured before the fix, on the live fleet map:

```
scripts/mesh-organ: line 83: v: unbound variable
scripts/mesh-organ: line 112: v: unbound variable
  mesh-home                  <unrestricted>         local     eligible     <- WHERE column blank
```

The WHERE axis had not merely *defaulted* to bound — **it was never evaluated**, and because
nothing ever printed it, nothing could say so. That is the paper's claim 1 as a defect: the
router analysed single aspects, so a structurally dead axis was indistinguishable from a
consulted one. This is the sibling of `a-detector-leg-aimed-at-absent-hardware-is-indistinguishable-from-a-quiet-one`.

### The change (uncommitted, genome source only)

`scripts/mesh-organ`:

- **`mesh-organ --why <name>`** — read-only reconstruction of the whole framework: every offerer in
  the option set, each declared constraint's **verdict on it** (`where` / `who` / `reach`), the
  **decisive** constraint, and the **ruled out** list naming node *and* cause. WHO is evaluated
  against the real caller with the real rule, not echoed back from the header. It **never executes
  the capability** — explaining a place-bound actuator must not fire it.
- **The route path prints its paradigm too**, from data already computed (no extra ssh):
  `[mesh-organ] paradigm: X chosen from N offerer(s) by where(cap-scope=fungible)+first-offered;
  not chosen: Y Z (no retry on failure — mesh-organ --why <name>)`.
- **`cap_scope`/`cap_allow`: `v=""`** — the latent `set -u` kill above.
- **`--as <role>` is pre-parsed before the read-only modes.** `--as genome --why <cap>` previously
  fell through to the route parser and died as `unknown organ '--why'`.
- **`MESH_ORGANS_JSON`** — a fixture seam at the `mesh-organs --json` boundary, deliberately *not*
  at the offerer list, so the real parser stays in the loop (`injected-fixture-bypasses-the-parser`).
  A PATH stub cannot be used: the script prepends `$HOME/.local/bin` to PATH itself, so no stub dir
  can shadow the deployed `mesh-organs` (`path-stub-cannot-shadow-a-mesh-tool`).

### A finding the mode publishes rather than papers over

The header advertised *"many → fungible routes/failover"*. There is **no failover**: on multiple
fungible offerers the router takes `head -1` and execs, with no retry if that node's ssh fails.
`--why` now says so in the output rather than the routing policy being quietly rewritten — a
routing change is a substrate-shaped decision and does not belong in a literature pass.

### Artifact

```
$ mesh-organ --why tv
=== mesh-organ --why tv — the paradigm of choice ===
  caller: genome
  constraint types declared by this router: where(cap-scope) who(cap-allow) reach(~/.mesh/nodes address)
  option set: 2 offerer(s)
  NODE             WHERE     WHO                    REACH     VERDICT
  mesh-home        bound     <unrestricted>         local     eligible
  phaedra          bound     <unrestricted>         addressed eligible
  ruled out: none
  decisive: where(cap-scope=bound) with 2 offerers — the router REFUSES (exit 1) and makes you name the instance

$ mesh-organ tv          # the PREDICTION checked against the artifact
mesh-organ: 'tv' is place-bound and 2 nodes offer it — name the instance: tv@<node>
  tv@mesh-home
  tv@phaedra
rc=1
```

`--why` predicted the refusal, the exit code, and the instruction; the router produced exactly
that. (The live fleet dropped from 2 offerers to 1 between two runs of this same command while the
mode was being written — which is precisely why every branch gate below is fixture-driven.)

### Gates

`--test` green (16s). **10 mutants, 10 RED**, each with the correct assertion firing: `--why`
executes the cap · prints only the winner · always says fungible · empties the ruled-out list ·
drops the route paradigm line · reverts `v=""` · renders an empty option set as a table · drops
the runners-up names · who-gate always eligible · reach never rules out.

The first mutant sweep was **discarded as a false red**: all ten "failed" at rc=127, because the
tmp fence re-execs `"$0"` and the scratch copy was invoked as a bare `m.sh` not on PATH. The
assertions had not run at all. Re-run from an absolute path with the unmutated copy green at the
same path (`a-mutant-can-go-red-for-the-wrong-reason`).

Legs worth naming: the cap fixture **touches a marker file**, so "never executes" is proven by the
marker's absence rather than by an exit code; the fungible fixture gives `peer-a` a TEST-NET
address and leaves `peer-b` without one, because with no addressed peer "no runners-up" and
"runners-up suppressed" print identically; and one leg runs `--why` against the **live** fleet map,
since a fixture-only gate cannot cover the live path.

## Open leads (not landed — abstract only, Springer walled from this egress)

- Recovery/regeneration as **expansion or recomposition**, never restoration of a prior state
  (2026-06-19 territorial semiosis; 2026-08-14 neurophenomenological rehabilitation). If it holds
  up on a full read, it aims straight at our healers — `mesh-link-heal`, `mesh-revive`,
  `mesh-selfcare` all score success as *the axis returned to its prior value*, and none can score
  the outcome where the node acquires a **different** route to the same function.
- Zhou 2023's two senses of freedom (possibility vs access, inversely related),
  https://doi.org/10.1007/s12304-023-09548-5 — **no abstract exists** in Springer, OpenAlex,
  Semantic Scholar or PhilPapers; cited as context in our code-duality review, never read here.
