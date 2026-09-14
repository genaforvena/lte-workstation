# MeshLand artifact intake — 2026-09-14

The genome checkout held a large parked delta at `refs/wip/genome` (`52f824ee`, snapshot
2026-09-14T08:50:05Z). The tree was still dirty when inspected. The default MeshLand scan found 304
settled candidates; the scheduled autoland log reported 239 held because no recent Genome completion
line supplied a concrete change description. That is a safe hold, but it leaves older work stranded
unless the steward returns to it.

The candidate enumerator also omitted untracked `docs/task-receipts/`, `docs/audits/`, and `tests/`,
plus tracked/staged test changes from its modified-path scan. That made finalized receipts, audit
evidence, and regression tests invisible to both landing and stranding reports. `scripts/mesh-land`
now includes the two write-once evidence lanes and queues both tracked and untracked test files as
repo-only candidates. Test files require steward verification because executing an arbitrary test
may touch live hardware; they never auto-run or deploy to `~/.local/bin`. Drafts and plan trees remain
excluded.

The enum regression fixture proves new receipts, audits, untracked tests, and modified tracked tests
are discovered; nested names resolve to the exact artifact; tests stay steward-held/repo-only; and
the existing draft/plan exclusions remain. It failed first on the missing receipt path and then on the
missing tracked-test path. Verification on the source tool: `bash -n scripts/mesh-land` passed and the
full `bash scripts/mesh-land --test` suite passed at 2026-09-14T09:29:57Z. Targeted dry-runs selected
exactly one path apiece for the source and this receipt. The source and this receipt
are queued for separate, path-limited `mesh-land --apply` operations after the settle gate, each with
its own concrete subject; no unrelated dirty paths are part of either landing.

Remaining work: the pre-existing dirty batch is not all landed. Genome must review the held
completion descriptions in semantic groups, land verified groups with concrete subjects, and retain
explicit dispositions for anything intentionally kept local. The new intake makes receipts, audits,
and tests visible to that reflex instead of silently omitting them.
