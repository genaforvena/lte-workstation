# Owner verification receipt: chaos consumer orphan declaration

Timestamp: 2026-09-09T04:02Z

- Live task check: `mesh-task audit` reported `OPEN_UNOWNED genome chat-review/chaos-consumer-orphan-declaration`.
- Declaration: `scripts/mesh-chaos-consumer:3` carries the truthful `# orphan-ok:` owner-routed, explicit-run declaration; no cron wiring was added.
- Deployment: `cmp scripts/mesh-chaos-consumer ~/.local/bin/mesh-chaos-consumer` PASS; both SHA-256 values are `a13159c226a05881c61636c8fef86e248babbbce434af26082630bb2f66ef8c8`.
- Consumer checks: `./scripts/mesh-chaos-consumer --test`, `./tests/test-mesh-chaos-consumer.sh`, and `./tests/test-mesh-chaos-emu.sh` all PASS.
- Bounded live orphan check: `timeout --signal=TERM --kill-after=3s 20 ./scripts/mesh-doctor --quiet` returned `124` after 20s. It emitted only the unrelated pre-existing failures `egress rides tailscale0 (overlay/VPN)` and `exit-node set (n2sbt7yy6t11CNTRL)`; no `mesh-chaos-consumer` orphan line was emitted before the bound.

The bounded result is recorded as unresolved coverage, not as a green full-doctor verdict. The orphan declaration itself is present and deployed identically.
