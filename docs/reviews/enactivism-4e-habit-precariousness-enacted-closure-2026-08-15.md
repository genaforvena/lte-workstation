# Enactivism & 4E — live review: PRECARIOUSNESS as the criterion for a habit relation

**Area:** enactivism & 4E cognition, entered from the angle the task names — *a foundational idea we
may have MISread or applied too loosely*. **Date:** 2026-08-15. **Window:** genome (mesh-home).
**Status:** landed, uncommitted in the tree. **Tool:** `scripts/mesh-closure` — new `--enacted` axis
(report-only, on-demand).

---

## I. The literature landed on

**Susana Ramírez-Vizcaya, "Extending the enactive concept of habit: from sensorimotor schemes to
regional identities", *Synthese* **206**:137 (2025), doi:`10.1007/s11229-025-05237-7`** — open
access, found by WebSearch and **read** 2026-08-15 (the Springer PDF, pp. 1–6 in full).

Her subject is the technical definition of habit in **Di Paolo, Buhrmann & Barandiaran,
*Sensorimotor Life: An Enactive Proposal* (OUP 2017)**, which she quotes and unpacks. The definition
is three words and every one of them is load-bearing:

> "*self-sustaining precarious sensorimotor schemes*" (Di Paolo et al. 2017, p. 144)

**PRECARIOUS**, verbatim as she glosses it:

> a sensorimotor scheme is habitual "when the elements that support it (muscular dispositions, neural
> connectivity patterns, spatial arrangement of objects and tools, etc.) **depend for their structural
> stability on the exercise of the scheme**" (p. 144)

**SELF-SUSTAINING** is the return half of the same loop — the lawn-path image the enactive tradition
inherits from Ravaisson:

> repeated walking "across a lawn in a park" gradually creates a path where the grass stops growing,
> which "in turn, encourages people to keep walking along it" — so "**a habit 'calls' for its exercise
> and its exercise in turn reinforces its durability**" (p. 144)

And the schemes are not isolated: the theory is "not based on an aggregation of individually
self-sustaining habits, but on a network of *mutually interweaving* schemes" — habits are
"related to a plastic equilibrium that involves the totality of the organism, including other habits"
(Barandiaran & Di Paolo 2014, quoted p. 6). Companion mechanism (same author, read for the
competition vocabulary): **Ramírez-Vizcaya & Froese, Front. Psychol. 10:301 (2019),
doi:`10.3389/fpsyg.2019.00301`** — "habits influence the viability of other habits, either preventing
them to occur or increasing the chance of its persistence."

Live, not a museum piece: this is a 2025 *Synthese* article extending a 2017 book, in a conversation
still running in 2026 (Dave Ward, "What Is Enactivism?", *Adaptive Behavior* 2026,
doi:`10.1177/10597123261450094`; Liao, *Critical 4E Cognitive Science*, Philosophy Compass 2026,
doi:`10.1111/phc3.70075`).

## II. The misread — ours, and it is structural

The mesh already reasons in terms of habit-like structures: reflexes, their cadences, their
dependence on one another. `scripts/mesh-closure` (landed 2026-07-28 from the autopoiesis lane) is
the tool that formalises the *network* half: it builds the process-enablement graph over the wired
reflex set and reports `CORE` / `SOURCE` / `PERIPHERAL` / `LOOP`.

Its enablement edge is defined — the file says so plainly — as:

> "B's source *consumes* A's product, approximated conservatively by **B's source invokes `mesh-A`**"

and implemented as `grep -oE 'mesh-[a-z0-9-]+' "$f"` over the **whole file** (`:252` before this
change). A `mesh-A` token in a comment block, a usage line, a doctrine header, or a `--test` fixture
counts as B depending on A.

Hold that against the definition. A mention in a comment is a support **whose structural stability
does not depend on the exercise of the scheme at all**: nobody has to run anything for the sentence
to stay in the file, and no run wears a path through it. Under the enactive criterion it is not a
weak habit relation — it is the *complement* of one. The mesh has been calling the mention a
dependency, and every closure number it has ever printed (CORE, LOOPS, and by subtraction
PERIPHERAL) is computed on that count. This is the mesh's own standing rule met in a new place —
*source text is never behaviour*, and *a name-only source gate passes on a comment* — but the
literature is what says the fix is not cosmetic: **closure over unexercised edges is not closure.**

Four candidate readings were checked against the genome first and **discarded as already embodied**:
the *network of mutually interweaving schemes* (that is `mesh-closure`'s graph, already there);
*habits compete / influence each other's viability* (`mesh-dispatch` cross-inhibition, the
response-threshold division of labour); *a scheme that never fires* (`mesh-reflex-health` mtime
aging, `mesh-doctor`'s orphan check); *declared vs enacted cadence* (landed this morning as
`mesh-reflex-health --routine-fit`). What survived is the one above, and it lands on the graph, not
on any single reflex.

## III. What was built

`scripts/mesh-closure --enacted` (new; report-only, advisory, never prunes). It recomputes **the same
graph** over three mention populations and diffs them:

| population | what counts as a mention |
|---|---|
| `declared` | any `mesh-*` token anywhere in B's source (what the tool always did) |
| `code` | tokens outside **full-line** comments |
| `live` | also outside a **test-harness function body** |

An edge in `declared` but not in `live` is **UNEXERCISED** — `PROSE-only` (documentation) or
`TEST-only` (only the gate walks it). The enacted graph is a strict subgraph, so classes can only
weaken: a reflex that was `CORE` on prose alone falls to `PERIPHERAL`, and a `LOOP` with one
unexercised leg is not a closed constraint pair. **DEMOTED** is the load-bearing output.

Implementation: one new `mention_tokens()` filter + a `site_mode` parameter threaded into the
existing `analyze()`, so the enacted classification is produced by **the same classifier** as the
declared one (no second copy of the CORE/SOURCE/PERIPHERAL rules to drift).

**Conservative in one direction, by construction** — every bound makes DEMOTED a *lower* bound:

- only a line that is **entirely** a comment is prose; `x=1  # like mesh-foo` counts as live code, so
  a live edge can never be miscounted as unexercised;
- a test body is recognised only via a **named** function whose name has an exact `_`-separated
  component `test|tests|testing|smoke|selftest` (the genome's `do_test`/`_test`/`smoke_test`/
  `run_test`/`selftest`/`ts_selftest` family). A tool inlining its gate under a `--test)` case branch
  keeps those mentions LIVE → `TEST-only` is under-counted. `parse_latest` contains "test" as a
  substring and is deliberately not matched — a substring rule would delete real edges and inflate
  demotions, the wrong direction;
- **a live mention is still only a mention.** It proves the token sits on a line that *could* run,
  never that it ran. This axis narrows the over-count; it does not remove it. The residue needs
  runtime tracing, which no reflex here carries — stated, not hidden;
- the graph reads `scripts/` only, so a tool consumed by a cron **command chain**
  (`mesh-load-gate x 11 && mesh-y`) has a real consumer no axis of this tool scans. Those demotions
  are **marked `[cron-chained]`, never suppressed** — an unmarked demotion is the strong claim, a
  marked one is a caveat for the reader.

## IV. Live finding (genome + `~/.mesh/reflexes.cron`, 2026-08-15)

```
edges (both ends wired+present): declared=757  LIVE=185  PROSE-only=567  TEST-only=5
UNEXERCISED=572 (75% of the declared graph — closure held by text no run ever walks)
class shift (declared -> enacted):
  CORE 182 -> 105    SOURCE 5 -> 14    PERIPHERAL 36 -> 104    UNKNOWN 2 -> 2
  LOOPS 90 -> 6
DEMOTED=79 (5 [cron-chained], 74 unmarked)
```

**Three quarters of the mesh's enablement graph is prose.** The headline the closure axis has been
reporting since July — *"the mesh is mostly closed, 82 mutual-dependence loops, this is a real
self-maintaining organization, not a pipeline"* — rests almost entirely on edges nothing exercises.
Six closed constraint pairs survive the exercise test:

```
mesh-chat-sync <-> mesh-doctor      mesh-correlate <-> mesh-ideate
mesh-dispatch  <-> mesh-mind-control  mesh-needs   <-> mesh-reflex-decay
mesh-rhythm    <-> mesh-situation     mesh-stress  <-> mesh-therm-watch
```

Those six are the mesh's actual interweaving; the other 84 were paper loops. And the peripheral set —
the tool's own load-bearing list, the reflexes spending a cron slot for nothing — is **104, not 36**.

Two demotions verified by hand, as claims and not as tool output:

- `mesh-sink-health` → PERIPHERAL. Its only mention anywhere outside itself is in `mesh-audio-active`,
  on **two comment lines** of the header (the reafference-confirmation review's own prose about it).
  No code path in the genome reads it. It was `CORE` because a review wrote about it.
- `mesh-algedonic → mesh-stress`, prose-only: `scripts/mesh-stress:31` and `:919` name
  `mesh-algedonic` in comments describing who its consumers are. The dependency is real *in the
  world* and absent *from the code* — which is exactly the distinction this axis exists to draw, and
  a good example of why the output is advisory: the fix may be to wire it, not to unwire it.

## V. Gate (RED-first, all mutants proven from a scratch copy)

14 new assertions on a fixture graph extended with three reflexes mentioned in exactly one kind of
site each (`mesh-fi` prose-only, `mesh-fj` test-only, `mesh-fk` inside `parse_latest()`), plus a
third mutual pair whose return leg is prose (`LOOPS 3 -> 2`) and a cron line chaining `mesh-fd &&
mesh-fi`. Every leg drives the real script (`bash "$0" --enacted`), so the wiring is asserted, not
just the helper.

| mutant | change | result |
|---|---|---|
| m1 | `mention_tokens` ignores its mode (declared graph everywhere) | RED — 8 legs |
| m2 | drop the full-line-comment skip | RED — prose legs |
| m3 | `is_test_fn` matches `test` as a **substring** | RED — the `parse_latest` legs, uniquely |
| m4 | enacted classes computed from the declared graph | RED — demotion + loop legs |
| m5 | `[cron-chained]` marker applied to every demotion | RED — the unmarked leg + the count |
| m6 | chained set never populated | RED — the marked leg + the count |
| m0 | no-op control (a comment line) | green |

Every previously landed axis is **byte-identical** — `mesh-closure`, `--json`, `--peripheral`,
`--timescale`, `--cadences` diffed against `git show HEAD:scripts/mesh-closure`, all unchanged.
`--test` 2.77s → 2.99s.

## VI. Not wired

On-demand, like the rest of `mesh-closure` (`orphan-ok`, advisory). Nothing auto-prunes, nothing
edits cron. The natural consumer is a steward pass over the 74 unmarked demotions; the honest reading
of several of them is *"wire this dependency", not "delete this reflex"*.

**Still open in this area** (unchanged): allostasis / anticipatory regulation; CRQA structural
coordination metrics; the timescale extension this paper actually argues for — habit at the scale of
*activities* (minutes–hours) and *regional identities* (months–years), which for the mesh would mean
asking whether a **channel/role** is a precarious self-sustaining network rather than a roster entry.
