# Independent mood pool verification — 2026-09-07

Verified `tinyfleet-specialists/wire-mood-pool` from the repository root.

Observed results:

- `bash tests/test-mesh-tiny-fleet-pool.sh` — PASS.
- `scripts/mesh-relay --test` — PASS.
- Forced `scripts/mesh-relay --pool tiny-fleet` guitar prompt — real adapter response.
- Guarded auto route with `MESH_RELAY_TINY_FLEET=1` — real adapter response.
- Forced candidate miss with `MESH_TINY_FLEET_DIR=/tmp/mesh-no-tiny-fleet` — pool-0 fallback returned `pong`.
- Unknown-domain prompt with the guarded candidate enabled — `[ABSTAIN] ... escalate` and exit `3`.

This independently confirms the candidate is opt-in, fallback remains available,
and specialist abstention is terminal rather than silently replaced by a generic
answer.
