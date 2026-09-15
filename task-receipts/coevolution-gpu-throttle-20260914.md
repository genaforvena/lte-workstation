# Coevolutionary GPU clock-reason link — 2026-09-14

Closed the live `mesh-gpu-throttle` → `mesh-situation` link (choice b). Before the edit,
`rg -l 'mesh-gpu-throttle|\.gpu-throttle' scripts --glob '!mesh-gpu-throttle'` returned no fusion
reader. The existing executable `scripts/mesh-gpu-throttle` already had its `orphan-ok` header and
real NVIDIA driver test; no new producer file was created.

`mesh-situation` now reads the producer's active mask directly from the repository source when no
installed command is on `PATH`, preserves the raw mask and active bit, pairs that observation with
the live internal-stress axis, and reports overlap coverage. Missing or malformed producer output
remains `UNKNOWN` and forces exit 2 in JSON/edge modes. The relation adds no score and does not
change posture.

## Verification

- The new test first failed because the consumer emitted no GPU clock-reason fields; after the
  source-path behavior was added, the isolated `mesh-situation --test` passed. Its fixtures assert
  the paired relation and `2/2` coverage, and assert UNKNOWN, `1/2`, and exit 2 when the producer is
  unreachable.
- The ordinary direct `mesh-situation --test` is blocked by its existing nested
  `mesh-perimeter --test`, which failed with `mesh-lan-newdevice --test changed a live LAN artifact`.
  The isolated pass supplied a no-op perimeter-test command only to bypass that unrelated child
  check; all situation fixtures still ran.
- `scripts/mesh-gpu-throttle --test` passed with a real `nvidia-smi` read at 08:40:24Z
  (`active_mask=0x0000000000000000`, `active=false`).
- Live `scripts/mesh-situation --json` at 08:48Z exited 0 and read the real GPU artifact: mask
  `0x0000000000000000`, active `false`, relation
  `STRESS-WITHOUT-ACTIVE-GPU-CLOCK-REASON`, coverage `2/2`.
- `bash -n scripts/mesh-situation`, `git diff --check -- scripts/mesh-situation`, and the
  post-change reader search passed. The search now returns `scripts/mesh-situation` as a fusion
  reader. Producer mode remains executable (`775`). No commit was made.

## Initial board gate

An earlier `mesh-doctor --quiet` attempt did not establish a complete pass: it reported then-live
egress/job-mail failures and its aggregate sweep produced no summary before interruption. The
`[sense]` post was withheld at that time. The completed recheck and the later post are recorded below.

## Gate recheck — 2026-09-14 20:34Z

- `scripts/mesh-gpu-throttle --test` passed with a real driver read at 20:32:48Z: mask
  `0x0000000000000000`, active `false`.
- `scripts/mesh-situation --test` passed, including the unreachable-producer UNKNOWN/exit-2 fixture.
- Live end-to-end at 20:34:08Z: the producer returned mask `0x0000000000000000`; the fusion read
  that same live value and returned internal `WATCH`, relation
  `STRESS-WITHOUT-ACTIVE-GPU-CLOCK-REASON`, coverage `2/2`.
- The reader search now returns only `scripts/mesh-situation`; the producer is absent from
  `~/.mesh/.doctor-orphans-state`.
- Fresh `rtk mesh-doctor --quiet` (run stamp 20:34:32Z) returned exit 0 before the 20:44:30Z board
  post, with `0 FAIL, 33 WARN`.
  Orphan census remains at 94 stable warnings (same count as the 20:23Z report); none names
  `mesh-gpu-throttle`. The unrelated baseline warnings remain.

The doctor gate cleared before the board post. At 20:44:30Z, `[sense] mesh-gpu-throttle ↔
mesh-situation` was posted with the live mask, relation, `2/2` overlap, test results, and doctor
summary. A textual handoff was written to `~/.mesh/handoff/senses.md`. No commit was made.
