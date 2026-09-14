# Mesh-home cross-namespace uevent join — 2026-09-14

Task: `health-device-churn-cross-namespace-join-20260914/investigate-cross-namespace-uevent-join`  
Node: `mesh-home`  
Disposition: historical device events can be named where the retained stream saw them, but the 78
remaining sequence increments have no retained cross-namespace or Docker/task join. The smallest
safe next step is a bounded capture on the next comparable live burst; no listener, service,
container, or network configuration was changed.

## Retrospective join

Matched the four requested `mesh-device-churn` counter ranges to retained `udev-stream.log` rows by
exact seqnum. Intervals are half-open `(baseline, total]`; the udev stream reports action,
subsystem, seqnum, and DEVPATH for every retained row.

| pass end UTC | seqnum interval | counter delta | retained rows in interval | missing / unknown |
|---|---:|---:|---|---:|
| 16:20:03 | (11734, 11752] | 18 | 11744, 11748–11752; all `change hwmon` at `/devices/pci0000:00/0000:00:18.3/hwmon/hwmon2` | 12 |
| 16:30:04 | (11752, 11786] | 34 | 11768, 11772, 11785–11786; same `change hwmon` DEVPATH | 30 |
| 16:50:03 | (11790, 11810] | 20 | 11809–11810; same `change hwmon` DEVPATH | 18 |
| 16:55:02 | (11810, 11832] | 22 | 11826, 11830–11832; same `change hwmon` DEVPATH | 18 |
| **total** |  | **94** | **16 named rows, all hwmon** | **78** |

The 78 are unknown sequence values, not proven dropped broadcasts. The stream's own header documents
that `/sys/kernel/uevent_seqnum` is global while netlink uevents are namespace-scoped; a listener in
one namespace cannot name events delivered only in another. Its `sgap` is an outstanding gauge and
was not used as a per-window loss count.

The retained mesh-home receipt for 14:25–14:55Z reaches the same retrospective limit: it matched
57/73 sequence values to 16 named hwmon rows, found no Docker lifecycle records in its interval,
and could not map the remainder to a container or task. The 2026-09-13 burst receipt documents a
different interval where Docker lifecycle and veth/queue activity overlapped, but it still could
not assign an ephemeral veth to a particular container/task retrospectively.

For the requested 16:15–17:00Z interval, `docker events --filter type=network` returned no rows and
`docker ps -a --no-trunc` showed no retained containers at inspection. These empty reads do not
prove that no lifecycle occurred; exited-container inspect state and the source-side join were not
retained. Therefore no Docker endpoint, host-veth, namespace, or mesh-task identity is assigned to
the 78 unknown values.

## Bounded retry on the next live burst

Trigger: immediately when a new `mesh-device-churn` pass reports `CHURN` and a positive
`missing=<n>` (or the equivalent `missing/unknown` count). While the event interval is live, run on
mesh-home:

```bash
scripts/mesh-docker-veth-join --seconds 300 --max-events 1000
scripts/mesh-udev-stream --tail 1000
```

The first command writes a bounded JSONL artifact under `$MESH_DIR/observations/` with each Docker
network event, inspect-derived endpoint/container/task label when readable, peer ifindex, host-veth
DEVPATH when unique, and the global uevent seqnum bracket. The second retrieves the concurrently
retained udev rows with action/subsystem/DEVPATH/seqnum. Join only when the observed host-veth
DEVPATH exactly equals a retained udev DEVPATH and the event times overlap the capture; preserve
unknown/ambiguous values otherwise. A seqnum delta around Docker inspection is a bracket, not proof
of causality.

This retry uses existing read-only tools and provides direct host-side evidence where available.
It does not itself observe netlink inside every private network namespace: `mesh-udev-stream` listens
in its own namespace, and `mesh-docker-veth-join` consumes Docker's network-event stream. If the next
capture still leaves a positive residual, the exact missing capability is a bounded, event-aligned
`udevadm monitor --kernel --property` capture in each relevant live network namespace, tagged with
that namespace's inode, alongside the Docker endpoint/veth/task tuple. Do not infer a namespace
source from the global counter or from timing alone; leave those rows unknown until that capture is
available.

## Evidence

- `/home/mesh-home/.mesh/device-churn.log`, lines 5299, 5301, 5305–5306: four requested CHURN
  intervals and the reported 94 delta / 78 missing counts.
- `/home/mesh-home/.mesh/udev-stream.log`, rows from 16:16:11Z through 16:54:44Z: the 16 exact
  seqnum matches, all at the PCI hwmon DEVPATH.
- `docs/task-receipts/device-churn-attribution-20260914-correlate-14h-mesh-home-bursts.md`: prior
  14:25–14:55Z range, with explicit unknown residual and no Docker lifecycle rows.
- `docs/task-receipts/device-churn-attribution-20260913-correlate-high-uevent-bursts.md`: earlier
  partial Docker/veth correlation and remaining attribution limits.
- `scripts/mesh-udev-stream`: namespace-scoped netlink, global counter, and `sgap` semantics.
- `scripts/mesh-docker-veth-join`: bounded read-only Docker event/inspect to unique host-veth
  mapping; seqnum brackets explicitly do not imply causality.
- Live checks on 2026-09-14: historical `docker events` interval query returned no rows;
  `docker ps -a --no-trunc` returned only its header.
