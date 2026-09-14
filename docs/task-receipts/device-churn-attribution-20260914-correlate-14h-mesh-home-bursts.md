# Device-churn attribution — 2026-09-14 14:25–14:55 UTC

Task: `health-observation-device-churn-mesh-home-20260914/correlate-14h-mesh-home-bursts`  
Node: `mesh-home`  
Question: what accounts for the 57 sequence values absent from the retained udev stream?

## Measurement

Joined the four CHURN counter deltas to the exact half-open seqnum ranges `(baseline, total]`, then
matched retained `udev-stream.log` records by `seqnum`. “Missing/unknown” means the global counter
advanced for a sequence with no retained row in this listener; it does not establish a dropped
broadcast or identify an event source.

| pass end (UTC) | seqnum interval | raw delta | signed probe | unsigned rows | missing / unknown | observed rows and class |
|---|---:|---:|---:|---:|---:|---|
| 14:25:03 | (11626, 11641] | 15 | 0 | 0 | 15 | none |
| 14:30:03 | (11641, 11653] | 12 | 3 | 3 | 6 | 11648–11653; all hwmon |
| 14:40:03 | (11653, 11677] | 24 | 3 | 3 | 18 | 11669, 11673–11677; all hwmon |
| 14:55:02 | (11677, 11699] | 22 | 2 | 2 | 18 | 11693, 11697–11699; all hwmon |
| **total** |  | **73** | **8** | **8** | **57** | **16 rows** |

Every retained row is a `change` at `/devices/pci0000:00/0000:00:18.3/hwmon/hwmon2`. Signed rows
carry the mesh probe UUID `6d657368-0002-4000-8000-756465767374`; unsigned rows carry `synth=0`.
The exact absent ranges are 11627–11647 (21 values), 11654–11668 (15), 11670–11672 (3), and
11678–11692 (15), 11694–11696 (3): 57 total. Thus the listener retained 16/73 (21.9%) of the
counter's sequence values in these four intervals. The zero-delta passes at 14:35:02, 14:45:02, and
14:50:02 add no sequence values.

## Lifecycle evidence and attribution

The connected Docker daemon returned no rows for `docker events --since 2026-09-14T14:20:00Z
--until 2026-09-14T15:00:00Z`; `docker ps -a` also returned no rows at inspection, and
`journalctl -u docker` had no entries for that interval. These queries provide no retained positive
container-lifecycle evidence. Their emptiness does not prove that no container lifecycle occurred
during the window.

No container ID, endpoint, veth, or task key can be joined to the 57 unknown sequence values from
the retained sources. The 16 visible events are all hwmon changes, not named virtual-network rows.
The exact attribution remains unrecoverable; do not assign the residual to Docker or external device
enumeration from temporal proximity or global-counter deltas. This differs from the 2026-09-13 case,
where retained Docker creates coincided with named veth/queue rows and supported only a partial
container-network contribution (see
[`device-churn-attribution-20260913-correlate-high-uevent-bursts.md`](device-churn-attribution-20260913-correlate-high-uevent-bursts.md)).

## Smallest next evidence

For the next comparable burst, retain one source-side join stream visible across the relevant network
namespaces with each event's monotonic timestamp, seqnum, action, subsystem, and DEVPATH. To attribute
container-created interfaces, include container ID, host-side veth DEVPATH, peer ifindex, and the
launching mesh task key when present in that same lifecycle record. Without the event-level namespace
capture and lifecycle tuple, these 57 values remain unknown.

## Evidence

- `/home/mesh-home/.mesh/device-churn.log`, lines 5276–5282: four CHURN ranges and three zero-delta
  passes.
- `/home/mesh-home/.mesh/udev-stream.log`, lines 6238–6254: retained rows and seqnums.
- `docker events`, `docker ps -a`, and `journalctl -u docker` queried for the interval on 2026-09-14;
  no rows were returned by those lifecycle sources.
- `scripts/mesh-udev-stream`, lines 35–63: the kernel sequence counter is global while netlink
  delivery is namespace-scoped; `sgap` is an outstanding gauge, not a per-window loss count.
- `scripts/mesh-device-churn`, lines 27–40: seqnum indicates churn but does not name a device;
  signed probes are excluded only by exact interval match.

No mesh, container, device, or service configuration was changed.
