# Chat-range review backlog cleanup — 2026-09-15

At 2026-09-15T22:xxZ, the live producer had already created 89 open
`witness-chat-range-review-*` chains before the review cadence was changed from
every minute to `*/15` and the pending cap from 10 to 3. The producer was
correctly holding (`open_reviews=89`, `max_pending=3`), but all 89 remained
visible as witness labor.

Cleanup disposition: retain the three newest exact review chains and reject the
other 86 as stale producer backlog. The rejection is terminal ledger evidence,
not a claim that their source ranges were reviewed; the cadence change bounds
future production and the saved cursors remain unchanged. The retained chains
are:

- `witness-chat-range-review-medium-65922-66206/review`
- `witness-chat-range-review-medium-66207-66549/review`
- `witness-chat-range-review-medium-66550-66879/review`

Each rejected chain was first explicitly taken by `witness`, then rejected
through `mesh-task` with the reason: `stale producer backlog after the
2026-09-15 cadence/cap adjustment; source range remains unreviewed and is not
being silently counted as verified; retain only the newest bounded review
window.`

Verification target: the canonical ledger and derived journal report exactly
three open review chains; the producer remains held at the cap without moving
the cursors; `mesh-task audit` reports no malformed task state; and the live
pane shows the reduced unfinished workload.
