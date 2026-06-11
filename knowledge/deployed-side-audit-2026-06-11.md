# Deployed-Side Audit — 2026-06-11

Scope: tools present in `~/.local/bin/` that are not in `scripts/` and are not currently listed in the on-demand canon. This is a drift audit only; no files are deleted or moved here.

## Findings

| Tool | Evidence | Verdict | Recommendation |
|---|---|---|---|
| `mesh-breath` | Header says it verifies how each node breathes via SSH/Tailscale and is read-only. | KEEP | Useful live probe. Add to canon only if it is intended as a first-class reflex. |
| `mesh-guardian` | Header says it is a survival reflex that checks node reachability, tmux sessions, and the Telegram organ. | KEEP | Real recovery tool, but the deployed copy is drifted from genome. Reconcile or move into genome if steward wants it owned. |
| `mesh-load` | Thin wrapper that reports agent load/quota to `mesh-chat` by calling `mesh-usage`. | KEEP | Helper, not a standalone reflex. Either add to genome as a support tool or fold into the caller that uses it. |
| `mesh-onboard` | Automated onboarding wrapper that opens a tmux window and optionally runs an install command. | KEEP | Operator-facing helper. Not currently wired in the genome; add only if onboarding automation is still wanted. |
| `mesh-reflect` | Telos reflection brief / autonomous reflection helper. | KEEP | Drifted support tool with a clear purpose. If it remains part of the operating model, it should be in genome or canon; otherwise retire explicitly. |
| `mesh-route` | Thin router for `voice-in.log` into channel inboxes. | KEEP | This looks like core plumbing, but the deployed copy is outside genome. Reconcile with `mesh-textin`/channel routing ownership before landing anything else. |
| `mesh-study` | Research-channel helper that rotates through fields and records a brief. | KEEP | Discovery helper. If field mining remains a standing practice, move it into genome/canon; otherwise mark it intentionally ad hoc. |
| `mesh-usage` | Python usage aggregator for Gemini/Claude token counts. | KEEP-AS-HELPER | This is a library-like utility, not a user-facing reflex. Leave deployed only if its callers depend on it; otherwise add it to genome or retire. |

## Summary

- 8 deployed-side `mesh-*` binaries are not present in `scripts/`.
- None of them need deletion as a result of this audit.
- The main action is ownership drift: decide whether each is canon, genome-owned support code, or intentionally out-of-tree.

