# Biosemiotics live review — CODE-DUALITY (analog action-code ↔ digital memory-code)

**Date:** 2026-07-29 · **Lane:** LITERATURE (live review), genome mind · **Area:** biosemiotics —
sign and meaning in living systems · **Angle:** cross-domain transfer to a distributed sensor mesh.

## The concept (named, cited)

**Code-duality** (Hoffmeyer & Emmeche): a living system is constituted by the interaction of **two
codes** — an **analog code** (the whole individual / phenotype: the organism *in action*, embedded in
its here-and-now context, continuous, un-transmissible) and a **digital code** (the genotype / DNA: a
discrete, context-free, reproducible *re-description* of the organism, stored for the future). In their
own words the minimal condition for life is *"at least two codes: one code for **action** (behaviour)
and one code for **memory** — the first necessarily analog, the second very probably digital."* Life
*alternates* between them: the digital code is passive memory that crosses the reproduction boundary;
each generation it is **re-interpreted** back into an analog organism to act, and the analog organism is
**re-described** back into digital form to persist. Neither code alone is alive.

A load-bearing property they stress: the digital code is **decoupled** from its referent — *"digital
codes allow for impossible messages, because there is no strict binding between the code and the message
it carries."* That decoupling is the **source of evolvability** (a description can vary independently of
any current organism) and, simultaneously, the source of **lethal transcription error** (a description
that corresponds to no viable organism).

**Sources (read live, web, 2026-07-29):**
- Hoffmeyer, J. & Emmeche, C. (1991) "Code-duality and the semiotics of nature." Full text (open):
  https://philpapers.org/archive/EMMCAT.pdf
- Hoffmeyer, J. "Code Duality Revisited." *S.E.E.D. Journal* (open):
  https://see.library.utoronto.ca/SEED/Vol2-1/Hoffmeyer/Hoffmeyer.htm
- Still-live in the current literature: Zhou, L. (2023) "More Constraints, More Freedom: Revisit
  Semiotic Scaffolding, Semiotic Freedom, and Semiotic Emergence." *Biosemiotics* 16:395–413,
  https://link.springer.com/article/10.1007/s12304-023-09548-5 — revisits the scaffolding/emergence
  cluster of which code-duality is the memory/action substrate. (The *Biosemiotics* journal reached
  Vol. 19 Issue 1, April 2026 — the seam is continuously published, not a fixed list.)

Not previously landed by this lane (frontier per `biosemiotics-review-coverage`: code-duality was on
the STILL-OPEN list). Distinct from the four prior biosemiotics landings (functional-cycle, information
balance, index-vs-icon, code-vs-interpretant).

## Cross-domain transfer — the mesh is already a code-dual system (the unifying finding)

The mesh has **convergently built code-duality three times** without naming it. Each tier is a digital
memory-code that must cross a "death" boundary and be re-interpreted into an analog action-code:

| tier | analog (action, live) | digital (memory, stored) | death boundary | re-description | re-interpretation | fidelity check |
|---|---|---|---|---|---|---|
| genome | deployed `~/.local/bin/mesh-*` running | `scripts/mesh-*` in the repo | redeploy | edit source | `cp scripts/* → bin/` | **`mesh-sync-tools`** (drift) ✓ |
| node   | the live running node | `~/.mesh-card` | reboot | `mesh-card --refresh` | card read on restore | **`--refresh` regenerates from live state** ✓ |
| mind   | the mind working in its pane | `~/.mesh/handoff/<win>.md` + `refs/wip/<win>` | `/clear` / engine restart | `mesh-handoff --snapshot` | SessionStart-hook `--restore` cat | **partial — see gap** |

Naming this unifies the handoff apparatus, the card, and the genome/sync-tools as one biological form:
digital memory-code + analog action-code + a re-interpretation across a death boundary. It also names
*why* the doctrine's `/compact`-is-retired / handoff-before-clear rule is not arbitrary — the handoff
**is** the genome that crosses the /clear death, and a bare /clear is reproduction with no memory-code.

## The ONE gap + concrete application (report-only, `scripts/mesh-handoff`)

Two of the three tiers **verify re-description fidelity**: `mesh-sync-tools` catches genome↔deployed
drift; `mesh-card --refresh` regenerates the card from live state. The **mind tier does not** — and
code-duality names exactly the failure it invites.

`mesh-handoff --snapshot` re-describes the analog pane into the digital handoff by an **extractive
grep** of the last N scrollback lines (`_extract_terse`). It has a **HOLLOW-GUARD** (`_snapshot_one`,
line ~193): if extraction yields nothing *and a prior handoff exists*, it preserves the prior rather
than clobber with noise. But that guard checks **non-emptiness, not fidelity** — and it only fires when
a prior file exists. The uncovered case, in code-duality terms an **"impossible message" crossing the
death boundary**:

> extraction is **hollow** (last N lines were shell furniture / an idle prompt, or the live thread
> scrolled above the window) **AND no prior handoff exists** **AND the worktree holds uncommitted work**
> (`refs/wip` dirty). The snapshot then writes a body whose work-state is literally *"no signal lines
> matched"* — a digital memory-code that names **none** of the analog work the tree is holding. The
> SessionStart hook faithfully re-interprets that hollow code into the next session, which wakes with no
> pointer to its own in-flight work. This is precisely the documented `2026-07-18` incident (the models
> mind /cleared mid fine-tune and **re-derived its loss log from scratch**).

This is the mesh's own recurring lesson **"non-empty is not correct"** ([[non-empty-is-not-correct]])
applied to the ONE channel that crosses death — and code-duality is the biosemiotic reason fidelity, not
non-emptiness, is what matters there.

**The application (implemented, report-only, uncommitted):** in `_snapshot_one`, when the extract is
hollow but `_git_wip_summary` reports uncommitted/unlanded work, the written handoff header now carries a
`# fidelity: LOW — …` comment line telling the re-interpreting session (and the operator) that this
digital re-description is **untrustworthy** and to recover from `refs/wip` + the pane scrollback, not
from this body. It **never blocks** the snapshot or the clear — the `refs/wip` commit is the reliable
digital code and remains the durable fallback; this only labels a known-lossy re-description as lossy.
Falsifiable: a furniture-only scrollback over a dirty worktree ⇒ `fidelity: LOW`; a scrollback naming a
`scripts/` path ⇒ no LOW line (extract carries the work). Wiring the `--test` assertion (RED-first on a
crafted hollow-over-dirty fixture) is the follow-on step, noted here so it is not mistaken for done.

**Antonym guard:** the fidelity line is a *comment* the restore-cat surfaces to a human/mind — it is
never fused into a verdict or exit code, and it must never gate the clear (that would strand work at the
very boundary it is meant to protect). Report-only, like the prior biosemiotics landings.
