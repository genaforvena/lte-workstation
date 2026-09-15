# Cross-sense occupancy result — 2026-09-12

Extended the existing `scripts/mesh-occupancy-kind` fusion. When no devices are seen and the room
sensor is unreachable, it now emits `PARTIAL-EMPTY` with an explicit room-unconfirmed reason;
`EMPTY` now requires the room sensor to report `EMPTY`. This prevents an offline input from reading
like a genuine all-clear. Added classifier assertions for both the label and reason, and corrected
the `--test` real-read assertion to accept the tool's existing `[occ-degraded] DEGRADED` prefix.

## Verification

- `mesh-occupancy-kind --test`: PASS (14 fusion assertions and its live cached-read path).
- `bash -n scripts/mesh-occupancy-kind`: PASS.
- `git diff --check -- scripts/mesh-occupancy-kind`: PASS.
- Live `mesh-occupancy-kind --json`: `DEGRADED`, `presence=OFFLINE`, timestamp
  `2026-09-12T14:31:43Z`, exit 2. This is a real live read and correctly declines an occupancy
  verdict because `.presence-state` is missing or stale.
- Source mode remains executable (`-rwxrwxr-x`). No new tool file was created.
- Full `mesh-doctor --quiet` rerun at `2026-09-12T14:32:55Z`: completed with exit 3, `3 FAIL, 33
  WARN`. FAILs: default egress via `tailscale0`, configured exit node `n2sbt7yy6t11CNTRL`, and the
  existing `mesh-fsnotify` real smoke test. The run traversed the previously stalled serial/orphan
  phase and completed its census: 92 unwired+non-canonical orphans, explicitly reported as
  stable/confirmed across 2+ checks; no new orphan warning names `mesh-occupancy-kind`. The doctor
  gate itself remains failed. Routing was left unchanged under single-writer substrate discipline.

No `[sense]` line was posted because the required clean doctor gate did not pass. No commit was made.

Next: the VPN/substrate writer must disposition the two egress FAILs. The fsnotify test passed on
direct recheck; its doctor serial-confirm timeout is still unassessed, not a confirmed failure.
Rerun `mesh-doctor` after the egress disposition and require exit 0 with no new orphan warning;
only then post `[sense]` citing this receipt and a fresh `mesh-occupancy-kind --json` read. The
last live occupancy read remains DEGRADED because `.presence-state` was offline, exit 2 at
`2026-09-12T14:31:43Z`.

## Live recheck — 2026-09-12 14:44Z

- `mesh-fsnotify --test`: PASS. Its direct run exercised event delivery, debounce coalescing,
  silent-window behavior, lock exclusion, a real inotify allocation count, unreadable-UID handling,
  both limit surfaces, and the no-sysctl `n/a` path.
- `mesh-doctor --quiet`: exit 2, `2 FAIL, 34 WARN`. The only FAILs remain default egress via
  `tailscale0` and configured exit node `n2sbt7yy6t11CNTRL`; routing was not changed. The rotating
  serial-confirm batch marked `mesh-fsnotify` as `TOO SLOW TO ASSESS` after its 60-second window,
  which is not a failure verdict. This does not contradict the direct passing `--test` above.
- The fsnotify smoke failure is not currently reproducible, while the required clean doctor gate
  remains blocked on the two egress findings. Do not post `[sense]` until the VPN/substrate writer
  dispositions those findings and a fresh doctor run passes.

## Live recheck — 2026-09-14

- The existing `scripts/mesh-occupancy-kind` extension publishes the joint body-motion × recent
  light-change relation (`MOTION_AND_LIGHT`, `SINGLE_AXIS`, `NO_ACTIVITY`, `PARTIAL`, or `UNKNOWN`)
  and overlap coverage. A missing/unusable axis remains `UNKNOWN`/partial; measured stillness on
  both live axes is `NO_ACTIVITY`. The occupancy fold also keeps `EMPTY` gated on room-confirmed
  emptiness and uses `PARTIAL-EMPTY` when the room axis is unreachable.
- The deployed `~/.local/bin/mesh-occupancy-kind` was a stale regular-file copy (13,774 bytes).
  Backed it up to `~/.mesh/tools-backup/mesh-occupancy-kind.20260914T142019Z` and atomically
  replaced only that entry with a symlink to `scripts/mesh-occupancy-kind`; the global
  `mesh-sync-tools --apply` was not run. Verified the installed path resolves to the source.
- Installed `mesh-occupancy-kind --test`: PASS, 25 fusion assertions including the real cached-read
  path. `bash -n scripts/mesh-occupancy-kind` and cached diff check: PASS.
- Real `mesh-occupancy-kind --json` read at `2026-09-14T14:20:50Z`, exit 2:
  `DEGRADED`, `activity_relation=UNKNOWN`, `activity_coverage=0/2`, with presence and motion
  `OFFLINE`, light `UNKNOWN`, and room `PRESENT`. This is a live unavailable-input result, not an
  all-clear or an empty-room verdict.
- `mesh-doctor --quiet`, started `2026-09-14T14:21:16Z`, completed after about 10 minutes with exit
  3: `3 FAIL, 33 WARN`; FAILs were egress via `tailscale0`, configured exit node
  `n2sbt7yy6t11CNTRL`, and the existing `mesh-usb` smoke test. Serial-confirm coverage was 1/164.
  The orphan census reported 94 stable warnings; `~/.mesh/.doctor-orphans-state` does not list
  `mesh-occupancy-kind`, so this extension added no orphan WARN. Routing/substrate state was left
  unchanged.

No `[sense]` line was posted because the required doctor gate remains failed. Next: the substrate
owner must resolve the two egress FAILs and the `mesh-usb` owner must disposition its smoke-test
FAIL; senses then reruns `mesh-doctor --quiet` and posts `[sense]` only after exit 0 with no new
orphan WARN. No commit was made.
