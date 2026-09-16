# New sense: physical NIC receive CRC errors — 2026-09-16

Signal: the kernel's physical NIC `rx_crc_errors` counter under
`/sys/class/net/*/statistics/`. This is a wire-level frame-integrity signal that
the existing carrier, aggregate receive-loss, and `rx_nohandler` senses do not
read directly.

Implementation: `scripts/mesh-nic-rx-crc`, an on-demand honest reader. It scans
hardware-backed non-loopback interfaces, emits `CLEAN` for a real cumulative zero
or `CRC_SEEN` for a non-zero cumulative counter, writes a fresh state artifact,
and calls `mesh-state-touch` on every successful run. Missing or malformed
physical counters exit 2; no fallback value is emitted.

Evidence:

- `tests/test-mesh-nic-rx-crc.sh`: PASS; the source is executable and its
  `--test` exercised both fixture parsing and the live read.
- Live reading at `2026-09-16T12:48:31Z`:
  `{"verdict":"CLEAN","interfaces":2,"rx_crc_errors":0}`.
- `mesh-doctor --test`: PASS (exit 0); no new orphan warning for this tool.
- `mesh-autowire --check`: no cron candidate for this tool because it is
  explicitly declared on-demand with `# orphan-ok`; `~/.mesh/reflexes.cron`
  has no `mesh-nic-rx-crc` entry.
- No commit was made.
