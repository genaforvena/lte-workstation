# Live driver process identity correction — 2026-09-11

## Result

Implemented and deployed the successor correction for `live-driver-process-identity-correction-20260911/fix-exact-driver-identity-and-lock`.

## Code landed

- `scripts/mesh-consume-all` now admits a driver only when `/proc/<pid>/cmdline` has the exact
  interpreter, deployed `mesh-pane-consume` argv spelling, channel, `--interval` position, numeric
  interval, and optional `--deliver` tuple. Candidate `pgrep` is only an accelerator; it is not an
  identity decision.
- A single-writer `flock` serializes supervisor passes. The spawned driver closes FD 9 before exec,
  so the lock covers only the supervisor turn and cannot be held for the driver's lifetime.
- `tests/test-mesh-consume-all-identity.sh` is red-first coverage for a decoy argv containing the
  historical text fragment and for two concurrent ensure passes converging to one driver.

## Deployment and live restoration

`mesh-sync-tools --apply` completed; source and `~/.local/bin/mesh-consume-all` have identical
SHA-256 `c2266ca6e0483073a0288e941ae1d25b884e8552d51fdcd9528aa31ffc76e19a`.

After one plain deployed supervisor pass, the live exact-tuple audit found exactly one current
process for each of the 15 eligible channels: genome, tg, senses, health, pub, discover, sound,
vpn, witness, tg-roz, job, adint, hire, haunt, and wake. No duplicate remained.

## Verification

- `bash -n scripts/mesh-consume-all tests/test-mesh-consume-all-identity.sh` — pass.
- `tests/test-mesh-consume-all-identity.sh` — pass: decoy excluded; concurrent passes converge.
- `scripts/mesh-consume-all --test` — pass.
- Deployed `mesh-consume-all --status` — all 15 eligible channels UP.
- Independent `/proc` argv tuple audit — 15/15 channels exactly one process.
