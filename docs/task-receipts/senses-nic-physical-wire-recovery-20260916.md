# senses-nic-physical-wire recovery — 2026-09-16

The stale claim `senses-nic-physical-wire/wire-nic-physical` was re-observed and
settled into a typed dependency block.

Evidence:

- `scripts/mesh-nic-physical --test` passed with a real sysfs read: `enp42s0`.
- `scripts/mesh-nic-physical --json` produced `UP-CLEAN`, `carrier=1`,
  `tx_carrier_errors=0`, `carrier_changes=2` at `2026-09-16T05:53:01Z`.
- The installed copy `/home/mesh-home/.local/bin/mesh-nic-physical` matches the
  source SHA-256 (`9e9ea5565ed1d2ebf7a946395bd9a6960161c74492c4904dfa10245b1e60fca8`).
- `mesh-autowire --apply` previously refused this source because it was absent
  from `HEAD`; the installed/reflex wiring therefore is not yet canonical.

Recovery action:

- Created and dispatched prerequisite
  `autoland/senses-nic-physical-wire-20260916/land-senses-nic-physical` to
  `genome`, with plan
  `docs/task-plans/autoland-senses-nic-physical-wire-20260916.tsv`.
- Blocked the parent with `dependency`, linked it to that exact prerequisite,
  and returned it to the queue. The retry edge is: once the prerequisite lands
  `scripts/mesh-nic-physical` in `HEAD`, rerun `mesh-autowire --apply`, verify
  the scheduled reflex line, and rerun `mesh-doctor --test`.

The parent remains open/waiting; no claim is silently active.
