# Health-warning triage: fc28c99a126fc9d25adf

Date: 2026-09-09
Task: `health-warning/fc28c99a126fc9d25adf/triage`

## Fresh read-only observations

- The exact bounded replay step was claimed with `MESH_TASK_ACTOR=health mesh-task take`.
- `mesh-health` at 2026-09-09T19:12:21Z passed `mesh-home` and `phaedra`; GL-MT3000,
  Redmi 10, ilya, imozerov-Default-string, imozerov-IdeaPad-3-15IIL05, and rip remain
  offline; `imac-rozalia` is SSH-skipped/unreachable from this node.
- `mesh-sensorium --test` passed its committed BODY/SITUATION/ROOM fixtures, including the
  cached device-free wifi-motion path and stale-producer distinctions. This validates the
  classifier/test fixtures, not a live wifi-motion producer.
- Live `mesh-wifi-motion --json` returned exit 2:
  `{"verdict":"UNCERTAIN","reason":"tape_stale","age_s":905780,"stale_limit_s":1800}`.
- `tailscale status` shows only `phaedra` and `imac-rozalia` online among the tagged peers;
  the remaining listed peers are offline. `mesh-doctor --once` available checks showed
  Anthropic reachability, camera, microphone capture, and supervised loops passing, with
  the known egress-over-tailscale/exit-node warnings and default-mic busy warning.

## Disposition

The warning is confirmed as a known wifi-motion/sensorium observability blindness: the
offline/cached sensorium evidence is not a live room-motion reading, and the live motion
tape is stale. Keep the condition **UNKNOWN / KNOWN BLINDNESS**, not DOWN or recovered.
No routing, DNS, firewall, VPN, WireGuard, Tailscale, or service mutation was made.

Close this exact triage with the artifact above. Retry only on a new producer/roll-call delta
or when a reachable owner can verify the affected path. Existing active/queued health work is
unchanged; no additional health-warning triage was admitted.
