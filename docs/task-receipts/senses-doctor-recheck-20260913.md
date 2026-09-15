# Senses doctor recheck — 2026-09-13

Resumed the occupancy-fusion gate after the prior `mesh-doctor` invocation stalled. A fresh bounded
`rtk timeout --signal=TERM --kill-after=30s 15m mesh-doctor --quiet` completed normally in 8m46s
(exit 2); it did not need the timeout. The long run was the comprehensive smoke suite, which emits
most findings only after serial-confirm and source-census work finishes.

The live doctor result was **2 FAIL, 33 WARN**. The two FAILs remain egress via `tailscale0` and the
configured exit node `n2sbt7yy6t11CNTRL`; both are routing/substrate-owned, so this senses pass made
no routing change. The census reported 93 stable unwired/non-canonical orphans, confirmed across
2+ checks. The live orphan ledger does not list `mesh-occupancy-kind` or `mesh-social-fusion`, so
this fusion work introduced no new orphan warning. The doctor is still not clean, and the `[sense]`
publication remains withheld under the existing gate.

The final doctor line also reported serial-confirm coverage 2/161, 16 carried FAIL(stale), 158
stale-verdict, and 1 never-assessed. Those are coverage limits, not new live FAIL confirmations.

Next: the VPN/substrate owner must disposition the two egress FAILs; then senses can rerun
`rtk mesh-doctor --quiet` and publish `[sense]` only if the doctor exits 0 and the census adds no
new orphan warning.
