# Communication family slice — 2026-09-12

Task: `tg-scripts-layout-migration-20260912/communication-family-slices` (owner: genome).

Moved only the `mesh-tg-filter` implementation into `scripts/communication/mesh-tg-filter` and
retained `scripts/mesh-tg-filter` as the executable compatibility entrypoint. Existing callers keep
using the old basename. The wrapper resolves an installed symlink to the checkout and also supports
a regular deployed copy via `MESH_REPO`, `MESH_GENOME`, or `~/lte-workstation` fallback. The checked
manifest inventories the nested implementation as non-deploying, owned by `scripts:mesh-tg-filter`,
and keeps the shim as the sole installed basename.

Caller census (source/runtime, excluding this receipt): the only command caller is
`scripts/mesh-channel-tg`, which gives `mesh-tg-filter` to `mesh-channel` as its stdin filter. The
remaining source hit is a format comment in `scripts/mesh-voice-rx`; `mesh-channel-tg` also checks
the command during its self-test. No caller paths were changed. The filter reads stdin, shapes a
prompt, and reads no bot token, Telegram session, or board credential; the shim adds no credential
handling.

Live path: `mesh-voice-rx.service` is active and its installed `ExecStart` is
`~/.local/bin/mesh-voice-rx`. Its event kick invokes `~/.local/bin/mesh-channel-tg`; the latter
passes the legacy filter basename to the active `mesh-channel` path. No direct `mesh-channel-tg`
crontab or `~/.mesh/reflexes.cron` entry was present in the current state, despite an old source
comment referring to a minute cron. The event-driven service path is the live resolution verified
here; cadence was not changed. No Telegram send was performed.

Verification:

```text
bash -n scripts/mesh-tg-filter scripts/communication/mesh-tg-filter
  pass
cd /tmp && /home/mesh-home/lte-workstation/scripts/mesh-tg-filter --test
cd /tmp && /home/mesh-home/.local/bin/mesh-tg-filter --test
  both pass: smoke-test: ok
regular-copy shim in an isolated temporary home with MESH_REPO pointing at this checkout
  pass: smoke-test: ok (deployed-copy fallback)
scripts/mesh-channel-tg --test
  pass: smoke-test: ok
scripts/mesh-manifest --check
  PASS (1201 complete rows; no duplicate installed basenames)
scripts/mesh-manifest --parity
  top-level mesh-tg-filter = same as deployed; nested implementation is inventoried/non-deployed
scripts/mesh-sync-tools --test
scripts/mesh-doctor --test
  both pass
scripts/mesh-land --test
  pass: smoke-test: ok (branch-override fixture)
mesh-voice-rx.service
  active; ExecStart resolves to ~/.local/bin/mesh-voice-rx
```

Rollback: restore the original implementation from `scripts/communication/mesh-tg-filter` to
`scripts/mesh-tg-filter`, remove the compatibility wrapper and empty `scripts/communication/`
directory, then run `scripts/mesh-manifest --check` and the original filter's `--test` from `/tmp`.
