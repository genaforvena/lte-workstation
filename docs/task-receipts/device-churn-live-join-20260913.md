# Docker endpoint to host-veth observer

Implemented `scripts/mesh-docker-veth-join`, a read-only observer bounded by a
1–300 second capture interval and a 1–1000 event cap. It reads Docker network
events, inspects the referenced container, joins a unique single-network peer
ifindex to the host `iflink` and sysfs DEVPATH, and records the endpoint ID and
mesh task label when present. Missing or ambiguous joins stay `UNKNOWN`. The
per-event uevent sequence delta brackets event processing and is explicitly not
causal attribution. No routing, network, container, USB, or service settings
were changed; the observer was not installed or scheduled.

## Evidence

- `tests/test-mesh-docker-veth-join.py`: 3 tests pass, including a known
  endpoint→peer-ifindex→host-veth mapping and cases where ambiguous mappings
  must not select a candidate.
- `python3 -m py_compile scripts/mesh-docker-veth-join tests/test-mesh-docker-veth-join.py`:
  passes.
- Live bounded capture: [`device-churn-live-join-20260913T2038Z.jsonl`](device-churn-live-join-20260913T2038Z.jsonl).
  Docker server version was 29.1.3; there were no running containers and no
  network events during the two-second capture. The kernel uevent sequence was
  9931 at start and 9934 at finish. This is a real empty event read, not a
  container/veth join observation.
- `git diff --check` for the observer and fixture passed.

The initial capture surfaced Docker CLI's expected SIGTERM status as 143 when
the bounded interval ended. The observer now treats 143 as normal deadline
termination; the retained capture above exits successfully.

## Next comparable burst

Run `scripts/mesh-docker-veth-join --seconds 60` on mesh-home during a live
container network burst. The default artifact location is
`$MESH_DIR/observations/` (or `/home/mesh-home/.mesh/observations/`). Do not
infer container ownership from temporal proximity alone.
