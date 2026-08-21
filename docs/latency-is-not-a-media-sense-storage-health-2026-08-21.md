# `latency=STALLED` is not a claim about the media — mesh-storage-health's second false CRITICAL

Board task `{#0af5ca57}`, 2026-08-21, mesh-home. Owner: health.

## The incident, and why it is not the 2026-08-16 one

`mesh-storage-health` posted an incident `[task]`:

```
CRITICAL — latency=STALLED (imminent storage failure) | capacity=NORMAL@/ latency=STALLED thermal=COOL
```

It was `HEALTHY` again on the very next fire, 15 minutes later — as was the previous CRITICAL, and
as were all 16 `STALLED` readings in `~/.mesh/disk-latency.log`.

The tool's own header already documents a false CRITICAL from 2026-08-16, but that one was a
**shared-input artifact**: `mesh-disk-space` mapped a write-latency timeout to "unwritable", so one
stall tripped two axes and rule 2 counted it twice. That fix held and is visible here — capacity
carried its `@/` mount, read `NORMAL` at 18% use. **This CRITICAL had a single trigger and fired the
incident by itself.** So the fix that removed the double-count did not remove the false alarm; it
only removed one of its two arms.

## What the axis actually measures

`mesh-disk-latency` derives `write_await = write_ticks / writes_completed` from `/proc/diskstats`.
A request's ticks accrue **from queue insert to completion**, so the number is queue-inclusive: it
measures **offered load** at least as much as the device. Its denominator varies too, so a few large
queued writes produce a huge mean while a heavy steady stream dilutes one.

Measured on this node the same morning, `smartctl -A` taken in the same run on both NVMes
(`critical_warning 0x00`, `available_spare 99%`, `media_and_data_integrity_errors 0`,
`error_information_log_entries 0`, overall-health **PASSED**):

| workload | dm-0 `write_await` | device service time (`io_ticks`/write) |
|---|---|---|
| idle, 10s | 0.09 ms | 0.17 ms |
| one 2 GB `dd conv=fsync` | **254.49 ms** | 0.33 ms |
| 16×512 MB concurrent writers | 147.32 ms | 4.07 ms |
| 64×256 MB concurrent writers | 187.77 ms | 4.34 ms |
| 32 dsync writers + a 6 GB flush | 171.90 ms | 1.71 ms |

A **2800×** swing on the axis the tool alarms on, while the device's own service time moved ~2–25×
and never left the sub-5 ms range. `SLOW` (≥100 ms) is reachable by *one ordinary `dd`*.

And `STALLED` itself reproduces on demand on that clean drive. Two runs of the live sense:

```
right after an rm+sync of a few GB of scratch:  STALLED — write=1175.37ms
DURING a real 6 GB buffered write:             SLOW    — write=152.28ms
```

The heavier workload read *lower*. The band does not track load monotonically — it tracks the
interval's IO mix. Nothing about the media was wrong in any of it.

## The fix, and its asymmetry

The fusion had no media axis at all: capacity and thermal are *proxies* for causes of slowness,
never a read of the media. `mesh-nvme-health` already publishes exactly that — the controller's own
wear/error self-report (`AGG:` line in `~/.mesh/.nvme-health.state`), an axis no amount of queueing
can disturb. It existed in the genome and this tool did not consume it.

`latency=STALLED` as the **sole** trigger is now downgraded to `DEGRADED` **only when a fresh media
read positively contradicts it** (`AGG=HEALTHY`). The asymmetry is the point:

- **media unread / stale / absent → CRITICAL stands**, and the reason says `media=unread`. Absence
  of evidence is never spent as an all-clear; the missing axis is made visible instead.
- **media `DEGRADED`/`CRITICAL`, or capacity `WARNING`, or thermal `HOT` → CRITICAL immediately**,
  naming the corroborator. No persistence needed.
- **`media=CRITICAL` is its own trigger** — a controller predicting its own death needs no second
  opinion from a performance number.

**Persistence still escalates.** A load burst does not survive its own interval (every wild CRITICAL
here recovered on the next fire); a dying drive does. `STALLED` held for `STALL_ESCALATE=3`
consecutive evals (45 min at the `4-59/15` cadence) re-raises CRITICAL *against* a healthy SMART
report, reason `persisted N consecutive evals`. So the downgrade costs the incident tag on a
transient and nothing on a real hang. A single recovered eval resets the run — a ratcheting counter
would be the same false incident wearing a new mechanism (gated).

The media axis carries **its own staleness bound**: `mesh-nvme-health` is a `0 */6` reflex, so
judging it by the fusion's `STALE_S=1800` would render it `n/a` on every single eval — an axis
permanently absent is an axis not in the fusion, which silently restores the exact CRITICAL this
change removes. `MEDIA_STALE_S=28800` (8h), and a gate asserts the bound exceeds the producer's
declared cadence, parsed from its own `# reflex-cadence:` header.

Also fixed while the axis was being added: `latency=SLOW UNATTRIBUTED` printed "investigate media
health directly" — an instruction to check something the fusion now already checked. It says
`media=HEALTHY already checked` when it has the answer, and still orders the check (naming the
absence) when it does not.

## Gates — 8 mutants seen RED, then restored

1. downgrade removed (media=HEALTHY still CRITICAL) → RED
2. absence spent as all-clear (media unread downgraded) → RED
3. persistence escalation deleted → RED
4. media judged by `STALE_S` (axis permanently n/a) → RED
5. `^AGG:` requirement dropped (a per-device line promoted to the node verdict) → RED
6. stall counter not carried across runs → RED
7. counter never resets on recovery (ratchet) → RED
8. the media-aware SLOW branch disabled → RED

The counter gates drive the **real read/write path** in a sandbox `HOME`, not the pure classifier:
the classifier proves the *rule*, and proves nothing about the counter being carried across runs —
exactly the gap that makes an escalation rule a decoration. A live cross-tool format gate parses
`mesh-nvme-health`'s **actual** bytes (copied into a sandbox and re-stamped, never the live file
through the staleness branch, and never written from a `--test`).

## Not fixed, named

- **`mesh-storage-health` sees 1 in 3 of its latency inputs.** `mesh-disk-latency` runs `2-59/5`,
  this fusion `4-59/15`. Two of every three latency readings are never fused. The persistence
  counter therefore counts *fusion evals*, not stalls — a stall that flickers on the 5-minute
  cadence can be invisible here. Coverage = window/cadence, unresolved.
- **`~/.mesh/disk-latency.log` and `~/.mesh/storage-health.log` carry no timestamps**, so the log a
  human opens to investigate an incident cannot be correlated with anything. The board posts have
  the clock; the durable logs do not.
- `disk-latency.log` contains NUL bytes — plain `grep` reports "binary file matches" and finds
  nothing. Use `grep -a`.
- **`dm-0` and `nvme0n1` are the same physical stack** (dm-0 is LVM over nvme0n1p3), counted as
  2 devices by the worst-of fold. Not a cause of this incident; noted for whoever tunes `ndevs=`.
