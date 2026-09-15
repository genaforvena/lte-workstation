# Haunt external sample scope packet — 2026-09-12

- Adint resolver: `unblock/adint/8221abf248b868e3/resolve`
- Haunt resolver: `unblock/haunt/00559dad400ae1aa/resolve`
- Original task: `tinyfleet-architecture-drift-review-20260907/freeze-independent-repository-sample`

The live Haunt resolver remains blocked on an owner-authored protocol/plan amendment. The protocol
v1 registered pilot specifies two local repositories (`tiny-fleet`, `lte-workstation`), while D04
and the active sample task require at least three independent external repositories. The frozen
sample contains only `lte-workstation`; its analysis was not run. The existing receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-00559dad400ae1aa-resolve-20260912.md`
contains the supporting hashes and confirms this is a preregistration contract gap, not evidence
that external repositories are unavailable.

Exact prerequisite: the protocol owner must choose which scope governs, amend both plan and protocol
consistently, and freeze deterministic repository identities, licenses, snapshot pairs/windows, and
inclusion rules before comparative analysis. Then re-check and resume
`tinyfleet-architecture-drift-review-20260907/freeze-independent-repository-sample`. Adint must not
select a scope or edit the Haunt-owned contract on its behalf. No sample, protocol, or task state
owned by Haunt was changed.
