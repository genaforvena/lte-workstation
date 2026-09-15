# New sense: kernel file-table allocation — 2026-09-14

Added `scripts/mesh-file-table`, an on-demand live reader for the previously uninstrumented
`/proc/sys/fs/file-nr` signal. It reports the kernel's allocated, unused, and maximum file-handle
counts plus the allocated/maximum percentage. It does not label this as a process open-FD count or
cache a reading. Missing, unreadable, or malformed input exits 2. The source declares
`# orphan-ok: on-demand ...`, is executable, and is available at
`~/.local/bin/mesh-file-table` through a symlink to the repository source.

Evidence:

- `/home/mesh-home/.local/bin/mesh-file-table --json` — live read:
  `{"source":"/proc/sys/fs/file-nr","allocated":9312,"unused":0,"maximum":9223372036854775807,"allocated_pct":0.00}`
- `scripts/mesh-file-table --test` — PASS; validates a fixture and malformed rejection, then
  requires and reports a live `/proc/sys/fs/file-nr` read.
- `tests/test-mesh-file-table.sh` — PASS; asserts JSON shape and numeric fields, exit 2 for a missing
  source, and the tool's real-read `--test` path.
- `bash -n` on source and wrapper — PASS; `git diff --check` — PASS.
- Full `mesh-doctor --quiet` — exit 0, `0 FAIL, 33 WARN`. Existing repository/node warnings remain.
  The orphan census stayed at 94 stable warnings with no `+new`; the on-demand exemption census
  increased from 97 to 98. `mesh-file-table` is absent from `.doctor-orphans-state`.

No state artifact is change-gated, no cadence is claimed, and no commit was made.
