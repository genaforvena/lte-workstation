# Senses live-state action — 2026-09-12

Consumed `mesh-dash --once senses`. The node had a partial perimeter (2/3 axes unreachable),
offline Wi-Fi/BLE vantage, stale organ markers, and a pending GPU-fan × stress relation whose
`[sense]` post was withheld pending `mesh-doctor`. The canonical `mesh-task queue --dispatch
--owner senses` returned no eligible owned rows.

## Action and evidence

The current doctor output confirmed default egress on `tailscale0`, a selected exit node
(`n2sbt7yy6t11CNTRL`), and a failing FYI ledger log. `ip route get 1.1.1.1` agreed with the first
finding. The FYI errors all named `chat.log:56425`, whose raw line has an interleaved timestamp and
author prefix before a complete later FYI event.

Updated `scripts/mesh-fyi-ledger` to salvage only that narrow interleaved-prefix shape while
recording its line number and publishing `coverage=partial`; the append-only chat source remains
untouched. Added a regression case in `tests/test-mesh-fyi-ledger.sh`.

- TDD red: the new fixture failed with `line 1: malformed FYI row` before the parser change.
- Green: `rtk bash tests/test-mesh-fyi-ledger.sh` passed.
- Live: `rtk mesh-fyi-ledger --build` produced 9052 events, `partial=yes`; the live manifest records
  `parse_gaps=1`, `parse_gap_lines=56425`, and `replay_parity=pass`.
- Live dash: `FYI view: events=9052 coverage=partial replay=pass`.

## Still open

The two route findings are substrate state and remain unchanged. The node had multiple other
Codex/doctor processes active, including the `vpn` mind, so no route ownership claim or routing edit
was made. The full doctor run started here was stopped after 10m37s when two other doctor scans were
found already active; its post-change full exit status is therefore unknown. Existing `[sense]`
stays withheld.

Next: when the concurrent scans clear, coordinate route ownership with the active VPN mind, inspect
the intended upstream/exit-node arrangement, resolve or explicitly disposition the two egress FAILs,
then run one complete `mesh-doctor`. Post the recorded `[sense]` only if that full run exits 0.
