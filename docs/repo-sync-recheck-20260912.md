# Repository synchronization recheck — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-repo-sync` (owner `tg`; dispatch eligibility exited 0 before owner-authored take).
Source: `docs/repo-sync-audit-20260907.md`; related current work: `tg-scripts-layout-migration-20260912/manifest-sync-doctor` (owner `genome`).

## Fresh repository state

| Repository | Fetch and comparison | Worktree / disposition |
|---|---|---|
| `/home/mesh-home/.fzf` | `fetch --all --prune` succeeded; `HEAD...@{upstream}` = 0/0 | clean, aligned |
| `/home/mesh-home/.mesh/gigaam-src` | fetch succeeded; 0/0 | clean, aligned |
| `/home/mesh-home/prebid-local/prebid-server` | fetch succeeded; 0/0 | clean, aligned |
| `/home/mesh-home/src/llama.cpp-prism` | fetch succeeded; `prism` = 43 ahead / 1131 behind `origin/prism`; non-shallow and merge base exists | clean but divergent; no refs changed |
| `/home/mesh-home/.mesh/knowledge` | configured `default-string/main` fetch timed out at 20 seconds; cached comparison = 85 ahead / 0 behind | clean locally; cached `HEAD` is `c0c72cf` and also `origin/main`; remote freshness is unknown |
| `/home/mesh-home/lte-workstation` | `origin` fetch succeeded; `main` = 0/0 with `origin/main`; secondary `mesh` fetch timed out at 15 seconds (the earlier all-remote fetch timed out at 20 seconds) | 806 porcelain paths were present before this audit added its plan and receipt; they block a clean future pull. No dirty paths were changed. |

## Source/deployed parity

`mesh-sync-tools --test` passed. Its report-only invocation returned 1 and recorded deployed drift in the runtime log; `--apply` was not run.

Eight reported tools have byte-identical committed source and deployed content, but their deployed entries are regular files, not the exact symlinks required by the sync tool: `mesh-body-motion`, `mesh-device-churn`, `mesh-health`, `mesh-land`, `mesh-mind-recycle`, `mesh-promises`, `mesh-stress`, and `mesh-travels`. For each, `sha256sum` of `git show HEAD:scripts/<tool>`, `scripts/<tool>`, and `~/.local/bin/<tool>` matched.

The ninth candidate, `mesh-gpu-fan`, exists only as untracked `scripts/mesh-gpu-fan`; it is marked `orphan-ok` and on-demand, is absent from `HEAD` and `~/.local/bin`, but the `scripts/mesh-*` candidate glob reports it as drift. A global apply could install it, so deployment was left untouched. The existing manifest-sync task covers the detector/enumerator; the new follow-up also requires separate treatment of this untracked candidate.

## Follow-up opened

Created exact-owner chain `repo-sync-followups-20260912` for `genome`, with six steps covering: safe ownership triage of the dirty root checkout; exact symlink repair for the eight tracked tools; exclusion or explicit disposition of untracked `mesh-gpu-fan`; a decision brief for the `llama.cpp-prism` divergence; a bounded refresh of the `default-string/main` knowledge remote; and bounded diagnosis of the root repository's secondary `mesh` remote. The first step is dispatched to `genome`. No checkout content was reset, stashed, staged, committed, merged, rebased, pushed, or deployed in this audit; fetches updated only remote-tracking refs.
