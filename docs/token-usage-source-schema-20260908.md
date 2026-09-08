# Token usage source schema (2026-09-08)

## Finding: current source boundary

The live lifecycle source is `~/.mesh/codex-lifecycle/<window>/*.json`, emitted by
`scripts/mesh-codex-lifecycle` (the deployed copy is `~/.local/bin/mesh-codex-lifecycle`).
The current event type is `agent-turn-complete`. A current event was inspected on this node;
its stable identity and attribution fields are:

```json
{
  "type": "agent-turn-complete",
  "thread-id": "01a07f4b-5a3d-7741-ade8-5354f05938ad",
  "turn-id": "01a07f4c-1ce8-7332-8ac3-fdb15918ee82",
  "cwd": "/home/mesh-home/lte-workstation",
  "client": "codex-tui",
  "window": "hire",
  "received_at": 1788842122.9781625,
  "status": "cleared"
}
```

The source event currently has no structured provider usage object. The fields
`input-messages` and `last-assistant-message` are lifecycle bookkeeping/content and are not a
token source. Transcript length, rendered `/status`, terminal text, and mesh accounting events
must therefore never be used to estimate token values.

## Normalized turn row

One row represents one provider turn, using the lifecycle identity
`event_key = engine + ":" + thread_id + ":" + turn_id`. `window` is attribution only and is
not part of the deduplication key.

```json
{
  "schema_version": 1,
  "event_key": "codex:01a07f4b-5a3d-7741-ade8-5354f05938ad:01a07f4c-1ce8-7332-8ac3-fdb15918ee82",
  "observed_at": "2026-09-08T09:00:00Z",
  "engine": "codex",
  "provider": "openai",
  "model": null,
  "thread_id": "01a07f4b-5a3d-7741-ade8-5354f05938ad",
  "turn_id": "01a07f4c-1ce8-7332-8ac3-fdb15918ee82",
  "window": "hire",
  "usage": {
    "total": null,
    "input": null,
    "cached_input": null,
    "output": null,
    "reasoning": null
  },
  "source": {
    "total": "missing",
    "input": "missing",
    "cached_input": "missing",
    "output": "missing",
    "reasoning": "missing"
  },
  "parser_version": "token-usage-source-schema-20260908.v1"
}
```

When the source event contains neither `observed_at` nor `received_at`, the normalized
`observed_at` is `null`; the recorder must not manufacture a wall-clock value because that
would make replay of the same event appear to conflict.

Token values are non-negative integers or JSON `null`. `null` means “not observed”; it is never
rendered as zero. Each usage field has an independent source state:

| source state | Meaning | Permitted value |
|---|---|---|
| `provider` | Explicitly present in the structured provider usage payload | integer |
| `computed` | Derived only where the schema explicitly permits it | integer |
| `missing` | Source event has no such field | `null` |
| `unavailable` | Source was present but could not be read/decoded | `null` |
| `invalid` | Field was present but failed validation | `null` |

Field semantics:

- `input`: provider-reported prompt input tokens excluding cache hits when the provider defines
  that distinction; never derive from text.
- `cached_input`: explicitly reported cache-hit detail. It is a subset/detail of input, not an
  additional quantity.
- `output`: provider-reported generated output tokens. Reasoning is included here when the
  provider defines reasoning as an output detail.
- `reasoning`: explicitly reported hidden reasoning detail; never add it to output or total.
- `total`: provider total when supplied. A computed total is allowed only when both `input` and
  `output` are present, and must be marked `computed`; cached/reasoning are never added again.

An absent `thread-id` or `turn-id` is an identity failure: quarantine the event rather than infer
identity from timestamps. A missing `window` remains unattributed. Raw usage-bearing input may be
retained by the recorder for replay, subject to its privacy whitelist; message bodies are not part
of this schema.

## Policy boundary

This artifact defines observation-only telemetry. No control-plane reads, thresholds, gates,
budgets, alerts, routing, scoring, prioritization, stopping, or slowdown may consume these values.
Reconciliation results are informational and must not affect completion callbacks or agent work.

## Bounded delivery canary receipt (2026-09-08)

The delivered request was received and started by the `genome` owner: the exact child task
`recreated-rejected-20260908-02-genome-canary/delivery-canary` is recorded as `active` in the
canonical task-chain state, with `started=2026-09-08T11:33:04Z`. This canary inspected the current
source-schema target only; it did not replay historical payloads.

Exact verification command and output:

```text
COMMAND=test -s docs/token-usage-source-schema-20260908.md
RC=0
```
