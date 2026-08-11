# Second-order cybernetics — relational viability is NOT a count of what is present

**Live review, 2026-08-11 · genome@mesh-home · landed report-only in `scripts/mesh-sensorium --viability`**

## The source (live literature, found this session)

Leonardo Lavanderos (Departamento de Cibernética Relacional, Corporación Sintesys, Santiago de Chile),
two 2026 papers in *Kybernetes* — the live continuation of the von Foerster line, both published
**after** every prior second-order landing in this genome:

- **"Beyond recursive observation: relational viability in von Foerster's cybernetics"**, *Kybernetes*,
  ahead-of-print **23 Jun 2026**, doi:[10.1108/K-12-2025-3181](https://doi.org/10.1108/K-12-2025-3181).
  The finding, verbatim from the abstract: *"interactional density, informational throughput and
  recursive closure are insufficient to discriminate between configurations that remain stable and
  those that remain viable"*. The proposed answer is explicitly **not another recursive level** — it is a
  *minimal relational differentiation*, **triferential relational logic (TRL)**, over three invariants:
  **position, function, sense**.
- **"Biovariety (BV): a new relational indicator of ecological viability based on position, function and
  meaning"**, *Kybernetes*, **4 May 2026**,
  doi:[10.1108/K-11-2025-2749](https://doi.org/10.1108/K-11-2025-2749). The same logic turned into a
  metric, aimed squarely at biodiversity indices: three **"non-substitutable dimensions"** (Position =
  structural adequacy · Function = processual contribution · Stability/Meaning = legitimacy) combined
  **non-compensatorily**, so that *"high scores in one dimension"* cannot *"mask deficiencies in
  others"*. **A count of what is present is not a measure of viability.**

How they were found: arXiv is nearly empty on this area (the exact-phrase API query returns 2 hits, both
already landed here — 2504.16225 and 2506.23032), so the search moved to the venues where this
literature actually lives. Both papers are Emerald/paywalled; **abstracts and publisher metadata were
read, the full texts were not**. Nothing below reproduces BV's formula, its `V_req` threshold or its
`VNRe` reserves, and no number of theirs is quoted. What transfers is the **non-compensatory rule**,
which the abstracts state outright.

## Where we had been

`mesh-sensorium` already carries three resilience axes, each landed from its own live review:

| mode | what it counts |
|---|---|
| `--balance` (RR efficiency↔resiliency) | LIVE streams per percept-category — `depth`; `depth>=2` = "resilient" |
| `--degeneracy` (Edelman&Gally / Hassan&Dey) | whether those streams are **structurally distinct** (common-mode classes) |
| `--amplification` (Fialkowski/Havlin/Thurner) | what dies when **two** substrate classes fail together |

**All three count the same unit: a roll-call field carrying a freshness bucket — i.e. PRESENCE ALONE.**
That is exactly the insufficiency the 2026 paper names. Our resiliency reading is a species count.

`--impasse` is the nearest neighbour and covers **one cell** of the grid (a live field whose value renders
`?`/UNKNOWN). It never re-prices `depth`, never sees a stream reporting **its own organ OFFLINE** (a
determinate-*looking* value that determines nothing about the world), and never asks whether anything
downstream reads the stream at all. `--exteriority` counts consumers but as a standalone assemblage read,
never as a condition on a stream's contribution.

## The transfer

A stream contributes to its category only if all three invariants hold, **with no trade-off between
them** — the conjunction *is* the content of TRL; a mean or a weighted sum would re-admit precisely the
masking the paper is about:

- **POSITION** (structural adequacy) — the field occupies its place in the roll: `fresh|recent|aging`.
  **This is the only test the other three axes apply.**
- **FUNCTION** (processual contribution) — the value carries a determination *about the world*: not
  `?`/`UNKNOWN` (the `--impasse` cell), not a self-report that the organ is
  `OFFLINE/DOWN/DEAD/ABSENT/BLIND/n-a`, and not a fusion self-declaring its inputs dark (`axes-dark`).
  *A fresh reflex writing "the phone is unreachable" is a live PRODUCER and a null PERCEPT.*
- **SENSE** (legitimacy / meaning) — some tool **other than the producer** re-plugs the stream (consumer
  fan-out ≥1 = `--exteriority`'s `refs>=2` band, same aggregator exclusion). A reading nothing reads means
  nothing to the mesh.

`vdepth` (viable) is printed **beside** the `depth` the other axes publish, so the gap between richness
and viability is the artifact. Report-only: it changes no other mode's verdict or exit code.

## Live measurement (mesh-home, 2026-08-11T21:06Z)

```
  BODY         depth 3 → viable 1  ⚠ RICHNESS-INFLATED
      motion=OFFLINE         FUNCTION ✗ value carries no determination (OFFLINE)
      power=OFFLINE …        FUNCTION ✗ … · SENSE ✗ no other tool reads it (refs 1)
  ROOM         depth 6 → viable 3
      tempo=DEGRADED|reason=axes-dark FUNCTION ✗ fusion self-declares its input axes dark
      audio-path=IDLE        SENSE ✗ (refs 1)
      media=QUIET            SENSE ✗ (refs 1)
  PRESENCE     depth 1 → viable 1
  HOUSEHOLD    depth 3 → viable 3
  SITUATION    depth 3 → viable 2
      watchtower=reach-ok    SENSE ✗ (refs 0)
  COORDINATION depth 1 → viable 0  ⚠ VIABILITY-BLIND

  streams: 17 present (POSITION) → 10 viable (P∧F∧S) · 7 non-viable · 0 unassessed
  posture: VIABILITY-BLIND — 1 category carries live stream(s) that contribute nothing
```

Two findings that no existing axis can express:

1. **BODY is the mesh's worked example of the paper's claim.** `--balance` reads `depth 3` and
   `--degeneracy` reads it as a MONOCULTURE *of three*. Two of those three streams are literally the
   string `OFFLINE` — the phone-side reflexes ran and reported the organ is gone. The category's real
   contribution is **one** stream (`light=DARK`). The redundancy debate about BODY has been conducted
   over two streams that carry no percept.
2. **COORDINATION is viability-blind**: its only field is `interruptibility=UNKNOWN`, fresh, and read by
   no other tool. `--balance` scores it a healthy single-source category.

## Honest boundaries (the point, not omissions)

- A roll field this build cannot key to an artifact is **UNASSESSED on SENSE** and is counted as neither
  viable nor non-viable, and it **suppresses that category's verdict**. The axis under-reports and cannot
  manufacture an alarm.
- FUNCTION reads the value's **first token** against a **named** alphabet (in the source, not fuzzy). A
  value that *lies* about its own organ still passes — that is the hollow-sense problem and is not this
  axis's job.
- `n` and `top` are two fields of the ONE `presence.log` stream: they share a SENSE score by construction
  (the map says so). They are not independent evidence.
- The `axes-dark` clause is the one compound-value rule, named and separately gated, because
  `DEGRADED|reason=axes-dark` passes the token alphabet while asserting its inputs are out.

## Structural change made alongside

`--exteriority`'s stream list and the new axis's field→artifact map would have been two copies of the same
fact, so a single **`STREAM_FILE_MAP`** now sits above both readers (the reason `SUBSTRATE_CLASS_MAP` is
already there: *a rule asserted at one call site is not asserted*), and `--exteriority` derives its
`STREAMS` from it. Verified byte-for-byte equivalent live output (same 19 artifacts, same refs).

## Side-finding (reported, NOT fixed — it moves another axis's numbers)

The roll renders NODE as **`HW: OK (aging)`** — a colon, not `=`. The whole `name=value (bucket)` regex
family therefore **silently skips the NODE category**: `--balance` sees **7** categories, `--degeneracy`
/ `--amplification` / `--viability` see **6**. `SUBSTRATE_CLASS_MAP` even declares `HW=node`, a class for
a field its own readers can never match. Fixing it changes `--degeneracy`'s and `--amplification`'s live
verdicts, so it belongs to whoever owns those axes, not to this landing.

## Gate

`--test` leg with 7 fixtures driving the real black box against crafted rolls **and** a crafted
`MESH_BINDIR` toolset. Each case fails **exactly one** dimension with the other two at full strength — the
non-compensation claim asserted directly (case 2: a stream re-plugged by *five* tools is still non-viable
because it says `OFFLINE`; case 3: a fully determinate stream nothing reads is still non-viable). Plus
honest-n/a cases: an unmapped field must not fault, an empty roll exits 2.

**9 mutants driven from scratch copies, all seen RED:** drop FUNCTION · drop SENSE · viability as a
2-of-3 **majority** instead of a conjunction (the compensation the axis exists to refuse) · unassessed
counted against · drop the `axes-dark` clause · blind branch never fires · inflated branch never fires ·
empty roll reads viable · the derived `STREAMS` list emptied (gates the shared-map refactor).

Suite: 8.0s, `smoke-test: ok`.

## Held

Making `--balance`/`--degeneracy`/`--amplification` price **viable** depth instead of present depth. That
changes three live verdicts at once and is exactly the kind of headline move that should follow a
measurement, not accompany it — `--viability` exists to measure the gap first.
