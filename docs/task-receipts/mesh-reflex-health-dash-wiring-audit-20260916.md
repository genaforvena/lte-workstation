# mesh-reflex-health → mesh-dash wiring audit

Audit-only receipt, 2026-09-16 UTC. No substrate, task ledger, board, or senses-owned state was
changed.

## Finding

The producer is wired and producing output. The apparent missing output is a dashboard role
selection mismatch: `scripts/mesh-dash` invokes `mesh-reflex-health --check` only in its `sense`
role (the `-- sense-reflex liveness (per-run artifact freshness) --` block). The generic
`mesh-dash --once check` role does not call that block; it shows only the compact autopoiesis line,
which reads `.reflex-health-state`.

## Evidence

- `mesh-reflex-health --check`: exit 1, 3,058 bytes; output began
  `reflex-health: STALE` and named `feed(stale 32324s>600s, 2+ consecutive)`.
- `mesh-dash --once check`: exit 0, 2,026 bytes; output included
  `-- autopoiesis: reflexes=STALE ...`, but no `sense-reflex` section. This is consistent with the
  source role branch, not producer silence.
- Source call site: `scripts/mesh-dash:2349` runs
  `timeout 15 mesh-reflex-health --check 2>/dev/null | head -4 | grep .` in the `sense` branch.
- Live launch: `~/.mesh/reflexes.cron:90` contains
  `*/10 * * * * $HOME/.local/bin/mesh-reflex-health ...`.
- Installed/source parity: SHA-256
  `b514c2ba14974a9e48b33aebd0c425d5c4c993f40b7d56e7862586b976e0394d` for both
  `scripts/mesh-reflex-health` and `~/.local/bin/mesh-reflex-health`; dash likewise matched at
  `729f5485b8dade4c6a3e8de06c99738828b20f92d894e8a71488dfc238e7d6f2`.
- The producer artifact `~/.mesh/.reflex-health-state` existed at audit time, 6 bytes, mtime
  `2026-09-16 03:30:50.903614046 +0000`.

## Safe checks run

`timeout 40s mesh-reflex-health --check`; `timeout 20s mesh-dash --once check`; source `rg`/`sed`
inspection; cron and systemd read-only inspection; `stat`; `sha256sum`.

## Disposition

No mutation is justified by this audit. The precise follow-up, if desired, is a dashboard UX change
to expose the existing sense-reflex block from the generic `check` role; that was not performed.
