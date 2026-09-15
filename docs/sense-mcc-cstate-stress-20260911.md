# MCC sense closure: `mesh-cstate` → `mesh-stress`

Date: 2026-09-11

Closed producer↔consumer link: `scripts/mesh-cstate` → `scripts/mesh-stress`.

`mesh-cstate` was a live hardware-backed producer, but the only existing reader was
`mesh-wakeup-attrib`, not one of the mesh fusions. `mesh-stress` now consumes its live JSON and
recognizes the joint pattern `SHALLOW-REST + load_norm <= 1.0` as a WARM wakeup-driven precursor.
Neither shallow rest alone nor heavy load alone creates this relation. Missing, malformed, or
unreachable c-state output stays `UNKNOWN`; machine-facing `mesh-stress --json` and `--check` exit
2 instead of manufacturing calm.

Verification:

- `bash -n scripts/mesh-stress`: PASS.
- `scripts/mesh-cstate --test`: PASS; real cpuidle read (`idle=62.8%`, `deep=47.6%`, `ratio=0.76`)
  and real misprediction counters (`48/48` coverage).
- `scripts/mesh-stress --test` with a 180-second bound: PASS; joint, negative-control, and malformed
  c-state consumer arms.
- Live `scripts/mesh-cstate --json`: PASS at `2026-09-11T15:25:30Z`, `BUSY`, `idle_pct=0.0`,
  `deep_ratio=0.92`.
- Live `scripts/mesh-stress --json`: PASS as a real partial result (exit 1 for existing STRESSED
  state); the output was generated after the producer read and included the existing live stress
  relations. The c-state producer was consumed as `BUSY`, so the new joint arm did not fire.
- `mesh-autowire --test`: PASS; no new tool file or orphan wiring was introduced.
- `mesh-doctor --test`: PASS; source exec-bit and no-new-orphan checks pass.
- `git diff --check`: PASS.

Full `mesh-doctor --quiet` is NOT CLEAN: pre-existing `egress rides tailscale0` and `exit-node set`
FAILs, plus existing busy-default-mic, untimed-peer-SSH, sole-path, and absence-as-negative WARNs;
the bounded run ended rc=124. No `[sense]` board post was made because the mint contract requires
a clean full doctor first. No commit was made.

Next action: coordinate the existing egress/exit-node doctor failures, rerun full
`mesh-doctor --quiet` to a clean result, then post:

`[sense] closed producer↔consumer: mesh-cstate → mesh-stress (shallow C-state rest × low scheduler load)`
