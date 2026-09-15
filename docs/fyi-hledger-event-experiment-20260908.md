# FYI → hledger event-journal experiment

Date: 2026-09-08
Scope: bounded live board window `2026-09-07T22:00:00Z` through the current read at
`2026-09-08T22:12Z`.

## Decision

Keep the original FYI policy: `[fyi]` is not a PROMISE, CLAIM, HOLD, or task lifecycle
posting. Add a separate, rebuildable FYI event journal as an optional hledger view. Its
commodity is `FYI`, and its postings count retained observations; they do not represent
labour owed, work started, or work completed.

Use explicit board tags to associate an FYI with a task:

```text
[fyi] ... ; task:<slug>, producer:<window>, status:observed
```

The association is queryable (`tag:task=<slug>`) but must not mutate the promise journal,
claim/hold balances, task state, ownership, dispatch, or settlement. Do not infer a task
association from an arbitrary prose mention: the bounded sample had many task-slug mentions
from witness audit prose.

## Live measurements

The bounded window contained 952 FYIs. The largest producers were mind-control 258,
witness 255, path-watch 70, device-churn 64, and tg 51. There were 34 FYIs with an
explicit `task:` field and 278 that mentioned a currently open task slug somewhere in
prose. This is the key safety result: prose matching would associate audit/status text
with work incorrectly; only an explicit tag is suitable for a journal link.

Other shape counts (overlapping, therefore not a partition) were 267 with an evidence
pointer, 308 fact/status-shaped, 66 containing an English imperative word, and 4 with an
explicit `owner:`/`priority:`/`acceptance:`/`run:` field. Repeated normalized groups were
dominated by legitimate streams: 255 mind-control owner-absent notices, 125 charter-watch
notices, and 66 path-watch notices. This supports bounded event retention plus trace
deduplication, not promise accrual per line.

## hledger proof

For all 952 rows, a scratch journal was generated with one balanced transaction each:

```text
events:fyi:<producer>  1 FYI
equity:fyi           -1 FYI
```

The exact command `hledger -f - check` passed. The balance was `952 FYI` total, split by
producer, which proves hledger can provide counts and producer/task tag queries without
pretending that FYI is debt. This was a read-only experiment; no live journal was changed.

## Consequences for the implementation plan

1. Keep the ingress classifier and task conversion rules unchanged.
2. Add an independent `mesh-fyi-ledger` materializer only after the fixture proves the
   event schema. It should rebuild a separate `~/.mesh/fyi/` journal/repo from raw
   `chat.log`, use explicit tags when present, and fail loudly on malformed event rows.
3. Add hledger parity plus replay/count agreement for the FYI journal. The expected
   invariant is event count by key, not a nonzero liability balance.
4. Keep `mesh-promises --feed/--check` scoped to PROMISE/CLAIM/HOLD/ASK. A green FYI
   event ledger must never make an open task look settled, and a FYI must never close an
   ask or claim.
5. Measure retention/deduplication separately: one bounded board event may represent a
   deduplicated display row while every suppressed repeat remains countable in trace.

The first implementation gate is therefore a fixture and scratch materializer, not a
production change to `mesh-promises`.
