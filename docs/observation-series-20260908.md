# Materialized observation series

Date: 2026-09-08  
Task: `autopoiesis-observation-windows-20260908/materialize-observation-series`  
Owner: senses

## Result

The reusable dataset is [observation-series-20260908.tsv](observation-series-20260908.tsv).
It materializes the verified 10:00:00–12:00:00Z window in eight aligned 15-minute
rows. The interval is half-open (`[window_start, window_end)`), UTC, and counts
source rows; a missing source is coverage loss/UNKNOWN, not a zero reading.

## Schema

| field | meaning |
|---|---|
| `window_start`, `window_end` | UTC interval boundary; fixed 15-minute bins in this artifact |
| `chat_rows` | all timestamped rows read from `~/.mesh/chat.log` |
| `health_observation_rows` | rows in that source window emitted by `health@*`; activity count, not a health score |
| `witness_rows` | timestamped rows from `~/.mesh/witness.log` |
| `sensor_rows` | timestamped rows from `~/.mesh/sensors.log` |

For a future producer, preserve `source`, `node`, `observed_at`, `value`,
`status` (`OK`, `UNKNOWN`, `HOLLOW`), `rc`, and `producer_observed_at` at event
level; aggregate rows must retain `n_seen`, `n_expected`, and `coverage` per
source. Correlation uses overlap of live axes only. Generated task-ledger
replays and tmux text are not health measurements.

## Coverage proof

The TSV contains 8/8 bins and 100% chat coverage. `sensors.log` contributes
9/9 rows per bin (72/72 overall), and `witness.log` contributes 7–8 rows per
bin (60/60 overall). The two logs therefore cover the complete requested
window; the counts are independently reproducible with timestamp filtering:

```sh
awk '$1 ~ /^2026-09-08T(10|11):/' ~/.mesh/sensors.log
awk '$1 ~ /^2026-09-08T(10|11):/' ~/.mesh/witness.log
```

`health_observation_rows` is deliberately allowed to be zero: that means no
health observation row was emitted in that bin, not that health was all-clear.
The health-state tape is a rendered state snapshot without a stable
per-observation timestamp and is inventory-only here, not silently promoted
to a time series.

## Retention limits measured live

| source | live extent / limit | interpretation |
|---|---|---|
| `~/.mesh/sensors.log` | 51,430 rows; 2026-07-14T22:33:01Z–2026-09-08T12:20:21Z | about 55.6 days currently retained; append-only, but no explicit size/age policy found |
| `~/.mesh/witness.log` | exactly 5,000 rows; 2026-08-28T14:48:04Z–2026-09-08T12:20:13Z | about 11.9 days; bounded row ring, horizon moves with cadence |
| `~/.mesh/chat.log` | 37,690 rows; 2026-06-12T22:40:02Z–2026-09-08T12:20:32Z | about 87.6 days in the current file; durable board history, not a typed sensor tape |
| `~/.mesh/health-state.log` | 146,244 lines; first line is an un-timestamped rendered header | cannot prove event retention from this file; use timestamped health board rows or add an event tape |
| tmux `mesh-home` scrollback | 16 windows / 31 panes; 3,129 capturable lines now, largest pane 1,624 | volatile current-session context; no stable event timestamps and no reboot retention guarantee |
| `~/.mesh/board-snapshots/` | latest snapshot ends 2026-09-08T12:00:28Z; files are periodic copies with uneven gaps | snapshot history is a recovery aid, not the canonical event stream |

Consequences: a two-hour analysis is covered today, but a request older than
the shortest relevant horizon (currently witness, about 11.9 days) is
UNKNOWN unless another durable artifact covers it. A reboot invalidates tmux
scrollback by design. The series must report per-axis overlap and freshness;
one aggregate “health” value would erase these limits.

## Verification

Live checks on 2026-09-08T12:20Z: `mesh-task status` showed this step open,
`mesh-task take` succeeded, source row counts and first/last timestamps were
read directly, the 8-bin totals above were independently computed from the
three timestamped tapes (595 chat rows, 45 health-actor rows, 60 witness rows,
72 sensor rows), and `tmux list-panes` confirmed 16 windows/31 panes.
No claim is made that the current health-state snapshot is a retained series.
