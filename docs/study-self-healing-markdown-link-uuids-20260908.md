# Self-healing Markdown links in the text board

This is the small codebase trial for the self-healing-systems study brief. Board task text is
mutable: a refactor can change its slug or wording while older Markdown references still point at
the task. `scripts/mesh-board-id` now treats the `{#...}` token as the durable identity and checks
Markdown fragments of the form `[label](#id)` against the newest `[task]` line carrying that token.

The behavior is intentionally read-only and on demand:

- `mesh-board-id markdown <id>` emits a Markdown link whose fragment is the durable token.
- `mesh-board-id check` reports `MARKDOWN` when an anchor resolves after refiling and
  `MARKDOWN-DANGLING` when no task carries the referenced token; dangling anchors fail the check.
- Both legacy 8-hex tokens and UUID-shaped tokens are covered, so introducing UUIDs does not
  discard existing board history.

Verification artifact: `tests/test-mesh-board-id-markdown.sh` exercises both token shapes, a refile,
current-target resolution, and both dangling-anchor failure cases. The source smoke test also covers
minting, tracing, claim healing, and the board grammar.
