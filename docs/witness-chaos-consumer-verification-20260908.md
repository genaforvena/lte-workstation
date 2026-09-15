# Witness verification: chaos consumer

Timestamp: 2026-09-08T16:56:56Z

- `cmp scripts/mesh-chaos-consumer ~/.local/bin/mesh-chaos-consumer`: PASS (rc 0).
- SHA-256 source/deployment: both `a13159c226a05881c61636c8fef86e248babbbce434af26082630bb2f66ef8c8`.
- `scripts/mesh-chaos-consumer --test`: PASS.
- `tests/test-mesh-chaos-consumer.sh`: PASS.
- `tests/test-mesh-chaos-emu.sh`: PASS.
- Source contains the truthful `# orphan-ok` declaration and remains absent from
  `~/.mesh/reflexes.cron`, systemd user configuration, and `/etc/cron*`.
- `mesh-doctor --test`: PASS (rc 0), including its orphan-check fixture gates.
- Bounded live `timeout --signal=TERM --kill-after=5s 90 mesh-doctor --quiet`: did
  not reach an orphan verdict. It emitted the unrelated pre-existing failures
  `egress rides tailscale0 (overlay/VPN)` and `exit-node set (n2sbt7yy6t11CNTRL)`
  before the run stopped; no `mesh-chaos-consumer` orphan line was emitted.

This is evidence for owner `mesh-chaos-consumer/genome`; the bounded live orphan
result is explicitly unresolved rather than claimed green. No cron wiring was added.
