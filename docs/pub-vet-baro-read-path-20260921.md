# Publication vet — baro read path: the sensor was fine, the read path was dead, and it died looking alive

Date: 2026-09-21 UTC
Source: `scripts/mesh-baro` (producer, uncommitted-clean read path), `scripts/mesh-climate`
(consumer), `scripts/mesh-situation` (consumer)
Live check (this wake, 2026-09-21T21:07–21:15Z): full producer→consumer chain reproduced from raw
hardware to verdict, all rc=0.

## The failure, in one sentence

The Note 3's LPS25H barometer never stopped working — the **read path** to it died twice, in two
different ways, and both ways looked healthier than the sensor.

## The two read-path failures

**Failure A — the plausible fossil.** The original backend was `adb shell dumpsys sensorservice`,
reading the `last=<hpa>` line. That line is a **frozen fossil**: proven at active-count=0 with values
frozen at ~17 minutes of uptime while the phone had been up 11.8 days (2026-07-17,
`memory/` note `note3-baro-and-friends-read-a-fossil`). The danger is not that it returned garbage —
981.8 hPa is a perfectly good atmospheric pressure. A stale value that never *looks* stale is worse
than no value, because nothing downstream has a reason to ask.

The fix moved the read to `sensorcat`, a native `ASensorManager` listener
(`~/.mesh/note3/`, `[[note3-native-hal-clients]]`), which makes the sensor actually sample. Raw output
captured this wake:

```
SENSOR|SHTC1 relative humidity sensor|12|55.175|45.66|3|243885381022196
SENSOR|SHTC1 ambient temperature sensor|13|23.4052|26.16|3|243885381030238
SENSOR|LPS25H Barometer Sensor|6|995.8|146.306|30.3104|243885601563443
```

It also recovered live temperature and humidity, which were permanently `n/a` under dumpsys (on-change
SHTC1 sensors with no listener report exactly `0.0`).

**Failure B — the wedged adb server.** The pane records the 2026-09-21 break as a wedged adb server:
the shell hung with rc=124 **while the device was still listed as present**. This is the ambiguous
case — `adb devices` says healthy, the read does not return. Recovery was a scoped, reversible
`adb kill-server`; no commit, no new tool.

Both failures are the same shape: **the sensor was fine, the read path was dead, and the dead path
advertised a present device.**

## What the measurement proves (all reproduced this wake)

The contract is not "produce a number" — it is "produce a *fresh* number, or say n/a loudly."
Three enforceable behaviours, each measured:

1. **A dark body cannot poison the state.** With the adb path forced dark (serial pointed at an
   absent device *after* the `~/.mesh/nodes` re-export, so the override actually reached the read):

   ```
   baro adb body unreachable — can't read barometer (not an alarm)     rc=2
   ```

   and `.baro-state`'s mtime was **unchanged** — a failed read writes no state, so a failure can
   never become tomorrow's baseline. The tool exit code is part of the signal: `rc=2` is the honest
   n/a that `mesh-land` treats as a pass, never as a faked all-clear.

2. **The offline marker is idempotent and self-clearing.** A second consecutive dark run emitted the
   stderr line once only (`[ ! -f "$OFFLINEFILE" ]` gates it) and touched
   `.baro-offline` again. The next live run removed the marker and returned rc=0 — verified, marker
   gone. One announcement per outage, not one per cron tick.

3. **The consumer does not trust the number — it trusts the number's freshness.** This is the part
   worth publishing on. With `.baro-state` aged 2 hours past its TTL:

   ```
   STABLE | pressure=STALE | out_c=18.1 ... | inputs=2/3
   ```

   `mesh-climate` **dropped the `in_hpa=` field entirely** rather than echoing the last good value,
   and decremented its own input count 3/3 → 2/3. Restoring freshness:

   ```
   STABLE | in_hpa=995.84 trend=STABLE d_hpa=+0.11 | out_c=18.1 ... | inputs=3/3
   ```

   A stale producer cannot ship a number, because the consumer removes the number and shows you the
   count went down.

## The live chain, end to end

```
adb sensorcat LPS25H → 995.8 hPa (raw, rc=0)
mesh-baro             → [baro-stable] 995.84 hPa — STABLE (Δalt≈-1.0 m)   rc=0, .baro-state fresh
mesh-climate          → in_hpa=995.84 trend=STABLE d_hpa=+0.11, inputs=3/3   rc=0
mesh-situation        → AMBIENT [baro] STABLE 995.82hPa (0min ago)           rc=0
```

Producer state file format is `<hpa> <trend> <baseline_hpa>` (`995.84 STABLE 995.73`); baseline is
updated only when STABLE, so the drift reference itself cannot be written by a noisy reading.

## What remains UNKNOWN

- **I did not reproduce the wedged adb server live this wake** — it was already recovered by the
  scoped `adb kill-server` before this vet ran. What I verified is the *contract the recovery relies
  on*: dark → rc=2, no state write, idempotent marker, clean recovery. The wedged-server incident
  itself, and its duration, are evidence from the pane and the rc=124 symptom, not a hang I replayed
  here. Stated as reported.
- The pane recorded 997.10 hPa at capture time; my live reads this wake were 995.82–995.85 hPa. That
  ~1.3 hPa difference is real drift across the interval (consistent with the FALLING entries in
  `~/.mesh/baro.log`), not a discrepancy. No weather interpretation is offered here.
- The SHTC1 temp/humidity recovery is noted as a side effect of the `sensorcat` migration; this vet
  does not separately instrument on-change-sensor semantics.
- No claim is made here about the other 2026-09-21 sense novelties (`mesh-body-context --power`
  fusion, cellsignal/touchidle MCC closures, tamper-attrib). Each is a separate vet case.

## Why this is publishable as a measured case

The generalisable shape is **a stale value that never looks stale**, and the corrective that makes it
impossible to ship.

The instinct when a sensor reading looks wrong is to distrust the sensor. Both failures here were in
the transport, and in both the transport reported itself healthy. The fossil returned a plausible
number; the wedged server returned a listed device. Neither failure was visible from the value alone.

The fix is not a better health check on the read path — it is making the **consumer** the freshness
authority. `mesh-climate` does not ask "is this a good pressure", it asks "is this pressure's mtime
within the producer's cadence", and when it is not, the field disappears and the input count drops.
The reader of the verdict sees `inputs=2/3` and knows one sense went dark, instead of reading a
confident number that stopped being measured. The producer reinforces this by never writing state on
a failed read, so no failure can ever become a baseline.

That transfers anywhere a cached reading is displayed as if it were live: the freshness gate belongs
on the consumer, the field should vanish rather than age, and the count of live inputs is itself part
of the verdict.

## Vet decision

**Publishability: draft-ready for a human-facing dev.to draft, no further code change needed.** The
case is bounded, measured live end-to-end this wake, and each of its three falsifiable behaviours is a
one-line check that fails loudly if regressed:

- a dark body must exit rc=2 and must not touch `.baro-state`
- `.baro-offline` must be announced once per outage and removed on the first live read
- a stale state must make the consumer drop `in_hpa=` and decrement its input count

The angle for the draft is *"the sensor was fine; the read path died looking alive"* — a stale-value
anti-pattern with the freshness authority placed on the consumer, proven on a real two-failure
read path.

Not for external publication: the wedged-adb incident and its duration (UNKNOWN-to-me, above), and
any claim that the other sense novelties share this failure mode.

Acceptance check: this artifact records the exact source tools and the raw sensorcat read, preserves
the UNKNOWN states, gives a bounded publishability recommendation, changes no deployed state, and
adds no claim about unvetted cases. No commit was made by this vet; the worktree's pre-existing dirty
paths (`scripts/mesh-ambient-clock`, `scripts/mesh-clear`, `scripts/mesh-mind-compact`,
`scripts/mesh-omp-lifecycle`, `scripts/mesh-queue-tend`) are untouched, and `.baro-state` was restored
to fresh after the staleness probe.
