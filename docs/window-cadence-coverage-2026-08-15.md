# Window/cadence coverage sweep — scheduled senses

**2026-08-15 · senses@mesh-home · task:window-cadence-aliasing-sweep**

A reflex's coverage is its sampling **window** divided by its **cadence**. Nothing in a green
`--test`, a fresh mtime, or an honest reading exposes the ratio — `mesh-psi` read a 10s kernel
average once per 600s (1.7% of wallclock) and reported CALM for 14.2 days on a measurably
STALLED node (fe35dd9). This is the sweep of the rest.

277 tools carry a `# reflex-cadence:` header. Most are actors, checkers or level-readers, where
sampling is legitimate: **a LEVEL is a state** (disk space free, battery %, a mode bit) and reading
it at an instant is a true claim. The aliasing bites only where the quantity is **bursty/transient**
*and* the reading is consumed as a claim about the interval. That is the class swept below.

## Method note — two false leads, both worth recording

1. **`sleep 1` in the file is not `sleep 1` in the live path.** A mechanical grep put
   `mesh-gpu-activity`, `mesh-package-power` and `mesh-cstate` on the offender list; in all three the
   matched sleep sits *inside* the `--test` block. They do sample narrowly in the live path too (via
   `SECS`), but the grep that "found" it was not evidence — it was a coincidence at the wrong line.
2. **100% coverage can still be blind.** `mesh-disk-latency` reads an accumulator over its whole
   life — nominally perfect coverage — and is the worst offender in the sweep, because the
   *denominator* only grows. Coverage and dilution are different axes; the task's ratio test does not
   catch this shape at all. See below.

## The table

Verified by reading the live path and, where marked ✓measured, by driving the hardware.

| tool | cadence | read window | coverage | accumulator available | verdict |
|---|---|---|---|---|---|
| **mesh-diskio** | 600s | 1s in-run delta | **0.17%** | ✓ `/proc/diskstats` (already read!) | **FIXED** ✓measured |
| **mesh-disk-latency** | 300s | since-boot mean | 100% but diluted | ✓ same file | **FIXED** ✓measured |
| mesh-package-power | 300s | 2.0s in-run | 0.67% | ✓ RAPL `energy_uj` | offender — filed |
| mesh-cstate | 300s | 2.1s in-run | 0.70% | ✓ cpuidle `usage`/`time` | offender — filed |
| mesh-swap-rate | 300s | 3.0s in-run | 1.0% | ✓ `/proc/vmstat` pswpin/out | offender — filed |
| mesh-fitness | 540s | PSI `avg10` | **1.85%** | ✓ `total=` in `/proc/pressure` | offender — filed |
| mesh-load-audit | 120s | 0.3s CPU-ticks | 0.25% | ✓ `/proc/stat` | offender — filed |
| mesh-doctor | 3600s | PSI `avg10` | 0.28% | ✓ `total=` | mitigated — has a second, level-based axis (swap/MemAvailable exhaustion) that carries the claim when PSI reads calm |
| mesh-mem-guard | 120s | PSI `avg10` | 8.3% | ✓ `avg60`/`avg300` in the same line | minor — PSI only *corroborates*; primary axis is MemAvailable%, a level |
| mesh-resource-guard | 120s | PSI `avg10` | 8.3% | ✓ same line | minor — same shape, corroborator only |
| mesh-swap-drain | 3600s | PSI `avg300` | 8.3% | — | **correct as written** — it is a *precondition* gate ("don't fight the kernel mid-stall"); it wants "right now", not the interval mean |
| mesh-gpu-activity | 300s | 2.0s in-run | 0.67% | ✓ RC6 residency | **n/a on this node** — exits 2 UNREACHABLE (no Intel iGPU; this box is NVIDIA) |
| mesh-pressure | 300s | `avg300` + `total=` | **100%** | uses it | clean — the model to copy |
| mesh-kbd-activity | 300s | across-run delta | 100% | uses it | clean |
| mesh-cpu-throttle | 300s | across-run delta | 100% | uses it | clean |
| mesh-psi | 600s | inst + interval | 100% | uses it | clean (fe35dd9) |
| mesh-psi-memory | 600s | avg10/60/300 | 100% | uses it | clean |

`mesh-conntrack-load`, `mesh-net-drop`, `mesh-wakeup-attrib`, `mesh-vram-watch`, `mesh-cpufreq`,
`mesh-cpu-avgfreq` carry across-run state; their state files hold *edges/verdicts*, and whether each
needs a counter carry is per-tool — not swept here rather than guessed at.

## The two fixes

### mesh-diskio — 1s per 600s, and the accumulator was already in its hands

It read `/proc/diskstats` **twice, 1s apart**, and threw the counters away. Measured on this node,
**at the same instant**:

```
INTERVAL(60s accumulator delta): read=202 KB/s write=77403 KB/s util=61.1%
1s sample at the same moment:    read=136 KB/s write=60    KB/s util= 0.1%
```

A 600x error on write throughput, and the verdict flips IDLE↔PRESSURED. Sampling the same disk
1s at a time across 120s gave util = **0%, 0%, 3%, 96%, 90%, 95%** — the tool publishes *one* of
those per 10 minutes as the interval's state. Its own log: **2119 IDLE / 8 PRESSURED** in 2391 runs,
on a disk that sustains 77 writes/s.

Fixed by carrying the raw counters in the state file (`|raw=<epoch> …`) and delta'ing across runs.
Both windows are kept — the interval mean dilutes a sharp spike, the instantaneous one misses
everything between ticks — folded with a max that **names its winner**, and the coverage is published
*in* the reading:

```
[diskio] IDLE — … | window=inst      inst=0%   iv=na%  won=inst | disk=dm-0   ← run 1, no baseline
[diskio] PRESSURED — … | window=inst+iv inst=100% iv=32% won=inst | disk=dm-0   ← run 2
```

### mesh-disk-latency — the alarm bands had decayed to unreachable

It banded on `read_ticks / reads_completed` straight from `/proc/diskstats` — the mean await
**since boot**. Coverage is nominally 100%, which is exactly why a ratio test misses it: the
denominator only grows, so the reading is diluted toward immovable. Measured on dm-0 (1.3d uptime,
19.9M writes accumulated):

- a 90s window moves the cumulative mean by **0.035%**
- dragging it from 27.35ms to the SLOW threshold (100ms) needs **10.5 hours** of sustained
  600ms-await storm
- reaching STALLED (500ms) needs **340 hours**

Both alarm bands are effectively unreachable, and they get **more** unreachable the longer the node
stays up. A sense that cannot alarm, reporting NORMAL forever, with a green `--test` and a fresh
mtime. Live proof, two runs 40s apart:

```
run 1 (cumulative only, the old behaviour): NORMAL — write=28.92ms  window=cum
run 2 (with the interval window):           SLOW  — write=354.81ms window=cum+iv won=iv
```

`storage-health` now reports `latency=SLOW`, a value the old sense could not produce.

## Rules this sweep earned

- **Missing evidence renders `na`, never 0.** No baseline (first run), a counter that went backwards
  (reboot/reset), a baseline past max-age, a garbage state field — each returns `na`. A reset
  counter differenced into `0` is a fabricated calm.
- **Publish the coverage in the reading** (`window=inst+iv` / `window=cum`) so a consumer cannot
  mistake the narrow claim for the wide one.
- **A max fold must name its winner** — `won=cum` reads as a *historical* alarm, `won=iv` as a live
  one. A max that hides its disjunction turns those into the same sentence.
- **Computing a window is not consuming it.** Both fixes carry a gate that seeds a loud interval and
  asserts the *verdict* moves — without it a tool can compute a perfect interval, print it, and still
  classify off the other window.
- **Coverage ≠ dilution.** A since-boot mean has perfect coverage and no sensitivity. Ask both
  "what fraction of the interval did I observe?" and "can a full interval of the alarm condition
  actually move this number?"

## Gates seen RED

Every gate was broken and watched fail before being trusted.

| mutation | gate that caught it |
|---|---|
| diskio: drop the `raw=` carry | `run 2 reported window=inst — the accumulator is NOT carried across runs` |
| diskio: missing baseline → 0 not na | `no baseline (first run) → '0 0 0 0' (expected na — 0 would be a fabricated calm)` |
| diskio: fold stops naming its winner | `fold_util 10 60 → 60 inst (expected '60 iv')` |
| diskio: verdict rides the 1s sample again | `fused util=81 but state=IDLE — the verdict does not ride on the fused axis` |
| disk-latency: band on cumulative only | `seeded a ~60000ms interval write-await; expected STALLED won=iv, got NORMAL … won=cum` |
| disk-latency: stop carrying counters | `run 2 did not widen to cum+iv` |
| disk-latency: accept a stale baseline | `baseline far past max-age but window='cum+iv won=iv'` |
| disk-latency: drop the reset guard | `torn counter reset … the window claimed 'cum+iv'` |

The last one is the one worth keeping. The **first** version of that gate seeded an
all-counters-AHEAD baseline and passed with the guard deleted — the plain `delta > 0` check catches
that case on its own, so the gate asserted nothing. Only a **torn** reset (completed-count behind,
ticks ahead) reaches the guard. A gate written against the obvious fixture can be vacuous against
the subtle one, and the only way to find out is to break the code and watch.
