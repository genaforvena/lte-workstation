# Mesh health fallback path diagnostic — 2026-09-14

The health handoff verified that `imac-rozalia` is tailnet-offline and has no configured
`MESH_LAN_FALLBACK` entry. The health renderer previously showed only `OFFLINE`, making a missing
alternate path indistinguishable from a configured candidate that did not answer.

`scripts/mesh-health` now reports `off-tailnet: no fallback configured` when no candidate is
configured and `off-tailnet: configured fallback unanswered` when candidates exist but none answer.
This reports path evidence without adding an unverified iMac address or changing network state.

Verification:

- TDD regression was observed red for both states before the renderer change, then green afterward.
- `scripts/mesh-health --test` — PASS.
- `bash -n scripts/mesh-health` — PASS.
- `git diff --check -- scripts/mesh-health` — PASS.
- Live `scripts/mesh-health` — exit 0; `imac-rozalia` rendered `OFFLINE ... off-tailnet: no fallback configured`; router and Redmi rendered configured fallbacks unanswered.

Source SHA-256: `1eb68e5e6925c47182cfe0ab85a7cf31425c3482fc85938110bcc4d7d96d3db0`.
