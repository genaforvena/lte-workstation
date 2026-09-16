# Pub measured-case draft receipt — 2026-09-16

## Provenance

- Source artifact: `docs/task-receipts/20260915T120000Z-140000Z-analyze-observation.md`
- Source SHA-256: `e5d1428f79f835acac530185813dfa43014218804c0a6fa64d803fc285f6d9dd`
- Selected repository commit: `46a1f50416f85d1444ee3bc286978697fa4fdaa0`
- Worktree: dirty; existing unrelated modifications and untracked artifacts remain.

The source receipt was read directly and reports 463 source rows/unique events, witness
UNKNOWN intervals, load 7.45–144.90, memory 22.5–69.9%, and no justified substrate
actuator. The draft preserves those claims and labels the missing attribution honestly.

## Artifact and disposition

- Draft: `docs/devto-measured-case-12-14-draft.md`
- Disposition: internal-only draft; no `mesh-devto-publish` call and no pre-push notice.

## Verification

```text
sed -n '1,280p' docs/task-receipts/20260915T120000Z-140000Z-analyze-observation.md
git rev-parse HEAD
46a1f50416f85d1444ee3bc286978697fa4fdaa0
git status --short
(non-empty; dirty worktree)
```
