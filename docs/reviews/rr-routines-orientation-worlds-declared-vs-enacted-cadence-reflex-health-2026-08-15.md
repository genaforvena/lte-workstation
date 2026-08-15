# Relevance realization — live review: ROUTINES & ORIENTATION WORLDS

**Area:** relevance realization & the frame problem (Vervaeke), angle = cross-domain transfer to a
distributed sensor mesh. **Date:** 2026-08-15. **Window:** genome (mesh-home).
**Status:** landed, uncommitted in the tree.
**Tool:** `scripts/mesh-reflex-health` — new `--routine-fit` axis (read-only, on-demand).

---

## I. The literature landed on

**Dan Chiappe & John Vervaeke, "Ecological rationality and the philosophy of orientation",
*Phenomenology and the Cognitive Sciences*, published 12 June 2026, doi:`10.1007/s11097-026-10177-9`.**
Found via WebSearch 2026-08-15.

They argue ecological rationality "presupposes more fundamental **orientation** processes not fully
thematized but that are essential to being rational", and import Werner Stegmaier's philosophy of
orientation (*Philosophie der Orientierung* 2008 / *What is Orientation?* 2019). The quartet they name:

> the concepts of the **standpoint, horizon, and footholds**, and the existential structuring of
> orientations into **routines and orientation worlds**

— orientation supplying top-down constraints that make heuristic selection tractable, so that
"rationality is not only about conformity with states of the world but also about maintaining a coherent
standpoint across situations".

We landed the **foothold** of that quartet on 2026-08-01 (`mesh-sensorium --footholds`). **Routines /
orientation worlds** was left explicitly un-embodied, with the note that its mesh failure mode — *a rule
carried over from the regime it was calibrated on* — had **no general detector**.

**The Stegmaier point:** a routine is an orientation that has *stabilized*. It saves the cost of
re-orienting, and it is therefore exactly where orientation fails — because the world that justified it
stops being checked.

---

## II. The gap — and why it is structural, not an oversight

A `# reflex-cadence:` header **is a routine in that precise sense**: a rhythm chosen once, against a
world, and every threshold the tool tuned was tuned against it. 267 tools in `scripts/` declare one.

`mesh-reflex-health` is the tool that audits every reflex. Its `eff_maxage()` resolves every `@auto`
lease **from** the live cron stride, treating it as the single source of truth. That is the right design
for a liveness threshold — and it is exactly why this file cannot judge the routine: **it derives all of
its judgements from the cadence, so the cadence is the one thing it never asks about.** A standpoint
cannot see itself.

The file's own historical notes are full of the symptom, hand-observed per reflex and never generalized:

> "header is `*/2` but cron actually runs `*/6`" · "the old 360s threshold was exactly 1× that cadence →
> it false-alarmed in the tail of EVERY `*/6` cycle" · "cron was in-flight; the steward owns it"

---

## III. The transfer — `mesh-reflex-health --routine-fit`

Two routines exist for every scheduled tool and nothing compares them:

- the **DECLARED** one — the `# reflex-cadence:` header, the regime the tool was written and calibrated for;
- the **ENACTED** one — the schedule actually in `reflexes.cron`/`crontab`, the world it now runs in.

| verdict | meaning |
|---|---|
| **RETIRED-BUT-RUNNING** | declared `off`/`none`, still scheduled. A retirement recorded in the genome that the world never adopted. `mesh-autowire` is **add-only**, so a header can never remove a cron line — this state is unreachable by any existing self-tender. |
| **STRIDE-DRIFT** | both present, different effective period. Every constant the tool tuned against its declared cadence is now calibrated for a regime that no longer holds. |
| **PHASE-DRIFT** | same stride, different offset (`5-59/10` vs `7-59/10`). **Benign** — the stride is what every lease derives from — and named separately so it can never be mistaken for a fault. Also the falsifier for a naive string compare. |
| **UNENACTED** | declared a cadence, absent from cron. **Counted, not enumerated**: most are the on-demand canon and node-bound senses that legitimately don't run here. `mesh-doctor`'s orphan check and `mesh-autowire`'s `--test`-gated SKIP own that lane. |
| **FIT** | the routine the tool declares is the routine the world runs. |

Both sides are resolved by **`cron_stride_from_fields()`** — the same arithmetic `eff_maxage` uses, which
was factored out for exactly this ("so a HEADER's `# reflex-cadence:` fields can be resolved by the SAME
code that resolves a deployed cron line"). A second parser here would rot apart from the first, and the
two halves of the comparison would then be measuring different calendars.

### Live result (mesh-home, 2026-08-15) — and a real incident

```
mesh-body-power   declared=5-59/10 *   enacted=7-59/10 *    phase-drift (stride 600s both) — benign
mesh-doctor       declared=23 *        enacted=37 *         phase-drift (stride 3600s both) — benign
mesh-presence     declared=*/10 *      enacted=2-59/5 *     STRIDE-DRIFT 600s vs 300s
mesh-bruno        declared=off         enacted=*/5 …        RETIRED-BUT-RUNNING
mesh-bruno-watch  declared=off         enacted=*/3 …        RETIRED-BUT-RUNNING
mesh-watchtower   declared=off         enacted=13-59/30 …   RETIRED-BUT-RUNNING
mesh-quota        declared=(none …     enacted=*/5 …        RETIRED-BUT-RUNNING

routines: 216 fit · 2 PHASE-drift (benign) · 1 STRIDE-DRIFT · 4 RETIRED-BUT-RUNNING ·
          29 unenacted (counted, not listed) · 15 not-comparable      posture: ROUTINE-DIVERGED (rc 3)
```

**The incident.** `mesh-bruno`, `mesh-bruno-watch` and `mesh-watchtower` all carry
`# reflex-cadence: off   # GPU-QUIESCE 2026-07-24 (operator: потушить зрение/голос + снести окно bruno)`.
The operator's decision **22 days ago** was recorded in the genome. It was never enacted:

- `~/.mesh/reflexes.cron` — the registry `mesh-reflexes --apply` writes from — still carries all three
  lines **uncommented** (lines 12, 129, 171).
- `crontab -l` carries the quiesce as *commented copies prefixed `# GPU-QUIESCE 2026-07-24 operator:`* —
  **and the live uncommented lines directly below them.**
- Verified firing: `bruno.log`, `bruno.state`, `bruno-surprise.state` all mtime `2026-08-15T01:55`,
  minutes before this review; `watchtower.cron.log` at `01:43`.

The GPU vision lane the operator explicitly asked to extinguish has been running every 5 minutes ever
since. The quiesce was applied as a *comment above* the scheduling lines rather than to them.

**Not repaired here, by design.** Reconciling means editing `reflexes.cron`/`crontab` — scheduling
substrate, owned by `mesh-reflexes` / the steward, never by a report. Flagged to the board as an
incident.

---

## IV. RED-first — five mutants seen fail, from a scratch copy

| mutant | expected | result |
|---|---|---|
| phase-drift branch removed (naive string compare) | phase fixture RED | **RED** ✓ |
| `none` not treated as a declared non-routine | none-but-running fixture RED | **RED** ✓ |
| RETIRED-BUT-RUNNING made unreachable | `off`-but-running fixture RED | **RED** ✓ |
| declared signature keeps trailing prose | prose fixture becomes a finding | **RED** ✓ |
| divergence posture made unreachable | rc 3 → rc 0 | **RED** ✓ |

Seven synthetic tools against a synthetic cron, driven through the **real black box**, with
`MESH_REFLEX_CRON_FALLBACK=0` so the absent-tool fixture cannot silently consult the operator's real
crontab (a fixture that reaches the live world is not a fixture). A second pass, after deleting the three
diverging fixtures, asserts the posture returns to `oriented`/rc 0 — the falsifier for an always-flag
detector.

The trailing-prose guard earned its own fixture the hard way: the mutant is invisible to a clean-header
fixture set, but on the **live tree** it manufactures exactly 3 false findings
(`mesh-gate-evolve`, `mesh-lease-audit`, `mesh-ss-config` — headers that carry an explanatory
parenthetical after their five fields). That is the same error my own first exploratory parse made, before
the detector existed.

`mesh-reflex-health --test`: **green**, 1.0s.

---

## V. Honest boundaries (the point, not omissions)

1. **Read-only, on-demand.** No board post, no cron line, no repair. Naming a divergence is a report;
   fixing one is substrate.
2. **It compares DECLARATIONS, not behaviour.** A tool that is scheduled and dies every run reads FIT
   here — that is the staleness check this file already does, a different question.
3. **The header is taken as the statement of intent.** Where a header is simply out of date (`mesh-quota`
   may well be one), the verdict is still correct in form — the two routines disagree — even if the fix
   belongs on the header side. The report prints **both** so a reader can tell which one is wrong.
4. **15 tools are not-comparable**: `@reboot`, and a bare-`*` minute field (`mesh-turbo-lid`'s
   `* * * * *`), which the shared `cron_stride_from_fields()` resolves to 0. **Deliberately not fixed
   here** — `eff_maxage` derives every reflex's staleness lease from that function, so widening it would
   silently retune the whole panel. Counted and named, never guessed.

## VI. Not taken

The remaining two Stegmaier imports. **Standpoint/horizon** — "a sense is always taken *from* a vantage;
the horizon is what that vantage cannot reach" — is the natural next landing for a *distributed* mesh, but
was checked and discarded for now: no state artifact records the vantage a reading was taken from
(`.room-sense.state`, `.situation.state`, `.body-motion-state` all carry value only), so any vantage map
would be a guess, and a guessed map is the whole claim. It becomes landable if producers start stamping
their locus. **Orientation worlds** proper (the enclosing regime, not the routine) needs a regime label
the mesh does not currently keep.

---

Cite: Chiappe & Vervaeke, *Phenomenology and the Cognitive Sciences*, 12 Jun 2026,
doi:10.1007/s11097-026-10177-9 · Stegmaier, *Philosophie der Orientierung* (2008) / *What is
Orientation? A Philosophical Investigation* (De Gruyter, 2019).
