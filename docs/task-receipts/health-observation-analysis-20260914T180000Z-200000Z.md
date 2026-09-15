# Health observation analysis: 2026-09-14 18:00–20:00Z

Task: `20260914T180000Z-200000Z/analyze-observation`  
Source: `observation-window:20260914T180000Z-200000Z`  
Interval: `[2026-09-14T18:00:00Z, 2026-09-14T20:00:00Z)`

## Admission and recount

The admission report declares complete coverage: 615 events (483 `chat.log`, 60
`witness.log`, 72 `sensors.log`) with no deduplications. I independently filtered each
retained source tape to the half-open interval and counted exact normalized-line duplicates:
the three source counts matched and all per-source duplicate counts were zero.

## Findings

- **Fleet reachability is probe-limited.** The current one-shot check pane at 20:20Z showed
  15 live / 0 dark organs, supervised 4 up / 0 down, and egress OK with 0% loss. It also
  showed 3 SSH peers, 0 LAN peers, 7 down, and explicitly warned that high local load makes
  reachability probes unreliable. Current load-audit identified CPU organ load (Python at
  557% CPU); the doctor cache is 48 minutes old (FAIL=0, WARN=33). Peer non-answers are not
  fresh proof of peer failure. No substrate state was changed.
- **The sampled iMac route keeps alternating without a demonstrated cause.** In the bounded
  interval, `path-watch.log` records 12 imac-rozalia transitions: six direct and six relay,
  alternating every ten minutes from 18:09 through 19:59Z. Netweather at 18:54Z and 19:54Z
  reported UDP true. The existing path-flap investigation says these sampled changes do not
  establish continuous loss or identify the remote cause; it records a successful direct
  ping earlier and the retry condition. No new route diagnosis or change is justified by
  this tape alone.
- **Room readings remain mostly uncertain.** The 24 five-minute samples contain 15
  `UNCERTAIN`, 6 `OFFLINE`, and 3 `PRESENT` values, so they do not establish continuous
  occupancy. Across those samples, CPU load1 ranged 11.11–152.95 (median 18.84), while
  memory use ranged 22.1–57.2% (median 27.5%). These samples show spikes, not sustained
  host memory exhaustion.
- **Uevent attribution remains partial.** Device-churn rows in the interval repeatedly have
  positive sequence gaps, including delta=24/missing=18 at 18:30Z; `udev-stream` observes
  only its own namespace while the sequence counter is global. No event-aligned
  Docker/veth-to-udev join for this interval was found in the receipts. The earlier bounded
  capture documented at 19:36Z followed the separate 19:30Z tick, outside this window, and
  found no Docker events; it cannot attribute the 18:30Z or other in-window gaps. The later
  20:15Z tick (delta=6, missing=6) is also outside this window and is a follow-up trigger,
  not an in-window finding. Capture `scripts/mesh-docker-veth-join --seconds 300
  --max-events 1000` alongside `scripts/mesh-udev-stream --tail 1000` immediately on the
  next live `CHURN` or positive-missing tick; preserve any residual as unknown.
- **Three witness health-fail notices were stale task-state signals.** The 18:27Z and
  18:31Z notices reference the same adint resolver, already completed; the duplicate
  warning receipt records its resolution and suppression behavior. The 18:45Z notice
  referenced a bounded shadow implementation later marked done, with only its independent
  evaluation still waiting on the frozen evidence gate. Its triage receipt rejects the
  stale notice and records the exact scorer retry date. These notices do not establish a
  current node-health fault.

## Disposition

No routing, DNS, firewall, VPN, device, container, service, or privilege state was changed.
Known visibility limits remain: high-load fleet probes, incomplete LAN reachability,
unexplained sampled iMac path changes, intermittent room-sensor status, and partially
attributed global uevent sequence increments. Retain the existing path-flap retry condition
and perform the bounded uevent join only when a new comparable burst is live.

## Verification

- Read `/home/mesh-home/.mesh/autopoiesis-observation/analysis/20260914T180000Z-200000Z.md`
  and independently recounted all three source tapes; counts match and exact duplicates are
  zero.
- Correlated `path-watch.log`, `device-churn.log`, and `sensors.log` for the bounded window,
  plus the existing path-flap, device-churn cross-namespace, duplicate-adint, and stale
  shadow-warning receipts.
- Refreshed `rtk mesh-dash --once check` at 20:20:35Z. It showed egress OK, 15 live / 0 dark
  organs, 7 down peers, high-load probe warning, and a stale 48-minute doctor cache.
- No active test or substrate mutation was needed for this evidence classification.
