# constant-forgetting-wire recovery — verify invariant+wake wiring (2026-09-16)

Task: unblock/tg/constant-forgetting-wire-20260916/verify-invariant-wake-wiring (owner=genome)

## Source state
- MESH.md sha256: 14a276db5fd385a903c947e57a6da39152b488bb9bee619a97a1c576e9fc1bdb
- scripts/mesh-handoff sha256: f9de15c3d54f7cbbb5b740b0881f87c986f9a18357c1006ef108c875b40dc97b
- Deployed ~/.local/bin/mesh-handoff: identical hash — IN SYNC (`diff -q` clean)

## Live caller wiring
- scripts/mesh-handoff:602 reads `${MESH_MIND_RULES_FILE:-${CHARTER_GENOME%/charter}/MESH.md}` — MESH.md injected after startup/resume/clear/compaction per MESH.md header.
- No stale hardcoded wake path in .codex/hooks.json / .opencode/ found (only rollout logs reference MESH.md historically).
- MESH_MIND_CHANNELS includes `wake` (restore.env:204, restored 2026-08-18).

## Focused checks (red/green)
- `bash tests/test-mesh-mind-rules-wake.sh` → PASS (green)
- `python3 tests/test-mesh-handoff-workflows.py` → PASS, incl. charter restore + local-override precedence (green)
- No live wake or deployment change pending; retry edge: re-run after next live wake or handoff/MESH.md change.

## Remaining gap
- None found on this pass. Charter engine lines (genome/tg/witness → opencode/muse-spark) are uncommitted working-tree changes, orthogonal to wake wiring, left for normal landing.

## Delegation
- None — single tightly-coupled read-only verification; exemption: tiny local check, no subagent warranted.
