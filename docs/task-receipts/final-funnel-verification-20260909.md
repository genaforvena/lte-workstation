# Ask→answer funnel canonical final verification — 2026-09-09

Task: `ask-answer-funnel-implementation-20260907/final-funnel-verification`
Owner: `tg`
Take recorded before tests: `2026-09-09T19:07:30Z`, via `mesh-task take`.

## Result

The funnel-specific paths and task-ledger gates pass, but the canonical final
verification is **BLOCKED**, not DONE. The deployed full `mesh-dash --test`
returned `rc=2` with the honest node-condition that this node's fixed frame
floor is 28 rows and cannot fit the pinned 27-row pane cap. The focused dash
mutation arm also returned `rc=1`: the hanging `mesh-mind-state --watch` is
bounded at 2 seconds, but the complete `minds` fixture still exceeds the
test's 12-second outer fence because later allocation/live probes remain in
the frame. No source change was made in this verification turn and no canary
was injected.

## Verification evidence

Passed:

- `bash tests/test-ask-answer-funnel-unit-2-remove-inference.sh` — `rc=0`.
- `bash tests/test-mesh-witness-ask-metrics.sh` — `rc=0`.
- `mesh-task --test` — `rc=0`.
- `mesh-task-journal --test` — `rc=0`.
- `python3 tests/test-mesh-task-no-expiry.py` — 12 tests, `OK`.
- `bash scripts/mesh-dispatch --test` — `rc=0`.
- `bash scripts/mesh-claim --test` — `rc=0`.
- `python3 scripts/mesh-witness --test` — `rc=0`.
- `MESH_DASH_FAST=1 scripts/mesh-dash --once witness` — `rc=0`; live frame
  rendered `ask_open=7`, `ask_stale_h=58.9`, `ask_resolve=0.757`,
  `ask_den=272`, `ask_p90_h=58.0`, `ask_unknown=0` and showed the canonical
  step as `RUNNING`.
- Source/deployed SHA-256 parity:
  - `mesh-dash` =
    `17b51f07289e3c2864e8470397ddaa87a88a71de66660abe67a459a104e423e5`.
  - `mesh-witness` =
    `f1de8ccdaf7834404c4e6c7fec1e6cd9fb6fc6569196bbb2a9a6d862d7db0713`.
  - `mesh-dispatch` =
    `0b5b594293aeb74a3e43d80d461bda04e65ace1e9951a8798278b3a4dd82e421`.
  - `mesh-claim-shape.sh` =
    `69866ba249c85ae53b57a0f529f743bf65c61b21dbbfffde35a04ebe1ee2f950`.

Failed / unresolved:

- `bash tests/test-mesh-dash-ask-resolution.sh` — first ask-resolution and
  UNKNOWN assertions passed; the bounded hanging-watch mutation arm failed
  its 12-second outer fence (`minds frame did not complete`).
- `timeout --signal=TERM --kill-after=10s 300s /home/mesh-home/.local/bin/mesh-dash --test`
  — `rc=2`, node-condition only: pinned-pane cap 27 versus untrimmable floor
  28. The run did not report an ask-answer funnel assertion failure.

## Resume verification — 2026-09-09T18:54Z

The focused fence was repaired RED→GREEN. `tests/test-mesh-dash-ask-resolution.sh` first reproduced the 12-second failure under node load (`rc=1`), then passed after the `MESH_DASH_FAST=1` minds frame stopped running secondary quota/spend/budget/context probes and declared that bounded surface (`rc=0`, 7s). Source and deployed `mesh-dash` are identical again: SHA-256 `ba4a2cf298ce8e997dd5d5c16a6527db038f5dc2d2c7082bd7f9b7593b2aa9e3`.

The deployed full rerun completed within its 300s outer fence but remains n/a: `timeout --signal=TERM --kill-after=10s 300s /home/mesh-home/.local/bin/mesh-dash --test` returned `rc=2` after 155.42s. Its only n/a reason is still the live node's untrimmable check-frame floor of 28 rows versus the pinned 27-row cap. No funnel assertion failed. Terminal captures are `/tmp/focused-green.out` and `/tmp/final-funnel-deployed-rerun.out`; `mesh-task done` remains forbidden until a full `rc=0` is obtained on a fitting/quiet node or the pane condition is genuinely resolved.

## Exact next action

Resolve the node-specific pane-cap/fence condition (or run the full gate on a
node whose fixed frame fits the declared cap), then rerun the focused dash
mutation test and deployed full `mesh-dash --test`. Only a completed full
`rc=0` plus a green mutation arm permits `mesh-task done` for this step.

## Final closure verification — 2026-09-09T19:04Z

After the pane condition cleared, current source and deployed `mesh-dash` both measured a
26-row untrimmable floor against the pinned 27-row cap and retained SHA-256
`ba4a2cf298ce8e997dd5d5c16a6527db038f5dc2d2c7082bd7f9b7593b2aa9e3`.

- `bash tests/test-mesh-dash-ask-resolution.sh` — `rc=0`.
- `timeout --signal=TERM --kill-after=10s 300s /home/mesh-home/.local/bin/mesh-dash --test`
  — `rc=0`, `smoke-test: ok`.
- Full output: `/tmp/unblock-tg-deployed-full-mesh-dash.out`, SHA-256
  `a5961704f10e836ee4843a3ffa064e719542b7c5d211f923fcacc7a3bf50b215`.

All required final gates are green; this step is eligible for `mesh-task done`. No canary was
injected.
