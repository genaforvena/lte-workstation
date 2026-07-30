# LITERATURE review — relevance realization: insight / reframe-at-impasse (2026-07-28)

**Area:** relevance realization & the frame problem (Vervaeke), **cross-domain transfer to a distributed
sensor mesh** — from the angle of the *frame-BREAKING* side of RR the mesh had not embodied.

## The concept (named, cited — grep 0 in the genome before this)

Relevance realization has **two** movements. One is *frame-tracking*: within the current relevance-frame,
weight what's relevant and ignore the rest (precision-weighting — already `scripts/mesh-precision`). The
other is *frame-breaking*: realizing the current frame **itself** is wrong and **restructuring** it — and

> *"the ability to reframe how we find things relevant is sometimes experienced as the 'aha' moment
> called **insight**."*

Its precondition is an **impasse**: the current frame *persistently fails* to resolve. Insight is the
restructuring that resolves the impasse — not more attention within the frame, a *new* frame.

- **Andersen, Miller & Vervaeke, "Predictive processing and relevance realization: exploring convergent
  solutions to the frame problem", Phenomenology and the Cognitive Sciences (2025)**,
  doi:10.1007/s11097-022-09850-6 (https://link.springer.com/article/10.1007/s11097-022-09850-6) — RR as
  opponent processing solving the frame problem; reframing/insight as the frame-breaking pole.
- **Riedl, Djedovic, Vervaeke & Walsh, "Naturalizing relevance realization", Frontiers in Psychology
  15:1362658 (2024)** (https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full)
  — RR as a self-organizing bioeconomic process; opponent trade-offs incl. reframing.
- Foundational: Vervaeke, Lillicrap & Richards, "Relevance realization and the emerging framework in
  cognitive science", J. Logic & Computation 22(1):79 (2012).

**Distinct from every prior RR land** (coverage map checked, grep 0 for `impasse|reframe|restructur` as
the RR concept): NOT precision-weighting, NOT `frame_coverage` (the *static* large-world limit — a signal
outside the catalog), NOT explore↔exploit (`mesh-needs`), NOT the just-landed efficiency↔resiliency
(`mesh-sensorium --balance`), NOT MCC open-ended divergence (`mesh-sense-evolve`). Those are all
frame-*tracking* or frame-*shape*. This is the frame-*breaking* trigger — the "aha".

## Where we'd been, and the gap

`mesh-precision` names the **static** large-world limit (weights only pre-listed senses). `mesh-sense-evolve`
**grows** the frame — but on a *blind timed rotation* (enrich→cross→new-sense→liveness every 40min), with
no input from where the sensorium is actually *failing*. `--balance`/`--exteriority` read the frame's
shape. **None detect the DYNAMIC impasse** — a percept the frame is actively *fed* but *cannot carve* —
which is exactly the insight-trigger: reframe *here*, not on a timer.

And the mesh already knows this failure by another name. CLAUDE.md doctrine: *"a reachable phone whose
driver returns empty is a hollow sense, cron-green while its artifact goes stale."* The **hollow sense is
an impasse seen from the RR side**: the producer *ran* (mtime moving) yet resolved *nothing*.
mtime-liveness (`mesh-reflex-health`) is structurally **blind** to it — the mtime is *fresh*. And it is
categorically different from a **stale** producer (dead → *restart*, a liveness fix): an impasse wants
**restructuring** (a new/cross sense), not a restart. Nothing measured that distinction.

## The concrete application (implemented, read-only)

**File: `scripts/mesh-sensorium`** — added `--impasse`, a read-only report that reuses the `--cached`
roll-call (the one source of truth for what's live) and flags each percept-category holding a field that
is **LIVE** (fresh/recent/aging bucket) yet **UNRESOLVED** (value renders `?` — `mark()` writes `?` when a
fresh producer's state is empty/unparseable — or literal `UNKNOWN`). That is the frame *fed-but-uncarving*
= an **IMPASSE**, the insight-trigger. Posture **FRAMED** (exit 0, every live percept resolves) /
**IMPASSE** (exit 3, ≥1 live-but-unresolved category → restructure, don't restart) / **NO LIVE STREAMS**
(exit 0, liveness is `--balance`/reflex-health's concern, not impasse). It sits beside `--balance`
(efficiency↔resiliency) and `--exteriority` (assemblage) as the third read-only RR/philosophy lens.

**It caught a real one on the first live run.** `COORDINATION interruptibility=UNKNOWN (recent)` — the
`mesh-interruptibility` fusion runs every ~12min (mtime 535s, fresh) but writes literal `UNKNOWN`: a
genuine hollow sense that `reflex-health` reads **green** while the coordination band never resolves. That
is the impasse `--impasse` exists to surface, found on real state, not a fixture.

**Honest / conservative.** Impasse is detected only where the *whole* field value is unresolved
(`name=? (fresh)`); a compound field (e.g. PRESENCE `n=? top=?` with a mid-value `?`) is a conservative
**miss**, never a false alarm — it under-reports, never over-reports (the `frame_coverage`/`--balance`
caveat spirit). Read-only, touches no verdict or weight downstream; the intended consumer is the mind /
`mesh-sense-evolve` (bias the next directive toward the *impasse category* instead of the blind rotation —
the natural follow-on wiring, left as a proposal, not wired here).

**Gate (RED-first verified).** `mesh-sensorium --test` drives the real `--impasse` black-box against
crafted cached state under a throwaway HOME: a resolved live field → FRAMED/exit0; a live-but-empty field
(`? (fresh)`) → IMPASSE/exit3; the SAME field made STALE (old mtime) → **not** impasse (dead producer =
liveness, the load-bearing distinction). Verified red-then-green: dropping the `?`/`UNKNOWN` alternatives
from the impasse regex turns the IMPASSE assertion red (`must be IMPASSE/exit3, got FRAMED`), restoring
goes green.

## Why not discarded

Discardable only if the mesh already detected a *live-but-unresolved* percept as a reframe-trigger. It did
not: `frame_coverage` names the static catalog boundary, `mesh-sense-evolve` grows the frame blind to
where it's failing, and mtime-liveness is definitionally blind to a fresh-but-hollow sense. The 2024–2025
RR literature names precisely this frame-breaking movement (insight at an impasse), the mechanism is cheap
(reuse the roll-call, cross freshness × resolution), and it found a real impasse on this node immediately.
