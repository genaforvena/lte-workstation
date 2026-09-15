# Device-churn attribution — 2026-09-13

Task: `device-churn-attribution-20260913/correlate-high-uevent-bursts`  
Interval: the 14 `mesh-device-churn` passes ending 2026-09-13 16:30:03Z through
17:35:04Z (the first pass's counter interval begins 16:25:04Z).

## Measurement

Compared each counter delta to `udev-stream.log` rows timestamped in the same interval, then
checked Docker's retained container lifecycle events and the contemporaneous task ledger. This is a
count overlap, not a claim that the two instruments observe the same event population.

| pass end (UTC) | seqnum delta | udev rows in interval | observed udev classes |
|---|---:|---:|---|
| 16:30:03 | 30 | 6 | 6 hwmon |
| 16:35:02 | 6 | 0 | — |
| 16:40:01 | 0 | 0 | — |
| 16:45:01 | 6 | 0 | — |
| 16:50:05 | 141 | 72 | 4 net, 66 queues, 2 module |
| 16:55:02 | 144 | 65 | 1 net, 62 queues, 2 hwmon |
| 17:00:03 | 284 | 140 | 8 net, 132 queues |
| 17:05:03 | 0 | 0 | — |
| 17:10:03 | 701 | 350 | 20 net, 330 queues |
| 17:15:02 | 278 | 140 | 8 net, 132 queues |
| 17:20:05 | 284 | 140 | 8 net, 132 queues |
| 17:25:04 | 11 | 9 | 3 net, 4 queues, 2 hwmon |
| 17:30:03 | 24 | 6 | 6 hwmon |
| 17:35:04 | 130 | 63 | 1 net, 62 queues |
| **total** | **2,039** | **991** | **973 veth/net-or-queue, 16 hwmon, 2 module** |

The 991 logged seqnums are unique. The raw count difference is 1,048 (51.4%); the 991 rows are
48.6% of the counter delta. Treat that as the *unmatched count*, not as 1,048 proven lost broadcasts:
the counter is global, while the udev listener cannot see some private-network-namespace events.
The listener was reported up since 11:40:01Z and with 100% temporal coverage; its first retained
row in this interval is 16:26:33Z. `sgap` is the stream's outstanding gauge, not a per-window loss
count, so it was not summed or used as coverage.

## Attribution

The large named clusters are all virtual-network paths under `/devices/virtual/net/veth…` and their
`queues` children. Docker's event history contains 14 container creates during the window, including
`trusting_dijkstra` at 16:47:29Z, `busy_brown` at 16:54:56Z, five creates from 17:06:08Z through
17:09:52Z, two at 17:11:23Z/17:11:27Z, two at 17:17:23Z/17:17:28Z, and `goofy_meninsky` at
17:33:28Z. Those times fall within the same counter intervals as the large veth/queue bursts. The
best-supported attribution is therefore that Docker-managed virtual-interface lifecycle activity
contributed materially to the high deltas. The counter and udev records do not prove which container
created a particular ephemeral `veth` name.

The other 18 rows are 16 changes at the physical PCI hwmon path
`/devices/pci0000:00/0000:00:18.3/hwmon/hwmon2` and two `module` events. Of the hwmon rows, eight
carry the mesh probe's signed synthetic UUID and are directly attributable to that probe; eight
are unsigned and remain unassigned. The module rows have no retained module name. No physical USB
device path appears in this interval's named rows.

The task ledger and Docker history contain no retained join from the ephemeral veth names/container
IDs to a mesh task or host process. Most historical containers had exited and their inspectable
network endpoint metadata was gone at recheck. Do not assign a process owner from the veth name or
from temporal proximity alone.

## Disposition and next evidence

No network, USB, container, or service configuration was changed. Keep the remaining 1,048-count
difference unattributed; the evidence supports container-network lifecycle as a major contributor,
not a full explanation, hardware fault, or named task owner.

To resolve the remainder on the next comparable burst, retain one contemporaneous join record per
container-network lifecycle: monotonic timestamp, container ID, network endpoint/peer ifindex,
host-side veth DEVPATH, and the launching mesh task key (when present), alongside the seqnum
baseline/delta. Without that source-side tuple, the exact container-to-veth mapping is unrecoverable
for already-removed containers.

## Evidence

- `/home/mesh-home/.mesh/device-churn.log`, lines 5013–5026: the 14 counter passes and deltas.
- `/home/mesh-home/.mesh/udev-stream.log`, lines 3409 onward: timestamped events; the analyzed
  window ends at line 4400 (17:35:04Z).
- `docker events` for 16:20–17:40Z: 14 create events and their matching retained die/destroy records;
  this is Docker daemon history, not a mesh-task ownership record.
- `/home/mesh-home/.mesh/chat.log`: contemporaneous task claims were checked; none joins these
  container IDs or veth names to a task owner.
- `scripts/mesh-udev-stream`: documents the global-seqnum/private-network-namespace population
  mismatch and defines `sgap` as an outstanding gauge.
