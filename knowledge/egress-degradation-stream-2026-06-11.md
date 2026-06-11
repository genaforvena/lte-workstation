# Egress degradation stream — 2026-06-11

Built `scripts/mesh-egress-stream` as a degrade-only wrapper around `mesh-egress-health`.

Behavior:

- Polls `mesh-egress-health` on each run.
- Feeds a mind only when the payload indicates degradation.
- Triggers on:
  - `state=BAD` / `FAIL` / `DOWN`
  - Anthropic code present and not `401` or `405`
  - optional latency/loss thresholds, if future payloads provide them
- Remains silent when the payload is healthy.
- Dedupes repeated prompts with a last-fed file in `~/.mesh/.egress-stream.lastfed`.

Verification:

- `scripts/test-mesh-egress-stream` passed.
- Healthy synthetic payload stayed silent.
- Degraded synthetic payload fed exactly once.
- Repeating the same degraded payload hit the dedupe guard and did not re-feed.

Notes:

- `mesh-egress-health` remains the source reflex.
- The stream is intentionally cheap and only engages a mind on degradation.
