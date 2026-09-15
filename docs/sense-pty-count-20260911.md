# New sense: live allocated PTYs — 2026-09-11

Added `scripts/mesh-pty-count`, an honest on-demand reader for the previously unsensed kernel
signal `/proc/sys/kernel/pty/nr`: the current number of allocated pseudo-terminals on this node.
It emits a JSON or human-readable live value, returns exit 2 for an absent/unreadable/malformed
procfs value, and has no fallback or fabricated zero. The source is executable and deployed at
`~/.local/bin/mesh-pty-count` as the standard repository symlink. It is marked `orphan-ok` because
there is no scheduled consumer yet; consequently `mesh-autowire` has no cadence to install.

Evidence:

- `scripts/mesh-pty-count --test` — PASS; the test exercises a fixture, malformed-input exit 2,
  and a real procfs read (`pty_count=37` at test time).
- `scripts/mesh-pty-count --json` — PASS; live reading observed `pty_count=41` at
  `2026-09-11T02:32:44Z` (the count is expected to vary as PTYs open/close).
- malformed live override — PASS; returned exit 2 with `UNKNOWN — cannot read ...`.
- `bash -n scripts/mesh-pty-count` — PASS.
- `scripts/mesh-autowire --test` — PASS.
- `scripts/mesh-doctor --test` — PASS.
- Full `mesh-doctor --quiet` — NOT CLEAN due pre-existing node blockers:
  `egress rides tailscale0`, `exit-node set`, and `mic DEFAULT device broken/busy`.
  The run reported no new `mesh-pty-count` orphan warning. No `[sense]` post was made because the
  contract requires a clean live doctor before birth; fixing those substrate issues is a separate,
  explicitly scoped task.

No commit was made.
