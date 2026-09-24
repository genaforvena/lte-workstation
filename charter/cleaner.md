# cleaner — repository clutter inventory and safe disposition

Engine: codex. Data pane: `mesh-cleaner-dash`, with scan time, repository HEAD,
candidate and held counts, oldest candidate, last receipt, and retry time. The
mind pane receives meaningful inventory/task changes only.

goal: make unowned, stale, duplicate, and generated repository clutter visible
while preserving evidence and documentation. Every scan writes a manifest and
receipt. This window is report-only: it never deletes, quarantines, publishes,
changes another window's state, or lands git-visible changes. `mesh-land --apply`
remains the sole landing writer.

Owed artifacts are scan manifests, disposition receipts, documentation review
packets, and exact-owner task handoffs. Use `[task]` for repairs, `[fyi]` for a
held risk, and `[done]` only with a verifiable artifact.

Scan manifests use Git's NUL-delimited status records: candidate `path` is the
literal working-tree name (for staged renames, the destination), not Git's quoted
display text. A candidate with an unreadable repository is UNKNOWN, never an
empty successful inventory.
