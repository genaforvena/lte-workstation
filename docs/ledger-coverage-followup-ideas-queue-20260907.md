# Ledger coverage follow-up — ideas queue ownership

Date: 2026-09-07  
Owner: `genome`  
Ask: `tg-operator-ledger-coverage-20260907`

## Exact obligation and mapping

The witness finding named the promise liability
`liabilities:promises:genome:ideas-queue-escalations-wifi-rf-disposit` and reported that the
earlier ideas-queue dispatch had no owner `[taking]` receipt. The exact mapping is:

| observed obligation | owner receipt | closure artifact | verification |
|---|---|---|---|
| `ideas-queue-escalations/wifi-rf-disposition` | board `[taking]` at `2026-09-07T15:05:53Z`, owner `genome`, lease through `2026-09-07T15:35:00Z` | `docs/ideas-queue-coverage-20260907.md` | `mesh-task status ideas-queue-escalations` reports complete `4/4`; coverage artifact SHA-256 is recorded below |
| prior ideas-queue dispatch with no owner receipt | superseded by the exact owner receipt above; no second chain was created | same coverage artifact, which maps all 28 live rows and all four escalation steps | `mesh-promises --balance` no longer lists the named genome promise; `mesh-promises --check` and `mesh-promises --feed` are the ledger gates |

The earlier dispatch was therefore a routing/lifecycle observation, not an additional work item.
The existing completed chain is the single source of ownership and closure; duplicating it would
create a second, conflicting obligation.

## Verification run

At follow-up time:

- `mesh-task status ideas-queue-escalations` — PASS, chain complete, all four steps done and owned by `genome`.
- `sha256sum docs/ideas-queue-coverage-20260907.md` — PASS; expected hash:
  `1608b909cc2e35fcce6444ce4831c780eb7dca0a22c308451ad9804071092561`.
- `mesh-promises --balance` — PASS for this finding: no
  `liabilities:promises:genome:ideas-queue-escalations-wifi-rf-disposit` row remains.
- `mesh-promises --feed` — PASS for this finding: `unrouted=0` and no open promise row for the
  named liability.
- `scripts/mesh-ideate --test` — PASS; queue mapping remains non-mutating and valid.

The three expiring mutes and one diagnosis remain visible in the coverage artifact; the next
required action is the expiry recheck on `2026-09-14`, not a new duplicate dispatch.
