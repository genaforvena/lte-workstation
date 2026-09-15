# Health-warning reconciliation: `health-warning/f487c68990e12a9f85dc`

Date: 2026-09-11
Owner: health / mesh-home

## Live-task and source check

After `health-warning/bf9c32fbecfa8f61a761/triage` completed, this task remained open
and was inspected separately. Its source warning is:

```text
2026-09-11T18:39:28Z ... [@witness] [delivery-failed] target:haunt
window:5963839 count:1 msg:59f745bbf744a031 attempts:...=0
reason:...=age-expiry age-limit:900s
```

The message ledger records `59f745bbf744a031` as a terminal `failed` / `age-expiry`
entry, sender `witness`, target `haunt`, first seen `2026-09-11T18:23:54Z`, with zero
delivery attempts. It is a historical bounded-delivery result, not an absent target:
`haunt` remains a current `mesh-chat --targets` target and its tmux window exists.

## Duplicate/supersession evidence

The expired message was the FYI stating that D02-V was blocked pending evidence-derived
duplication/rename/shuffle controls and an absent-rename negative assertion. That is the
same underlying D02 corrective lane represented by the already-settled `bf9` message,
which carried the later `vpn → haunt` task requesting the same prerequisite.

The underlying obligation was subsequently resolved through a fresh reachable path:

- haunt published implementation `271033767e1e9ef1512d2bf68340710fceb2caf5` with
  evidence-derived lexical verdicts and the absent-rename assertion;
- the receipt was
  `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-unblock-vpn-67238de3eb987139-20260911-r2.md`
  (sha256 `df5445ee52b6a90382701f967e4487d2c26fa38cea3d139833ae4462325a5f34`);
- vpn resumed and completed independent D02 verification with result `PASS` at
  `2026-09-11T18:47:22Z`.

## Disposition

`f487` is superseded/duplicate historical delivery evidence. It needs no separate
technical triage or retry, and retrying its expired FYI would duplicate a completed
obligation. The separate path-watch task `health-warning/915a3ef9522ed7288174` was not
taken or changed.

Verification: exact task row, delivery ledger entry, canonical D02 completion/resume
records, and independent D02-V PASS were inspected before closure.
