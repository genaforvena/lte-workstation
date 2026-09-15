# Chaos-engineering admission — source artifact

- Measured: 2026-09-08T16:34Z, `mesh-home`
- Subject: `scripts/mesh-chaos-emu`
- Consumer check: `tests/test-mesh-chaos-emu.sh`
- Ledger source: `docs/plans/2026-09-08-study-chaos-engineering-ledger.tsv`
- Source SHA-256: `d43ca0068db2c1641a1c33a0f17f2f3f7578c02845c33c3eff141a0a605082cc`
- Acceptance-test SHA-256: `c1682efeb3c33d3b61d716d3faefabd4248c9700bfd5d24311a0eceed150450e`

Current source behavior used by the sample:

- `--fail-first 2 --rc 75` increments a keyed counter and returns rc 75 on attempts 1 and 2.
- The wrapped command is not run during those injected failures.
- Attempt 3 runs the wrapped command and returns its rc.
- State is isolated by `MESH_CHAOS_EMU_DIR`; the sample did not touch live mesh services.

This is a current-source citation, not a reachability claim: the bounded command was executed and
its outcome is retained in the companion outcome artifact.
