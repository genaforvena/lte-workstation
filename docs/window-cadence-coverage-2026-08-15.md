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

---

# The narrow-window accumulator family — the other five

**2026-08-15 · senses@mesh-home · task:narrow-window-accumulator-family**

The five tools the sweep filed. One shared idiom in all of them: *read counter, sleep N, read
again, store the verdict, throw the counters away* — while the counter itself was a monotonic
accumulator whose across-run delta covers 100% of the interval for free. All five now carry the raw
counters in their state, keep BOTH windows, fold with a max that **names its winner**, publish
`window=inst+iv` in the reading, and render `na` (never 0) on an absent, reset, cross-domain or
stale baseline.

| tool | was | now |
|---|---|---|
| **mesh-swap-rate** | 3 s / 300 s = **1.0%** of `/proc/vmstat` pswpin+pswpout | `window=inst+iv`, `pps_inst`/`pps_iv`/`won`, `raw=` carry |
| **mesh-cstate** | 2.1 s / 300 s = **0.70%** of cpuidle `state*/time` | folds on the ACTIVITY direction (busier window wins), publishes `level_inst`/`level_iv` |
| **mesh-package-power** | 2.0 s / 300 s = **0.67%** of RAPL `energy_uj` | interval watts + a wrap-decidability rule (below) |
| **mesh-load-audit** | 0.3 s / 120 s = **0.25%** of per-process CPU ticks | whole-snapshot carry → a per-process mean over the interval |
| **mesh-fitness** | PSI `avg10` / 540 s = **1.85%**, and it is a VERDICT axis | avg10+avg60+avg300+`total=` delta, folded, winner named in the deferral note |

## Four things this round taught that the disk pair did not

**1. A max fold is not always "the bigger number".** `mesh-cstate` measures idle%, so the *louder*
window is the LOWER one; the fold runs on the activity direction and takes the busier window's
deep%/ratio with it, so the pair stays coherent. And because idle% alone cannot express
SHALLOW-vs-DEEP (the disjunction the sense exists for), both windows' LEVELS are published — a fold
that kept only the busier reading could hide a SHALLOW-REST the other window saw.

**2. A wrapping counter's interval can be undecidable, and the ambiguity does not look like an
error.** RAPL `energy_uj` wraps at `max_energy_range_uj`. Across an interval the counter may have
wrapped *k* times and nothing in the two values says which: each extra wrap ADDS `max`, so the usual
single correction silently picks the SMALLEST — a fabricated calm that reads as an ordinary number.
Two drafts of this fix got it wrong in opposite ways (first "an absurdly HIGH reading means
multi-wrap" — backwards; then "dt too long means ambiguous" — a fixed rule that made every reading
at the live cadence `na` on this node's small 65.5 kJ counter). What decides it is **physics**: the
package cannot exceed `MAX_PLAUSIBLE_W`, so the reading is published only when the *next* wrap
candidate is impossible. Self-adapting: at 300 s the candidates are 218 W apart and the interval is
decidable; stretch it toward an hour and they close up until both fit under the ceiling — which is
exactly when the reading stops being knowable.

**3. A narrow window has a RESOLUTION, and a plain max hands it every verdict.** `mesh-load-audit`
samples 0.3 s at 100 Hz, so one tick is **33.3%** and the reading is quantised in 33-point steps.
Measured on this node: a `kworker/u32:*` read **1544%** in a 1 s window (kernel stime for unbound
workqueue threads lands in bursts) while its interval mean was ~100%. A plain max would hand that
artifact the top spot every pass and the interval would be computed, published, and never consumed.
The fold therefore lets the in-run window win only when it clears the interval by more than one
tick's worth. And the same *physical* rule now applies to both windows: a row claiming more CPU than
the machine HAS (100% × nproc) is not a measurement. The interval ranking always dropped those; the
in-run one published them — live at **cpu_inst=5776.7%** on a 16-core box, in the same state line as
a 98.9% interval that called the identical shape impossible. One rule, both windows, and the drop is
counted in `impossible_rows=` so "the artifact stopped appearing" can never be read as "nothing was
dropped". The burst *below* that ceiling is real in `/proc` and is left alone — it is a separate
finding, not something to launder inside a coverage fix.

**4. Widening a gate has a direction, and it must be argued.** `mesh-fitness`'s PSI read is not a
corroborator; it decides whether an **auto-revert** fires on a real commit, and it decides in the
"do not flag" direction. Widening can only make it defer more often — safe for a tool whose known
failure mode is reverting innocent commits (2026-07-10T06:54Z, 403a6c0), and a genuine regression
fails again at the next */9 tick. The gate that pins the other side is the one asserting that with
all four windows calm and memory healthy, a repeat rc=1 is **still flagged**.

Two smaller ones, both from watching mutants survive:

- **An overlapping guard cannot be seen to fail.** `mesh-cstate`'s explicit reset check is shadowed
  by `compute()`'s own negative-delta rejection, and `mesh-load-audit`'s backwards-tick check by its
  `d>0` filter. One is kept (documented as pinning behaviour, not the line), one was deleted. A
  redundant guard that no gate can redden is decoration that reads as protection.
- **A gate on a busy node can be vacuous by luck.** The package-power fold gate asserted `level=HIGH`
  while the live 2 s sample already read HIGH — so classifying off the WRONG window produced the same
  word and the mutant survived. Fixed by pinning `MESH_PKG_HIGH_W=120` for the gate's child, a
  threshold the live sample cannot reach.

## Gates seen RED (this round)

31 mutants, each run from a scratch copy against the real hardware.

| tool | mutations watched fail |
|---|---|
| mesh-swap-rate | carry deleted · na→0 · fold ignores iv · verdict off inst · reset guard · stale guard (6) |
| mesh-cstate | carry deleted · na→0 · fold ignores iv · verdict off inst · ncpu-hotplug guard · stale guard · both reset guards (7) |
| mesh-package-power | carry deleted · na→0 · fold ignores iv · verdict off inst · stale guard · wrap-ambiguity · ceiling · cross-domain baseline (8) |
| mesh-load-audit | snapshot carry deleted · iv table never consumed · fold always inst · unexplained-old-proc credited · impossible-row cap (both windows) · iv percentage math · dt/stale guards (8) |
| mesh-fitness | avg300 leg dropped · interval dropped · reset guard · stale guard · fold takes first not max · na can win · deferral silenced (7) |

`mesh-wakeup-attrib` was touched as a consumer: it reads cstate's `_inst` fields on purpose, because
its method is correlating cstate against an irq rate sampled back-to-back — pairing a 5-minute mean
with a 3-second irq read would attribute one window's restlessness to another window's interrupts.
Its sub-sense binaries now resolve **sibling-first**, so a fused tool's `--test` asserts against the
generation it is being landed with rather than the stale deployed copy.
