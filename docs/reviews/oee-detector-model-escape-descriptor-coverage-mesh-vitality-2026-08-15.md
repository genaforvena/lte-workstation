# ALife / open-ended evolution — live review: THE DETECTOR'S OWN BLIND SPOT

**Area:** artificial life & open-ended evolution, angle = a known **CRITIQUE / failure mode** of the area.
**Date:** 2026-08-15. **Window:** genome (mesh-home). **Status:** landed, uncommitted in the tree.
**Tool:** `scripts/mesh-vitality` — new `model_escape()` sign (report-only, in the standard report line).

---

## I. The critique landed on

**Susan Stepney & Simon Hickinbotham, "On the Open-Endedness of Detecting Open-Endedness",
*Artificial Life* **30**(3):390–416 (2024)** — the journal's OEE special issue (editorial introduction
doi:`10.1162/artl_e_00445`). Found via WebSearch 2026-08-15; the MIT Press full text is 403 to us, so the
abstract/claims below are quoted from the publisher listing, PubMed, and the Semantic Scholar record.

Their thesis, aimed squarely at every quantitative OEE metric:

> an open-ended system will eventually move **outside its current model of behavior**, and hence outside
> any measure based on that model

and therefore

> establishing open-endedness is a case of continually developing **system-specific** measures for
> detecting the continually arising open-ended novelties

— results are reported using **system-generic measures first, then system-specific measures**, and "a
process of analysis, starting with system-generic measures but going on to system-specific measures, will
be needed wherever the phenomenon of open-endedness is involved". They demonstrate it over eight long runs
of the spatial Stringmol automata chemistry, and conclude the focus should be on the **mechanisms** of
open-endedness, not on quantifying it. The community summary of the position is blunter still: *the desire
for a single quantitative measure of open-endedness is a dead end.*

**The line is live.** The same caveat is restated at the current end of it by the Ω paper this repo already
implements — López-Díaz, Rivera-Torres, Febres & Gershenson, arXiv:2512.15534, whose interpretation
"remains conditional on the chosen state variables, phenotype map, system boundary, and timescale".

The failure mode, stated plainly: **a fixed measure goes blind at exactly the moment the system does
something genuinely new, and it goes blind SILENTLY** — still emitting a confident number about the part
it can still see.

---

## II. The critique lands on this repo, hard

Every population-based sign in `scripts/mesh-vitality` is computed over **one fixed descriptor**:

```python
def is_tool(p):
    b = p.split('/')[-1]
    return p.startswith('scripts/') and (b.startswith('mesh-') or b.startswith('test-')) and '.' not in b
```

`ecology_potential` · `nfds_coefficient` · `mls_conflict` · `evo_activity` · `inheritance_mu` ·
`heaps_beta` · `action_occupancy` · `omega_cycle` · `rhizome_index` · `phylum_coherence` ·
`loop_closure_frac` · `assembly_signature` — all of them. That descriptor **is** this file's model of what
a component of the mesh *is*.

**Not one sign reports what fraction of the mesh's self-production that model accounts for. Each silently
assumes it is 1.0.** That assumption is the measurable form of Stepney & Hickinbotham's critique, and it is
the one thing none of those functions can check about itself. `evo_activity` has a control run — but the
shadow shares the same descriptor (it redistributes the same tools). `heaps_beta` counts tool creations
against commits — the numerator is modelled by construction.

---

## III. The transfer — `model_escape()`, a META-sign

It does not measure the mesh. **It measures the panel's own blindness.**

- Over the repo's full history, take the **BIRTH** (first-ever appearance) of every path.
- Bucket each into a coarse artifact **KIND** (`scripts/mesh-*` · `docs/reviews` · `docs/` ·
  `scripts/other` · top-level dir · `(root)`).
- **coverage** = modelled births / all births, per window (`ME_WIN_D`, default 60d), against the prior
  window of the same length.
- **Births, not edits** — because the signs that matter here are birth-based (`evo_activity`'s
  new-activity, `mls_conflict`'s newborns, `inheritance_mu`, `heaps_beta`). The two **diverge**, and the
  divergence is itself the finding: an established tool is edited many times, while a whole new artifact
  KIND is created once and rarely re-touched, so an edit-share read *flatters the model*.
- Verdicts: **COVERED** · **EXTENDING** (a KIND whose first-ever instance falls in this window — the model
  needed a new bin; Stepney's "moved outside the model", caught as it happens) · **ESCAPED** (coverage
  below `ME_FLOOR`, default 0.70 — the panel above is reporting confidently about a *minority* of what the
  mesh makes).
- The blind kinds are **named with their shares**, because the paper's prescription is to go system-specific
  next and a mind cannot do that without an address.

### Live result (mesh-home, 2026-08-15)

```
model_escape = ESCAPED:0.55(prior 0.71,Δ-0.16;blind=docs/reviews 0.20,scripts/other 0.18;
                            newkind=caps.example/,docs/reviews)
```

**45% of the mesh's new production over the last 60 days is invisible to its entire open-endedness panel**,
and coverage fell from 0.71 the window before. The single largest blind class is `docs/reviews` at 20% of
all births — the mesh's fastest-growing product class, **first created 39 days ago**, with no bin in any
vital sign. (`mesh-ideate`'s `viability_tally` / `evolvability_tally` do read `docs/reviews`; the
*open-endedness panel* in `mesh-vitality` does not.)

The edit-share view says the opposite and is the trap: by **edits**, `scripts/mesh-*` coverage is 82.5%
and *rising* (78.5% the prior window), because the modelled population is where the churn is. Births 0.55
falling, edits 0.83 rising — same repo, same windows. Only the birth read matches what the birth-based
signs actually consume.

---

## IV. RED-first — six mutants seen fail, from a scratch copy

| mutant | effect on the fixtures | result |
|---|---|---|
| invert `is_tool` inside `kind()` | EXTENDING collapses | **RED** ✓ |
| invert `is_tool` inside the coverage ratio | covered → `ESCAPED:0.04`; births fixture → `COVERED:1.00` | **RED** ✓ |
| drop the first-ever-KIND check | EXTENDING → COVERED | **RED** ✓ |
| `births_of` keeps the LAST appearance (edit tally) | births fixture flips `ESCAPED:0.00` → `COVERED:0.75` | **RED** ✓ |
| make `ESCAPED` unreachable | escaped fixture → COVERED | **RED** ✓ |
| remove the minimum-births `n/a` guard | thin fixture manufactures a verdict from 3 births | **RED** ✓ |

Five synthetic fixtures, no git and no clock: (1) COVERED, (2) ESCAPED at exactly 0.50 with the blind kind
named, (3) EXTENDING with a brand-new `uxn/` kind, (4) **births-not-edits** — 120 tools born long ago and
all re-edited inside the window against 40 unmodelled births, which reads `ESCAPED:0.00` under births and
`COVERED:0.75` under an edit tally, and (5) a 3-birth window → `n/a`. No single hardcoded verdict satisfies
all five.

The births-vs-edits choice is gated by a **tag flip**, not a digit — the first version of that fixture
moved only `ESCAPED:0.00 → ESCAPED:0.02` and was strengthened before landing. `births_of()` is a named
function rather than inlined in the git loop for exactly that reason: a fixture starting from an
already-built births map could not tell births from edits at all.

`mesh-vitality --test`: **green**, 3.2s.

---

## V. Honest boundaries (the point, not omissions)

1. **An unmodelled birth is not proof of open-ended innovation.** It can be routine doc churn. The sign
   says "your model covers X% of new production", never "novelty happened". Distinguishing the two is
   precisely the system-specific work the paper says cannot be automated away; this sign's only job is to
   say **when** and **where** to do it.
2. **It cannot detect novelty inside a kind it already has a bin for.** A genuinely new sort of `mesh-*`
   tool reads as covered. This is not a fixable oversight — it is the critique applying to the detector
   itself, which is why it is called `model_escape` and why the verdict is a prompt for a reading, not a
   gate.
3. **Report-only.** No `[vitality-low]` edge, no exit code — same posture as `heaps_beta` / `omega_cycle`.
4. **Not gated:** that this file's `is_tool` copy stays in step with `evo_activity`'s and
   `mls_conflict`'s. Nothing asserts the three texts are identical, and a drift would have this sign
   reporting coverage for a model no other function computes over. Stated in the source.

## VI. Not taken

Stepney & Hickinbotham's actual prescription — *build the system-specific measure* for whatever the
generic one lost — is by construction not landable as a general mechanism; it is the work the ESCAPED
verdict now points at. The obvious first instance, given the live reading: a `docs/reviews` population for
the birth-based signs (ecology / evo_activity / mls over review artifacts as components, not just tools).
That is a real piece of work with its own descriptor choices, and belongs to the steward, not to this
landing.

---

Cite: Stepney & Hickinbotham, *Artificial Life* **30**(3):390–416 (2024), OEE special issue
(doi:10.1162/artl_e_00445) · López-Díaz, Rivera-Torres, Febres & Gershenson, arXiv:2512.15534.
