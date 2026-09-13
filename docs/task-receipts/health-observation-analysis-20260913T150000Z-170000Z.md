# Health observation analysis: 2026-09-13 15:00–17:00Z

Task: `20260913T150000Z-170000Z/analyze-observation`  
Source: `observation-window:20260913T150000Z-170000Z`  
Interval: `[2026-09-13T15:00:00Z, 2026-09-13T17:00:00Z)`

## Coverage and findings

The generated report says admission evidence is complete: 557 rows across
`~/.mesh/chat.log` (425), `witness.log` (60), and `sensors.log` (72); all 557
events are unique. I checked the timestamped source rows and current task ledger.

- **Device enumeration is the clearest unowned anomaly.** At 16:50:05Z,
  `device-churn@mesh-home` reported 141 uevents in 301 seconds, above the
  learned idle floor of 24. At 16:55:02Z it reported 144 in 299 seconds. Both
  reports have `candidates=none`; the accompanying instrument description says
  level instruments had returned to healthy and a removal may leave no device
  node to age. The event itself is real according to the detector, but its
  device/source attribution is unknown. This is a specific visibility gap,
  not evidence that no hardware changed. Source: `~/.mesh/chat.log` lines 60111
  and 60136; detailed per-pass tape `~/.mesh/device-churn.log`.
- **Peer-path fallback recurred, with one episode resolved.** `phaedra` crossed
  direct→relay by 16:19Z, triggered a debounced warning at 16:24Z, and returned
  to direct by 16:29Z; contemporaneous status then showed UDP true. A separate
  `imac-rozalia` relay edge was reported at 16:19Z and again at 16:54Z. The
  path-watch triage receipt records no 16:24 netweather sample, so it cannot
  establish UDP state at the first warning. Do not attribute either fallback
  to local UDP failure or same-LAN conditions without paired contemporaneous
  evidence. Existing disposition: `docs/health-warning-triage-a11c256e2e2565d08e9d-20260913.md`.
- **The household Wi-Fi/router incident remains externally gated.** The
  actuator audit found no direct mesh writer for GL-MT3000 Wi-Fi/WAN/power; one
  mesh-home WireGuard relay may affect the VPN/WAN path indirectly, with no
  causal link established. The router is offline, preventing inspection of
  its runtime or logs. The existing
  `wifi-router-periodic-outage-20260913/root-cause-access` task is typed-blocked
  until operator-owned read-only access or a timestamped WAN/uptime/radio/log
  export is supplied. This remains the retry condition; do not infer that
  configuration was or was not changed from absence of a log entry. Receipts:
  `task-receipts/audit-actuators-wifi-router-periodic-outage-20260913.md` and
  `task-receipts/correlate-outages-wifi-router-periodic-outage-20260913.md`.
- **Two-hour sensor samples show intermittent uncertainty, not a continuous
  outage.** `room_sense` had 13 PRESENT, 9 UNCERTAIN, and 2 OFFLINE samples at
  five-minute cadence. `cpu_load1` had 24 samples (median 13.72, maximum
  103.77); isolated peaks cannot establish sustained load between samples.
  `mem_used_pct` ranged from 20.2 to 56.8 across 24 samples. The current pane
  at 17:52Z separately reports high load, so present pressure is live evidence,
  not a conclusion from this historical window.
- **Witness summaries were mostly stable but sometimes unknown.** Across 60
  samples, reflex status was OK throughout; node reachability was 3–4/11 and
  live minds were 14–15 when known. Eight samples had `ask_unknown=1` and three
  had unknown mind counts, with known values returning on later samples. The
  known stale-ask p90 rose from 151.2h to 153.2h and resolve ratio moved from
  0.752 to 0.746. These counters indicate a persistent old backlog; this window
  does not establish its cause.

## Disposition

The path-watch episode and router access obligation already have exact task
receipts and were not duplicated. No substrate change is justified by this
window. The repeated device-churn burst is recorded as an unresolved
attribution blindness: the detector sees enumeration counts, but this evidence
does not identify the device or cause. The specific next evidence is the full
per-pass device-churn tape and a source that maps the affected uevents to device
identity; `candidates=none` alone is not a clean bill of health.

The live pane read for this turn was `mesh-dash --once check` at 17:52:12Z
(render completed 17:52:20Z); it showed degraded fleet reachability, a local
load warning, and 91% GPU VRAM use. Those are current observations outside this
report's two-hour interval. The active mesh-home route/VPN posture remains
observe-only under the health charter.

## Verification

- Confirmed the generated report's interval, source counts, and deduplication
  metadata by reading
  `~/.mesh/autopoiesis-observation/analysis/20260913T150000Z-170000Z.md`.
- Re-read the bounded source rows in `chat.log`, `witness.log`, and
  `sensors.log`; calculations above are sample counts/ranges, not interpolated
  state between samples.
- Checked `mesh-task status` for the two health-warning chains and the router
  chain. The path warning chains are complete; router `root-cause-access` is
  blocked on the recorded operator input.
