# Relay-crossing episode cooldown — 2026-09-09

Implemented in `scripts/mesh-path-watch`.

The per-peer mode row now carries `last_alert_epoch` as its fourth field. A direct recovery resets
only the relay streak; it carries that epoch forward. On a later debounced crossing, the aggregated
board post fires only when at least one crossing peer is outside `MESH_PATH_RELAY_COOLDOWN` (default
3600 seconds) or has no prior epoch. A peer with no epoch is the peer-set escalation path, so a new
peer joining the crossing set remains visible during the cooldown of existing peers. UDP=false
suppression does not stamp an epoch because no relay alert was posted.

## Verification artifact

Command:

```text
scripts/mesh-path-watch --test
```

Result:

```text
smoke-test: ok (live status --json real-read + baseline/debounce-2/once-only/recovery/offline/netcheck-udp-edge/BLIND/same-pass-batch/udp-false-suppress + derp-lat-cooldown/escalate fixtures)
```

The fixture sequence asserts: first two-peer crossing = one board line; recovery plus a repeated
two-peer flap within cooldown = zero board lines; adding `new-peer` to the later crossing set = one
board line naming the new peer. The same test also verifies the existing first-crossing, batch, and
UDP-root-cause suppression behavior.
