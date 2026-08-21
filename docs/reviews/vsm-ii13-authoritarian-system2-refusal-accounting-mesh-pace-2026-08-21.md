# LITERATURE review — Viable System Model / management cybernetics (Stafford Beer), entered from a **known critique / failure mode**: pathology **II13, "Authoritarian System 2"** (2026-08-21)

**Area:** the Viable System Model & management cybernetics (Stafford Beer).
**Angle (as the task named it):** a known CRITIQUE or failure mode of the area.
**Reviewer:** genome mind · live web review, read today.
**Landing:** a concept the mesh does **not** embody → shipped to a named organ, with a gate seen RED.

## Where the frontier already was (checked before reading, not after)

`docs/reviews/` holds **27** VSM / management-cybernetics reviews. Pérez Ríos's *Taxonomy of
Organizational Pathologies* (TOP) is already the mesh's most-used lens in this area, and the
pathologies taken are **II1–II7, II11, II14, II16, II17** (`grep -ohE 'II1?[0-9]\b' docs/reviews/*.md`).
Two nearby landings are already closed and are **not** what this review re-files:

- `vsm-system2-anti-oscillation-gpu-2026-07-28.md` — the **absent**-S2 pole ("missing S2 →
  uncontrolled oscillation between operational units"), applied to GPU contention.
- `vsm-boundary-critique-witness-channel-vitality-2026-08-19.md` — Ulrich's critique lineage.
- `vsm-syntegrity-reverberation-rounds-icosahedron-promises-2026-08-20.md` — Team Syntegrity.

**Unused in all 27:** II8, II9, II10, **II12**, **II13**, II15. This review takes **II13**.

## The concept — II13, "Authoritarian System 2"

Source, read in full today: **José Pérez Ríos, "Models of organizational cybernetics for diagnosis and
design", *Kybernetes* 39(9/10), 2010, pp. 1529–1550** (Emerald). Found via search, fetched as the
University of A Coruña copy —
`https://www.udc.gal/export/sites/udc/goberno/_galeria_down/vepes/documentos/ORGANIZATIONAL_CYBERNETICS_PEREZ_RIOS.pdf_2063069239.pdf`
— and text-extracted locally (`pdftotext -layout`) because the MDPI 2025 restatement of the same
taxonomy returns HTTP 403 to a fetcher. Section **II, "Functional pathologies"** enumerates the failure
modes of each VSM function. System 2 — the coordination function, whose whole job is damping
oscillation between autonomous System 1 units — gets exactly **two**, and they are opposite poles:

> **II12. Disjointed behaviour within System 1.** A lack of adequate interrelations between the
> elemental operating units that conform to System 1 lead to their fragmentary behaviour.
>
> **II13. Authoritarian System 2.** System 2 shifts from a service orientation towards authoritarian
> behaviour.

Beer's rule is that S2 is a **service to** S1 and never a **command over** it. The critique's force —
and why it is a failure mode rather than a slogan — is that **the drift from service to authority is
invisible from inside the coordinator**. A coordinator that has become an authority still reports
that it is coordinating; the only party who can see the difference is the unit being refused, and
that unit's experience is not in the coordinator's books.

Corroborating live sources read the same session (for the S2 charter, not for II13):
- Espinosa, A. (2025), *Revisiting the Viable System Model as an emancipatory systems approach*,
  **Systems Research and Behavioral Science 42(1), 171–188**, https://doi.org/10.1002/sres.3090 —
  revisits Jackson's "unitary, functionalist" critique of the VSM. Read; it argues the critique has
  been answered and proposes a "critical empathetic approach" — **no operational mechanism**, so it
  is cited as context, not as the landing.
- Umbrex, *Viable System Model (Stafford Beer)*, https://umbrex.com/resources/frameworks/organization-frameworks/viable-system-model-stafford-beer/
  and *VSM Training*, https://vsm-training.org/columns/ — S2 as damping oscillation between units
  "while preserving the autonomy of the operational systems".

## Why it is not already embodied — measured on this node, this session

`scripts/mesh-pace` **is** this node's System 2: a min-interval gate that damps the oscillation of
paid work-creating lanes competing for one 5-hour window, exempting operator-facing and safety
reflexes by design. It booked its **permissions and none of its refusals**:

| what | where | what it recorded |
|---|---|---|
| PASS | `~/.mesh/pace/<key>` | a durable epoch timestamp |
| HOLD — hard `$`-cap | `scripts/mesh-pace` gate branch | **nothing** (the source comment even said `# (no record)`) |
| HOLD — gap not elapsed | same | **nothing** — bare `exit 1` |

Three consequences, each verified against the code before the change:

1. `--gate-ledger` tallies the budget decision (`over`/`under`/`nocap`/`blind-*`) **globally, with no
   key** — it can say the cap held, never *whom* it held.
2. `--status` enumerates `$DIR/*`, so it can only list keys that have **passed at least once**. A lane
   refused every time it ever asked has no file and is **structurally absent from the coordinator's own
   status table** — the mesh's `a-capability-at-zero-adoption-reads-as-absent` shape, sitting inside
   the governor.
3. Live at the time of writing, `~/.mesh/pace/` held exactly two key files (`dispatch`, `feed`). That
   is a list of who has been *served*. Nothing on this node could produce the list of who has been
   *denied*.

The mesh has met one instance of II13 already and filed it as a local bug rather than a pathology:
memory `a-budget-below-the-suite-is-a-permanent-exclusion`. That is II13 in one lane; this is the
instrument that makes the class visible.

## What shipped — `scripts/mesh-pace` (report-only)

**Refusal accounting.** Both hold branches now book one row per lane at `~/.mesh/pace/holds/<key>`:

```
<total> <streak> <streak_start> <last> <soon> <cap> <gap>
```

`streak` is consecutive refusals since the last pass (a pass clears the streak and **only** the
streak; the lifetime total is the evidence trail). The `soon`/`cap` split **is the II13 axis**: `soon`
is a lane held by **its own cadence** — service, the unit's own resource bargain; `cap` is a lane held
by a **global budget it cannot influence** — authority. `gap` is the effective gap the lane actually
asked with, so starvation is judged against **the lane's own bargain**, never an assumed constant
(doctrine: calibrate against the live value, and a wide lane's long streak must not read as
starvation — that is its own smoke-test leg).

**`mesh-pace --refusals`** reads it and grades:

- **SILENCED** — streak past `MULT × the lane's own gap` and the lane has **never once passed**. This
  is the lane `--status` cannot show at all.
- **STARVED** — same, on a lane that has passed before: the hold has stopped being the lane's cadence
  and become its exclusion.
- **SERVED** — refusals inside the lane's own bargain. Pacing working as designed; not a finding.

It also prints the **authority share** — what fraction of all holds came from the global `$`-cap
rather than the lanes' own cadences. `rc 3` on a finding, `0` clean, `2` honest n/a with no ledger.
`--status` gained a section **below** its table naming held-only lanes (below, never as a new column:
`mesh-quota:88` and `mesh-dash:1943` both parse that row by field position — verified unchanged).

**The fix must not itself be II13**, so it is structurally inert: it never changes a gate decision,
never writes `$DIR/$key` (writing there would *extend* the gap — the record would become the command),
lives in a subdirectory so `--status`'s `[ -f ]` + bare-epoch shape guard cannot mistake a hold row for
a key, and the read-only `--check` probe books nothing on **either** would-hold branch. Writes are
temp+`mv`: a truncate-in-place here would let a colliding sibling read the counter empty and restart
the streak at zero — a starved lane erasing its own evidence (the shape of HEAD `2288289`).

## The gate, seen RED

`mesh-pace --test` gained ten legs. Each was driven red by mutating the real script and watching the
named leg fail, then restored:

| mutation | leg that caught it |
|---|---|
| drop the too-soon booking | `the too-soon hold was not booked at all` |
| book cap holds as `soon` | `a cap hold must book to cap (got soon=1 cap=0)` |
| drop the streak-clear on pass | `a pass must clear the refusal streak (got 9)` |
| judge starvation against a constant, not the lane's gap | `a lane held past 4x its own gap must exit 3, got 0` |
| collapse SILENCED into STARVED | `a lane that never once passed must read SILENCED` |
| make `--check` book (gap branch) | `--check booked a refusal on the gap branch` |
| make `--check` book (cap branch) | `--check booked a refusal on the cap branch` |

The `--check` pair is worth its own note: the **first version of that leg was vacuous**. It drove only
`MESH_PACE_BUDGET_OVERRIDE=over`, which short-circuits before the gap branch is ever reached — a
booking added to the gap branch survived the leg untouched. It was caught by mutating, not by reading.
Both branches are now driven.

## Live reading

`~/.mesh/pace/holds/` is empty at the time of writing, so `mesh-pace --refusals` returns the honest
"ledger present, no lane has been refused yet". It fills from the first hold after the steward lands
this; the first real reading is therefore a *future* artifact, not one this review can quote.

## Honest limit — the verdict has no automated reader yet

`--refusals` is a human/`--status` surface today. Nothing polls it, so a SILENCED lane will sit in the
ledger until someone looks — the mesh's own `a-gates-verdict-with-no-reader` shape. Naming it rather
than claiming otherwise: the next step is one line in `mesh-dash`'s `minds` pane or a `mesh-doctor`
leg, which is deliberately **not** in this change's scope.

## Discarded on the way (recorded so the next pass does not re-walk them)

- **II12, "Disjointed behaviour within System 1"** — measured a real instance: `~/.mesh/.debounce` is
  one flat namespace written by three tools (`mesh-reflex-health`, `mesh-pulse`,
  `mesh-organ-keepalive`) running three copy-pasted `debounce()` bodies, partitioned only by an
  unenforced prefix convention (`rh.` / `pulse.` / `organ.` / `up.`). Live keys checked: no collision
  today. Left un-shipped because the hazard is latent and the same session's II13 landing is live;
  the measurement is here for whoever takes it.
- **Espinosa 2025** — read, no operational mechanism (above).
- **Boundary critique / Ulrich, Team Syntegrity, S3\*, requisite variety, S3–S4 homeostat** — already
  filed in `docs/reviews/`.
