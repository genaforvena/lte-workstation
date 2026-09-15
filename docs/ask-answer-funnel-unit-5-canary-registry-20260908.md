# Ask-answer funnel Unit 5 — canary registry

Status: `READY`; registry published, no synthetic ask injected.

## Registry

| field | value |
|---|---|
| canary id | `ask-answer-funnel-unit-5-board-20260908-01` |
| trigger | explicit operator action only; never a reflex or timer |
| rate ceiling | at most 1 injected ask per 24 hours, and at most 1 outstanding canary |
| target | the live board's normal ask/answer path |
| synthetic marker | exact task marker `CANARY[ask-answer-funnel-unit-5-board-20260908-01]` |
| expected payload | harmless acknowledgement request; no operational mutation |
| measurement | opened timestamp, first answer timestamp, resolved timestamp, and UNKNOWN-safe denominator/age fields |
| stop rule | do not inject while Units 1–4 are not fully green or while another canary is outstanding |

## Honesty rule

The marker must remain in the task text and in the resulting ledger/chat evidence. A canary is
recognized after the fact only when its exact id is present in the source event, the answer/claim
chain, and the settlement record. Missing any link is `UNKNOWN`/failed evidence, never success.
Synthetic asks must not be counted as ordinary operator work or used to claim real workload
resolution.

## Current disposition

The registry is safe to use for a future explicit run, but no ask was injected in this turn. A fresh
deployed `/home/mesh-home/.local/bin/mesh-dash --test` completed `rc=0`; the earlier `rc=2`
node-condition remains historical Unit 4 evidence, not the current gate result. Injection remains
explicit-operator-only and was not requested here.

## Verification

- `bash tests/test-mesh-dash-ask-resolution.sh` — `rc=0`.
- `bash -n scripts/mesh-dash` — `rc=0`.
- `bash scripts/mesh-dash --test-fast` — `rc=0`.
- `timeout --signal=TERM --kill-after=10s 300s /home/mesh-home/.local/bin/mesh-dash --test` — `rc=0`,
  receipt `/tmp/unit5-deployed-full-final-20260908.out`, SHA256
  `a5961704f10e836ee4843a3ffa064e719542b7c5d211f923fcacc7a3bf50b215`.
- Wiring is present in `scripts/mesh-dash`: `render_ask_resolution` is called in the fused
  `witness|chat` path.
