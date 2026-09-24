# cleaner — repository clutter inventory and safe disposition

Engine: mishe-tauftauf with a tool-free omp reviewer. Data pane:
`mesh-mishe-cleaner-run watch` renders the live scanner, matching dry-run
settlement, checked review, task holds, and System Zero result. Start or
repair only this window with `scripts/mesh-mishe-cleaner-run ensure`.

goal: make unowned, stale, duplicate, and generated repository clutter visible
while preserving evidence and documentation. Every scan writes a manifest and
receipt. This window is report-only: it never deletes, quarantines, publishes,
changes another window's state, or lands git-visible changes. `mesh-land --apply`
remains the sole landing writer.

Owed artifacts are scanner manifests, dry-run disposition receipts, and
source-linked review packets covering every current candidate. A cleaner-owned
task stays visibly held until an exact-owner task path is installed; this Mind
does not claim, settle, or post tasks or board messages.

Scan manifests use Git's NUL-delimited status records: candidate `path` is the
literal working-tree name (for staged renames, the destination), not Git's quoted
display text. A candidate with an unreadable repository is UNKNOWN, never an
empty successful inventory.
