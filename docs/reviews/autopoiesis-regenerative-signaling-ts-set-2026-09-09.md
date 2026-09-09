# Live literature review — autopoiesis / biology of cognition → `scripts/mesh-ts-set.sh`

**Date:** 2026-09-09 · **Lane:** genome · **Angle:** cross-domain transfer to a distributed sensor mesh
**Arm:** treated (assigned)
**Target organ/reflex:** `scripts/mesh-ts-set.sh` (the shared `tailscale set` actuator library)
**Assignment:** randomized re-entry, p=0.20; target fixed by the assignment and not retargeted.

## Live sources actually read

The current literature is extending Maturana and Varela's organizational closure into explicit
recurrent mechanisms, rather than treating “autopoiesis” as a synonym for persistence.

- Cariani, **“Organizational closure through regenerative signaling as a possible basis for
  conscious awareness,”** *Frontiers in Computational Neuroscience* (2026),
  [full article](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2026.1806695/full).
  Its proposed mechanism is **active signal regeneration**: mutually supporting productions form a
  closed loop, and a full cycle resets the initial operating state so the process can repeat. The
  paper explicitly presents this as a hypothesis/design principle, not as established proof of
  consciousness.
- Astorga & Letelier, **“Anticipation and Structural Coupling: Two Sides of the Same Coin,”**
  preprint (April 2026), [PhilSci-Archive record and submitted PDF](https://philsci-archive.pitt.edu/29005/).
  It connects Maturana's structural coupling to Rosen-style anticipation: repeated coupling makes a
  regulatory subnetwork dynamically conjugate with relevant environmental dynamics, and proposes a
  fixed-point condition rather than a merely descriptive prediction.
- Lyon, **“Fundamental Principles of Cognitive Biology 2.0,”** *Biological Theory* (2025),
  [Springer article](https://link.springer.com/article/10.1007/s13752-025-00497-5). This review
  places sensorimotor coupling, memory, anticipation, decision and error correction inside a
  biogenic account of cognition, while keeping the Maturana/Varela connection to biological
  organization explicit.

## One concept the target does not already embody

**Regenerative signaling / cycle completion.** A successful event is not yet a closed, sustaining
actuator loop: the actuator's output must produce the signal that establishes the next cycle's
starting condition. This is narrower than “we verify a command” and different from retry. The
current `ts_set` implementation has two permission paths (unprivileged, then `sudo -n`) and returns
the command's acceptance/error text, but it has no actuator-local cycle token or next-cycle
postcondition. Its callers in `mesh-revive` and `mesh-exit` perform some verification separately;
the shared organ itself does not make the accepted write and the resulting FIB state one closed
production relation.

I searched the target and its callers for regenerative signaling, cycle completion, and an
actuator-owned outcome token. The code contains `ts_set`, FIB checks, and failure ledgers, but no
such mechanism. Existing mesh “closed loop” and regeneration references concern other organs or
the wider production graph, so they do not establish this target-specific actuator contract.

## One concrete application

In **`scripts/mesh-ts-set.sh`**, add an actuator-cycle record for each accepted `tailscale set`:
write `attempt_id`, exact operation class, and start time before the call; return the id to the
caller; and require the caller's named postcondition check (for this lane, the real FIB device and
world-fetch result) to close that id as `verified` or `unverified`. A subsequent invocation must
see an unclosed prior cycle and report it as stale/incomplete rather than treating command
acceptance as a healthy state. This would make the setter's output regenerate the next observation
obligation, analogous to the literature's signal completing and restarting its production cycle.

The first safe consumer would be the existing exit-node restore path in `scripts/mesh-revive`:
`ts_set --exit-node=...` opens the cycle, its already-present `ip route get` + real fetch closes it,
and `RESTORE-UNVERIFIED` remains retryable. Do not fire a new substrate action from the library, and
do not infer verification from the setter's return code; the FIB is the postcondition.

**Status:** proposal only. The application is deliberately not implemented in this review because
the generic library cannot safely choose a postcondition for every future setter argument, and
changing the substrate actuator requires a separate implementation/test pass with caller wiring.

## Verification of the review artifact

```text
Web search and full-page reads completed 2026-09-09 for the three linked sources.
Target/caller novelty search: no actuator-cycle/regenerative-signaling implementation found.
No mesh tool edited; no deployed copy touched; no commit made.
```

