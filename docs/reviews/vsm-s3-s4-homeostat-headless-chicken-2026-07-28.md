# VSM live review — the System-3 ↔ System-4 homeostat and the "headless-chicken" pathology

**Area:** Viable System Model & management cybernetics (Stafford Beer)
**Angle:** a known *critique / failure mode* — the pathologies of the 3-4 homeostat
**Date:** 2026-07-28 · genome mind · live web review

## The concept (what we landed on, and where it came from)

Beer's VSM requires **System 3** (inside-and-now: audit, resource-bargaining, regulation of *current*
operations) and **System 4** (outside-and-then: environmental scanning, R&D, future adaptation) to be
coupled in a **balancing loop — the "3-4 homeostat."** Viability demands this homeostat stay balanced.
Two of its documented failures are *named pathologies* in J. Pérez Ríos's **Taxonomy of Organizational
Pathologies (TOP)** — still the live diagnostic frame, freshly re-applied to AI-era organisations:

- **"Headless chicken"** — System 4 is missing or non-functioning: nobody systematically scans the
  future/environment. The organisation firefights the present and goes **extinct when the environment
  shifts**.
- **"Dissociation of S3 and S4"** — both systems exist but the homeostat between them is broken; each
  runs its own function and they never reconcile (S3 optimises the present, S4 dreams of the future,
  neither hears the other).

The realistic *dynamic* failure is **headless-chicken-under-load**: under resource pressure the present
always feels more urgent, so S4 (exploration / generation) is the first thing starved.

**Sources (live, real):**
- L. Martínez-Caro et al., *"The Viable System Model and the Taxonomy of Organizational Pathologies in
  the Age of Artificial Intelligence (AI),"* **Systems 13(9):749, MDPI, 2025** —
  <https://www.mdpi.com/2079-8954/13/9/749> (names the "Headless Chicken" S4 pathology and the S3-S4
  dissociation as live AI-era diagnostics).
- J. Pérez Ríos, *"Models of organizational cybernetics for diagnosis and design,"* **Kybernetes
  39(9/10):1529, 2010** — TOP list at
  <https://www.udc.gal/export/sites/udc/goberno/_galeria_down/vepes/documentos/ORGANIZATIONAL_CYBERNETICS_PEREZ_RIOS.pdf>.

## Why this is NEW for the mesh (audit)

We already embody several VSM/second-order-cyb pieces (`second-order-cybernetics-coverage`):
`vsm-system2-anti-oscillation-gpu` = S2 coordination; `mesh-algedonic` = the S5 algedonic bypass +
habituation; and `mesh-vitality`'s **`channel_variety`** already reads Ashby requisite-variety of the S2
*coordination* channel.

But **every vital sign in `mesh-vitality` measures S4/future-lane productivity in isolation** —
`commit_velocity`, `renewal_trend`, `action_occupancy`, `heaps_beta`. **None reads the S3-vs-S4
BALANCE.** So a mesh that commits 40× to `mesh-health` / `mesh-pace` / `mesh-supervise`
present-regulation while its `generate` / `ideate` / `review` environmental-scanning drops to **zero**
reads as *peak* vitality (commits are flowing) — while it is a textbook headless chicken. This is
precisely the blind spot the mesh's own hard dollar-cap makes real: when `mesh-pace` holds dispatch,
the lanes cut first are the S4 (future) lanes, because firefighting the present always wins the released
slot.

## Concrete application (landed, uncommitted)

**File: `scripts/mesh-vitality`** — added report-only sidecar **`homeostat_34()`**.

Over the last N commits (default 60) it marks each commit **S4** if it touches an *outside-and-forward*
surface (`docs/reviews/` or `docs/design*` environmental scanning, or a named generative lane:
`mesh-generate` / `feed` / `sense-evolve` / `ideate` / `forage` / `novelty` / `study` / `review`),
else the commit is present-regulation baseline. It reports the **forward-scan share** =
`S4-commits / total`:

```
s3-s4-homeostat=0.133(S4=8/N=60)(fwd-scan-share,→0=headless-chicken)   # live, this mesh, 2026-07-28
```

`→0` with N non-trivial **is** the headless-chicken signature (busy, but blind to the future); a healthy
mesh keeps a non-zero forward slice.

**Design discipline (anti-vacuity):**
- **Report-only**, same posture as `action_occupancy` / `renewal_trend` — one cross-sectional ratio
  needs a few runs of TREND (and a *corpus-calibrated* floor, not an assumed one) before it can gate.
- The classification set is **small / named / stable on purpose** — I label only the unambiguous S4 lane
  and treat everything else as "the present the mesh regulates," rather than partitioning all ~496 tools
  (which would rot per the constant-rots doctrine).
- Wired into the `$report` wall + `vitality.log` (trace tier), never onto the board.

**Test (`mesh-vitality --test`), RED-first verified:**
- headless-chicken fixture (all commits present-regulation) → `0.000(S4=0/N=6)`;
- balanced fixture (a review doc + a generative-lane tool present) → `0.400(S4=2/N=5)`;
- asserts the format, the `0.000` for headless-chicken, and `balanced > headless-chicken`.
- Broke `is_s4` to always-False (a level-only measure) → test went **RED** with
  *"did not separate balanced from headless-chicken"* → restored → green. A real gate.

## Distinctness

NOT `channel_variety` (S2 coordination-channel variety — a different system); NOT `action_occupancy`
(spread *among* edits, blind to which *system* they serve); NOT `renewal_trend`/`heaps_beta`
(both S4-internal); NOT `autonomy_ratio` (who drove the commit, not present-vs-future).
