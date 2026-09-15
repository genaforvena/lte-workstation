# Ledger/dispatch flow analysis — 2026-09-09

## Flow

`chat.log` is the source tape. `mesh-task-journal` replays structured task records into
`~/.mesh/tasks.journal`; `mesh-task audit` classifies current steps as `DONE`, `REJECTED`,
`BLOCKED`, or `QUEUED`. `mesh-dispatch` then reads the claimable task queue, obtains the live
staffing census, checks the mind state, and routes at most one task per pass. A dispatch is not a
claim: the owner must emit `[taking]`, then `[progress]`/`[done]` with an artifact.

## Evidence before the fix

At 2026-09-09T17:36Z:

- Source replay: 42,301 events, 339 task rows, 144 unfinished, 26 rejected, 169 done.
- The unfinished set was 23 genuinely blocked current steps plus 121 queued successor steps;
  `mesh-task queue --dispatch` was empty. This is a blocked dependency graph, not a parser loss.
- `mesh-mind-control --status` showed the non-protected windows idle, but `mesh-staffing` saw
  59 open holds, 55 marked leaked, and 92 open promises, 63 leaked.
- The old staffing predicate treated every open hold/promise as current ownership. Only `wake`
  therefore entered the dispatch pool; the other idle minds were excluded before routing.
- `MESH_DISPATCH_NO_PACE=1` was already active, so the spend governor was not the cause of the
  dispatch slowdown.

## Changes

`scripts/mesh-staffing` now preserves total open counts but separately reports active and leaked
counts. Only active holds/promises exclude an otherwise eligible idle mind. A row with leaks is
eligible with reason `eligible-with-leaks`, making the debt visible while preventing historical
leaks from becoming a permanent capacity lock. Protected, human-owned, communication, and active
ownership exclusions remain unchanged.

`scripts/mesh-pace` now uses a 60-second cache only for report-mode labor-meter reads. Gate and
`--check` paths remain live and uncached. This prevents the dashboard's derived pace views from
re-running the expensive labor replay several times in one report.

## Verification

- `bash tests/test-mesh-staffing.sh` — PASS.
- `bash tests/test-mesh-staffing-hyphen-heading.sh` — PASS.
- `bash tests/test-mesh-tg-dispatch-policy.sh` — PASS.
- `python3 -m py_compile scripts/mesh-staffing` — PASS.
- Live staffing changed from one idle candidate to six (`adint`, `haunt`, `hire`, `job`, `senses`,
  `wake`); `witness` is also eligible with visible leaks. Active/protected lanes stayed excluded.
- Live `mesh-dispatch --status` now reports six idle workers and zero claimable tasks. The zero is
  explained by the audit's blocked/queued dependency state, not by staffing starvation.
- Source/deployed parity is preserved because both commands resolve to the repository scripts.

## Remaining obligation

The 23 `BLOCKED` steps require their named operator/external events or prerequisites; the 121
`QUEUED` successors must remain parked until their current predecessor advances. The next useful
action is to re-audit after an owner claim or prerequisite event, not to fabricate dispatchable
work.
