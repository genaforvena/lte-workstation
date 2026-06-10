# Control Theory Application: Homeostatic Breath Cadence

**Proposal**: Replace the fixed-interval `mesh-tick` cron with a **closed-loop homeostatic
controller** that adapts breath cadence to mind-beat age. One concrete application; design only.

---

## The problem: open-loop breathing

`mesh-tick` fires at a fixed `*/10` cron interval — 600 seconds, regardless of what the mind
is doing. This is **open-loop control**: the mesh has no feedback path from mind state to
breath frequency.

Two failure modes follow directly:

1. **Unnecessary interruption.** A mind that stamped 30 seconds ago is actively processing.
   Sending it a nudge is noise — the tick is wasted and may fragment the mind's context.

2. **Slow recovery from idle.** A mind that went quiet 15 minutes ago won't get another nudge
   for up to 10 more minutes (depending on cron phase). The mesh is slow to re-animate a
   sluggish mind.

The fix is to close the loop: let the breath rate respond to what the sensor (beat age) reports.

---

## Control model

```
                  ┌──────────────────────────────────────────────┐
                  │                                               │
    set-point     │  Controller        Actuator        Plant      │
    SP = 600s ──► │  (zone table)  ──► mesh-tick  ──► mind       │
                  │       ▲                                ▼       │
                  │       │               Sensor           │       │
                  │       └──── beat age ◄── mind-stamp ◄─┘       │
                  │                                               │
                  └──────────────────────────────────────────────┘
```

| Term | Concrete value |
|------|----------------|
| **Plant** | Mind process in tmux (Claude / Gemini) |
| **Process variable (PV)** | Age of `~/.mesh/mind-beat.ts` in seconds |
| **Set-point (SP)** | 600 s — "mind stamped within one nominal tick cycle" |
| **Error** | `e = PV − SP` (positive = mind is behind; negative = mind is ahead) |
| **Controller** | Relay controller with hysteresis (zone-based bang-bang) |
| **Actuator** | `mesh-tick local <win>` — injects a nudge into the idle pane |
| **Feedback sensor** | `stat -c %Y ~/.mesh/mind-beat.ts` — file mtime |

---

## Why not PID

PID is the standard choice for continuous processes, but three properties of this plant make
it a poor fit:

1. **Settling time is long and variable.** An LLM response takes 10–120 s. During that time the
   beat age climbs even though the mind is healthy. A proportional term would call for more ticks
   precisely when the mind is busiest — the opposite of what we want.

2. **Integrator wind-up.** During a long compute burst (30+ min) the integral accumulates a
   large error. When the burst ends, the I-term fires a burst of compensatory ticks that
   hammers the mind for several cycles.

3. **The output is discrete.** We either fire a tick or we don't. A continuous PID output
   (e.g., "send 0.37 ticks") has no meaning. Forcing a continuous signal through a comparator
   to get a binary output is exactly the relay controller — so we should design the relay
   directly, with explicit hysteresis to prevent chattering.

**Relay controller with hysteresis** is the standard alternative for bang-bang processes with
slow plant dynamics. It maps directly to biological homeostasis: define health zones with
hysteresis bands between them, and respond to the zone, not to instantaneous error.

---

## Homeostatic zone table

The zones are defined on EWMA-smoothed beat age (see below). Hysteresis: zone transitions
require the smoothed age to cross the boundary by at least 30 s before switching, preventing
oscillation near zone edges.

| Zone | Smoothed beat age | Name | Meaning | Tick interval |
|------|------------------|------|---------|--------------|
| 0 | < 240 s | **FRESH** | Mind recently active; back off | 600 s |
| 1 | 240–600 s | **NOMINAL** | Normal operating range | 300 s |
| 2 | 600–1 200 s | **SLUGGISH** | Mind quiet for 1–2 ticks | 90 s |
| 3 | 1 200–1 800 s | **STALE** | Likely idle/stuck | 60 s |
| 4 | > 1 800 s | **DEAD** | Beat threshold exceeded | 60 s + escalate |

Zone 4 is the `mesh-mind-watch` threshold (1 800 s). The controller's zone-4 action is to
fire `mesh-tick` at maximum cadence AND hand off to `mesh-mind-keepalive`. The controller
does not attempt to restart the mind itself — that is `keepalive`'s job.

Transition hysteresis example: if smoothed age is 610 s (just entered SLUGGISH), it must
reach 240 s (not 600 s) before being declared NOMINAL again — prevents thrashing on a mind
that stamps erratically near the boundary.

---

## EWMA smoothing

Raw beat age is a **monotonically increasing counter** that resets to zero on each stamp. It
carries no measurement noise, but it reacts instantly to a fresh stamp — without smoothing,
the controller drops from zone 2 back to zone 0 on the first stamp, overshoots the back-off
period, and may re-enter zone 2 before the next real work cycle.

EWMA smoothing damps this over-response:

```
smooth(t) = α × age_raw(t)  +  (1 − α) × smooth(t−1)
```

With α = 0.4 and a base clock of 60 s, the time constant τ ≈ 60 / ln(1/(1−0.4)) ≈ 118 s
(~2 ticks). A sudden stamp drops the smoothed age by ≈ 40 % per clock tick rather than
instantly. This prevents the FRESH back-off from being prematurely triggered by a single
stamp during a sluggish cycle.

State is persisted in `~/.mesh/tick-age-smooth` (a single integer, updated by the controller
each run).

---

## Implementation sketch

The cleanest implementation avoids a persistent loop (another process to supervise) by
running the controller as a **frequent cron job** that gates its own action:

```
* * * * *  mesh-tick-ctrl local claude   # runs every 60 s; decides whether to act
```

`mesh-tick-ctrl` (new script, ~60 lines):

```bash
#!/usr/bin/env bash
# mesh-tick-ctrl [tgt] [win] — closed-loop homeostatic breath controller.
# Reads beat age, computes zone, fires mesh-tick only when zone cadence has elapsed.
export PATH="$HOME/.local/bin:$PATH"
TGT="${1:-local}"; WIN="${2:-claude}"
MESH="$HOME/.mesh"; ALPHA=0.4

# 1. Read beat age (sensor)
beat="$MESH/mind-beat.ts"
now=$(date +%s)
if [ -f "$beat" ]; then
  age_raw=$(( now - $(date -r "$beat" +%s 2>/dev/null || echo $now) ))
else
  age_raw=9999   # no beat file = treat as DEAD
fi

# 2. EWMA smoothing
smooth_f="$MESH/tick-age-smooth-${TGT//\//_}-$WIN"
prev=$(cat "$smooth_f" 2>/dev/null || echo "$age_raw")
smooth=$(awk -v a="$ALPHA" -v r="$age_raw" -v p="$prev" 'BEGIN{printf "%d", a*r + (1-a)*p}')
echo "$smooth" > "$smooth_f"

# 3. Zone dispatch
if   [ "$smooth" -lt 240  ]; then interval=600; zone=FRESH
elif [ "$smooth" -lt 600  ]; then interval=300; zone=NOMINAL
elif [ "$smooth" -lt 1200 ]; then interval=90;  zone=SLUGGISH
elif [ "$smooth" -lt 1800 ]; then interval=60;  zone=STALE
else                               interval=60;  zone=DEAD
fi

# 4. Check if interval has elapsed since last tick
last_f="$MESH/tick-last-${TGT//\//_}-$WIN"
last=$(cat "$last_f" 2>/dev/null || echo 0)
elapsed=$(( now - last ))
[ "$elapsed" -lt "$interval" ] && exit 0   # too soon — skip

# 5. Fire
echo "$now" > "$last_f"
mesh-tick "$TGT" "$WIN"

# 6. Zone-4 escalation
if [ "$zone" = DEAD ]; then
  command -v mesh-mind-keepalive >/dev/null 2>&1 && mesh-mind-keepalive
fi
```

The existing `*/10 mesh-tick local gemini` cron line is replaced with
`* * * * * mesh-tick-ctrl local gemini`. No other scripts change.

---

## Integration with existing tools

| Existing tool | Interaction |
|--------------|-------------|
| `mesh-tick` | Still the actuator — controller calls it, doesn't replace it |
| `mesh-mind-stamp` | Still the sensor stamp — no change |
| `mesh-mind-watch` | Watches the same beat file; zone-4 fires keepalive in parallel |
| `mesh-mind-keepalive` | Zone-4 escalation path; controller calls it after the final tick attempt |
| `mesh-supervise` | Unchanged — supervises loops, not mind liveness |
| `mesh-card --refresh` | Can expose current tick-zone as a capability field for observability |

---

## Expected behavior — worked examples

**Example 1: Mind actively processing a long task**
- Mind stamps at t=0; zone = FRESH (age_smooth ≈ 0 → 100 s over 2 min with EWMA)
- Controller backs off to 600 s interval — no interruption for 10 min
- Mind stamps again at t=8 min; EWMA resets smoothly; FRESH maintained
- No wasted ticks during active computation

**Example 2: Mind goes idle after completing a task**
- Last stamp at t=0; no further activity
- At t=4 min: age_smooth ≈ 240 s → entering NOMINAL; tick fires (300 s interval)
- At t=10 min: age_smooth ≈ 600 s → SLUGGISH; tick fires every 90 s
- At t=15 min: age_smooth ≈ 900 s → still SLUGGISH; 5 ticks in 7.5 min (vs 1 tick/10 min fixed)
- Mind likely woken within 5 min of going idle rather than up to 10 min (worst-case fixed)

**Example 3: Mind crashes / hangs**
- Stamps stop at t=0
- At t=20 min: age_smooth > 1 800 s → DEAD; tick fires at 60 s + keepalive called
- `mesh-mind-keepalive` detects claude is not running → relaunches with `--continue`
- Mind restamps; EWMA drops rapidly; controller backs off to NOMINAL within ~3 ticks

---

## Failure modes and mitigations

| Failure | Effect | Mitigation |
|---------|--------|-----------|
| Beat file missing (new node) | age_raw = 9999, zone = DEAD immediately | Controller treats missing beat as DEAD, fires keepalive — correct behavior |
| `mesh-tick-ctrl` itself crashes | No ticks until cron restarts it | 1-min cron period; max gap = 60 s. Add to `supervise.list` if longer gaps unacceptable |
| EWMA state file corrupted | One-tick zone mis-classification | `awk` sanity: if parsed value > 86400 s, reset to age_raw |
| Two controllers running for same window (multi-agent) | Double-tick | last-tick file write is atomic (single integer); both read/compare the same file; at worst one extra tick per collision |

---

## Why this is the right one to build first

The mesh has threshold detectors (`mesh-mind-watch`, `mesh-beacon-watch`) and restart loops
(`mesh-supervise`, `mesh-mind-keepalive`), but no **continuous regulator** — nothing that
adjusts behavior proportionally to how far from equilibrium the system is. Homeostatic breath
cadence is the simplest closed loop that fills this gap:

- Touches only one cron line and adds one ~60-line script
- Directly exercises the feedback principle from `eternity-and-its-fields.md` ("homeostasis
  via feedback" — the cybernetics row)
- Immediately measurable: compare tick-firing logs before/after for wasted ticks and
  idle-to-active latency
- Composable: the zone state can be exposed in the mesh card and read by other controllers
  (e.g., a future egress-load controller could back off its polling when this node's mind is
  in DEAD zone, knowing it can't act on alerts anyway)
