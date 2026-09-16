# Pub top-pane refresh — 2026-09-16

Task: `pub-top-pane-refresh-20260916/refresh-pub-top-pane`

Changed `scripts/mesh-pub-dash` to put the actionable publishing priority first: inspect and answer dev.to replies before a new publish, then vet one measured case while preserving UNKNOWNs and provenance; HN/Reddit remain monitor-only.

Verification:

- `bash scripts/mesh-pub-dash --test`: PASS (`smoke-test ok`).
- Source and deployed hashes match: `ef9a319cd70bfc7e6a1c953e38ff582e5654a3680e0422657bb0c8edaee05124`.
- Restored live `mesh-home:5.0` data pane capture at `/tmp/pub-pane-refresh-20260916.txt` shows the new `NEXT: dev.to reply queue first` line, current `5 REPLY OWED`, Reddit/HN status, and a ticking `pane live` footer.
- The two-pane layout was restored after an accidental respawn targeted the shared pub window; live data is pane `.0`, Codex mind is pane `.1`.

Separate reply follow-up: board notice posted at `2026-09-16T02:51:28Z` for owed comment `3ecl5`; draft staged at `~/.mesh/devto-drafts/reply-3ecl5.md`. Posting is blocked because Chrome is not installed (`use_browser`: Chrome not found); no external comment was sent.
