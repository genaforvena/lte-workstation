# Live-literature review — autopoiesis vs allopoiesis: the mesh names its self-production loop too loosely

Date: 2026-07-29 · lane: genome (idea-queue LITERATURE task) · status: implemented + gated, uncommitted

## Area & angle

Autopoiesis & the biology of cognition (Maturana & Varela), entered from the angle demanded: **a
foundational idea we have applied too loosely.** The idea is the **autopoiesis ↔ ALLOPOIESIS**
distinction — and the loose application is *in this repo's own vocabulary*: `mesh-vitality` opens by
calling itself "the AUTOPOIESIS vital-signs reflex" and the mesh calls `mesh-generate→mesh-feed→genome`
its "autopoiesis lane."

## The distinction, and the live source

An **autopoietic** system produces the very components *and the boundary* that constitute itself,
through operations that close on themselves. An **allopoietic** system produces a **product other than
itself** and depends on an **external agent** to organize/integrate it (Maturana & Varela's
factory-making-cars). The freshest literature makes the operational cut explicit for *artificial*
systems:

> **"From intelligence to autopoiesis: rethinking artificial intelligence through systems theory"**,
> Front. Commun. 10:1585321 (2025) — https://doi.org/10.3389/fcomm.2025.1585321

Its criterion (quoted from the reading): a self-organizing artificial system remains **allopoietic, not
autopoietic**, whenever its *"boundary and operational logic remain externally determined"* — i.e. it
cannot **internally close its own production loop** and needs external reflection/integration to close
it. Corroborating live sources: *"Autopoiesis of the artificial: from systems to cognition"*, BioSystems
(2023), https://www.sciencedirect.com/science/article/pii/S0303264723001119 ; the APICe autonomy note
https://apice.unibo.it/xwiki/bin/view/Courseproject/AutopoiesisAllopoiesis . (Found via live WebSearch
2026-07-29; the 2025 Frontiers paper is the anchor.)

## Where it bites — HERE

The mesh's self-production loop is: production (`mesh-generate`/minds) → SETTLE → **LAND + DEPLOY**
(`mesh-land`) → back into the genome it samples from. That last edge — closing the loop by landing its
own products onto `origin` and deploying them — is **not operationally closed**. It is performed by the
STEWARD lane, and when the steward cannot self-close (a diverged `main` → `git pull --ff-only` aborts,
or push-heal hits `DIVERGED from origin`) it logs **`manual reconcile needed`** every 15 min and waits
for a **human**.

This is not hypothetical — it was measured **today**:

> 2026-07-29 ([[autoland-divergence-jams-autopoiesis]]): local `main` forked from `origin`; `mesh-land
> --autoland` aborted ff-only every 15 min for **~10h** (`~/.mesh/land.log`, 112 `manual reconcile
> needed` lines) while generation kept producing (71 uncommitted files). **Nothing landed** until an
> operator **restart** reconciled it (push-heal pushed `c6f948c → 16354b0` at 11:18, landing resumed).

That is the textbook allopoietic boundary: **external closure required.** The lane we *call*
"autopoiesis" is, at its production→deployment boundary, **allopoietic** — and no instrument named that.

## The mechanism we do NOT already embody

`mesh-vitality` measures whether the lanes **produce** — but nothing measures whether the loop can
**close itself** versus stalling **open awaiting an external agent**. The nearest cousins are all
distinct:

- `stranded` — a **count** of unlanded fixes (queue depth); blind to *why* they're unlanded, for *how
  long*, and to the self-vs-external-closure axis (a big count during normal throughput is not an open
  loop).
- `loop_closure_frac` — a **static topology census** of senses lacking an actuator (perception→action
  wiring), a different boundary entirely.
- `autonomy_ratio` — who **initiated** a commit (provenance of the loop's *start*), not whether it can
  self-*complete*.
- the prior `docs/reviews/autopoiesis-closure-of-constraints-organizational-2026-07-28` — **internal**
  reflex-network enablement closure, not the genome's own production→landing loop.

## Concrete application (implemented, uncommitted)

**File: `scripts/mesh-vitality`** — new report-only vital sign **`allopoiesis_gap()`**. One `awk` pass
over the steward's own trace (`~/.mesh/land.log`): a self-close marker (`landed + deployed` / `nothing
settled` / `push-heal: pushed`) closes the loop; the first stuck signature after a close (`manual
reconcile needed` / `DIVERGED from origin`) opens a streak. Reports:

- **`closed`** — the most recent landing event self-closed (loop operationally closed, *autopoietic* at
  the boundary this run), or
- **`OPEN:<h>`** — hours the loop has stood open since the last self-close (the *allopoietic* gap: how
  long production has been stranded awaiting external human reconcile).

**Verification (red→green, real incident):**
- `bash scripts/mesh-vitality --test` → `smoke-test: ok` (fixtures: OPEN streak → `OPEN:~2.0h`;
  streak **followed by** a self-close → `closed`; never-stuck log → `closed`).
- Live `--check` now → `allopoiesis-gap=closed` (the loop recovered at 11:18 today).
- Pointed at the **real** `land.log` truncated to its incident state (last `manual reconcile` line,
  11:03, before the 11:18 recovery) → **`OPEN:10.2h`** — exactly the ~10h stall diagnosed. The
  instrument would have named the mesh's loop as open-and-allopoietic for those 10 hours.

**Posture:** report-only, matching the file's instrument-first doctrine (like `heaps_beta`/
`autonomy_ratio`/`homeostat34`) — it measures the mesh's **honesty about its own autonomy**; it does not
gate a revert or alarm. The LOUD alarm for a stuck landing belongs to `mesh-land` itself (that memory's
proposed fix), not to a vital-signs read.

## Not discarded — landed

The idea applies and is now measured: the mesh can read, each run, how far its self-described
"autopoiesis" is from the real thing at the one edge that has always been externally closed.
