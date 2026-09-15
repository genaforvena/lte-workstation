# Literature canary bounded application

Chain: `literature-canary-map-elites-20260908`
Source: `review:map-elites-illumination-literature-lane-2026-07-28`

Command (isolated state, real deployed source/tool):

```text
HOME=<fresh sandbox> MESH=<fresh sandbox> GENOME=/home/mesh-home/lte-workstation \
REVIEWS=/home/mesh-home/lte-workstation/docs/reviews \
scripts/mesh-ideate --lit --dry
```

Observed real application output:

```text
LITERATURE (live review): land on the area of autopoiesis & the biology of cognition (Maturana, Varela), from the angle of a RECENT result (2023-2026) — what's new in this area right now. Do an ACTUAL review — search current, real sources (web), read, and surface ONE concept, paper, or mechanism we do NOT already embody. Name it, cite where you found it, and propose ONE concrete application to a real organ/sense/reflex (name the file) — or discard in one line why it does not apply. The point is LIVE literature (continuously published), not a fixed list: land somewhere we have not been.
RC=0
```

This proves the generator crossed the literature-origin path and produced a
bounded, non-queued directive. `--dry` was deliberate for the application
attempt: it prevents an unreviewed live prompt from entering the shared queue.
The acceptance run below drives the same consumer's real predicate.
