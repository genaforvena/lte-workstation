# Swarm/stigmergy live review — sematectonic vs sign-based stigmergy (marker-reality decoupling)

**Date:** 2026-07-29 · **Lane:** genome · **Area:** swarm intelligence & stigmergy · **Angle:** a known
FAILURE MODE not yet embodied — marker-reality decoupling (the seventh live-review landing on this area).

## The concept (live sources)

Grassé's original stigmergy distinguished two mechanisms, sharpened by E.O. Wilson / Theraulaz &
Bonabeau:

- **Sematectonic stigmergy** — the stimulus *is* the performed work. A half-built structure invites its
  own completion; the trace and the operational state are the same object.
- **Sign-based (marker) stigmergy** — a *separate* signal (a pheromone) *points at* the work. The trace is
  a signal ABOUT the state, decoupled from it.

**Live 2026 source — the critique:** *Ledger-State Stigmergy: A Formal Framework for Indirect
Coordination Grounded in Ledger State* (arXiv:2604.03997, April 2026) formalises this for append-only
coordination media and names the failure mode: **marker-reality decoupling** — "the trace should BE the
operational state," not a signal pointing at it. Its §7.4 warning ("Pheromones evaporate. Ledger state
does not") concerns stale traces that mis-recruit; its deeper prescription is **reality-grounding**:
"A task's OPEN flag in contract storage is not a separate signal pointing to reality — it *is* the
reality agents act upon."

Sources:
- [Ledger-State Stigmergy (arXiv:2604.03997, 2026)](https://arxiv.org/html/2604.03997)
- [Stigmergy as a Universal Coordination Mechanism (Heylighen, VUB)](https://pespmc1.vub.ac.be/Papers/Stigmergy-varieties.pdf)
- [Stigmergy — ScienceDirect overview](https://www.sciencedirect.com/topics/engineering/stigmergy)

## Where the mesh already stands (what NOT to re-land)

The append-only-trace *mis-recruitment* half of the paper is already embodied: the board is read through
**windowed tails** (evaporation proxy), `mesh-promises` ages open claims to LEAK, and `mesh-dispatch`
density-adaptively evicts never-taken `[task]`s. Leaked promises are read-only (they don't re-dispatch),
so a stale trace does **not** trigger wasted foraging here — and staying "LOUD forever" is a *deliberate*
accountability choice (`mesh-promises:35`), the opposite of the paper's concern.

## The un-embodied gap

`mesh-promises` discharges a liability the moment a matching `[done]` MARKER appears — it **never checks
the artifact**. Per the mesh's own top doctrine ("a claim is not an artifact") a `[done]` can clear a
promise with no work behind it: the ledger shows the liability discharged while the operational state is
unchanged. That is exactly the paper's marker-reality decoupling, and no axis **measured** it — the mesh
knew it only as prose doctrine. The three prior board axes on `mesh-forage` all catch *too-little* or
*wrong-shaped* deposition (dead lane / abandoned branch / circling mill); none asks whether a *settling*
deposit is grounded in a verifiable artifact.

Automating a per-`[done]`→git cross-check is blocked here (board slugs are descriptive, not tool-named;
git is centrally attributed to `mesh-land`, not per-lane). But the doctrine "[done] states the result +
cite (commit/file)" gives a deterministic, false-positive-conservative proxy: **does the discharge text
cite a verifiable artifact?**

## The application (landed, uncommitted — steward lands)

A seventh axis in `scripts/mesh-forage`, `grounding()` — the **sematectonic-grounding** reading:

- A `[done]` is **sematectonic (grounded)** if its text cites something a reader can go verify: a repo
  path (`scripts/`|`docs/`|`tests/`), a file (`.md/.sh/.py/.json/.onnx/.wav/.log/.service/.timer`), a
  `mesh-<tool>` name, or a `commit`/`Artifact`/`RED-`/`smoke` keyword. Otherwise **sign-based** (a bare
  completion claim).
- **Colony-level scalar + the sign-based TAIL** (the actual bare deposits), never a per-lane accusation.
  Reports the tail, not a saturating verdict — the grounded fraction runs high on a disciplined colony,
  so the value is *which* discharges are ungrounded, not a colony grade (avoids the median-is-max /
  pooled-saturation trap).
- **Additive, rc-neutral** (never changes the evenness exit code), honest `n/a` when the window holds no
  `[done]`.
- JSON: `grounded_discharge_pct` / `grounded_marks` / `sign_based_deposits`.
- **RED-first `--test`:** a 4-mark fixture (3 cite path/tool/commit, 1 bare) asserts `grounded_marks:3`
  and the bare `vpn/axis-d` is flagged; the `MESH_FORAGE_GROUND_BREAK=1` hook forces all-grounded and the
  flag must vanish (classifier reads the text, not a constant). Seen RED — breaking the classifier
  (force `cited=1`) flips `grounded_marks` to 4 and empties the tail, failing both assertions; restored → PASS.

**Live first run (12h window):** `grounding: 96% sematectonic (25/26)` — flagged ONE real sign-based
discharge, `health/loadaudit-junk-load-1440Z`: a `[done]` that cleared its promise on a bare marker with
no trace a reader can verify. A disciplined colony with a visible, nameable tail — exactly the reading
the axis exists to surface.

## Still un-covered neighbours (for the next review)

order-parameter / polarization (alignment); velocity-correlation entropy; Harwell-Gini emergence (swarm
output minus Σ individual). That ground is still open.
