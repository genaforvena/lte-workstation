# Pub measured-case provenance reconciliation — 2026-09-15

## Signal

The `pub` pane had only a `PUB DATA` header. The charter goal is to publish a measured
case with artifact-backed provenance and a pre-push board notice.

## Evidence

- Source artifact: `task-receipts/health-observation-analysis-20260915T110000Z-130000Z.md`
- Source SHA-256: `c8ad5ee000c0431c3dba0e689fe8d2707ba50c3e041dba6e353f9090e1055936`
- Selected repository commit: `8587a49108dbe96662ff6b4859485f9f4d388b1d`
- Worktree status: dirty; `git status --short` reported modified `AGENTS.md`, `CLAUDE.md`,
  `charter/pub.md`, multiple scripts/tests, and untracked task plans/receipts.

Commands run:

```text
sha256sum task-receipts/health-observation-analysis-20260915T110000Z-130000Z.md
c8ad5ee000c0431c3dba0e689fe8d2707ba50c3e041dba6e353f9090e1055936  task-receipts/health-observation-analysis-20260915T110000Z-130000Z.md

git rev-parse HEAD
8587a49108dbe96662ff6b4859485f9f4d388b1d

git status --short
(non-empty; dirty worktree)
```

## Disposition

The draft remains internal-only. It is not eligible for the irreversible pre-push notice
or `mesh-devto-publish` until a clean provenance choice is made. No external publication
was attempted.
