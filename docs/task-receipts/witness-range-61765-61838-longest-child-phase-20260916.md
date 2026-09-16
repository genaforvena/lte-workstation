# Witness corrective receipt: longest observed child phase

Task: `witness-chat-range-review-near-61765-61838-longest-child-phase-corrective/record-longest-child-phase`
Checked: 2026-09-16T08:17Z UTC on `mesh-home`

## Acceptance field

`longest_observed_child_phase: UNKNOWN`

The producing receipt records the natural `mesh-doctor --cron` invocation from
2026-09-14T03:23:01Z through completion at 2026-09-14T03:32:09Z (9m08s), with
final `2 FAIL, 34 WARN` and a sampled parallel smoke-test fanout peaking at
1,171 processes. Its process-tree samples identify child commands, but neither
the observer nor `~/.mesh/doctor.log` emits phase names or per-phase start/end
timestamps. Therefore no child phase can be selected as longest without
inventing evidence.

## Evidence inspected

- Source review: `docs/chat-range-reviews/witness-chat-range-review-near-61765-61838.md`.
- Producing receipt: `task-receipts/health-doctor-next-slot-20260914-observation.md`.
- Canonical source lines: `~/.mesh/chat.log:61767` and `~/.mesh/chat.log:61836-61838`.
- Canonical task state: `mesh-task status witness-chat-range-review-near-61765-61838-longest-child-phase-corrective` showed the owned step active after the exact-owner take.

## Honest retry edge

Retry only on a future naturally scheduled doctor run after the observer or
doctor output exposes phase identity plus bounded phase durations. Do not infer
the phase from process-tree depth, command name, CPU percentage, or total run
duration; do not start a competing doctor aggregate.

No routing, DNS, firewall, VPN, service, or other substrate state was changed.
