# Live-literature review — biosemiotics: INCENTIVE SALIENCE ("wanting" ≠ "liking") as the missing outcome axis of `mesh-needs`

Date: 2026-08-18 · lane: genome (idea-queue LITERATURE task) · status: implemented, uncommitted (steward lands from the tree)

## Area & angle

Biosemiotics — sign and meaning in living systems — from a **recent result, sampled off the live feed**,
not a fixed reading list. Method (reproducible): the Springer *Biosemiotics* journal is walled to
WebFetch/curl (303 → `idp.springer.com`), so the current issue was enumerated through **Crossref**
(`api.crossref.org/journals/1875-1350/works?filter=from-pub-date:2025-06-01&sort=published`) and
abstracts pulled from **OpenAlex** (`api.openalex.org/works/doi:…`). That yields the genuinely live
front: 44 articles since 2025-06, newest 2026-08-14.

Candidates read and set aside, with the reason:

- *Measuring Meaning of Molecular Motifs* (doi:10.1007/s12304-026-09637-1) — **already ours**: Schneider's
  R<sub>sequence</sub>≈R<sub>frequency</sub> is `docs/reviews/biosemiotics-information-balance-wake-recognizer-2026-07-27.md`.
- *How Do Organisms Measure Spacetime? Measurement by the Insider Players* (doi:10.1007/s12304-025-09621-1) —
  E-series (second-person, coadjusted) vs B-series (clock) time. Overlaps
  `biosemiotics-interactive-sign-claim-liveness-2026-07-30.md` ("a claim's life is its interaction cycle, not its age").
- *Umwelt Degeneracy … Pink Salmon* (doi:10.1007/s12304-026-09646-0) — ours since `umwelt-degeneracy-inert-axis-2026-07-27.md`.
- *Information is Non-physical at both the Micro and Macro Levels* (doi:10.1007/s12304-026-09642-4) —
  metaphysical claim, no mesh-checkable mechanism. Discarded.
- *Ultraviolet "Umwelten": … Semantic Organs* (doi:10.1007/s12304-026-09648-y) — a UV-photography protocol;
  no UV organ on this node. Discarded (hardware absent).

## The concept we did NOT embody: incentive salience — wanting is dissociable from liking

Source (live, 2026):
**"Motivation and Meaning: A Biosemiotic Perspective"**, *Biosemiotics* (2026),
doi:[10.1007/s12304-025-09634-w](https://doi.org/10.1007/s12304-025-09634-w) — abstract via OpenAlex.

The paper folds **Berridge's incentive-salience model** into the Peircean triad, proposing a revised
schema "in which the motivated subject functions simultaneously as **interpretant and agent**", motivation
being "a relational process mediating between agents, **cues**, and ecological affordances" — an
*axiological* dynamic, a felt orientation toward value, shaped by semiotic scaffolding. It closes with
"implications for … the evaluation of **artificial systems that simulate, but do not instantiate,
motivational dynamics**."

The load-bearing import is Berridge's dissociation:

> **"Wanting"** (cue-triggered incentive salience — the pull to pursue) and **"liking"** (the hedonic/outcome
> evaluation of what pursuit delivers) are **separable systems**. Salience attaches to the **CUE**, not to
> the result — so an organism can want harder and harder for a cue whose outcome has stopped delivering.

Wanting without liking is not motivation working. It is motivation running **open-loop**.

Distinct from every prior biosemiotics landing here (11 reviews): those are about *sign reading*
(code duality, index vs icon, functional-cycle closure, interpretant, information balance, interactive
sign). This is about the **valuation half** — whether pursuing an object ever changed anything — which
nothing in the genome measures.

## Where we are exactly that (measured, not argued)

`scripts/mesh-needs` is the autopoiesis lane's goal source. `collect()` reads three deficit **cues**
(`mesh-verify-table` ✗ · `mesh-reflex-health` STALE · `mesh-reflex-decay` candidate) and mints a goal per
cue, every 15 minutes, forever. It already measures **how much it wants** — `--balance` reports the
explore/exploit poles and a demand density. Nothing anywhere asked the liking question: **did pursuing
this object ever clear it?**

Live artifact, this node's `~/.mesh/needs.log` (2009 lines, 2026-07-14 → 2026-08-18):

```
122 injection events over 12 distinct objects  →  93% are re-mints
  44  lan-newdevice        2026-07-29 .. 2026-08-16   (19 days, at the full */15 cadence)
  35  mesh-rns-offgrid     2026-07-31 (single day)
  23  mesh-phone-beacon2   2026-07-31
  12  mesh-skill-ls        2026-07-31
```

The deficit never cleared and the wanting never dropped. Worse, `--balance`'s demand-tracking verdict
reads that re-firing as **demand**, and an unsatisfiable cue therefore scores `TRACKING-HIGH` =
*"RR-CORRECT tuning, NOT a collapse"*. **The pathology was certified as health** — the same shape as
"a green `--test` on a reflex that was never wired", one level up: a green *posture verdict* on a lane
that is pursuing nothing that moves.

**Second, mechanical cause found while implementing** (a real bug, not a metaphor): the dedup token was
`grep -oE 'mesh-[a-z-]+'`, and on an empty match the guard was **skipped entirely** rather than falling
back — so any object whose name is not `mesh-`-prefixed (a reflex named `lan-newdevice`) re-minted on
**every single run**, even while its item still sat in the queue. That is precisely the queue-runaway
this file's own header claims to have solved. An absence-guard below a fuzzy read, again.

## The fix — a liking axis in `scripts/mesh-needs` (implemented, uncommitted)

- **`_need_obj`** — THE one canonicalization of "what is wanted", used by the dedup **and** the count, so
  the key that suppresses is the key that is counted. Handles non-`mesh-*` objects (`scheduled reflex X`).
- **`_liking_scan`** — per-object re-mint counts over a log window (read-only, pure).
- **`_liking_verdict`** — `WANTING-WITHOUT-LIKING` / `PARTIAL-PIN` / `LIKING-OK` / `INSUFFICIENT`, keyed on
  the **pinned share** of demand (how much of the wanting is the same object re-fired).
- **`_satiation <obj>`** → `mint | escalate | suppress`. At `K` re-mints (default 4,
  `MESH_NEEDS_PIN_K`) an object is **cue-pinned**: the reflex stops re-minting the same goal and mints a
  **different** one once — *the fix CLASS is wrong, not the effort: diagnose why it never clears / decay it /
  mute it with a stated reason* — then suppresses further re-mints. Priority 4 (productive forage) is
  **exempt**: deliberate repetition is its whole point, and it is the explore pole this guard must not amputate.
- **Suppression is LOUD** — its own log verb (`cue-pinned SUPPRESSED -> …`) plus a board line every run it
  fires. A guard that quietly eats goals is indistinguishable from a dead reflex.
- **`--balance` gains the liking report** beside the wanting report, and says out loud that the
  demand-track line above it will call a pinned lane healthy.

Live output of the new axis (window widened to cover the history):

```
liking (last 2100 log lines): 122 mint(s) over 12 distinct object(s) · cue-pinned(>=4x)=4 · pinned share=93% · WANTING-WITHOUT-LIKING
    pinned: lan-newdevice                44 re-mint(s)
    pinned: mesh-rns-offgrid             35 re-mint(s)
    pinned: mesh-phone-beacon2           23 re-mint(s)
    pinned: mesh-skill-ls                12 re-mint(s)
    verdict: WANTING WITHOUT LIKING — most demand is the SAME object(s) re-fired, not deficits clearing.
```

## Gates — seen RED, then green

`--test` gains five legs, one of them **end-to-end through the real inject path** (only the external
organs are stubbed: a wrapper's test must exercise the thing it wraps). It plants a pinned history + a
stubbed `mesh-reflex-health` emitting `STALE lan-newdevice`, runs the script as a child with a redirected
`HOME`, and asserts the queue: escalation on the first run, **queue empty on the second with the queue
cleared first**, so dedup cannot be what stopped it.

Six mutants, each red for its own reason (`bash mesh-needs --test`, from a scratch copy):

| mutant | verdict |
|---|---|
| guard disabled (`if false`) | FAIL — pinned object re-minted the same `REFLEX REPAIR` goal (**this is the pre-fix behaviour, reproduced**) |
| `_need_obj` reverted to the mesh-only token | FAIL — `'mesh-foo scheduled mesh-bar'` |
| suppression log line removed | FAIL — "suppression was SILENT" |
| `WANTING-WITHOUT-LIKING` branch deleted | FAIL — verdict falls to `PARTIAL-PIN` |
| escalation not recorded | FAIL — not in needs.log |
| `PIN_K` raised to 99999 | FAIL — verdict `INSUFFICIENT` |

Then green: `smoke-test: ok`.

## What this does NOT claim

- The four pinned objects are not thereby diagnosed. The guard says *the fix class is wrong*, it does not
  say which of (diagnose / decay / mute) is right — that is the escalated goal's job, done by a mind.
- Pin memory is a **window** (`MESH_NEEDS_LIKING_WINDOW`, default 500 log lines ≈ 5 days at */15). A
  deficit re-minted slower than the window ages out and re-mints legitimately. That is deliberate — a
  permanent blacklist would be the opposite failure — but it means the axis reports a window, not a
  lifetime (`a-senses-coverage-is-window-over-cadence`).
- `93%` is a reading of the current log, which rotates. Re-derive with `mesh-needs --balance`; never quote it.

## Files

- `scripts/mesh-needs` (+~120 lines: doctrine block, `_need_obj`/`_liking_scan`/`_liking_verdict`/`_satiation`,
  `--balance` liking report, satiation guard in the inject loop, 5 test legs) — **uncommitted**.

## Sources

- Motivation and Meaning: A Biosemiotic Perspective — *Biosemiotics* (2026) — https://doi.org/10.1007/s12304-025-09634-w
- Measuring Meaning of Molecular Motifs — https://doi.org/10.1007/s12304-026-09637-1
- How Do Organisms Measure Spacetime? Measurement by the Insider Players — https://doi.org/10.1007/s12304-025-09621-1
- Ultraviolet "Umwelten": Exploring Semantic Organs Beyond the Visible Spectrum — https://doi.org/10.1007/s12304-026-09648-y
- Information is Non-physical at both the Micro and Macro Levels — https://doi.org/10.1007/s12304-026-09642-4
- Live feed enumerated via Crossref (ISSN 1875-1350) + OpenAlex; Springer article pages are walled from this node.
