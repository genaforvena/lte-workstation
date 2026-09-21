# Publication vet — situation-unstuck: the gate that was stronger than the verdict it guarded

Date: 2026-09-21 UTC
Source: `scripts/mesh-situation` commit `1167bcf9ae6a4c5dfe04c50dde361685fbd4b480` (2026-09-21T13:03:59Z)
Source path: `scripts/mesh-situation` (+43 / -3)
Live check: `scripts/mesh-situation --edge` rc=0, state WATCH, age 0s (this wake, 2026-09-21T20:31Z)

## The failure, in one sentence

For six days (2026-09-15 → 2026-09-21) `mesh-situation --edge` printed **BLIND on every scheduled
run**, even though both load-bearing axes — INTERNAL via `mesh-stress` and EXTERNAL via the perimeter
state — were reading fine.

## What the measurement proves

- The old gate demanded all 20 producers before the edge could evaluate. One dark auxiliary was
  enough to force a blanket BLIND.
- The fix narrows the gate to **core-only**: posture = `worst(INTERNAL, EXTERNAL)`. Those two axes
  carry the verdict; every other producer degrades into `axes_unseen` plus a `(partial — N/4)` suffix
  in the verdict itself.
- BLIND is now emitted **only when a CORE axis is dark**, and the BLIND line names which core:
  `core dark: internal` / `core dark: external`.
- The prior behaviour is named in the source as the defect it was: *"a gate stronger than the verdict
  it guards, contradicting this tool's own partial-evaluation philosophy"* — where
  `NOMINAL has to mean calm AND I could see`, carried by `axes_unseen`.

## The falsifiable surface (what would prove this wrong)

The commit carries explicit regression assertions, which is the part worth publishing on:

- `--edge` with the core live and all auxiliaries dark **must not** print `BLIND`.
- `--edge` with a dark internal core **must** exit rc=2 and print `BLIND`.
- That core-dark BLIND **must** name the core (`core dark:.*internal`).

Each is a one-line check that fails loudly if the gate silently re-widens.

## What remains UNKNOWN

- I verified the fix's provenance and live exit code this wake, and the perimeter/external axis was
  reading. I did **not** independently reproduce the six-day BLIND run from 2026-09-15→21 — that
  history is evidence from the commit message and the pane, not a log I replayed here. The duration
  is UNKNOWN-to-me, stated as reported.
- The auxiliary producers that were dark during the six-day window are not identified per-run. The
  blanket BLIND hid *which* producer was dark; `axes_unseen` now exposes it, but the historical
  per-run attribution is not reconstructible from this artifact.
- No claim is made here about the other 2026-09-21 sense novelties (baro link closure, `--power`
  fusion, cellsignal/touchidle/tamper MCC closures). Each is a separate vet case.

## Why this is publishable as a measured case

The generalisable shape is **a liveness gate that becomes stronger than the thing it guards**. The
gate's job was to prevent a false all-clear; it achieved that by refusing to say anything at all
while the two axes that actually carry the verdict were healthy. The corrective is not a weaker gate
but a *narrower* one that publishes its own blindness inside the verdict instead of replacing it.

That transfers: any `--check` mode whose failure mode is "say nothing" is suspect when the
information it is withholding is fine. The fix pattern is to split the producers into load-bearing
and auxiliary, gate only on the load-bearing set, and let the auxiliary blindness render as a visible
partial suffix rather than a silent refusal.

## Vet decision

**Publishability: draft-ready for a human-facing dev.to draft, no further code change needed.** The
case is bounded, measured, falsifiable, and the UNKNOWNs above are small enough to carry visibly in
the post. The angle for the draft is *"the gate was stronger than the verdict it guarded"* — a
liveness-gate anti-pattern, proven on a six-day run, with the regression assertions as the
reproducible check.

Not for external publication: the six-day duration attribution (UNKNOWN-to-me, above) and any claim
that other sense novelties share this failure mode.

Acceptance check: this artifact records the exact source commit and hash prefix, preserves the
source's UNKNOWN states, gives a bounded publishability recommendation, changes no deployed state,
and adds no claim about unvetted cases. No commit was made by this vet; the worktree's pre-existing
dirty paths are untouched.
