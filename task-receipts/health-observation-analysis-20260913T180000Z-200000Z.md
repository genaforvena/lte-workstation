# Health observation analysis: 2026-09-13 18:00–20:00Z

Task: `20260913T180000Z-200000Z/analyze-observation`  
Source: `observation-window:20260913T180000Z-200000Z`  
Interval: `[2026-09-13T18:00:00Z, 2026-09-13T20:00:00Z)`

## Findings

The frozen admission report declares complete coverage: 652 unique events and no exact duplicates
from `chat.log` (520), `witness.log` (60), and `sensors.log` (72). The source rows are in the
specified half-open UTC interval.

- **Virtual-network lifecycle remains the strongest recurring device-churn signal.** The 24
  five-minute counter passes contain 13 `CHURN`, 4 `TICK`, and 7 `QUIET` verdicts; their accumulated
  delta is 2,665. The contemporaneous udev tape has 1,288 named rows: 1,260 under virtual `net` /
  `queues` paths and 28 `hwmon` changes. In the same interval, retained Docker history has 18
  container-create events; the per-pass overlap places creates inside several of the large veth
  bursts (including 2, 4, and 4 creates in the 18:15, 18:25, and 19:35 passes). This is strong
  evidence that Docker virtual-interface lifecycle contributes to the bursts, but no retained tuple
  maps a particular container to a particular ephemeral host veth. The counter is a global kernel
  seqnum while udev cannot receive events confined to another network namespace, so the raw
  counter-minus-stream difference (1,377) is an unmatched count, not proven lost broadcasts. The
  prior `device-churn-attribution-20260913/correlate-high-uevent-bursts` task is complete and
  covers an earlier interval; it does not close this new interval's source-side join gap.
- **Sampled local conditions were variable, not continuously bad.** Across 24 five-minute sensor
  points, `cpu_load1` ranged 11.36–99.36 (median 26.44), memory use 18.6–32.8% (median 25.1%), and
  room sensing was UNCERTAIN 17 times, PRESENT 6 times, and OFFLINE once. These are point readings;
  they do not establish duration or cause. The 60 witness rows reported reflex `OK` throughout,
  while mind counts were UNKNOWN in 10 samples and ask metrics UNKNOWN in 12. Reachability varied
  from 2/11 to 4/11, and the known stale-ask p90 rose from 154.4 to 155.3 hours while resolve ratio
  remained 0.746. Unknown samples are coverage gaps, not zeros.
- **The health-warning alerts in this interval have dispositions.** I checked all eleven
  `health-warning/*/triage` chains emitted between 18:00 and 20:00Z; each is complete with a receipt.
  They include the 18:27 autonomy stall (the named task progressed and later autonomy passes
  passed), repeated bounded chat-delivery age expiries (zero successful attempts recorded, exact
  failed hop unobservable), the 18:52 queue timeout (later queue probes passed; cause unknown), and
  the 19:40 check-versus-claim race (candidate claimed during the serialized sweep; later run
  passed). These dispositions support neither replaying expired messages nor changing delivery or
  substrate behavior.

The one-shot live check pane at 20:17:40Z still marked local load high and reachability probes
unreliable. Its visible load lines were about 19.88–22.91 on 16 cores with a Python process above
500% CPU; the doctor section was cached from 19:34Z (FAIL=3, WARN=33). The visible doctor warnings
include egress through `tailscale0` and a configured exit node; the pane also reports no recent WG
client handshake. Those are observations, not authorization or evidence for routing, DNS, firewall,
WireGuard, exit-node, or other substrate changes. The dash output itself elided detail, so I treat
only its visible lines as current evidence.

## Disposition

I registered `device-churn-live-join-20260913/capture-veth-container-join` to capture the missing
source-side mapping during future events. It asks for a read-only bounded observer that records the
container ID, network endpoint/peer ifindex, host veth DEVPATH, available launching task key, and
nearby seqnum baseline/delta, preserving unknown fields explicitly. The repeated correlation
justifies instrumentation; it does not justify changing network, container, USB, or service state.
No other new health follow-up is warranted by this window.

## Verification and evidence

- Re-read the admission report and independently filtered the exact interval from all three source
  tapes; counts matched 520 + 60 + 72 = 652.
- Summarized the 24 device-churn passes, 1,288 udev rows, and retained Docker create events by
  five-minute interval. The per-pass counts are reproducible from
  `/home/mesh-home/.mesh/device-churn.log:5031-5054`,
  `/home/mesh-home/.mesh/udev-stream.log:4411-5698`, and `docker events` for the bounded interval.
- Read the complete sensor and witness windows at `/home/mesh-home/.mesh/sensors.log:55610-55681`
  and `/home/mesh-home/.mesh/witness.log:4929-4988`; checked the eleven alert chains with
  `mesh-task status`, all complete.
- Read the full in-window chat span at `/home/mesh-home/.mesh/chat.log:60395-60916`, the live
  `mesh-dash --once check` pane, the previous attribution receipt, and the relevant udev-stream
  netns/seqnum explanation in `scripts/mesh-udev-stream`.
